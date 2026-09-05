# Definitions follow this reading, not persistent completion or visited menus.
init python:
    import json as glossary_json
    from glossary_rules import revealed_glossary

    with renpy.file("glossary.json") as glossary_file:
        GLOSSARY_ENTRIES = glossary_json.load(glossary_file)["entries"]

    def glossary_entries():
        return revealed_glossary(
            GLOSSARY_ENTRIES, BOOK_SCENE_KEYS, scene_key, visited_scenes,
            (entry.what for entry in _history_list),
        )

    def glossary_description(key):
        return glossary_entries().get(key, {}).get("description", "")

screen glossary():
    tag menu
    default selected_term = None
    $ known_terms = glossary_entries()
    $ term = selected_term if selected_term in known_terms else next(iter(known_terms), None)
    use book_menu("Glossary"):
        vbox:
            spacing 28
            text "Terms and details appear as this part of the story introduces them." style "small_text"
            if known_terms:
                hbox:
                    spacing 55
                    viewport:
                        xsize 340
                        ysize 690
                        scrollbars "vertical"
                        vscrollbar_unscrollable "hide"
                        mousewheel True
                        draggable True
                        pagekeys True
                        vbox:
                            spacing 8
                            for key, entry in known_terms.items():
                                textbutton entry["title"]:
                                    action SetScreenVariable("selected_term", key)
                                    selected key == term
                                    xsize 310
                                    padding (15, 12)
                                    text_size 27
                                    background Solid("#c2ae8512")
                                    hover_background Solid("#c2ae8530")
                                    selected_background Solid("#c2ae8538")
                    viewport:
                        xsize 910
                        ysize 690
                        scrollbars "vertical"
                        vscrollbar_unscrollable "hide"
                        mousewheel True
                        draggable True
                        pagekeys True
                        vbox:
                            spacing 25
                            text known_terms[term]["title"] size 43 color "#d9bf8e"
                            text known_terms[term]["description"] id "glossary_description" size 31 line_spacing 10 xmaximum 855
            else:
                text "No terms yet. As you read, you can return here for a reminder." size 31 xmaximum 1100
