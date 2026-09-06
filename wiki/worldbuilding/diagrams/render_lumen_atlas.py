"""Render the wiki's schematic atlas; no Blender or source art is modified.

Run from any directory: MPLCONFIGDIR=/tmp/lumen-mpl python3 render_lumen_atlas.py
Requires matplotlib. Numeric place targets live in ../lumen-layout.json.
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle


def render():
    root = Path(__file__).resolve().parent
    data = json.loads((root.parent / "lumen-layout.json").read_text())
    points = {p["id"]: p for p in data["places"]}
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                         "svg.fonttype": "none", "svg.hashsalt": "lumen-atlas-v1"})
    bg, ink, teal, gold = "#f4f4eb", "#243d42", "#377b78", "#a97635"
    fig = plt.figure(figsize=(16, 12), facecolor=bg)
    grid = fig.add_gridspec(2, 3, width_ratios=[1.1, 1.05, 1.25], height_ratios=[1.25, 1],
                           left=.055, right=.97, bottom=.08, top=.88, wspace=.30, hspace=.38)
    plan, local, key, section = (fig.add_subplot(grid[0, 0]), fig.add_subplot(grid[0, 1]),
                               fig.add_subplot(grid[:, 2]), fig.add_subplot(grid[1, :2]))
    fig.text(.055, .955, "LUMEN  /  PHYSICAL ATLAS", fontsize=24, weight="bold", color=ink)
    fig.text(.055, .924, "Version 1 · C+10 reference, with later additions marked · all dimensions in metres",
             fontsize=11, color=ink)
    for ax in (plan, local, section):
        ax.set_facecolor(bg)
        ax.tick_params(colors=ink, labelsize=8)
        for spine in ax.spines.values():
            spine.set_color("#bac8c1")
        ax.grid(alpha=.2)

    body, later, chamber = data["body"], data["later_body"], data["city_chamber"]
    plan.add_patch(Ellipse((0, later["plan_centre_y"]), later["width"], later["length"],
                          fill=False, edgecolor=gold, linestyle="--", linewidth=1.6))
    plan.add_patch(Ellipse((0, 0), body["width"], body["length"],
                          facecolor="#dce9df", edgecolor=teal, linewidth=2))
    plan.add_patch(Rectangle((chamber["x_min"], chamber["y_min"]),
                            chamber["x_max"]-chamber["x_min"], chamber["y_max"]-chamber["y_min"],
                            facecolor="#fcfaf1", edgecolor=teal, linewidth=1.1))
    plan.text(-1250, 120, "Supporting\nchambers", ha="center", color=teal, fontsize=8)
    plan.text(950, -450, "Living\nstructure", ha="center", color=teal, fontsize=8)
    plan.annotate("Growth end", (0, 3550), (0, 3000), ha="center", color=gold,
                  arrowprops={"arrowstyle": "->", "color": gold})
    for pid in ("P01", "P12", "P14", "P17"):
        p = points[pid]
        x, y, _ = p["xyz"]
        color = gold if pid == "P17" else teal
        plan.plot(x, y, "o", color=color, markersize=4)
        plan.annotate(pid, (x, y), xytext=(7, 4), textcoords="offset points", fontsize=8, color=ink)
    plan.text(0, -2180, "Aft drive region\nside-facing docks above", ha="center", fontsize=8, color=ink)
    plan.set(xlim=(-1950, 1950), ylim=(-2600, 4150), xlabel="X · cross-body", ylabel="Y · toward growth")
    plan.set_aspect("equal")
    plan.set_title("BODY PLAN\nDashed envelope: illustrative later growth", loc="left", color=ink, fontsize=10)

    garden = data["maia_garden"]
    local.add_patch(Rectangle((garden["x_min"], garden["y_min"]),
                             garden["x_max"]-garden["x_min"], garden["y_max"]-garden["y_min"],
                             facecolor="#d6e5cd", edgecolor=teal, alpha=.8))
    local.text(-470, 405, "Maia's\ngarden", color=teal, fontsize=8)
    local.add_patch(Rectangle((-90, -70), 180, 140, facecolor="#eadabd", edgecolor=gold))
    for route in data["routes"]:
        a, b = points[route["from"]], points[route["to"]]
        if b["id"] in ("P14", "P17"):
            continue
        local.plot([p[0] for p in route["waypoints"]], [p[1] for p in route["waypoints"]],
                   color="#869990", linewidth=.7, linestyle=":", zorder=1)
    offsets = {"P01": (5, -15), "P02": (8, -4), "P03": (5, 6), "P04": (6, 5),
               "P05": (-32, 5), "P06": (3, 7), "P07": (-32, -6), "P16": (-30, 2)}
    for p in data["places"]:
        x, y, _ = p["xyz"]
        if p["id"] in ("P14", "P17"):
            continue
        future = p["state"] in ("later_household", "later_use")
        local.plot(x, y, "o", markersize=5, markeredgecolor=gold if future else teal,
                   markerfacecolor=bg if future else teal, zorder=3)
        local.annotate(p["id"], (x, y), xytext=offsets.get(p["id"], (6, 5)),
                       textcoords="offset points", color=ink, fontsize=8)
    local.annotate("Dome view toward\nbasin and gardens", (0, 350), (150, 850),
                   fontsize=8, color=gold, arrowprops={"arrowstyle": "->", "color": gold})
    local.set(xlim=(-760, 760), ylim=(-1050, 1250), xlabel="X", ylabel="Y")
    local.set_aspect("equal")
    local.set_title("CITY DETAIL\nDotted lines follow the first blockout routes", loc="left", color=ink, fontsize=10)

    centre_z = (body["bottom_z"] + body["top_z"]) / 2
    section.add_patch(Ellipse((0, centre_z), body["length"], body["depth"],
                             facecolor="#dce9df", edgecolor=teal, linewidth=2))
    section.add_patch(Rectangle((chamber["y_min"], 0), chamber["y_max"]-chamber["y_min"],
                               chamber["top_z"], facecolor="#fcfaf1", edgecolor=teal))
    section.axhline(0, color=gold, linewidth=.8, linestyle=":")
    section.text(100, 435, "Main inhabited chamber\nlocal vaults and canopies below its overhead", ha="center", color=ink)
    section.text(0, -280, "Metabolic tissues · reservoirs · service and cultivation chambers", ha="center", color=teal)
    section.text(0, 860, "Structure, shielding, light and environmental services", ha="center", color=teal)
    for pid, label, offset in (("P01", "Plaza / datum", (0, -45)),
                               ("P04", "Garden +20 m", (0, 25)),
                               ("P12", "Dome platform +85 m", (42, 47)),
                               ("P13", "Observation +100 m", (-75, 44)),
                               ("P14", "Arrival", (-22, 30))):
        p = points[pid]
        _, y, z = p["xyz"]
        section.plot(y, z, "o", color=teal, markersize=4)
        section.annotate(label, (y, z), xytext=offset, textcoords="offset points", fontsize=8,
                         color=ink, ha="center", arrowprops={"arrowstyle": "-", "color": "#879991"})
    section.annotate("DOWN\n1 g", (1950, -50), (1950, 420), ha="center", fontsize=9, color=gold,
                     arrowprops={"arrowstyle": "->", "color": gold, "lw": 2})
    section.set(xlim=(-2500, 2500), ylim=(-750, 1250), xlabel="Y · aft to growth end", ylabel="Z · height")
    section.set_aspect("equal")
    section.set_title("LONGITUDINAL SECTION\nEqual horizontal / vertical scale; place markers projected across X", loc="left", color=ink, fontsize=10)

    key.axis("off")
    key.text(0, 1, "PLACE REGISTER", fontsize=12, weight="bold", color=ink, va="top")
    yy = .955
    for p in data["places"]:
        note = {"later_household": "later household", "later_use": "later story use",
                "after_125": "after C+125", "inferred_infrastructure": "new infrastructure"}.get(p["state"], "")
        key.text(0, yy, p["id"], color=gold if note else teal, weight="bold", fontsize=9, va="top")
        key.text(.12, yy, p["name"], color=ink, fontsize=9, va="top")
        if note:
            key.text(.12, yy-.019, note, color=gold, fontsize=8, va="top")
        yy -= .047
    key.text(0, .115, "READ THIS AS A BLOCKOUT TARGET", fontsize=10, weight="bold", color=ink)
    key.text(0, .092, "Rounded envelopes, not pressure-hull engineering.\nOpen markers indicate later use or occupancy.\nRoutes measured; detailed room fitting remains open.\nKeep old places fixed as new chambers grow.\nRadiators extend beyond the body shown here.",
             fontsize=9, color=ink, va="top", linespacing=1.7)
    fig.text(.055, .025, "Canon: wiki/worldbuilding/Lumen-Atlas.md  ·  Numeric targets: lumen-layout.json  ·  No source prose or VN art changed",
             fontsize=9, color=ink)
    output = root / "lumen-atlas.svg"
    fig.savefig(output, facecolor=bg, metadata={"Date": None})
    # The PNG is a disposable visual-review artifact, not a duplicate wiki asset.
    fig.savefig("/tmp/lumen-atlas-review.png", dpi=130, facecolor=bg)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    render()
