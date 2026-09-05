# Earliest Memories: the relationships behind Cali's childhood.
# The prose draft remains authoritative. See docs/BOOK_ONE_COVERAGE.md.
define arin = Character("Arin", who_color="#bdcbd8")
define selene = Character("Selene", who_color="#d0bfdf")
define dorian = Character("Dorian", who_color="#ddbf94")
define sage = Character("Sage", who_color="#c4d4be")
define kael = Character("Kael", who_color="#d8c69c")
define lyra = Character("Lyra", who_color="#c7d6a3")

label family_book_one:
    call family_plant_disagreement
    call family_workshop_first
    call family_music_first
    call family_dorian_stories
    call family_sage_story
    call family_daily_rhythm
    call family_tree_echoes
    call family_pond_scare
    call family_soup_experiment
    call family_festival_lights
    return

label family_plant_disagreement:
    $ enter_scene("plant_disagreement")
    scene bg garden_close
    with mood_transition()
    play music "audio/home_theme.ogg" fadeout 2.0 fadein 2.0
    play ambience "audio/garden_air.ogg" fadeout 1.0 fadein 1.0
    n "Maia let us help arrange the new plants. Kael carried the pots; I stood back on the path to decide where they should go."
    show calista home at at_left
    show kael young at at_right
    with mood_transition()
    kael "Here. There's loads of light."
    c "Put them by the pond. You'll see them from the other side."
    n "He lowered the first pot into the bright patch. I picked it up again."
    kael "Cali, I just put that there."
    c "I know. Look from over here."
    kael "They're plants. They need light."
    c "There's light by the pond."
    n "There was some. Not as much as where he stood. I didn't want that to settle it."
    kael "Then you carry them."
    c "Fine."
    hide kael
    show maia home at at_right
    with mood_transition()
    n "Maia came over before I'd managed to lift the next pot. She rested a hand on each of our shoulders."
    m "Show me. One at a time."
    c "If they're by the water, you can see the flowers twice."
    n "I pointed to the reflection of a low branch. Maia crouched beside me to follow its shape on the water."
    m "And your place, Kael?"
    kael "It stays bright longer."
    m "It does. These ones would like that."
    c "So he gets to choose."
    m "For all of them? There are quite a few pots."
    n "I looked along the edge of the pond. The bright patch reached farther toward it than I'd noticed."
    c "What if we start there? And bring them round?"
    kael "Not right under that branch."
    c "No. Round this way."
    n "I traced a curve in the soil with my shoe. Kael moved one pot onto it, then looked back at me."
    hide maia
    show kael young at at_right
    with mood_transition()
    kael "There?"
    c "A bit closer. Yes."
    m "Let's try it before we dig."
    n "We moved the pots until the curve held together. From across the pond, little pieces of color trembled in the water."
    c "You can still see them."
    kael "And they've got light."
    n "This time, when he set a pot down, I left it there."
    r "I remember wanting Maia to say I'd been right. What she gave us took a little longer to enjoy."
    return

label family_workshop_first:
    $ enter_scene("workshop_first")
    scene bg workshop
    with mood_transition()
    play music "audio/discovery_theme.ogg" fadeout 2.0 fadein 2.0
    play ambience "audio/workshop_air.ogg" fadeout 1.0 fadein 1.0
    n "In Arin's workshop, every surface seemed to be waiting for something to be finished. I liked standing close enough to watch their hands."
    n "They hummed as they worked. The tune stopped when my elbow caught the jar."
    c "Oh—"
    n "Screws scattered over the bench and dropped to the floor. One kept rolling long after the others had stopped."
    c "I'm sorry. I didn't see it."
    arin "Stay there a moment. Let me find that last one."
    n "They caught it against the leg of the bench. I pressed both hands against my stomach."
    c "Have I broken anything?"
    arin "The jar's all right. So are you?"
    c "Yes."
    arin "Good."
    n "Arin set the jar farther back and knelt down. I stayed where I was."
    c "You were working."
    arin "I was. Now we have another job first."
    c "I can pick them up."
    arin "I'll take this side. You start by your feet."
    n "I gathered the screws into my palm. There were more than I'd expected, some so small they hid between the boards."
    c "Do they all go back together?"
    arin "They did. It wasn't a very good system."
    n "They put three shallow trays on the bench. I tipped my handful into the nearest one."
    show arin everyday at at_right
    show calista home at at_left
    with mood_transition()
    arin "How would you sort them?"
    c "Big ones here. Little ones there."
    arin "Try it."
    n "I made two piles, then stopped with a screw balanced between my fingers."
    c "This one's in between."
    arin "That's what the third tray is for."
    n "By the time we finished, I could find the smallest screws without emptying the jar. Arin checked the floor once more."
    c "I won't knock it over again."
    arin "You don't have to promise never to make a mistake, Cali. Just tell me when something happens."
    c "Even if you're busy?"
    arin "Especially then."
    hide arin
    hide calista
    with mood_transition()
    n "They drew my stool closer and went back to the device. After a while, the humming began again."
    r "I had expected the sound of their disappointment. I remember the relief of hearing that little tune instead."
    return

label family_music_first:
    $ enter_scene("music_first")
    scene bg music_room
    with mood_transition()
    stop music fadeout 2.0
    play ambience "audio/room_air.ogg" fadeout 1.0 fadein 1.0
    n "Selene's music reached the hall before I reached her door. She looked up when I came in."
    show selene everyday at at_right
    show calista home at at_left
    with mood_transition()
    selene "Come and sit with me."
    c "Am I going to play with you?"
    selene "If you'd like. Let's hear one note first."
    hide selene
    hide calista
    with mood_transition()
    n "She made room beside her at the piano and laid a small flute across my hands. Its surface caught the light when I turned it."
    n "She showed me where to put my fingers. I took a breath large enough for a whole song."
    play sound "audio/flute_attempt.wav"
    n "The first sound trembled, thinned, and broke. I lowered the flute."
    stop sound fadeout 0.08
    c "That wasn't it."
    selene "There was a note in there. I heard it."
    c "Only at the start."
    selene "Then we'll start there again. You can take a smaller breath."
    n "I tried. This time I listened for the moment the air became something I could hold."
    c "Like that?"
    selene "Yes. Don't chase it."
    n "Her hand moved gently with the rhythm of my breathing. When I stopped, she waited for me to be ready."
    c "How do I know which one comes next?"
    selene "I'll sing it first. Then you can answer."
    play sound "audio/flute_first.wav"
    n "We went a few notes at a time. Sometimes I lost one and had to begin again; sometimes her voice met mine in the middle."
    selene "Do you hear that color?"
    c "A color?"
    selene "Pale blue. Something quiet, just waking up."
    n "I looked down at the flute. I had been thinking about holes and fingers, and whether I would get it wrong."
    c "Can a song be green?"
    selene "What would your green sound like?"
    c "I don't know yet."
    selene "Neither do I. You'll have to play it for me when you find it."
    n "I raised the flute again. This time I wanted to hear what it would do."
    stop sound fadeout 1.0
    play music "audio/home_theme.ogg" fadein 2.0
    r "Selene never asked me to stop seeing pictures. She gave me another way to make them."
    return

label family_dorian_stories:
    $ enter_scene("dorian_stories")
    scene bg library
    with mood_transition()
    play music "audio/wonder_theme.ogg" fadeout 2.0 fadein 2.0
    play ambience "audio/room_air.ogg" fadeout 1.0 fadein 1.0
    n "Dorian had a way of arranging an evening before he said a word. A lamp moved closer. A map unrolled. His glasses settled on his nose."
    show dorian everyday at at_right
    with mood_transition()
    dorian "And so the historian gathered his listeners."
    kael "We're here."
    dorian "His remarkably patient listeners."
    n "Kael drew his knees up on the seat. Lyra leaned against me, watching Dorian's hands on the edges of the map."
    dorian "Tonight, the explorers."
    kael "Can we follow their routes one day?"
    dorian "Perhaps. Which route were you thinking of?"
    n "Kael pointed to a line that crossed nearly the whole map. Dorian let him follow it to the far edge."
    kael "That one."
    dorian "All the way?"
    kael "Why not?"
    dorian "Then we had better find out what happened along it."
    c "Is it a long story?"
    dorian "Do you need to be somewhere?"
    c "No."
    n "I tucked my feet beneath me. He lowered his voice, and the little reading area seemed to grow around it."
    n "The names were unfamiliar at first. By the time he returned to them, I could remember who had gone ahead and who was still waiting."
    lyra "Did they get home?"
    dorian "Stay with them a little longer."
    n "He gave us the pauses as carefully as the words. Even Kael stopped trying to turn the page ahead of him."
    r "I remember the lamp on the paper better than every place he described. But I remember wanting those strangers to find their way."
    n "When the story ended, Kael leaned over the map again."
    kael "I'd still go."
    dorian "Good. Now you know a little more about where you'd be going."
    c "Will you tell the next one tomorrow?"
    dorian "Keep my place for me."
    n "I slid a scrap of paper between the pages. For once, Kael didn't argue about who got to choose."
    return

label family_sage_story:
    $ enter_scene("sage_story")
    scene bg sage_room
    with mood_transition()
    play music "audio/home_theme.ogg" fadeout 2.0 fadein 2.0
    play ambience "audio/room_air.ogg" fadeout 1.0 fadein 1.0
    n "That evening, Lyra was still upset about the last piece of dessert. Kael had eaten it. Telling her that it was gone hadn't helped."
    show sage everyday at at_right
    with mood_transition()
    sage "Would you like a story?"
    hide sage
    with mood_transition()
    n "Sage drew her onto their lap. I pulled a blanket over my knees; Kael sat at the other end of it."
    lyra "Not one he chooses."
    sage "I'll choose this time. There are three siblings in it."
    kael "Are they us?"
    sage "Their names are Aria, Bram, and Cora. You can decide who they remind you of."
    n "Lyra leaned against Sage. The candlelight moved over the folds of the blanket."
    play music "audio/wonder_theme.ogg" fadeout 2.0 fadein 2.0
    # This is the draft's first explicit living, traveling Astravus: a story
    # within the story. Direct identification of Lumen waits for Tree of Echoes.
    sage "They lived aboard an Astravus, a great living ship traveling through the cosmos. Its passages were as familiar to them as these halls are to you."
    sage "Aria wanted to explore every one. Bram wanted to know how everything worked. Cora kept bringing things home to make into art."
    lyra "Like Cali."
    c "You bring things home too."
    sage "One day, the water stopped running. Not just in their home. All through the living quarters."
    sage "People checked their taps and carried empty cups next door. But their neighbors had no water either."
    lyra "What happened to it?"
    sage "Bram asked that very question. Aria was already looking for her bag."
    sage "She wanted to search the far passages for another source. Bram wanted to examine the water system. Cora thought they ought to make something that could help."
    kael "They could look while he fixes it."
    sage "They might have. But first, each of them wanted the others to agree that their plan was best."
    n "Sage gave Aria a quick, impatient voice. Bram spoke more slowly, growing slower still whenever she interrupted."
    sage "Aria said the community couldn't wait. Bram said wandering off wouldn't tell them why the water had stopped. Cora couldn't get either of them to listen."
    c "What did they do?"
    sage "They tried Aria's plan first. They searched for hours, until their feet hurt, and came back with no more water than they'd taken."
    kael "So Bram was right."
    sage "Bram found something. The pipes were clogged with mineral deposits from the filtration system."
    sage "But finding the blockage wasn't the same as clearing it. The work was slow. The cups were still empty."
    lyra "What about Cora's thing?"
    sage "She'd been working on a small filter for her art. Watching them struggle, she thought it might help. This time, they listened."
    c "Did it fit?"
    sage "Not by itself. Bram knew the system, and Cora knew her device. They worked out how to use them together."
    sage "Aria helped too. They were all there when the water began to move again."
    n "Sage let the room fall quiet. Somewhere beyond their door, I could hear our little fountain."
    lyra "Did everyone get some?"
    sage "The water came back to the living quarters. There was a great deal of filling cups."
    kael "I'd have had two."
    n "Lyra looked at him. He glanced down at the blanket between us."
    kael "Not if there was only one left."
    n "She didn't answer immediately. Then she let him pull a little more of the blanket over his feet."
    sage "They still had different ideas afterward. They just got better at hearing the other two."
    lyra "You can tell another one."
    sage "A little one. It's getting late."
    n "By the end, Lyra's hand had gone slack in Sage's. Kael waited for me at the door instead of running ahead."
    r "I don't know how many stories Sage found for us, or how often we needed to hear the same one again. They never seemed impatient with the repetition."
    return

label family_daily_rhythm:
    $ enter_scene("family_rhythm")
    scene bg family_home
    with mood_transition()
    play music "audio/home_theme.ogg" fadeout 2.0 fadein 2.0
    play ambience "audio/room_air.ogg" fadeout 1.0 fadein 1.0
    n "There were mornings with nothing particular to remember. Bread cooling. Fruit from Maia's garden. Shadow stretching at the foot of my bed."
    n "Barkley waited outside my door. Nibble was already stirring in her cage. Before I reached the table, I could hear Kael explaining his dream."
    show shadow at shadow_home
    show barkley at barkley_home
    show nibble at nibble_home
    show kael young at at_left
    show lyra young at at_right
    with mood_transition()
    kael "The cave was full of crystals. They were glowing everywhere."
    lyra "Were there creatures? Did they see you? Were you scared?"
    kael "Little insects. They showed me where to go."
    c "Wait. What color were the crystals?"
    n "Arin passed the bread while Kael began again for me. Maia set down a bowl of fruit; Selene's unfinished tune followed her into the room."
    r "A day couldn't hold all the things I remember doing. They belong to many mornings, many evenings. In memory, I keep walking from one room to the next."
    scene bg garden_close
    with mood_transition()
    play ambience "audio/garden_air.ogg" fadeout 1.0 fadein 1.0
    n "In the garden, Maia showed me a seedling leaning toward the light. I crouched beside its pot to follow the bend of the stem."
    c "Why doesn't it grow straight?"
    m "It's reaching toward what it needs. See where the light falls?"
    c "Over there."
    m "That movement has a name: phototropism."
    c "It knows which way to go."
    m "It responds to the light. Slowly enough that we have to come back to see it happen."
    n "She smoothed the soil around it. We had learned to look for changes smaller than a flower opening."
    scene bg workshop
    with mood_transition()
    play ambience "audio/workshop_air.ogg" fadeout 1.0 fadein 1.0
    n "At Arin's bench, I was allowed to help with more than the sorting."
    show arin everyday at at_right
    show calista home at at_left
    with mood_transition()
    arin "The wrench, please, Cali."
    c "This one?"
    arin "That's it."
    c "What's it for? The machine, I mean."
    arin "An irrigation system for Maia. A prototype, so we'll be making some changes."
    c "Can I do this bolt?"
    arin "Hold it steady. I'll guide the wrench."
    n "I felt the resistance through the tool. Arin let me do the last turn."
    scene bg music_room
    with mood_transition()
    stop music fadeout 1.5
    play ambience "audio/room_air.ogg" fadeout 1.0 fadein 1.0
    n "There came an evening when I could play Selene's melody without stopping to find each note."
    play sound "audio/flute_practice.wav"
    n "Lyra clapped along. By the end she was racing ahead, and I had to stop because we were both laughing."
    c "You're too fast."
    lyra "You're too slow."
    selene "Together, this time. Listen for each other."
    show shadow at familiar_at(1260, 770, 220)
    show nibble at familiar_at(910, 735, 90)
    with mood_transition()
    n "Shadow's ears twitched from her place in the corner. Nibble scurried past, indifferent to our attempts to keep time."
    stop sound fadeout 1.0
    play music "audio/home_theme.ogg" fadein 2.0
    scene bg library
    with mood_transition()
    n "In the library, Kael began spreading out the maps himself. I searched for places whose names I remembered."
    c "Here. This was in the story."
    kael "And if you follow that line—"
    c "I know. I want to find it."
    n "He waited while I traced the route. Dorian sat nearby, answering when we asked."
    scene bg family_home
    with mood_transition()
    n "At dinner, there was always something to show. Lyra's latest stone. A sketch. A part that hadn't fitted until the third attempt."
    show lyra young at at_right
    with mood_transition()
    lyra "Pass the salad. Look what I found today."
    sage "Let me see. Where did you find this one?"
    n "She turned the stone so its shiny face caught the light. I held the salad while she explained."
    kael "Knowledge quests after dinner? I'm going to win this time."
    c "You said that last time."
    kael "This time, then."
    scene bg sage_room
    with mood_transition()
    n "By bedtime, the board was put away and the arguments had usually worn themselves out. Sage drew us close for a story."
    sage "Once there was a brave little mouse named Nibble."
    lyra "Nibble's a rat."
    sage "Our Nibble is. Shall we see what this one does?"
    n "Lyra nestled against them to listen. Later, Shadow found the foot of my bed, Barkley settled near Kael, and the rooms grew quiet."
    r "I wouldn't have called those days important. I expected to have them again."
    return

label family_tree_echoes:
    $ enter_scene("tree_echoes")
    scene bg echoes
    with mood_transition()
    play music "audio/wonder_theme.ogg" fadeout 2.0 fadein 2.0
    play ambience "audio/garden_air.ogg" fadeout 1.0 fadein 1.0
    n "One clear afternoon, we followed a path we hadn't taken before. Kael pushed ahead through the thicket; Lyra and I tried to keep sight of him."
    kael "Come on! There's something here."
    n "Barkley bounded into the clearing first. Shadow slipped between the roots behind us. At the center stood a tree much older than the paths around it."
    show shadow at shadow_path
    show barkley at barkley_path
    with mood_transition()
    lyra "Look at the trunk."
    n "It was hollow, the wood folded into deep ridges. I ran my fingers along one without going inside."
    show calista home at at_left
    show lyra young at at_right
    with mood_transition()
    c "The Tree of Echoes. Dorian told us about it."
    kael "This one?"
    c "I think so. It was already old when they brought it here."
    lyra "How do you bring a whole tree?"
    c "I don't know. Carefully."
    n "I tried to remember the story in the order Dorian had told it. There had been a gift, long before Lumen."
    c "It grew from a seed another Astravus gave. An ancient one. Then the tree came here when Lumen was founded."
    lyra "So it's older than home."
    n "I hadn't thought of it that way. I looked up into the branches, trying to imagine them somewhere else."
    kael "Let's listen."
    hide calista
    hide lyra
    with mood_transition()
    n "He leaned against the trunk and pressed his ear to the wood. Lyra held her breath."
    stop music fadeout 2.0
    play sound "audio/tree_creak.wav"
    n "At first, I heard leaves and Barkley shifting on the path. Then a low creak moved through the tree."
    lyra "Did you hear it?"
    c "Yes."
    lyra "It sounds like someone."
    n "We waited. The branches moved, and another faint sound passed through the hollow. Almost a voice, until I tried to make out a word."
    c "It's the wood. Listen when the branches move."
    kael "It still sounds like talking."
    n "He made room for me. I put my ear where his had been and felt the rough bark against my cheek."
    play music "audio/wonder_theme.ogg" fadein 3.0
    n "Lumen was a living ship. I had grown up inside that life without needing to picture its whole shape."
    $ lumen_known = True
    n "Here was something older: a tree grown from another Astravus's gift, carried into our young home. The stories had left something we could touch."
    c "Can we come back?"
    kael "We know the way now."
    lyra "I want to hear it again."
    n "None of us moved for a while. We stood together, listening for the next almost-word."
    r "The tree wasn't speaking. What I felt beside it was real enough without that."
    return

label family_pond_scare:
    $ enter_scene("pond_scare")
    scene bg garden_close
    with mood_transition()
    stop music fadeout 2.0
    play ambience "audio/garden_air.ogg" fadeout 1.0 fadein 1.0
    n "Another day, we were playing beside a small pond. Lyra stepped too close to the edge."
    play sound "audio/water_splash.wav"
    n "Her foot slipped. Water broke around her, and for a moment I couldn't understand why she wasn't beside me anymore."
    c "Lyra!"
    lyra "I can't swim!"
    n "The pond was shallow. She was frightened enough that she couldn't find the bottom with her feet."
    kael "Here. Take my hand."
    n "I knelt beside him and reached for her. Barkley barked behind us; Shadow paced along the bank."
    c "I've got you. This way."
    n "Between us, we helped her to the edge. She held on hard, still trying to climb after her knees were on the ground."
    kael "You're out. You're out now."
    n "I put my arms around her. Her clothes soaked through mine, and I could feel her shaking."
    lyra "I slipped."
    c "I know."
    lyra "I didn't mean to go in."
    c "I know. You're here."
    n "Kael crouched on her other side. For once, he wasn't looking toward the next place to go."
    kael "Shall we go home?"
    n "Lyra nodded without letting go of me. I waited until she was ready to stand."
    lyra "Will you hold my hand?"
    c "Yes."
    n "We took the wider part of the path. Barkley stayed close, and Lyra kept her wet fingers locked around mine."
    play music "audio/home_theme.ogg" fadein 3.0
    r "Afterward, it was a story with a safe ending. In the moment, all I wanted was to get her back beside me."
    return

label family_soup_experiment:
    $ enter_scene("soup_experiment")
    scene bg family_home
    with mood_transition()
    play music "audio/home_theme.ogg" fadeout 2.0 fadein 2.0
    play ambience "audio/room_air.ogg" fadeout 1.0 fadein 1.0
    n "Lyra liked having a job when we made dinner. One afternoon, she gave herself an extra one."
    n "We discovered it when everyone took the first spoonful of soup. Arin put their spoon down and coughed."
    arin "Did someone add something?"
    n "Lyra looked from one face to the next. The smile she'd been waiting with had disappeared."
    lyra "A spice. From Maia's garden."
    m "Which one, love? Show me."
    n "Lyra brought it to the table. Maia recognized it immediately."
    m "Ah. This one's very strong."
    lyra "I only put a little in."
    arin "A little of that goes a long way."
    lyra "I thought it would be better."
    n "Her eyes filled. I set my spoon down quietly."
    lyra "I'm sorry. I wanted to help."
    n "Maia drew her close. For a moment, nobody asked her to explain again."
    m "You can help me make another batch. We'll try the spice together."
    lyra "You're still going to use it?"
    m "A much smaller amount. Then we'll taste before we add any more."
    n "Lyra stayed beside her while the rest of us cleared the bowls. The new pot took time; we passed the bread around again."
    c "Can I taste it too?"
    lyra "Not yet."
    n "She was concentrating on Maia's hand, watching how little spice went in."
    m "Now. What do you think?"
    lyra "It's different."
    m "Would you like any more?"
    lyra "No. I think that's enough."
    n "At the table, she watched my first spoonful. I took another before I answered."
    c "This one's good."
    n "She began to eat. The conversation found its way back to the things we'd done that day."
    r "I remember the terrible soup. I remember the second pot more kindly, and the way Maia kept a place for Lyra beside it."
    return

label family_festival_lights:
    $ enter_scene("festival_lights")
    scene bg festival
    with mood_transition()
    play music "audio/festival_theme.ogg" fadeout 2.0 fadein 3.0
    play ambience "audio/plaza_air.ogg" fadeout 1.0 fadein 2.0
    n "Every year, the Festival of Lights drew our home into the wider community. The central plaza filled with lanterns and living displays."
    n "We celebrated what nature and technology could make together. I wanted to look at everything before any of it changed."
    show lyra young at at_right
    show calista festival at at_left
    with mood_transition()
    lyra "Look up there. And there!"
    kael "It's like the stars came down."
    n "Light moved across their faces as we walked. Beyond us, a familiar melody rose from the small stage."
    c "That's Selene."
    n "We stopped to listen to her harp. I knew some of the phrases from home; here they traveled out among people I didn't know."
    lyra "Can she see us?"
    c "Maybe when she looks up."
    n "Lyra lifted a hand and kept it there. We waited through the end of the tune."
    hide lyra
    show kael young at at_right
    with mood_transition()
    n "Maia's flowers glowed in the display. I moved closer to find the places where one color changed into another."
    kael "You're going to draw all this, aren't you?"
    c "I'm trying to remember it."
    kael "There's more over here."
    n "There was always more. Another lantern, another pattern in the leaves, another bit of music reaching us through the crowd."
    hide calista
    hide kael
    with mood_transition()
    n "Later, we stood together to release our lanterns. Each carried a wish. Lyra watched hers as though looking away might make her lose it."
    lyra "Which one's mine now?"
    c "That one. Just above the others."
    n "I followed it until I wasn't certain anymore. The separate lights were becoming a whole sky."
    c "What did you wish for, Kael?"
    kael "To explore new worlds."
    c "Of course you did."
    kael "What was yours?"
    c "To capture all this. All the beautiful things we get to see."
    kael "You'll need a bigger book."
    n "I smiled without taking my eyes off the lanterns. For once, a bigger book seemed like the only difficulty."
    r "There was so much I expected the world to give us. I hadn't begun to count any of it."
    n "Around us, other families watched their wishes rise. Soon, some of those faces would become as familiar as my own."
    return
