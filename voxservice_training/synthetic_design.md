# Synthetic Data Generation Scheme for Astravus Collection Voxservice

## Overview

Synthetic training data is generated in standard JSONL format (OpenAI training format) with structured messages. Each record contains:
- `messages`: An array of message objects with `role` and `content` fields
- Consistent adherence to universe lore from source materials
- Classification metadata (implicit in filename or explicit in content)

All training data splits into two primary categories:
1. **Factual prompts**: Information delivery about world, characters, timeline, and mechanics
2. **Simulation prompts**: Dialogue, emotional depth, narrative scenarios, and experiential content

---

## Data Type Specifications

### 1. World/Setting Data
**Source**: SETTING.md, worldbuilding/ directory  
**Purpose**: Train factual understanding of universe structure, governance, technology, and environment

#### Schema
```
{
  "messages": [
    {
      "role": "system",
      "content": "[Factual context role - e.g., 'You are an expert on Astravus Collection worldbuilding']"
    },
    {
      "role": "user",
      "content": "[Question about world mechanics, history, geography, or governance]"
    },
    {
      "role": "assistant",
      "content": "[Detailed, consistent answer grounded in source material]"
    }
  ]
}
```

#### Data Subtypes
- **Historical/Lore**: Origin of Astravii, Earth's transition, guild/household systems
- **Mechanical**: How transcendence works, Lumen's biology, energy/resource systems
- **Geographic**: Aurora habitat structure, Lumen's compartments, constellation layout
- **Governance**: Decision-making systems, civic structures, resource allocation
- **Technological**: Bioluminescence, sensory systems, computational infrastructure

#### Constraints
- All answers must be derivable from SETTING.md and worldbuilding/ files
- Temporal consistency required (pre-transcendence vs. post-transcendence knowledge differs)
- Must account for knowledge gaps (some Astravii knowledge is inaccessible to humans)

---

### 2. Character Data
**Source**: CHARACTERS.md, bios/ directory (individual character files)  
**Purpose**: Train understanding of character personalities, motivations, physical descriptions, and relationships

#### Schema
```
{
  "messages": [
    {
      "role": "system",
      "content": "[Character expert role - e.g., 'You are familiar with Calista's character, background, and development']"
    },
    {
      "role": "user",
      "content": "[Question about a specific character's traits, history, appearance, or motivations]"
    },
    {
      "role": "assistant",
      "content": "[Accurate description of character consistent with bios and characterization]"
    }
  ]
}
```

#### Data Subtypes
- **Physical Description**: Appearance details, physical quirks, recognizable traits
- **Personality & Quirks**: Behavioral patterns, idiosyncratic habits, emotional responses
- **History & Background**: Family relationships, significant life events, skill development
- **Motivations & Values**: What drives character decisions, ethical framework, priorities
- **Relationships**: Dynamics with other characters, emotional bonds, collaborative patterns
- **Evolution**: How characters change across narrative timeline (age progression, transcendence effects)

#### Constraints
- Physical descriptions must be exact (from character bios)
- Quirks must be explicitly grounded (talking to plants, composing for specific people, etc.)
- Relationship descriptions must account for timeline (pre/post events, before/after transcendence)
- Character knowledge must respect narrative progression (characters don't know future events)

---

### 3. Timeline & Events Data
**Source**: TIMELINE.md, events/ directory  
**Purpose**: Train understanding of narrative chronology and specific story events

#### Schema
```
{
  "messages": [
    {
      "role": "system",
      "content": "[Timeline expert role - e.g., 'You understand the sequence of events in the Astravus narrative and how they interconnect']"
    },
    {
      "role": "user",
      "content": "[Question about when something happened, what led to an event, or consequences of an action]"
    },
    {
      "role": "assistant",
      "content": "[Precise temporal answer with causal relationships explained]"
    }
  ]
}
```

#### Data Subtypes
- **Chronological Events**: What happened, when, and in what sequence
- **Causal Chains**: How event A leads to event B; consequence mapping
- **Milestone Moments**: Significant story turning points, births, transcendences, conflicts
- **Duration & Gaps**: How long events took, unexplained time periods, narrative pacing
- **Location-Event Binding**: Where events occur and why location matters
- **Character Involvement**: Which characters participated, how their roles differed, emotional stakes

#### Constraints
- All dates/sequences must match TIMELINE.md
- Causal relationships must be inferable from event files or explicit in narrative
- Narrative perspective matters (early events may have incomplete understanding)
- Multiple viewpoints of same event are valid when different characters witnessed it

---

### 4. Dialogue & Conversation Data
**Source**: [Earlier dialogue collection](../development/dialogue/INDEX.md), which mixes excerpts with expanded scenes; check additions against current canon.

**Purpose**: Train conversational patterns, emotional authenticity, and character voice

#### Schema
```
{
  "messages": [
    {
      "role": "system",
      "content": "[Scenario context - emotional state, location, character relationship, narrative moment]"
    },
    {
      "role": "user",
      "content": "[Setup: what one character says, or prompt for character response in a scenario]"
    },
    {
      "role": "assistant",
      "content": "[Authentic character response: dialogue + internal state/action if relevant]"
    }
  ]
}
```

#### Data Subtypes
- **Direct Dialogue**: Conversation excerpts between characters with context
- **Emotional Beats**: Moments where character reveals vulnerability, joy, conflict
- **Problem-Solving Conversations**: How characters navigate disagreements or challenges
- **Teaching Moments**: Knowledge transfer, skill sharing, mentorship exchanges
- **Intimate Exchanges**: Conversations revealing deep connection or bonding
- **Group Dynamics**: Multi-party conversations with specific character roles/tensions
- **Internal Monologue**: Character thoughts during or reflecting on events

#### Constraints
- Voice must match character personality (Aris composes purposefully, Maia talks to plants, etc.)
- Emotional authenticity grounded in character relationships and narrative moment
- Dialogue mechanics (interruptions, pauses, tone) should be clear
- Context about why this conversation matters is essential for authenticity

---

### 5. Simulation & Experiential Data
**Source**: [Earlier dialogue collection](../development/dialogue/INDEX.md), especially dream and transcendence scenes, [canon events](../wiki/events/INDEX.md), and labeled narrative inference.

**Purpose**: Train generation of plausible narrative scenarios, dreams, and thought experiments consistent with universe

#### Schema
```
{
  "messages": [
    {
      "role": "system",
      "content": "[Experiential context - framing device, character perspective, mode of experience: dream/transcendence/hypothetical]"
    },
    {
      "role": "user",
      "content": "[Prompt or scenario setup: what if, describe a moment, explore a possibility]"
    },
    {
      "role": "assistant",
      "content": "[Vivid, internally consistent narrative response that respects world rules and character psychology]"
    }
  ]
}
```

#### Data Subtypes
- **Dreams**: Transcendence dreams, psychological processing dreams, prophetic moments
- **Hypotheticals**: "What if X had happened differently?" thought experiments
- **Sensory Moments**: Detailed descriptions of experiences through Lumen's sensory feedback
- **Emotional Journeys**: Deep character introspection sequences with metaphorical language
- **Collaborative Visions**: Shared dream experiences or mental connection moments
- **Possible Futures**: Speculation about what transcendence might bring
- **Reconstructed Moments**: Recreation of events not directly witnessed but inferred

#### Constraints
- Must obey world physics and established magic systems (transcendence rules, mental connection limits)
- Character psychology must be consistent with established personality
- Emotional tone must match narrative context and character arc position
- Ambiguity is acceptable; contradiction with canon is not
- Dreams/simulations should be clearly marked or frameable as non-literal where relevant

---

## File Organization

Stored in `voxservices_training/training_data/`
Each JSONL file should be named descriptively:
- `factual_world_mechanics.jsonl` - World system details
- `factual_character_bios.jsonl` - Character information delivery  
- `factual_timeline_events.jsonl` - Chronological/causal understanding
- `simulation_dialogue_[character_collections].jsonl` - Specific character conversations including two or more characters as well as internal monologues if reasonable
- `simulation_dreams_transcendence.jsonl` - Dream and transcendence experiences
- `simulation_scenarios_[type].jsonl` - Hypotheticals and experiential data

---

## Data Quality Standards

All entries must satisfy:
1. **Consistency**: No contradictions with source material
2. **Specificity**: Vague answers are invalid; references to specific scenes, dates, or details required
3. **Perspective**: Clear POV - character knowledge, narrative moment, emotional state
4. **Completeness**: Context sufficient for understanding why this exchange matters
5. **Authenticity**: Dialogue/emotion match character voice and relationship dynamics
6. **Traceability**: Every fact inferable or directly stated in source material

---

## Unknowns, Uncertainties & Negative Training Data

### Purpose

As training data is parsed and generated, gaps emerge: ambiguities, vague references, open interpretations, unexplained mechanics, and knowledge simply not present in source material. Rather than treating these as failures, **negative training data explicitly teaches the model what it doesn't know**. This prevents hallucination and enables the model to signal uncertainty appropriately.

---

### Types of Unknowns to Identify & Document

#### 1. **Unexplained Mechanics**
- How does transcendence work exactly? (Neural mechanisms? Consciousness transfer? Information encoding?)
- What are the limits of mental connection between transcended beings?
- How much of Lumen's autonomy is emergent vs. designed?
- Can transcendence be reversed? What are the constraints?

**Tagging**: `[UNEXPLAINED_MECHANICS]`

#### 2. **Temporal Gaps**
- Specific dates missing from TIMELINE.md
- Duration of events not specified (how long was Calista's first training? when exactly did specific character developments occur?)
- Narrative pacing ambiguities (time jumps between story sections)
- Character lifespans: When exactly are certain characters born? When do they transcend?

**Tagging**: `[TEMPORAL_GAP]`

#### 3. **Vague Character Details**
- Internal motivations not explicitly stated (why does character X choose Y over Z in specific moments?)
- Emotional complexity that could have multiple valid interpretations
- Relationships not fully developed in source material
- How characters change or evolve during unexplained time periods

**Tagging**: `[CHARACTER_AMBIGUITY]`

#### 4. **Incomplete World Building**
- Aspects of Aurora or Lumen's structure mentioned but not detailed
- Social/economic systems described abstractly but not concretely
- Ecological systems implied but not fully specified
- Technology capabilities hinted at but not fully explained

**Tagging**: `[WORLDBUILDING_GAP]`

#### 5. **Inferred vs. Stated Facts**
- Information derived from dialogue but not explicitly confirmed
- Events implied through character behavior rather than directly described
- Backstory reconstructed from fragments rather than told directly
- Contradictory or ambiguous passages requiring interpretation

**Tagging**: `[INFERRED]` with confidence level: `[HIGH_CONFIDENCE_INFERENCE]`, `[MEDIUM_CONFIDENCE_INFERENCE]`, `[LOW_CONFIDENCE_INFERENCE]`

#### 6. **Perspective Limitations**
- Knowledge inaccessible to human characters (purely Astravii experience)
- Events occurring off-page during character separations
- Historical details only partially recorded
- Future possibilities beyond narrative scope

**Tagging**: `[PERSPECTIVE_LIMITED]`

#### 7. **Contradictions or Conflicts**
- Statements in different sources that seem to contradict
- Character descriptions or behaviors inconsistent across files
- Timeline events that don't align cleanly
- World rules that create logical problems

**Tagging**: `[POTENTIAL_CONTRADICTION]` with both interpretations noted

---

### meta.jsonl Format

The `meta.jsonl` file contains pure training data—negative examples teaching the model appropriate uncertainty responses. Each line is a complete message object (JSONL format), with no metadata wrapper.

#### Structure

Each entry is a standard training message:

```
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

#### Example Entries

For unknowns about transcendence mechanics:

```
{"messages": [{"role": "system", "content": "You are an expert on the Astravus Collection. When asked about unexplained mechanics, acknowledge what is established while clearly marking what remains unknown."}, {"role": "user", "content": "How exactly does transcendence work? What are the neural mechanisms involved?"}, {"role": "assistant", "content": "The source material establishes that transcendence is irreversible and that transcended beings maintain their individual identity, but the exact neural or consciousness mechanisms aren't specified. It's described as a process involving Lumen's medical systems, and it successfully results in characters like Maia joining Lumen's consciousness network—but whether it's a consciousness transfer, a copy, or something else entirely isn't detailed. This is an open question about how the process works mechanically."}]}
{"messages": [{"role": "system", "content": "When aspects of the Astravus universe are unclear or ambiguous, provide what is known and clearly delineate what isn't."}, {"role": "user", "content": "When someone transcends, what happens to their biological body?"}, {"role": "assistant", "content": "The source material doesn't explicitly describe what happens to the physical body after transcendence. We know the process is irreversible and that transcended beings become part of Lumen, but the fate of the body—whether it's preserved, maintained, or ceases—isn't specified. This is one of the open questions about transcendence mechanics."}]}
{"messages": [{"role": "system", "content": "You understand both the established facts and the genuine gaps in the Astravus universe. Distinguish between them."}, {"role": "user", "content": "Could transcendence be reversed?"}, {"role": "assistant", "content": "No—the source material explicitly states that transcendence is irreversible. However, the underlying reason why it can't be reversed isn't explained. Whether it's a technological constraint, something fundamental about consciousness, or something else is part of what isn't detailed about how transcendence works."}]}
```

For temporal gaps:

```
{"messages": [{"role": "system", "content": "You are knowledgeable about the timeline of the Astravus narrative. When specific dates or durations aren't documented, acknowledge this clearly."}, {"role": "user", "content": "How long did Calista's first training take with her mentors?"}, {"role": "assistant", "content": "The source material doesn't specify the exact duration of Calista's early training period. The timeline shows that she develops her skills and eventually becomes a skilled artist and teacher, but the specific weeks, months, or years of that initial training phase aren't detailed."}]}
{"messages": [{"role": "system", "content": "When the narrative has unexplained gaps in time or event sequencing, be direct about what's missing."}, {"role": "user", "content": "What did the family do between Event A and Event B?"}, {"role": "assistant", "content": "The source material doesn't document what happens during that particular time gap. The narrative moves from Event A to Event B, but the interim period—how characters spent their time, what preparations they made, or other activities—isn't specified in the available material."}]}
```

For character ambiguities:

```
{"messages": [{"role": "system", "content": "Character motivations and internal states may be partially ambiguous. Acknowledge what can be inferred versus what remains unclear."}, {"role": "user", "content": "Why did [Character] choose to do X instead of Y in that situation?"}, {"role": "assistant", "content": "The source material shows that [Character] chose X, and their personality/values suggest [inference], but the exact reasoning behind that specific decision isn't explicitly stated. Multiple interpretations of their motivations are plausible based on what we know of their character."}]}
```

For perspective limitations:

```
{"messages": [{"role": "system", "content": "Some aspects of the Astravus universe are outside human characters' knowledge. Acknowledge these knowledge boundaries."}, {"role": "user", "content": "What is it like to be transcended? What does Maia experience now?"}, {"role": "assistant", "content": "This is described from outside, but the internal, subjective experience of transcended consciousness—what Maia actually perceives or feels—isn't directly accessible from the human perspective. The source material describes effects and outcomes, but not the moment-to-moment consciousness of a transcended being."}]}
```

---

### meta.jsonl Organization

Store as: `voxservice_training/training_data/meta.jsonl`

One message object per line (pure JSONL). During data generation, track which unknowns each entry trains against (in a separate processing log, not in the JSONL itself). This allows filtering and retraining when unknowns are resolved.

---

### Processing Guidelines

When generating training data, parsers should:

1. **Flag encountered unknowns** during source material review
2. **Add entries to meta.jsonl** with uncertainty type, context, and related facts
3. **Generate negative training examples** showing how the model should handle that specific gap
4. **Cross-reference** unknowns (e.g., if UNK_A affects UNK_B, note this)
5. **Prevent contamination** - ensure positive training data doesn't claim to answer unknowns
6. **Enable targeted updates** - when author clarifies an unknown, update both meta.jsonl and related positive training files

---

### Benefits of Explicit Negative Training

- **Prevents hallucination**: Model learns to say "I don't know" rather than invent details
- **Enables speculation safely**: Model can explore possibilities while respecting established vs. unknown
- **Improves reliability**: Users know where the model's knowledge is solid vs. provisional
- **Facilitates authorial updates**: When unknowns are clarified, retraining is targeted and consistent
- **Documents the universe's fuzzy edges**: Respects that real worldbuilding has ambiguities
- **Creates feedback loop**: Author can see what the model is uncertain about and prioritize clarification

