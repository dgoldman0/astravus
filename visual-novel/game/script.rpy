# Adapted from revision/latest.md, Book I. See docs/ADAPTATION.md.
# Say IDs are retained where possible; start fresh to review revised scene pacing.
# Keep a cue running across adjacent scenes that share it; new cues still fade.
label start:
    stop music fadeout 1.0
    $ met_cassia = False
    $ met_joren = False
    $ visited_scenes = []
    $ pending_scene_save = None
    $ lumen_known = False
    $ joren_lost = False
    $ childhood_stage = "early"
    $ quick_menu = True
    jump chapter_one

label chapter_one:
    $ enter_scene("first_memory")
    scene cg first_memory
    with mood_transition()
    play music "audio/first_light.ogg" fadein 2.0 if_changed
    call screen chapter_card("BOOK I", "Seeds of Youth", "Calista's childhood · A life remembered")
    $ remember_scene("first_memory")

    r "My earliest memory wasn't really mine." id opening_001
    r "It belonged to the people who brought me home." id opening_002
    n "They told me about the Sanctuary. About my First Breath, and the five pairs of hands waiting to hold me." id opening_003
    n "In every telling, someone remembered a different thing: the sound I made, or the way I gripped a finger and wouldn't let go." id opening_004
    r "I used to ask them to tell it again. They always began with the joy of it." id opening_006
    r "Only later did I wonder how nervous they'd been. They'd brought Kael home before me, but did that make it any easier?" id opening_007
    n "Lumen, the child of Aurora and Nyx, was still a young world when I was born." id opening_008
    n "My own parents were Maia, Arin, Selene, Dorian, and Sage." id opening_009
    $ scene_title = "The shape of home"
    scene bg family_home
    with mood_transition()
    n "The home I grew to know gathered around a round wooden table. There were books on the seats, drawings on the walls, and always something left unfinished." id opening_home_001
    show shadow at shadow_home
    show barkley at barkley_home
    show nibble at nibble_home
    with mood_transition()
    n "Shadow watched from the sofa. Barkley came to meet us at the door. Nibble's tiny feet tickled when she ran across my hand." id opening_home_002
    n "With Lyra's arrival, my parents' constellation had three children to raise together." id opening_010
    n "Arin's workshop hummed. Selene's music found its way under every door. Dorian could turn a question about breakfast into the history of an entire world." id opening_011
    n "Sage made sure everyone had their say. My older brother Kael usually had a plan; my younger sister Lyra usually had questions about it." id opening_012
    scene bg garden_close
    with mood_transition()
    play ambience "audio/garden_air.ogg" fadein 2.0 if_changed
    $ remember_scene("garden")
    n "And Maia had the garden." id opening_013
    n "It folded around our home: pond water, dark leaves, paths lit by little living lights. Beyond the garden wall, there were paths I had yet to follow." id opening_014
    r "I knew the smell of that garden before I knew what a garden was." id opening_015
    n "Wet earth. Warm wood. Something green crushed gently between a finger and a thumb." id opening_016
    n "When I try to remember the beginning, that is where I find myself." id opening_017

label garden_lesson:
    $ enter_scene("garden")
    scene bg garden_close
    play music "audio/home_theme.ogg" fadeout 2.0 fadein 2.0 if_changed
    play ambience "audio/garden_air.ogg" fadeout 1.0 fadein 1.0 if_changed
    show maia at at_right
    show calista young at at_left
    with mood_transition()
    n "One morning Maia cleared a little patch beside the path and called me over." id seed_001
    m "Here, Cali." id seed_002
    n "She opened her hand. A single striped seed lay in her palm." id seed_003
    c "What will it grow into?" id seed_004
    m "A sunflower. Tall and bright, just like you." id seed_006
    c "One of the big ones?" id seed_008
    m "Oh, taller than Kael." id seed_009
    n "I took it carefully and looked along the bed for a space." id seed_007
    c "Here. I want it here." id seed_010
    m "All right. Make a hole with your finger." id seed_011
    n "Maia's hand guided mine as I pressed a finger into the soil. Then she nudged a little earth back in." id seed_014
    m "There. That's plenty." id seed_016
    n "I set the seed in the hollow. We covered it together, and she passed me the watering can." id seed_018
    c "Will it be up tomorrow?" id seed_019
    m "It needs a little patience first." id seed_020
    c "But I can look tomorrow." id seed_022
    m "Of course. We'll take care of it together." id seed_023
    n "I tipped the can too far. Water splashed onto my boots, and Maia caught the handle." id seed_021
    m "Slowly. Let me hold this bit." id seed_015
    n "This time most of it reached the soil. When we put the can down, I couldn't see where we'd made the hole." id seed_017
    c "How will I know which one's mine?" id seed_028
    m "We could put a stone beside it." id seed_030
    n "I chose a flat stone from the edge of the path and pressed it into the wet earth." id seed_029
    n "I stood back on the path to check that I could spot the stone. Maia waited with the watering can against her knee." id seed_033
    m "Come on, Cali. Let's wash our hands." id seed_034
    hide maia
    hide calista
    with mood_transition()
    r "I went back every morning. For a while, there was only the stone." id seed_036
    scene bg garden
    with mood_transition()
    n "From that patch I could see the ladder into the old oak. I'd played in the hollow underneath it, but I had never climbed all the way up." id seed_039
    $ renpy.force_autosave(take_screenshot=True, block=True)
    call family_book_one

label meeting_cassia:
    $ enter_scene("meeting_cassia")
    scene bg community_courtyard
    with mood_transition()
    play music "audio/discovery_theme.ogg" fadeout 2.0 fadein 2.0 if_changed
    play ambience "audio/plaza_air.ogg" fadeout 1.5 fadein 1.5 if_changed
    n "As I grew, I went farther from the garden. At one community gathering, I stopped to listen to a girl telling a story." id cassia_001
    n "A few children sat around her. I stayed at the edge, with my sketchbook held against my chest." id cassia_003
    show cassia young at at_right
    with mood_transition()
    a "Its wings shone like starlight. When it flew, even the clouds seemed to make room for it." id cassia_004
    show calista young at at_left
    with mood_transition()
    n "I could picture the creature as she spoke. She noticed me listening and made a space on the blanket." id cassia_010
    a "It just landed here. What color do you think its eyes are?" id cassia_007
    c "Purple. With little bits of gold." id cassia_008
    a "Yes! Like the first stars coming out." id cassia_009
    hide calista
    hide cassia
    show cg cassia_storytelling
    with mood_transition()
    n "I sat beside her and opened my sketchbook. The other children leaned closer as I began to draw the creature from her story." id cassia_013
    a "I'm Cassia. What's your name?" id cassia_018
    $ met_cassia = True
    c "Cali." id cassia_028
    a "Do you want to join our adventure? We're about to find out what it's searching for." id cassia_invitation
    c "Can I draw the way there?" id cassia_acceptance
    a "Yes. We'll need that if we get lost." id cassia_map
    n "By the time our parents came to find us, the creature had crossed three rivers. We'd used another page for the last one." id cassia_020
    c "But we haven't finished." id cassia_021
    a "You can bring it back. Will you be here next time?" id cassia_022
    c "I think so. Don't go on without me." id cassia_029
    a "I won't. You have to draw the next bit." id cassia_030
    hide cg
    with mood_transition()
    n "At the next gathering, I went looking for her. Soon we were visiting each other's homes, too." id cassia_023
    $ renpy.force_autosave(take_screenshot=True, block=True)
    call cassia_family_visit

label meeting_joren:
    $ enter_scene("meeting_joren")
    scene bg construction_path
    with mood_transition()
    play music "audio/discovery_theme.ogg" fadeout 1.5 fadein 1.5 if_changed
    play ambience "audio/workshop_air.ogg" fadeout 1.5 fadein 1.5 if_changed
    n "I first met Joren in one of Lumen's construction zones. He came around the corner at the head of a group of children, laughing and calling for the others to catch up." id joren_002
    show joren young at at_right
    show calista young at at_left
    with mood_transition()
    j "Come on, let's explore! Let's see who can find the coolest thing first!" id joren_004
    $ met_joren = True
    c "You're on! But I bet I'll find something amazing before you do." id joren_007
    j "I'm Joren. What's your name?" id joren_006
    c "Cali." id joren_021
    j "Come on, Cali!" id joren_009
    n "I tucked my sketchbook into my bag and ran after him. Half-built passages branched ahead of us; every turning looked worth trying." id joren_011
    j "You're pretty fast for an artist!" id joren_013
    c "You'll have to keep up, then." id joren_014
    n "He laughed with his whole body and hurried alongside me. The other children followed us through the archway." id joren_017
    n "By the end of the afternoon, we were already planning where to explore next." id joren_033
    hide calista
    hide joren
    with mood_transition()
    call joren_family_visit

label after_joren_family:
    n "When I introduced Joren to Cassia, he wanted to know where the creature in my sketchbook lived. Cassia said she could show him." id joren_018
    scene bg family_home
    with mood_transition()
    stop ambience fadeout 2.0
    n "We spread out some paper at home. By lunchtime our map had taken over the table, and Maia needed it back." id joren_019
    n "After that, more and more of our afternoons ended in the treehouse." id joren_020
    $ renpy.force_autosave(take_screenshot=True, block=True)

label the_treehouse:
    $ enter_scene("treehouse")
    scene bg garden
    with mood_transition()
    play music "audio/discovery_theme.ogg" fadeout 1.5 fadein 1.5 if_changed
    play ambience "audio/garden_air.ogg" fadein 2.0 if_changed
    play sound "audio/wood.wav"
    n "One afternoon I climbed up ahead of the others. Joren stopped on the landing to help Cassia with the last rung." id tree_001
    j "Remember the first time, Cali? You wouldn't look down." id tree_002
    c "I wasn't that scared." id tree_003
    a "Can you take my book before you start arguing?" id tree_005
    n "I reached back for it. By then, I knew which boards creaked and where to duck under the branches." id tree_006
    scene bg treehouse
    with mood_transition()
    $ remember_scene("treehouse")
    n "Our drawings covered the walls. Stones and feathers filled the little chests; the blankets never stayed folded for long." id tree_007
    n "Through the leaves, we could see patches of Maia's garden and the glowing paths below." id tree_008
    show cassia young at at_left
    show joren young at at_right
    with mood_transition()
    a "Do you think we'll ever outgrow this place?" id tree_010
    c "We could move the table. There's room." id tree_011
    a "I mean, will we still want to come?" id tree_012
    j "I will. We'll always meet here, no matter how old we get." id tree_promise
    a "Promise?" id tree_promise_question
    c "I'll come too." id tree_009
    n "Joren had unrolled the map on the little table. One end curled back up as soon as he let go." id tree_013
    j "Can someone hold this?" id tree_015
    n "Cassia put her book on one corner. I found a smooth stone for the other." id tree_014
    j "We can put the creature here." id tree_017
    c "That's the pond." id tree_018
    j "It's a sea on the map." id tree_016
    c "But it needs somewhere to land." id tree_019
    a "An island. Leave a bit in the middle." id tree_021
    n "I drew around a patch of empty paper. Joren reached for the pencil." id tree_020
    j "And a path, all the way—" id tree_022
    c "Wait. I'm not finished." id tree_023
    n "He pulled his hand back. I added a tree, then passed him the pencil." id tree_024
    j "I'm going round here, then." id tree_037
    a "No, it sleeps in that tree. You wake it up if you step on the roots." id tree_038
    j "Then we'll go round the back." id tree_039
    a "There's a river at the back." id tree_040
    j "Cassia!" id tree_041
    a "Well, there is." id tree_042
    n "He took the path right to the edge of the page. Cassia followed his pencil, already telling him what was waiting there." id tree_027
    n "Some days that table was the deck of a pirate ship. On others, it was a station above a distant planet, and Joren was our captain." id tree_025
    n "When we needed more supplies, someone went down to the hollow beneath the treehouse. We kept treasures there, too, behind its second entrance." id tree_026
    hide cassia
    hide joren
label chapter_rain_refuge:
    $ enter_scene("rain_refuge")
    play music "audio/rain_refuge.ogg" fadeout 2.0 fadein 3.0 if_changed
    stop ambience fadeout 2.0
    play ambience "audio/rain.ogg" fadein 3.0 if_changed
    scene bg treehouse_rain
    with mood_transition()
    n "On rainy afternoons, we huddled under blankets while the drops pattered on the wooden roof." id rain_001
    n "One afternoon, a branch creaked overhead. Cassia looked up from our map." id rain_003
    a "Imagine a world where the trees could talk." id rain_004
    c "All of them?" id rain_005
    a "Even this one. What do you think it would say?" id rain_006
    j "It must know loads of things. Look how old it is." id rain_007
    j "I'd ask it where to go next. There must be places we haven't found." id rain_009
    c "Maybe it only knows this garden." id rain_010
    a "Its roots go farther than that." id rain_014
    n "Cassia traced a root across the map with her finger, out past the river and the edge of the page." id rain_008
    j "So what did it find?" id rain_011
    a "You have to let me tell it." id rain_015
    n "We settled closer under the blanket, and she began." id rain_016
    n "Rain kept falling through the leaves. For once, Joren wasn't in a hurry to go anywhere." id rain_020
    jump book_one_later
