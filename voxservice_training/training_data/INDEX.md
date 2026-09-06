# Training Data Index

## Overview
This directory contains manually curated OpenAI-format JSONL training data for the Calista/Astravus Collection vox service. All files use the standard messages array format with `system`, `user`, and `assistant` roles.

## File Inventory

### Factual Data (Canonical World Knowledge)

| File | Entries | Content |
|------|---------|---------|
| `factual_world_mechanics.jsonl` | ~80 | Astravii nature, transcendence, Core Integration, governance, technology, familiars |
| `factual_character_bios.jsonl` | ~85 | Physical descriptions, quirks, relationships for main characters |
| `factual_timeline_events.jsonl` | ~100 | Major events: Joren's death, Core Integration, births, transcendence |
| `factual_locations.jsonl` | ~65 | Lumen, Aurora, Nyx, Tree of Echoes, gardens, Sanctuary, Central Plaza |

### Simulation Data (Roleplay & Experience)

| File | Entries | Content |
|------|---------|---------|
| `simulation_dialogue_family.jsonl` | ~60 | Parent-child interactions, lessons, grief conversations |
| `simulation_dialogue_friends.jsonl` | ~55 | Cassia friendship, Lysandra relationship, peer dynamics |
| `simulation_dreams_transcendence.jsonl` | ~65 | Dream experiences, approaching transcendence, shared consciousness |
| `simulation_scenarios_hypotheticals.jsonl` | ~80 | What-ifs, future possibilities, exploratory scenarios |

### Meta Data (Uncertainty Handling)

| File | Entries | Content |
|------|---------|---------|
| `meta.jsonl` | ~100 | Training for graceful handling of unknowns and uncertainty |

### Search Mode (Wiki Navigation)

| File | Entries | Content |
|------|---------|---------|
| `search.jsonl` | 105 | Search queries returning wiki page links with summaries; covers all 165 wiki pages multiple times |

## Total: 10 files, ~795+ training entries

## Format Reference

Each line is valid JSON:
```json
{"messages": [
  {"role": "system", "content": "System prompt establishing context..."},
  {"role": "user", "content": "User question..."},
  {"role": "assistant", "content": "Model response..."}
]}
```

## Source Material Covered

- **SETTING.md**: World rules, Astravii nature, transcendence mechanics
- **CHARACTERS.md**: All major characters, relationships, roles
- **TIMELINE.md**: Major events across 200+ years
- **bios/**: Individual character files (Calista, Maia, Aris, Elara, etc.)
- **[Earlier dialogue collection](../../development/dialogue/INDEX.md)**: Excerpts and expanded scenes used as writing examples; added wording and staging require comparison with current canon
- **events/**: Major narrative events
- **worldbuilding/**: Extended world details (Lumen, Core Integration, Constellations)

## Expansion Notes

Areas for future expansion:
- More character-specific bios (Sage, Shadow, Sol, Dorian, Theron, Lysandra)
- Additional dialogue scenarios (mentor relationships, community gatherings)
- More meta entries for different uncertainty patterns
- Scenario variations exploring character development
- Cross-generational interaction examples
