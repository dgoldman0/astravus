# Book I, Early Friendships. Canonical events: revision/latest.md:345–513.
# Dialogue and small physical beats adapt the prose; see BOOK_ONE_COVERAGE.md.
define thalia = Character("Thalia", who_color="#d2b4c7")
define lyron = Character("Lyron", who_color="#bfd0a3")
define soren = Character("Soren", who_color="#dbb18a")
define kaleb = Character("Kaleb", who_color="#d3bd85")

label cassia_family_visit:
    $ enter_scene("cassia_home")
    scene bg cassia_home
    with mood_transition()
    play music "audio/home_theme.ogg" fadeout 2.0 fadein 2.0
    play ambience "audio/room_air.ogg" fadeout 1.0 fadein 1.0
    n "Cassia's home had paper in places I hadn't thought of keeping paper. Between books. Under cups. Drying from a line above the table."
    show calista home at at_left
    show cassia young at at_right
    with mood_transition()
    a "That one's mine. Thalia says I have to let the paint dry before I put it away."
    c "You painted the wind."
    a "It's taking somebody's hat. Look."
    n "Her mother brought tea. Thalia moved a drawing by its dry corner and found room for the cups."
    thalia "Cassia tells me you've been making maps together."
    c "She keeps putting rivers in the way."
    a "There have to be things in the way."
    n "Thalia listened to both of us before she sat down. At work, she helped people through disagreements much larger than our imaginary rivers."
    thalia "So, Cali, you want to get somewhere. And Cassia wants something to happen on the journey."
    c "I want things to happen too. I just want to finish drawing them."
    a "You could say when you're ready for the next bit."
    thalia "That sounds like something you can try."
    c "Is that what you do? When people argue?"
    thalia "I listen until I understand what they're trying to say. Sometimes that takes a while."
    c "What if they're still angry?"
    thalia "Then I try not to hurry them."
    n "Cassia pushed the drawing toward me, leaving her cup on its own patch of table."
    a "There's room on this side. If you want it."
    n "On another evening, her father showed us how the gardens shared water. Lyron managed agricultural systems; a question about a plant could lead him all through Lumen."
    lyron "If this bed uses the water, what happens farther along?"
    c "Does the next one get less?"
    lyron "It could. That's one of the things we watch. A garden doesn't stop at its own wall."
    a "Cali's Maia has a pond."
    c "And things growing in it. Does that count too?"
    lyron "Very much."
    c "So the water goes through everything. The plants, and us, and back again."
    lyron "Yes. We have to care for the whole journey."
    hide calista
    hide cassia
    with mood_transition()
    n "Later, Lyron and Dorian would sit together long after everyone else had finished eating. One followed the water; the other followed the stories of the people who tended it."
    n "Cassia kept a place for our unfinished map. The next time I came, she'd found a bigger sheet of paper."
    return

label joren_family_visit:
    $ enter_scene("joren_home")
    scene bg soren_workshop
    with mood_transition()
    play music "audio/discovery_theme.ogg" fadeout 2.0 fadein 2.0
    play ambience "audio/workshop_air.ogg" fadeout 1.0 fadein 1.0
    n "Joren's mother, Soren, had a workshop full of unfinished inventions. He could tell me what nearly all of them were meant to do."
    show joren young at at_right
    show calista home at at_left
    with mood_transition()
    j "That one used to turn the wrong way."
    soren "It still does, if you put the contacts back where you found them."
    j "I only did it once."
    n "She looked up from the bench. Her short hair was pushed back with one grease-marked hand; the other kept a small assembly steady."
    soren "What would you make, Cali? Something you could take exploring?"
    c "A little rover. It could go ahead and show us what's there."
    j "It needs lights."
    c "It needs wheels first."
    soren "Then start there. What does it have to get across?"
    c "Stones. And roots. Things we can't see around."
    n "She cleared a place beside her. I sketched while Joren searched the parts trays. Soren made us turn the drawing around and look at it from the ground."
    c "That bit would catch."
    soren "What could you change?"
    n "I rubbed out a line. The rover was still mostly a drawing when we stopped, but I could see how we might begin."
    hide calista
    hide joren
    with mood_transition()
    $ enter_scene("kaleb_walk")
    scene bg construction_path
    with mood_transition()
    play ambience "audio/garden_air.ogg" fadeout 1.0 fadein 1.0
    n "His father, Kaleb, sometimes took us down passages we hadn't followed before. He brought stories back from expeditions; we wanted every walk with him to become one."
    show calista home at at_left
    show joren young at at_right
    with mood_transition()
    kaleb "What are you hoping to find today?"
    j "Somewhere nobody's been."
    c "Something nobody's noticed."
    kaleb "Those aren't always the same place."
    n "He let us choose a turning, then asked how we would recognize it on the way back. Joren studied the arch. I drew its uneven curve."
    j "You'll know it because you drew it."
    c "So will you. I can show you."
    n "Kaleb's maps were full of places we couldn't reach yet. At home, among Soren's prototypes, we tried to make things that might take us farther."
    hide calista
    hide joren
    with mood_transition()
    return

label book_one_later:
    $ enter_scene("waterwheel")
    $ childhood_stage = "later"
    scene bg workshop
    with mood_transition()
    play music "audio/discovery_theme.ogg" fadeout 2.0 fadein 2.0
    play ambience "audio/workshop_air.ogg" fadeout 1.0 fadein 1.0
    n "As we grew, the things we imagined began to turn into things we wanted to build. My old overalls no longer reached my ankles. Our plans took up more than paper."
    show calista older at at_left
    show joren older at at_right
    with mood_transition()
    j "If the water pushes here, the whole thing turns."
    c "Unless it catches on the side."
    j "It won't."
    n "It did. I held the two supports while he tried the little wheel again. One paddle scraped the wood."
    c "There. Hear it?"
    arin "May I have a look?"
    n "Arin watched us turn it before touching anything. Then they showed us how to check the spacing on the axle."
    arin "You want room to move, but not so much that it wanders."
    j "Can we cut this bit down?"
    arin "A little. Mark it first."
    n "We learned to shape the wood, fit the pieces, try them, and take them apart again. Cassia kept the smaller parts from disappearing into the shavings."
    hide calista
    show cassia older at at_left
    with mood_transition()
    a "This one's yours, Joren. You put it down three times."
    j "I know where it is."
    a "Now you do."
    c "Try it again. Slowly."
    n "The paddle passed the support. Joren turned it once more, watching the gap."
    scene bg waterwheel
    with mood_transition()
    play ambience "audio/garden_air.ogg" fadeout 1.5 fadein 1.5
    n "When we carried it to the pond, Lyra was waiting. Arin helped us settle the supports; water pressed against the little wooden paddles."
    lyra "Look at it go!"
    show calista older at at_left
    show joren older at at_right
    with mood_transition()
    j "It's working. Cali, look."
    c "I am looking."
    n "Shadow watched from the stones. Barkley's bark startled Nibble off her perch, and Cassia caught the box of spare pieces before it tipped."
    show shadow at shadow_path
    show barkley at barkley_path
    show nibble at nibble_path
    with mood_transition()
    a "Let's leave it alone for a minute."
    n "For a while we did. We watched something we'd made answer the moving water."

    $ enter_scene("outer_exploration")
    scene bg construction_path
    with mood_transition()
    play ambience "audio/workshop_air.ogg" fadeout 1.5 fadein 1.5
    n "The outer construction areas became another place to explore. We packed a small bag, Arin's multi-tool, and a portable scanner."
    show joren older at at_right
    show calista older at at_left
    with mood_transition()
    n "Joren went ahead with a light. Cassia and Kael followed; Lyra stayed beside me, holding on whenever the path narrowed."
    lyra "Do you think there's something special? Is it far? Can we get back this way?"
    c "We'll remember the turnings. Stay with me."
    n "Machinery hummed beyond the passage. Shadow slipped ahead between the supports; Barkley and Nibble kept close."
    show shadow at shadow_path
    show barkley at barkley_path
    show nibble at nibble_path
    with mood_transition()
    j "In here. Look at all of this."
    hide calista
    hide joren
    scene bg construction_room
    show shadow at shadow_path
    show barkley at barkley_path
    show nibble at nibble_path
    with mood_transition()
    n "In a room of tools and machines, Cassia found a small device. A touch brought a blueprint into the air. We gathered around its pale lines."
    a "That's the passage we came through."
    c "And that bend. So where does this go?"
    j "We could build a hideout here. If we knew how these worked."
    kael "One thing at a time."
    n "We found tools for shaping materials, mechanisms that moved without anyone pushing them, plans for spaces that weren't finished yet."
    scene bg family_home
    with mood_transition()
    play ambience "audio/room_air.ogg" fadeout 1.0 fadein 1.0
    n "At home, I tried to explain three discoveries at once. Arin found me some paper."

    $ enter_scene("lyra_included")
    scene bg garden
    with mood_transition()
    play music "audio/home_theme.ogg" fadeout 2.0 fadein 2.0
    play ambience "audio/garden_air.ogg" fadeout 1.0 fadein 1.0
    n "Lyra came with us sometimes. To me, that seemed like often. To her, it wasn't nearly enough."
    show calista older at at_left
    show lyra young at at_right
    with mood_transition()
    lyra "Are you going again?"
    c "Cassia's waiting. We're looking for something."
    lyra "You always go with them. Don't you want to play with me? Is it because I'm little?"
    n "I had one hand on my bag. I put it down."
    c "I do want to. I didn't know you were waiting."
    lyra "I was right here."
    c "I'm sorry. Do you want to come today?"
    lyra "All the way?"
    c "With us. Yes."
    hide calista
    hide lyra
    with mood_transition()
    n "Cassia made room for her in the plan. Joren waited at the turnings. When we forgot and got ahead, I went back."
    n "Shadow rubbed against Lyra's cheek; Nibble climbed onto her shoulder. Her questions followed us down every path."
    n "The next time we packed a bag, Lyra brought hers too."

    $ enter_scene("dome_ascent")
    scene bg construction_path
    with mood_transition()
    play music "audio/discovery_theme.ogg" fadeout 2.0 fadein 2.0
    play ambience "audio/workshop_air.ogg" fadeout 1.0 fadein 1.0
    n "One day we found the unfinished dome. No one was working on it just then. Its scaffolding rose above us, full of places to put a hand or a foot."
    show joren older at at_right
    show calista older at at_left
    with mood_transition()
    j "Let's see the view from the top."
    c "How far up?"
    j "To that platform."
    n "I looked at the platform, then at the way back down. Cassia was doing the same."
    a "Together."
    n "We climbed carefully. At each level the paths below became smaller. I kept looking at the next place for my hand."
    scene bg dome
    with mood_transition()
    play music "audio/wonder_theme.ogg" fadeout 2.0 fadein 3.0
    play ambience "audio/garden_air.ogg" fadeout 2.0 fadein 2.0
    n "Then we were on the platform. Gardens and passages spread away beneath us; home was part of a pattern I couldn't see from the ground."
    a "It's like we're on top of the world."
    j "We are. Look how far it goes."
    c "I can't fit it on a page."
    n "We stayed through the afternoon, inventing journeys across the view. The light softened while we talked."
    n "When we climbed down, Shadow went ahead along the beams. Barkley stayed close to Lyra; Nibble rode on Cassia's shoulder."
    a "Can we come back?"
    c "I want to draw it next time."
    j "Then we'll bring more paper."

    $ enter_scene("treehouse_dispute")
    scene bg treehouse
    with mood_transition()
    play music "audio/discovery_theme.ogg" fadeout 2.0 fadein 2.0
    play ambience "audio/garden_air.ogg" fadeout 1.0 fadein 1.0
    n "We did not always agree. One afternoon, an argument over the next stage of an artifact hunt filled the treehouse."
    show calista frustrated at at_left
    show joren frustrated at at_right
    with mood_transition()
    j "We go this way. It's quicker."
    c "You haven't even looked at mine."
    j "I have. It takes us back round the same place."
    c "Because we haven't finished looking there."
    j "We've been there twice."
    c "You always want to be in charge."
    n "His face reddened. He paced beside the table, making the loose boards answer every turn."
    j "And you always think your idea's better."
    n "I opened my mouth before I knew what I would say."
    stop music fadeout 1.5
    a "Wait. Both of you."
    a "We're still trying to find the same thing. Tell me the two ways. One at a time."
    c "I was trying to."
    a "Then let him finish afterward."
    n "Shadow jumped onto the table between us. Barkley whined from the cushions; Nibble hurried around the edge of a box."
    show shadow at familiar_at(1130, 795, 240)
    show barkley at familiar_at(190, 795, 330)
    show nibble at familiar_at(735, 805, 95)
    with mood_transition()
    n "I moved the map away from Shadow's paws. Joren stopped pacing."
    j "You go first."
    c "I want to check the place by the roots. We left before I could see behind them."
    j "And I want to see what's past the bridge."
    a "Can we do both?"
    n "Not as quickly as either of us wanted. We worked out a way, with pauses where the argument kept trying to begin again."
    hide calista
    hide joren
    with mood_transition()
    play music "audio/rain_refuge.ogg" fadein 2.0
    n "Joren held the map flat while I marked the place by the roots. Then I passed him the pencil."
    n "There were more projects, more quarrels, and more afternoons when none of us wanted to go home."

    $ enter_scene("loss")
    scene bg home_dusk
    with mood_transition()
    stop music fadeout 2.0
    stop ambience fadeout 2.0
    n "Joren went with his family on a routine research expedition to a nearby moon."
    n "There was a malfunction. An accident. Rescue teams went out."
    n "Joren did not survive."
    $ joren_lost = True
    pause 1.0
    r "I remember hearing it and waiting for the rest of the sentence. For something that would change what it meant."
    n "There wasn't anything."
    n "Among the Astraviin, death before transcendence was almost unheard of. We expected centuries together. I had never thought to count them."
    r "This was not Joren joining his Astravus. It was an accident that ended his life."
    n "The words had reached me. I could repeat them. For a long time, they didn't seem able to belong to him."

    $ enter_scene("family_grief")
    play music "audio/grief_theme.ogg" fadein 4.0
    play ambience "audio/room_air.ogg" fadein 3.0
    show calista mourning at at_left
    show maia home at at_right
    with mood_transition()
    n "Maia stayed with me one evening. The house was familiar in every detail, and I couldn't find a familiar way to be in it."
    m "Cali."
    c "I keep thinking I should tell him something."
    m "I know."
    c "Then I remember. Every time."
    n "She waited. I watched the light on her hands."
    m "The things you did together still happened. The stories you tell, the things you remember—those are yours to keep."
    c "I don't want only those."
    hide maia
    hide calista
    with mood_transition()
    n "She put her arms around me."
    m "No. Of course you don't."
    c "Why did it happen?"
    m "I don't have an answer that will make it hurt less. I'm so sorry, sweetheart."
    c "It hurts all the time."
    m "You don't have to hold it by yourself. We're here."
    n "All my parents tried to reach me. Sometimes I could bear company; sometimes I couldn't answer even a small question."
    n "Lyra was frightened by our sadness. She was too young to understand why we couldn't bring him back."
    r "I wondered how people had lived when a century was almost all the time they had. Whether so much loss had ever become easier to understand."
    n "I couldn't imagine it. I could barely imagine tomorrow."

    $ enter_scene("painting_grief")
    scene bg family_home
    with mood_transition()
    show calista painting at at_left
    with mood_transition()
    n "Eventually, I began painting. Some days I could do that when I couldn't talk."
    n "I painted the paths we had taken and the places we had invented. His hair never seemed to be the right color at first. I kept trying."
    r "There was something to do with my hands. A color to mix. A line to find again."
    n "Shadow sat nearby. Barkley rested his head against my lap, and I held the brush still until he'd settled. Nibble interrupted me often enough that sometimes I looked up."
    hide calista
    show shadow at shadow_home
    show barkley at barkley_home
    show nibble at nibble_home
    with mood_transition()
    c "That's his side of the map. He wanted the path to go there."
    n "I said it to whoever was listening. Sometimes that was only Shadow."
    hide calista
    with mood_transition()
    n "When the light faded, I washed the brush and left the picture where I could find it in the morning."

    $ enter_scene("cassia_grief")
    scene bg treehouse
    with mood_transition()
    play ambience "audio/garden_air.ogg" fadeout 2.0 fadein 2.0
    show calista mourning at at_left
    show cassia mourning at at_right
    with mood_transition()
    n "Cassia and I kept finding each other. Some days we talked about him. Some days we sat with everything we couldn't say."
    a "I miss him."
    c "Me too."
    a "Do you think he knew? How much we wanted him here?"
    n "I looked at the drawings on the wall. At the corner of the map we'd held down together."
    c "I think he did. We kept coming back, didn't we? All of us."
    a "We said we always would."
    n "I reached for her hand."
    c "I remember."
    n "There wasn't a way to finish that conversation. We stayed in it for a while."
    a "Tell me about the light you found when you met him."
    c "It went blue if you stood in the right place. He kept stepping away and coming back."
    n "She listened. Then she told me something I hadn't been there to see. For a little while, I could imagine his laugh without losing the sound of her voice."
    hide calista
    hide cassia
    with mood_transition()

    $ enter_scene("community_memorial")
    scene bg memorial_plaza
    with mood_transition()
    stop music fadeout 3.0
    play ambience "audio/plaza_air.ogg" fadeout 2.0 fadein 2.0
    n "The central plaza filled with flowers and messages. I knew it as a place of lanterns and music. Now people stood together and spoke quietly."
    n "Soren's inventions were still around us, part of the workings of Lumen. I couldn't see them without thinking of the workshop, and Joren showing me what each thing was for."
    n "Kaleb spoke at one of the gatherings. I had heard him tell so many stories about going away and coming home."
    # Kaleb has no authored portrait yet; keep the children he addresses visible.
    show calista mourning at at_left
    show cassia mourning at at_right
    with mood_transition()
    kaleb "Joren wanted to see what was beyond the next turning. Most of you know that. Some of you had to go and fetch him."
    n "A few people smiled through their tears. Kaleb waited before going on."
    kaleb "He brought such life into a room. Such curiosity."
    kaleb "I want us to remember that part of him. The things he found. The things he made us stop and look at."
    kaleb "Keep finding things. Keep sharing them. That's something we can carry on for him."
    kaleb "And look after one another."
    n "He looked out across the people gathered there. No one hurried him away."
    play music "audio/remembrance_theme.ogg" fadein 4.0
    r "Lumen grieved with us. That didn't divide the hurt into smaller pieces, but it meant we didn't have to explain why it mattered."

    $ enter_scene("mural_remembrance")
    scene bg memory_mural
    with mood_transition()
    play ambience "audio/garden_air.ogg" fadeout 2.0 fadein 2.0
    show calista painting at at_left
    with mood_transition()
    n "In Maia's garden, I made a mural of our adventures. It held the places we'd known and the places we'd meant to find."
    n "I worked a little at a time. The wall was larger than any page I had used. Some days that helped."
    c "The tree needs to be wider here. We never left enough room for the creature to land."
    a "Then make it wider. It's your wall."
    n "Cassia helped me remember. We could disagree about a color, then fall quiet because we'd both thought of asking him."
    r "The garden gave the painting a life around it: water, leaves, people passing. I could go there when I wanted to be close to a memory."
    hide calista
    with mood_transition()

    $ enter_scene("treehouse_remembrance")
    scene bg treehouse_memory
    with mood_transition()
    play ambience "audio/rain.ogg" fadeout 2.0 fadein 3.0
    n "We brought new drawings to the treehouse, and messages to Joren. There were still maps we hadn't finished. We made room for both."
    a "He would have liked this one."
    c "Which part?"
    a "That you've made the river even bigger."
    c "That was your idea."
    n "For a moment we almost laughed. Then Cassia put her hand against the edge of the paper."
    a "Let's do the dome next. The view from the top."
    c "Together?"
    a "Yes."
    n "Rain moved through the leaves beyond the open windows. We listened to the familiar sound and began another drawing."

    $ enter_scene("annual_remembrance")
    scene bg memorial_plaza
    with mood_transition()
    play ambience "audio/plaza_air.ogg" fadeout 2.0 fadein 2.0
    r "Each year, the community gathered to remember him. We told stories, shared our grief, and celebrated the life he had lived."
    r "There were days when remembering brought warmth before it brought pain. There were others when I was back at the beginning."
    n "The treehouse and the mural remained places we could go. Cassia and I kept adding what we remembered."
    stop ambience fadeout 3.0
    n "But there would be no new adventures with Joren to add to the old ones."
    $ persistent.book_one_complete = True
    $ renpy.save_persistent()
    $ pending_scene_save = None
    window hide
    $ quick_menu = False
    $ renpy.force_autosave(take_screenshot=True, block=True)
    call screen chapter_end
    stop music fadeout 2.0
    stop ambience fadeout 1.5
    return
