---
name: grammar-insert
description: Files a new Spanish sentence, example, rule, or note into the user's Spanish grammar notes (Grammar.md) under the existing section and list that fits it best. Use this whenever the user wants to add, file, save, put, or "insert" something into their Grammar notes or Grammar.md. It also applies when they paste a Spanish sentence or phrase and say "add this", "where does this go", "put this in my notes", or "save this example", even if they never name the file. Never creates new headings.
---

# Grammar Insert

The user keeps a large personal Spanish grammar notebook at `/Volumes/NO_NAME/knowledge_base/Spanish/Guide/Grammar.md`. It is about 28k lines and 1.7 MB, so never read it whole. Your job is to find where a new piece of content belongs, show the user the proposed spot, and insert the content only after they approve.

## The ground rules, and why

- **Never create a heading** (`#`, `##`, and so on). The user has deliberately settled on the section structure, and every new section dilutes it. Every insertion goes under a heading that already exists.
- **A new top-level topic bullet inside an existing section is fine** when no existing bullet fits. For example, add `- sin embargo - however` under `# Random Phrases` if that phrase isn't there yet. Prefer nesting under an existing bullet whenever a real match exists.
- **Propose first, write second.** The user wants to approve the location before the file changes.
- **Keep the user's wording.** Do not silently fix spelling or accents. If you notice mistakes, mention them in your proposal so the user can decide whether to correct them.
- **Add a missing translation.** The file's convention is `Spanish - English`. If the user gives only the Spanish, append ` - <natural English translation>`. If they give only English, ask for the Spanish or offer one.

## How the file is laid out

- Headings run from `#` to `#####`. Top-level sections include Small things, Adverbs, Verbs (with Tricky verbs: llevar, Quedar, Poner, Pasar…), Moods (Subjunctive uses, Subjunctive vs Indicative), Tenses (each tense has a `#### Examples`), Pronouns (DO/IO, relative, interrogative), Conjunctions, Prepositions (Por/Para), Se (reflexive, impersonal, passive, accidental…), Que, lo, ya, Idioms, Random Phrases, Special Verb usage (Ser vs Estar), and Questions for next spanish class.
- Content is mostly bulleted lists **indented with tabs**. A few older spots use spaces. Copy whatever indentation the target list's neighbors use.
- There are two common list shapes:
  1. **Topic bullet with nested examples**, used in Small things, Random Phrases, and Tricky verbs:
     ```
     - hasta que - until, up to the point that
     	- When hasta que refers to an event that hasn't happened yet, you use the subjunctive
     	- No me voy hasta que tú llegues - (I'm not leaving until you arrive.)
     ```
     Explanations or rules come first under the topic, then example sentences.
  2. **Flat example list** under `#### Examples` for a tense or construction:
     ```
     - Que buscas ? - what are you looking for?
     ```
- Some sections hold only links (Reddit, YouTube). If the user gives a URL, it goes with the other links for that topic.

## Workflow

### 1. Understand the content
Work out what grammar point the sentence actually shows. A sentence often touches several points. "Se me olvidó la llave" involves accidental se, the preterite, and IO pronouns. Pick the point the user most likely wants to remember.

**The user's focus overrides your own judgment.** The user often says in plain words which part of the sentence matters. For example: "focus on the iba part because I want to put emphasis on the imperfect", "this is for quedar", "I care about the por here", or "put it with the subjunctive stuff". Read that as a placement instruction:
- If they name a grammar topic, such as the imperfect, use the section for that topic even when another point in the sentence is more prominent. In "Se me olvidó que le dije a mi mamá que iba a cocinar hoy en la noche", the obvious home is Accidental se. With "focus on the iba part, the imperfect", it goes to `### Indicative - Imperfect`, usually its `#### Examples` list, or a more specific bullet there such as the imperfect use for a planned action like *iba a + infinitive*, if one exists.
- If they only point at words ("focus on the iba part"), work out which grammar point those words show and place the sentence by that.
- In the proposal, say which focus you applied ("Placed for the imperfect (*iba a cocinar*), as you asked"). You can mention the otherwise-obvious section as an alternative in one line. Don't argue for it.
- The focus instruction is not part of the content. Insert only the sentence, plus a translation if one is needed.

### 2. Check for duplicates
Run the similarity finder on each item. It searches the whole file, ignoring accents, case, punctuation and the English half:
```bash
python3 ~/.claude/skills/grammar-insert/scripts/find_similar.py /Volumes/NO_NAME/knowledge_base/Spanish/Guide/Grammar.md "<the Spanish sentence>"
```
It prints `line: score/words  text`, best match first. Look at the top hits and decide for yourself: a high score with the same meaning is a near-duplicate, but a high score can also come from unrelated lines that happen to share words. Close variants often live far from where you plan to insert (e.g. in a tense's Examples list), which is why the search covers the whole file and not just the target section. Examples of near-duplicates: ("Ojalá no llueva mañana" vs "Ojala que no llueva mañana", or "Ella es tan inteligente como su hermano" vs "Es tan inteligente como su hermana".)

- **Exact duplicate** (same sentence, ignoring only case, accents and punctuation): don't add it. Tell the user where it already is.
- **Near-duplicate** (same idea, small wording differences): **still add it.** The user wants every version they give you recorded. Flag the similar line(s) with their line numbers and the existing text, so the user can merge or clean them up by hand later. Don't edit or remove the existing lines yourself.

### 3. Find candidate sections
Get the heading map with line ranges:
```bash
python3 ~/.claude/skills/grammar-insert/scripts/outline.py /Volumes/NO_NAME/knowledge_base/Spanish/Guide/Grammar.md          # all headings
python3 ~/.claude/skills/grammar-insert/scripts/outline.py /Volumes/NO_NAME/knowledge_base/Spanish/Guide/Grammar.md quedar   # filter by text
```
Each output line shows `start-end`, the heading, and its count of top-level bullets.

Big sections like `# Small things` (about 180 topics) and `# Random Phrases` have no subheadings. Their topics live in top-level bullets, so list those bullets:
```bash
awk 'NR>=START && NR<=END && /^- /{print NR": "$0}' /Volumes/NO_NAME/knowledge_base/Spanish/Guide/Grammar.md
```
Substitute START and END with the range outline.py printed for that section. Line numbers shift as the file grows, so never reuse old ones.
Also grep the whole file for the key word or construction (`grep -n -i 'tan .* como'`). Topics are often a bullet buried inside a large section rather than a heading of their own, and grep finds them.

### 4. Choose the most specific fit
Prefer the deepest, most specific home:
- An existing topic bullet about this exact word or construction beats a general section. For example, the `- tan and tanto` bullet beats `# Adverbs` for "tan… como".
- A dedicated verb section such as `### Quedar` beats the generic tense `#### Examples` when the sentence is mainly about that verb's meaning.
- Use a tense's `#### Examples` list when the sentence mainly illustrates the tense.
- If several places are equally good, pick one and mention the runner-up in one line.

Read only the target region, about 30–80 lines around it, to see the exact list, its indentation, and its ordering. Insert at the end of the relevant sub-list unless an obvious order such as rules before examples suggests a better spot.

### 5. Propose
Show the user:
- The heading path, for example `# Verbs > ## Tricky verbs > ### Quedar`, and the parent bullet if nesting.
- The line number you'll insert after.
- The exact line(s) that will be written, with the translation added if needed.
- Any spelling or accent issues you noticed, without changing their text.
- Any near-duplicates already in the file (line number + existing text), noting that you're adding the new one anyway.
- Optionally, the runner-up location in one line.

Keep it short and wait for approval. If they pick a different spot, use that one.

### 6. Insert
Use the Edit tool. Anchor on the specific line you're inserting after, plus enough nearby context to make the match unique, because example sentences repeat in this file. Match the neighbors' indentation exactly, with tabs vs. spaces and the same depth. Afterwards, show the inserted line with one line of context above and below, and give its line number. Repeat any near-duplicate flags here so they aren't lost.

### Multiple items at once
If the user gives several sentences, run steps 1–4 for each one, then present one numbered proposal table so the user can review everything at a glance:

| # | Sentence | Location | Insert after |
|-|-|-|-|
| 1 | Yo estaría más tranquila si me dijeras la verdad - I would feel calmer if you told me the truth | #### Subjunctive in Conditional Clauses > "Use the imperfect subjunctive in hypothetical, contrary-to-fact if-clauses…" | 8215, after *Si no tuviera un despertador…* |
| 2 | Ya habían estado aquí antes - They had already been here before | ### Indicative - Past Perfect (Pluperfect) > "Use the past perfect to express an event…" | 9969, after *Marta había salido cuando yo entré* |
| 3 | Si estuviéramos juntos, sería diferente - If we were together, it would be different | Same bullet as #1 | right after #1 |

What goes in each column:
- **Sentence:** exactly the line that will be written, with any translation you added.
- **Location:** the most specific heading, then `>` and the quoted parent bullet if the sentence nests under one. Shorten long bullets with "…".
- **Insert after:** the current line number plus a few words of that line, so the user can recognize the spot. If two items share a list, say "right after #N".

Under the table, add short numbered notes only for items that need them: accent or spelling issues, near-duplicates (line + text), the focus you applied, or a runner-up location. Leave out items that have nothing to say.

Use a plain markdown table with a minimal `|-|-|` separator, which renders as a boxed table in the terminal.

Then wait. The user may approve everything ("ok", "go"), or change individual rows in plain words, e.g. "move 3 under Si clauses instead", "skip 2", "put 4 with the aunque indicative examples". Apply the changes, show the updated table again if anything moved, and insert once they approve.

When inserting, edit from the **bottom of the file upward**, highest line number first. Then each insert doesn't shift the line numbers of the ones still to come. After all inserts, report the final line number of each item by its #.
