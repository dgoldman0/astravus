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
    thalia "Understanding comes from listening first. What do you do when you disagree with someone, Cali?"
    c "I try to understand their side before I say mine. I don't always remember."
    thalia "It takes practice."
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
label chapter_kaleb_walk:
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
    j "It's working. Cali, look."
    c "We did it!"
    n "Shadow watched from the stones. Barkley barked excitedly, and Nibble ran along the bank to inspect our work."
    # Keep the small project visible and the companions on the stone banks.
    show shadow at familiar_at(90, 800, 205)
    show barkley at familiar_at(1805, 810, 330)
    show nibble at familiar_at(205, 765, 85)
    with mood_transition()
    a "Let's leave it alone for a minute."
    n "For a while we did. After all that measuring and adjusting, our little wheel was finally turning in the pond."

label chapter_outer_exploration:
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

label chapter_lyra_included:
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
    c "I'm sorry, Lyra. I didn't mean to make you feel left out. Do you want to come with us today?"
    lyra "All the way?"
    c "With us. Yes."
    hide calista
    hide lyra
    with mood_transition()
    n "Cassia made room for her in the plan. Joren waited at the turnings. When we forgot and got ahead, I went back."
    n "Shadow rubbed against Lyra's cheek; Nibble climbed onto her shoulder. Her questions followed us down every path."
    n "The next time we packed a bag, Lyra brought hers too."

label chapter_dome_ascent:
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

label chapter_treehouse_dispute:
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
    a "Hey, hey. Let's take a breath."
    a "We're a team, remember? Even the heroes in stories disagree sometimes—but they find a way."
    n "Even Shadow, who usually stayed out of our arguments, jumped onto the table between us, meowing loudly as if to say, 'Listen to Cassia!'"
    show shadow at familiar_at(1130, 795, 240)
    show barkley at familiar_at(190, 795, 330)
    show nibble at familiar_at(735, 805, 95)
    with mood_transition()
    n "Barkley sat down and whined softly, looking between Joren and me with concerned eyes. And Nibble ran circles around us, trying to lighten the mood with her antics."
    n "Her words, along with the pets' actions, were a reminder of the importance of cooperation, and we reluctantly agreed to put aside our differences and find a compromise."
    n "It wasn't always easy, but through these disagreements, we learned valuable lessons about communication, empathy, and the strength of our friendship."
    hide calista
    hide joren
    with mood_transition()
    play music "audio/rain_refuge.ogg" fadein 2.0
    n "Through our projects and adventures, we bonded and grew, learning from each experience."
    n "The lessons from our parents, each other, and our insightful pets shaped us, making us more resilient, creative, and empathetic."
    n "Our days were filled with discovery and the warmth of friendship, building a foundation for the challenges ahead."

label chapter_loss:
    $ enter_scene("loss")
    scene bg home_dusk
    with mood_transition()
    stop music fadeout 2.0
    stop ambience fadeout 2.0
    n "However, life has a way of introducing unforeseen tragedies."
    n "One fateful day, Joren and his family embarked on a routine research expedition to a nearby moon."
    n "An unexpected malfunction caused a catastrophic accident, and despite the rescue teams' best efforts, Joren did not survive."
    $ joren_lost = True
    pause 1.0
    n "In our world, where transcendence and joining with one's Astravus was the norm, and death among the Astraviin was nearly unheard of, Joren's loss was profoundly shocking and unbearably painful."
    n "It was as if a piece of Lumen itself had been torn away. The vibrant energy that once filled our days was replaced by a hollow emptiness."
    n "I remember the moment I found out, the words not fully registering at first. My mind refused to accept the possibility."
    r "Before the Astraviin, how did people cope when they lived for barely a century?"
    r "The thought of losing loved ones so frequently, living with the constant presence of death, seemed unbearable. Were people just numb to the loss?"
    n "Cassia and I clung to each other, our shared grief a heavy, suffocating presence."
    n "Lyra, too young to fully comprehend the permanence of death, was confused and frightened by the sorrow that enveloped our home."
    n "The places we had explored together now felt different, empty. The treehouse, once a place of joy and adventure, stood as a silent reminder of what we had lost."

label chapter_family_grief:
    $ enter_scene("family_grief")
    scene bg home_dusk
    play music "audio/grief_theme.ogg" fadein 4.0
    play ambience "audio/room_air.ogg" fadein 3.0
    show calista mourning at at_left
    show maia home at at_right
    with mood_transition()
    n "My parents tried to comfort me. One evening, Maia stayed with me while the light faded from the room."
    m "Cali."
    m "Joren's spirit will always be with us. In the stories we tell, in the memories we cherish, he lives on."
    c "But it hurts so much, Maia."
    n "I tried to wipe my face. The tears had started again."
    c "Why did this have to happen?"
    hide maia
    hide calista
    with mood_transition()
    n "She pulled me into her arms. I held on to her."
    m "I know, sweetheart. It's so hard to understand."
    m "We have each other to lean on. We'll get through this together."
    n "I stayed there for a long time. When I started crying again, she held me a little closer."
    n "That evening, I just wanted Maia to stay."

label chapter_painting_grief:
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

label chapter_cassia_grief:
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
    a "Do you think he knew how much he meant to us?"
    n "I looked at the drawings on the wall. At the corner of the map we'd held down together."
    c "I think he did, Cassia. He made every afternoon into an adventure. I loved being part of that."
    a "We promised we'd always meet here."
    n "I reached for her hand."
    c "I remember."
    n "We sat quietly, still holding hands. Then Cassia looked toward the window."
    a "Do you remember the dome? When he said we were on top of the world?"
    c "He looked so pleased with himself. I was still trying to catch my breath."
    a "We stayed up there all afternoon."
    c "I didn't want to come down."
    n "We talked about the view, and the journeys we'd imagined while we sat above Lumen. Remembering still hurt, but I was glad she remembered it with me."
    hide calista
    hide cassia
    with mood_transition()

label chapter_community_memorial:
    $ enter_scene("community_memorial")
    scene bg memorial_plaza
    with mood_transition()
    stop music fadeout 3.0
    play ambience "audio/plaza_air.ogg" fadeout 2.0 fadein 2.0
    n "The central plaza filled with flowers and messages. I knew it as a place of lanterns and music. Now people stood together and spoke quietly."
    n "Soren's inventions were still around us, part of the workings of Lumen. I couldn't see them without thinking of the workshop, and Joren showing me what each thing was for."
    n "Kaleb spoke at one of the gatherings. I had heard him tell so many stories about going away and coming home."
    show calista mourning at at_left
    show kaleb everyday at at_right
    with mood_transition()
    kaleb "Joren was a light in our lives. He had a boundless spirit and an insatiable curiosity."
    n "His voice was steady, but I could hear the effort it took. Around us, people listened with tears on their faces."
    kaleb "He taught us all the value of adventure and the importance of living each day to the fullest."
    kaleb "Let us honor his memory by continuing to explore, to learn, and to cherish the time we have together."
    n "He looked out across the people gathered there. No one hurried him away."
    play music "audio/remembrance_theme.ogg" fadein 4.0
    r "Lumen grieved with us. That didn't divide the hurt into smaller pieces, but it meant we didn't have to explain why it mattered."

label chapter_mural_remembrance:
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

label chapter_treehouse_remembrance:
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

label chapter_annual_remembrance:
    $ enter_scene("annual_remembrance")
    scene bg remembrance_plaza
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
