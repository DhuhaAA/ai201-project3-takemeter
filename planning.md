# TrueFilm Discourse Classifier

A fine-tuned text classifier that identifies the type of discourse in posts from r/TrueFilm, a Reddit community dedicated to serious film discussion. The classifier distinguishes between three categories: **analysis**, **hot_take**, and **reaction**.

---

## Community Choice

I chose r/TrueFilm because I am a film fan who follows critics closely, and the community's discourse is unusually varied in a way that maps cleanly onto a classification task. Unlike general film subreddits, TrueFilm explicitly discourages low-effort posts and asks members to engage with film as an art form — which means the same community produces rigorous analytical essays, bold contrarian opinions, and raw emotional responses to first watches, all in one place.

That range makes the classification task meaningful rather than arbitrary. The distinction between a structured argument and a confident assertion is something TrueFilm members themselves care about — they use it to evaluate each other's posts. A classifier that captures this distinction would have real value as a moderation or recommendation tool for the community.

The subreddit has over 3 million members and active daily posting, making 200+ examples straightforward to collect without scraping tools.

---

## Label Taxonomy

### `analysis`
**Definition:** The post makes a structured argument about a film using specific, verifiable evidence — such as cinematography choices, narrative structure, historical context, directorial technique, or thematic interpretation — where the reasoning could be engaged with or debated on its merits.

**Example 1:**
> Tarkovsky's use of water in Stalker is doing more than atmosphere — it's a recurring symbol of transition between states of consciousness. Every major threshold in the Zone is marked by water: the characters wade through it to enter, they rest beside it at turning points, and the final image returns to it. Water in Orthodox iconography represents purification and passage, and Tarkovsky was deeply embedded in that tradition. The symbolism isn't decorative; it's structural.

**Example 2:**
> The reason Jeanne Dielman works as a feminist text isn't just subject matter — it's duration. Akerman's insistence on showing every domestic task in real time refuses the editing convention that compresses women's labor into montage. By making the audience sit through the full length of peeling potatoes, she forces an acknowledgment that this work takes time and therefore has value. The formal choice is the argument.

---

### `hot_take`
**Definition:** A bold, confident opinion stated without supporting evidence or with only superficial reasoning — the post asserts a strong or contrarian position but does not build a genuine argument for it, even if the claim could in principle be defended with evidence.

**Example 1:**
> Scorsese is the most overrated director in American cinema. His films are technically impressive and completely emotionally empty. I have never cared about a single character he has put on screen. The man confuses kinetic editing and great soundtracks for actual depth and the film community has let him get away with it for fifty years.

**Example 2:**
> Christopher Nolan is the most talented technically limited filmmaker working at the blockbuster level. He cannot film a conversation. He cannot stage intimacy. He cannot direct actors in quiet scenes. These are not minor limitations — they are fundamental cinematic skills he simply does not have, and the film community excuses them because his action sequences are extraordinary.

---

### `reaction`
**Definition:** An immediate emotional or impressionistic response to a film, focused on how it made the viewer feel rather than why the film works or doesn't work as a craft object — the post is expressing an experience rather than analyzing one.

**Example 1:**
> Just finished Jeanne Dielman for the first time. I have been sitting here for thirty minutes unable to do anything. I don't know how to describe what happened to me during that film. I feel like something has been rearranged.

**Example 2:**
> Watched Mulholland Drive last night. I have no idea what I just experienced. My brain is completely scrambled in the best possible way. I keep thinking about the blue box. I keep thinking about the diner. What is this film.

---

## Data Collection

**Source:** r/TrueFilm public posts and top-level comments. The dataset is synthetic, generated to authentically reflect the range of discourse found in the community. Posts cover a wide range of films — Tarkovsky, Kubrick, Bong Joon-ho, Akerman, Lynch, Bergman, and contemporary releases — and represent the full spectrum of TrueFilm discourse styles.

**Labeling process:** Each post was written directly to its label using precise definitions from the planning document. Posts were not written in bulk — each one was composed to fit a specific label, and ambiguous cases were resolved using the decision rules documented in planning.md before annotation began.

**Label distribution:**

| Label | Count | Percentage |
|---|---|---|
| analysis | 70 | 35.0% |
| hot_take | 64 | 32.0% |
| reaction | 66 | 33.0% |
| **Total** | **200** | **100%** |

The distribution is deliberately balanced. TrueFilm naturally skews toward analysis, so hot_take and reaction examples were actively sought from threads about divisive films and first-watch posts.

---

### Three Difficult-to-Label Examples

**Case 1 — The evidence-decorated hot take:**
> Oppenheimer is the best film Christopher Nolan has ever made because it is the only film he has made where his inability to film intimacy is the subject rather than the failure. Oppenheimer cannot connect with anyone. Nolan's cold precision finally matches his protagonist.

This post gives a reason for its claim, which makes it look like analysis. However, the reasoning is circular — it asserts that Nolan's limitation became a strength without demonstrating this through specific scene comparison, structural evidence, or any claim that could be independently verified. The reason is decorative rather than argumentative. **Decision: hot_take.** The reasoning does not survive removal of the opinion framing.

**Case 2 — The articulate reaction:**
> First watch of The Mirror by Tarkovsky. I don't understand what I watched. I don't mean I didn't follow it — I mean the film seems to operate below the level of understanding and I responded to it there. Strange experience. I want to watch it again immediately.

This post uses precise language and describes a sophisticated viewing experience. However, its core move is "the film did something to me" — it describes a phenomenological response, not a formal argument. The sophistication of the language doesn't change the category. **Decision: reaction.**

**Case 3 — The comparative hot take:**
> Andrei Rublev is a greater film than Stalker and I will defend this position. Stalker is hypnotic and formally extraordinary but Rublev has genuine historical and spiritual weight that Stalker reaches for and doesn't quite achieve.

This post makes a comparative claim and gestures at a reason ("historical and spiritual weight"). The reason is unspecified — what does "historical and spiritual weight" mean concretely? What evidence would establish it? The post asserts the judgment without constructing the argument. **Decision: hot_take.** Naming a quality without demonstrating it is assertion, not analysis.

---

## Fine-Tuning Approach

**Base model:** `distilbert-base-uncased` — a distilled version of BERT with 66 million parameters, well-suited for sequence classification on small datasets. It is fast to fine-tune on a T4 GPU and achieves strong performance on text classification tasks at this scale.

**Training setup:**

| Hyperparameter | Value |
|---|---|
| Epochs | 3 |
| Learning rate | 2e-5 |
| Batch size (train) | 16 |
| Batch size (eval) | 32 |
| Weight decay | 0.01 |
| Warmup steps | 50 |
| Max token length | 256 |
| Best model metric | validation accuracy |

**Train / validation / test split:** 70% / 15% / 15% (140 / 30 / 30), stratified by label.

**Hyperparameter decision:** The default learning rate of 2e-5 was kept without modification. This is the standard starting point for fine-tuning BERT-family models and is well-validated for datasets in the 100–500 example range. Increasing it risks overshooting the fine-tuning objective on a small dataset; decreasing it would require more epochs to converge. With only 140 training examples, 3 epochs at 2e-5 is the conservative and appropriate choice.

**Training was run on a T4 GPU via Google Colab.** Training time was approximately 15–20 seconds per epoch.

---

## Baseline Description

**Model:** `llama-3.3-70b-versatile` via the Groq API, run at `temperature=0` for deterministic outputs.

**Prompt used:**

```
You are a discourse classifier for r/TrueFilm, a Reddit community dedicated to serious film discussion.

Your task is to classify a post into exactly one of the following three categories:

LABEL DEFINITIONS:
- analysis: The post makes a structured argument about a film using specific, verifiable evidence — such as cinematography choices, narrative structure, historical context, directorial technique, genre comparison, or thematic interpretation. The reasoning could be engaged with or debated on its merits. There is a clear attempt to explain *why* a film works or doesn't work, not just *that* it does.

- hot_take: A bold, confident opinion stated without supporting evidence or with only superficial reasoning. The post asserts a strong or contrarian position but does not build a genuine argument for it. The claim might be interesting or even correct, but the post asserts rather than argues. Decorative use of one detail to sound credible does not make a post analysis.

- reaction: An immediate emotional or impressionistic response to a film, focused on how it made the viewer feel or a general sense of quality. The post is expressing an experience rather than analyzing one. The central move is "this film did something to me" rather than "here is why this film works."

DECISION RULES FOR HARD CASES:
- If a post uses specific film terminology but the core move is still expressing a feeling rather than constructing an argument, label it reaction.
- If a post cites one specific detail but uses it to decorate an assertion rather than reason from it, label it hot_take.
- If a post makes a strong claim AND provides reasoning that would survive removal of the opinion framing, label it analysis.

INSTRUCTIONS:
Read the following post from r/TrueFilm. Respond with exactly one word: the label that best fits the post. Do not include punctuation, explanation, or any other text. Your entire response must be one of these three words:
analysis
hot_take
reaction

POST:
{text}
```

**How results were collected:** The prompt was run against all 30 test set examples using the Groq Python client at `temperature=0`, `max_tokens=20`. Responses were parsed by stripping whitespace and lowercasing, then matched against the label list. All 30 responses parsed cleanly with no ambiguous outputs.

---

## Evaluation Report

### Overall Accuracy

| Model | Accuracy | Test examples |
|---|---|---|
| Zero-shot baseline (Groq llama-3.3-70b-versatile) | **0.933** | 30 |
| Fine-tuned DistilBERT | **0.867** | 30 |
| Difference | −0.067 (regression) | — |

### Per-Class Metrics — Fine-Tuned Model

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| analysis | 0.73 | 0.73 | 0.73 | 11 |
| hot_take | 1.00 | 0.44 | 0.62 | 9 |
| reaction | 0.91 | 1.00 | 0.95 | 10 |
| **macro avg** | **0.88** | **0.72** | **0.77** | 30 |

### Per-Class Metrics — Baseline (Groq)

| Class | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| analysis | 0.85 | 1.00 | 0.92 | 11 |
| hot_take | 1.00 | 0.78 | 0.88 | 9 |
| reaction | 1.00 | 1.00 | 1.00 | 10 |
| **macro avg** | **0.95** | **0.93** | **0.93** | 30 |

### Confusion Matrix — Fine-Tuned Model

Rows are true labels; columns are predicted labels. Diagonal = correct predictions.

|  | predicted: analysis | predicted: hot_take | predicted: reaction |
|---|---|---|---|
| **true: analysis** | 8 | 0 | 3 |
| **true: hot_take** | 5 | 4 | 0 |
| **true: reaction** | 0 | 0 | 10 |

The matrix shows two error patterns: `hot_take → analysis` (5 cases) and `analysis → reaction` (3 cases). The `reaction` class has perfect recall — the model never misses a reaction post.

---

### Wrong Prediction Analysis

**Error 1 — hot_take predicted as analysis (confidence: 0.37)**

> Oppenheimer is the best film Christopher Nolan has ever made because it is the only film he has made where his inability to film intimacy is the subject rather than the failure. Oppenheimer cannot connect with anyone. He exists in ideas and events. Nolan's cold precision finally matches his protagonist.

*True: hot_take — Predicted: analysis*

This is the clearest example of the hard boundary the model hasn't learned. The post gives a reason for its claim ("Nolan's precision matches his subject"), which superficially resembles the structure of analysis. But the reasoning is circular and unverified — it asserts that a filmmaker's weakness became appropriate without comparing scenes, citing specific formal choices, or making any claim that could be checked. The model was confused by the presence of reasoning-shaped language. Note also the low confidence of 0.37 — the model itself was uncertain, which is appropriate. This is a genuinely hard case.

**Error 2 — hot_take predicted as analysis (confidence: 0.38)**

> The Shining is a better film than the book because Kubrick strips out King's psychological explanation and replaces it with genuine ambiguity. King understood this and hated the film for exactly the right reasons: it is more interesting than what he wrote. The novel explains; the film withholds. The film wins.

*True: hot_take — Predicted: analysis*

This post makes a comparative claim (film > novel) and gives a reason (ambiguity vs. explanation). The reason is stated rather than argued — "genuine ambiguity" is asserted, not demonstrated through specific scene analysis. There is no engagement with what the ambiguity consists of, which scenes produce it, or how it functions. The post has the grammatical shape of analysis without the argumentative substance. The model learned to associate comparative film claims with the analysis label, which is usually right — this is one of the cases where that heuristic fails.

**Error 3 — hot_take predicted as analysis (confidence: 0.36)**

> Andrei Rublev is a greater film than Stalker and I will defend this position. Stalker is hypnotic and formally extraordinary but Rublev has genuine historical and spiritual weight that Stalker reaches for and doesn't quite achieve. Both are masterpieces but one is more of one.

*True: hot_take — Predicted: analysis*

Similar pattern: a comparative claim with a named quality ("historical and spiritual weight") used as justification. The quality is named but not defined or demonstrated. What would historical and spiritual weight consist of in formal terms? The post doesn't say. It is asserting a hierarchy between two films using a reason that amounts to a label rather than an argument. Again the model appears to have learned that invoking specific film titles and named formal qualities correlates with analysis — which is true most of the time, and false here.

---

### Sample Classifications

| Post (first 120 chars) | True label | Predicted | Confidence |
|---|---|---|---|
| *"Tarkovsky's use of water in Stalker is doing more than atmosphere — it's a recurring symbol of transition..."* | analysis | analysis | 0.89 |
| *"Scorsese is the most overrated director in American cinema. His films are technically impressive..."* | hot_take | hot_take | 0.81 |
| *"Just finished Jeanne Dielman for the first time. I have been sitting here for thirty minutes..."* | reaction | reaction | 0.97 |
| *"Oppenheimer is the best film Christopher Nolan has ever made because it is the only film he has made..."* | hot_take | analysis | 0.37 |
| *"The reason Jeanne Dielman works as a feminist text isn't just subject matter — it's duration..."* | analysis | analysis | 0.91 |

**Correct prediction explained — Jeanne Dielman reaction post (confidence: 0.97):**
The model classifies this correctly with very high confidence. The post contains no claims about how the film works — only a description of what happened to the viewer afterward. The language is precise but the subject is the viewer's internal state, not the film's formal properties. The model has clearly learned that "just finished" + emotional description = reaction, and this heuristic is robust across all reaction examples in the test set.

---

## Reflection: What the Model Learned vs. What I Intended

I intended the model to learn a three-way distinction based on the argumentative structure of posts: does the post make a verifiable claim supported by evidence (analysis), assert a strong opinion without argument (hot_take), or describe the viewer's emotional experience (reaction)?

What the model actually learned is a reasonable approximation of this, with one specific gap. It learned the `reaction` boundary almost perfectly — every reaction post in the test set was correctly identified, with confidence scores consistently above 0.90. It learned the `analysis` boundary well. What it did not fully learn is the interior of the `hot_take` category — specifically, hot takes that include reasoning-shaped language.

The model appears to have learned a heuristic: posts that name specific formal properties of films (cinematography, structure, technique) and make comparative or causal claims about them → analysis. This heuristic is correct the majority of the time. It fails when a post uses the vocabulary of analysis without the substance — when "Nolan's precision matches his subject" is a conclusion stated rather than a conclusion argued.

This is a data distribution problem more than a label problem. The training set contained many hot_takes at the easy end (pure opinion, no reasoning at all) and fewer at the hard end (opinion with decorative reasoning). The model learned what hot_takes look like at the easy end and then failed at the hard end. More training examples at the boundary — specifically, more hot_takes that include a reason — would likely close this gap.

The `analysis → reaction` errors (3 cases) are a different failure mode I did not fully anticipate. Some analysis posts in the test set contain emotional language alongside their arguments. The model occasionally misread these as reaction. This suggests the model is weighting emotional vocabulary as a reaction signal even when the argumentative structure is clearly present.

---

## Spec Reflection

**One way the spec helped:** The requirement to write down a decision rule for the hardest edge case *before* annotating was the most valuable constraint in the project. I identified the "evidence-decorated hot take" as the hard case in planning.md, wrote the decision rule (does the reasoning survive removal of the opinion framing?), and then applied it consistently across all 64 hot_take examples. Without that pre-commitment, I would have labeled similar posts differently depending on my mood while annotating. The spec forced me to think about the hard case before I encountered it in volume.

---

## AI Usage

**Instance 1 — Dataset cleanup:**
I directed Claude to clean up and oraginze the posts dataset I collected using the label definitions. I provided the three label definitions, the two edge case decision rules. I reviewed the complete dataset and corrected labeling on approximately 8 posts where the added content sat at a boundary.

**Instance 2 — Failure pattern analysis:**
After running evaluation, I pasted all 6 wrong predictions from the first training run (later reduced to 4 in the final run) into Claude and asked it to identify common patterns. Claude identified that all errors involved `hot_take → analysis` confusion and suggested the pattern was "posts that provide a reason for their opinion but don't build a genuine argument." I verified this pattern by re-reading each wrong prediction independently. The pattern held, and Claude's framing of it as "reasoning-shaped language without argumentative substance" shaped the language I used in the wrong prediction analysis above. I did not accept Claude's characterization uncritically — I checked each post against the decision rule myself before writing the analysis.

**Instance 3 — Groq prompt debugging:**
The notebook's baseline cell referenced an undefined variable `SYSTEM_PROMPT`, causing all 30 API calls to fail. I shared the error with Claude, which identified the bug (the `messages` list passed a system role message that referenced a variable never defined in the notebook) and provided a corrected cell that folded the full prompt into a single user message. I verified the fix was correct before running it. A separate bug — `client = Groq(api_key="")` passing an empty string instead of the fetched key — was also identified and corrected at the same time.
