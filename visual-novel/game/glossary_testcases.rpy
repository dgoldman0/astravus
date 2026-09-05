# Development-only tests; excluded from desktop and browser exports.
testcase glossary_review:
    assert screen "main_menu"
    click "Begin Book I"
    click "Enter the memory"
    assert eval (not glossary_entries()) timeout 4.0
    click "Glossary"
    assert screen "glossary"
    assert eval ("No terms yet" in _test_screen_text("glossary") and "Transcendence" not in _test_screen_text("glossary"))
    pause .4
    screenshot "glossary-empty"
    click "Return"
    advance until eval (_history_list[-1].what.startswith("They told me about the Sanctuary."))
    assert eval (set(glossary_entries()) == {"first_breath", "sanctuary"})
    click "Glossary"
    click "Sanctuary"
    assert eval ("waiting parents" in _test_screen_text("glossary") and "Astravus" not in _test_screen_text("glossary"))
    screenshot "glossary-first-use"
    click "Return"
    run Rollback(force=True)
    assert eval (not glossary_entries()) timeout 4.0
    advance until eval (_history_list[-1].what.startswith("Shadow watched from the sofa."))
    assert eval ("familiar" not in glossary_entries())
    advance until eval (_history_list[-1].what == "Our familiars were part of the family, each with their own place in our daily lives.")
    assert eval ("familiar" in glossary_entries() and "constellation" not in glossary_entries())
    click "Glossary"
    click "Familiar"
    assert eval (all(name in _test_screen_text("glossary") for name in ("Shadow", "Barkley", "Nibble")) and all(term not in _test_screen_text("glossary").lower() for term in ("core integration", "longevity", "astraviin")))
    click "Return"
    run Rollback(force=True)
    assert eval ("familiar" not in glossary_entries()) timeout 4.0
    advance until eval (_history_list[-1].what.startswith("With Lyra's arrival,"))
    assert eval (set(glossary_entries()) == {"first_breath", "sanctuary", "lumen", "familiar", "constellation"})
    click "Glossary"
    click "Constellation"
    assert eval ("romantic partnership among adults" in _test_screen_text("glossary"))
    screenshot "glossary-constellation"
    click "Return"
    run FileSave(12, confirm=False, page="1")
    $ persistent.chapter_spoiler_warnings = False
    click "Chapters"
    click "09 · The Tree of Echoes"
    assert eval (glossary_entries()["lumen"]["level"] == 0 and "tree_of_echoes" not in glossary_entries()) timeout 4.0
    advance until eval (_history_list[-1].what == "The Tree of Echoes. Dorian told us about it.")
    assert eval (glossary_entries()["tree_of_echoes"]["level"] == 0)
    advance until eval (_history_list[-1].what.startswith("It grew from a seed another Astravus gave."))
    assert eval (glossary_entries()["tree_of_echoes"]["level"] == 1 and glossary_entries()["lumen"]["level"] == 0)
    advance until eval (_history_list[-1].what.startswith("Lumen was a living ship."))
    assert eval (not lumen_known and glossary_entries()["lumen"]["level"] == 1)
    click "Glossary"
    click "Lumen"
    assert eval ("living Astravus" in _test_screen_text("glossary") and "Transcendence" not in _test_screen_text("glossary"))
    screenshot "glossary-lumen-reveal"
    click "People"
    click "Lumen"
    assert eval (people_lumen_description() == glossary_description("lumen"))
    click "Return"
    run Rollback(force=True)
    assert eval (glossary_entries()["lumen"]["level"] == 0 and "living" not in people_lumen_description()) timeout 4.0
    click "Chapters"
    click "25 · The news"
    assert eval ("transcendence" not in glossary_entries() and "astraviin" not in glossary_entries()) timeout 4.0
    advance until eval (_history_list[-1].what.startswith("In our world, where transcendence"))
    assert eval (len(glossary_entries()) == 9)
    click "Glossary"
    click "Transcendence"
    assert eval ("Joining with one's Astravus" in _test_screen_text("glossary") and "Core" not in _test_screen_text("glossary"))
    screenshot "glossary-later-knowledge"
    click "Return"
    run FileLoad(12, confirm=False, page="1")
    assert eval (scene_key == "first_memory" and len(glossary_entries()) == 5 and "familiar" in glossary_entries() and glossary_entries()["lumen"]["level"] == 0) timeout 4.0
    click "Chapters"
    click "07 · Three ways forward"
    assert eval ("astravus" not in glossary_entries() and len(glossary_entries()) == 5) timeout 4.0
    advance until eval (_history_list[-1].what.startswith("They lived aboard an Astravus,"))
    assert eval ("astravus" in glossary_entries() and glossary_entries()["lumen"]["level"] == 0)
    click "Glossary"
    click "Astravus"
    assert eval ("living ship" in _test_screen_text("glossary") and "Transcendence" not in _test_screen_text("glossary"))
    screenshot "glossary-astravus-before-lumen"
    click "Return"
    run MainMenu(confirm=False)
    assert screen "main_menu" timeout 4.0
    click "Begin Book I"
    click "Enter the memory"
    assert eval (not glossary_entries()) timeout 4.0
    exit
