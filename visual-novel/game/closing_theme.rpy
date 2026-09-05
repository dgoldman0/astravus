# One cue sheet drives the in-game montage and standalone video renderer.
# Reusing the source art avoids bundling an additional full-length movie.
init -5 python:
    import bisect
    import json

    with renpy.file("closing_theme.json") as theme_file:
        CLOSING_THEME = json.load(theme_file)
    THEME_STARTS = tuple(shot["at"] for shot in CLOSING_THEME["shots"])
    renpy.music.register_channel("closing_theme", mixer="music", loop=False)

    class ClosingTheme(renpy.Displayable):
        def __init__(self, reduced_motion=False, **kwargs):
            super(ClosingTheme, self).__init__(**kwargs)
            self.reduced_motion = reduced_motion
            self.last_position = 0.0
            self.last_st = 0.0
            self.children = [Transform(shot["image"], size=(1920, 1080), fit="cover")
                             for shot in CLOSING_THEME["shots"]]
            self.title = Text("ASTRAVUS", font="fonts/Story-Serif.ttf", size=68,
                              color="#f4e7cb", outlines=[(1, "#00000096", 0, 0)])
            self.subtitle = Text("S E E D S   O F   Y O U T H", font="fonts/Lato-Regular.ttf",
                                 size=25, color="#e2cba2", outlines=[(1, "#00000096", 0, 0)])

        def position(self, st=None):
            # Audio positions may arrive in buffer-sized steps. Advance on the
            # display clock, using audio only to gently correct sustained drift.
            # This also works with muted/disabled audio, without jumps on resume.
            elapsed = max(0.0, st - self.last_st) if st is not None else 0.0
            if st is not None:
                self.last_st = max(self.last_st, st)
            if not renpy.music.get_pause(channel="closing_theme"):
                position = self.last_position + elapsed
                audio_position = renpy.music.get_pos(channel="closing_theme")
                if audio_position is not None:
                    drift = audio_position - position
                    # Ignore normal buffering; cap synchronization changes at
                    # 5% of elapsed time so the camera can never jump backward.
                    if abs(drift) > .10:
                        position += max(-elapsed * .05, min(elapsed * .05, drift))
                self.last_position = position
            return self.last_position

        def draw_shot(self, result, index, position, alpha, st, at):
            shot = CLOSING_THEME["shots"][index]
            # Hold both pictures still while they blend. Movement starts once
            # the new picture is clear, and settles before the next dissolve.
            start = shot["at"] + (CLOSING_THEME["dissolve"] if index else CLOSING_THEME["fade_in"])
            end = (THEME_STARTS[index + 1] if index + 1 < len(THEME_STARTS)
                   else CLOSING_THEME["duration"] - CLOSING_THEME["fade_out"])
            progress = min(1.0, max(0.0, (position - start) / (end - start)))
            progress = progress * progress * (3.0 - 2.0 * progress)
            first, last = shot["zoom"]
            zoom = 1.0 if self.reduced_motion else first + (last - first) * progress
            child = Transform(self.children[index], zoom=zoom, alpha=alpha, subpixel=True)
            picture = renpy.render(child, 1920, 1080, st, at)
            fx, fy = shot["focus"]
            tx, ty = shot.get("focus_to", shot["focus"])
            fx, fy = fx + (tx - fx) * progress, fy + (ty - fy) * progress
            # Render bounds are integers; deriving the offset from those bounds
            # makes a slow camera jump. Keep scale and position fractional.
            result.subpixel_blit(picture, (1920 * (1.0 - zoom) * fx,
                                          1080 * (1.0 - zoom) * fy))

        def render(self, width, height, st, at):
            position = self.position(st)
            index = max(0, min(len(THEME_STARTS) - 1, bisect.bisect_right(THEME_STARTS, position) - 1))
            result = renpy.Render(1920, 1080)
            result.blit(renpy.render(Solid("#000"), 1920, 1080, st, at), (0, 0))
            fade = 1.0 if self.reduced_motion else min(
                1.0, position / CLOSING_THEME["fade_in"],
                max(0.0, CLOSING_THEME["duration"] - position) / CLOSING_THEME["fade_out"])
            blend = min(1.0, (position - THEME_STARTS[index]) / CLOSING_THEME["dissolve"])
            blend = blend * blend * (3.0 - 2.0 * blend)
            if index and blend < 1.0 and not self.reduced_motion:
                self.draw_shot(result, index - 1, position, fade, st, at)
                self.draw_shot(result, index, position, blend * fade, st, at)
            else:
                self.draw_shot(result, index, position, fade, st, at)
            if position >= CLOSING_THEME["title_at"]:
                title_alpha = 1.0 if self.reduced_motion else min(
                    1.0, (position - CLOSING_THEME["title_at"]) / CLOSING_THEME["title_fade"])
                for child, y in ((self.title, 465), (self.subtitle, 560)):
                    text_render = renpy.render(Transform(child, alpha=title_alpha * fade), 1920, 1080, st, at)
                    result.blit(text_render, (1920 * CLOSING_THEME.get("title_x", .5) - text_render.width / 2, y))
            # Let the display refresh drive animation; a 50fps timer on a 60Hz
            # display alternates frame holds even with perfectly smooth motion.
            renpy.redraw(self, .1 if self.reduced_motion or renpy.music.get_pause(channel="closing_theme") else 0)
            return result.subsurface((0, 0, 1920, 1080))

        def event(self, ev, x, y, st):
            if self.position(st) >= CLOSING_THEME["duration"]:
                return "finished"
            renpy.timeout(.1)

        def visit(self):
            return self.children + [self.title, self.subtitle]

    def toggle_closing_theme_pause():
        renpy.music.set_pause(not renpy.music.get_pause(channel="closing_theme"), channel="closing_theme")
        renpy.restart_interaction()

screen closing_theme():
    modal True
    default player = ClosingTheme(persistent.reduced_motion)
    on "show" action [Function(renpy.music.set_pause, False, channel="closing_theme"), Play("closing_theme", CLOSING_THEME["audio"], loop=False, relative_volume=10 ** (CLOSING_THEME["runtime_gain_db"] / 20.0))]
    on "hide" action [Stop("closing_theme"), Function(renpy.music.set_pause, False, channel="closing_theme")]
    add player id "montage"
    hbox:
        xalign .98
        yalign .97
        spacing 15
        textbutton ("Resume" if renpy.music.get_pause(channel="closing_theme") else "Pause"):
            action Function(toggle_closing_theme_pause)
            background Solid("#07191dbb")
            text_size 23
        textbutton "Skip closing theme":
            action Return("skipped")
            background Solid("#07191dbb")
            text_size 23
    key "K_SPACE" action Function(toggle_closing_theme_pause)
    key "game_menu" action Return("skipped")

label play_closing_theme:
    stop music fadeout .5
    stop ambience fadeout .5
    call screen closing_theme
    stop closing_theme
    play music "audio/home_theme.ogg" fadein 1.5
    return
