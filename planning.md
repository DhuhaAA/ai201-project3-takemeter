Planning: r/TrueFilm Discourse Classifier

Community

I chose r/TrueFilm (reddit.com/r/TrueFilm) because it is a film discussion community that explicitly values thoughtful criticism over casual fandom. The subreddit's own rules ask users to go beyond simple reactions and engage with film as an art form — which means the community naturally produces a wide range of discourse quality in a single place. Some posts are rigorous analytical essays; others are bold one-sentence verdicts; others are purely emotional responses to a recent watch. That range makes it an ideal source for a classification task: the signal differences between labels are real and meaningful to the community, not invented by me. I am also a film fan myself and follow critics closely, which gives me genuine domain familiarity to annotate accurately.

The discourse is text-heavy (TrueFilm discourages low-effort posts) and varied in structure: long analytical threads sit alongside short hot takes and emotional first-watch reactions. With over 3 million members and daily active posting, collecting 200+ examples is straightforward without needing scraping tools.


Labels

I am using three labels that reflect how TrueFilm members themselves talk about discourse quality.

analysis

Definition: The post makes a structured argument about a film using specific, verifiable evidence — such as cinematography choices, narrative structure, historical context, directorial technique, genre comparison, or thematic interpretation — where the reasoning could be engaged with or debated on its merits.

Example 1:


"Kubrick's use of one-point perspective in The Shining isn't just a stylistic quirk — it's doing psychological work. Every symmetrical hallway frames Jack as the inevitable center of the frame, reinforcing his sense of predestination. The few scenes where Wendy holds center are deliberately off-balance by comparison, shot slightly wider to make her look small in the same spaces."



Example 2:


"People underrate how much A Separation's ambiguity is structural, not accidental. Farhadi withholds the one piece of information that would resolve the central legal question — did Razieh know the old man had Alzheimer's — and he withholds it symmetrically: we never see the scene, no character has a complete account. The film earns its moral uncertainty because the form matches the theme."




hot_take

Definition: A bold, confident opinion stated without supporting evidence or with only superficial reasoning — the post asserts a strong or contrarian position but does not build a genuine argument for it, even if the claim could in principle be defended with evidence.

Example 1:


"Parasite is the most overrated Best Picture winner of the last 20 years. It's a well-made thriller but it does not deserve to be spoken about in the same breath as actual great cinema. The ending is ridiculous and the class commentary is surface-level."



Example 2:


"Christopher Nolan has never made a film with a convincing female character. Not one. Every woman in his filmography is either a plot device or a refrigerator. I'll die on this hill."




reaction

Definition: An immediate emotional or impressionistic response to a film, focused on how it made the viewer feel or a general sense of quality, without structured argument or specific evidence — the post is expressing an experience rather than analyzing one.

Example 1:


"Just finished Jeanne Dielman for the first time. I don't even know what to say. I've been sitting here for twenty minutes. Nothing I've seen has made me feel like this. It's like the movie broke something open."



Example 2:


"Watched Mulholland Drive last night and I genuinely have no idea what I just watched but I loved every second of it. My brain is completely scrambled. This is the most I've thought about a movie in years."




Hard Edge Cases

The evidence-decorated hot take: The hardest boundary is between analysis and hot_take when a post cites a specific detail or statistic to support what is structurally still an assertion. For example:


"Spielberg is overrated and Schindler's List proves it — the black-and-white cinematography is gorgeous but the film manipulates you emotionally at every turn rather than trusting you to respond. The little girl in the red coat is the most cynical filmmaking choice in his career."



This post references a specific filmmaking decision (the red coat) but doesn't build an argument — it uses the reference to sound credible while asserting rather than reasoning.

Decision rule: If the post provides specific evidence that would support the claim even if you removed the opinion framing, label it analysis. If the evidence is selected to sound credible but the post isn't actually reasoning from it — if removing the detail wouldn't weaken the underlying claim — label it hot_take. The red coat example is hot_take: the assertion ("cynical manipulation") is stated, not argued.

The articulate reaction: A post can be emotionally driven but use sophisticated vocabulary, making it look like analysis. For example:


"The mise-en-scène in Stalker left me completely undone. I've never felt so immersed in a film's texture. Tarkovsky just operates on a different level."



This uses film terminology but is still expressing a feeling, not constructing an argument. If the core move is "this made me feel something profound," it is reaction regardless of how it is phrased.

Decision rule: Ask — is the post explaining why the film works or reporting that it worked on the viewer? If the latter, label it reaction.


Data Collection Plan

Source: r/TrueFilm public posts and top-level comments, collected manually via the Reddit web interface. I will use the "top" and "hot" sorting filters across different time ranges (past month, past year, all time) to get variety in film topics and post styles. I will not use posts behind any authentication barrier.

Target distribution:


analysis: ~75 examples (37.5%)
hot_take: ~65 examples (32.5%)
reaction: ~60 examples (30%)


This is roughly balanced. TrueFilm skews toward analysis by design, so I will need to actively seek out shorter, more opinionated threads to find hot_takes and reactions — searching for posts about divisive films (Midsommar, Hereditary, recent Oscar winners) tends to surface more emotional and contrarian responses.

If a label is underrepresented after 200 examples: I will search specifically for post types that generate that label. For reaction, I will look in "first watch" or "just finished" threads. For hot_take, I will look in threads debating overrated/underrated films. I will collect additional examples until no label falls below 20% of the total dataset. I will not artificially lower the threshold — I will collect more data instead.

What I will not collect: Posts that are primarily questions ("Can anyone recommend a film like X?"), posts that are primarily quotes with no commentary, and posts under ~30 words (too short to reliably classify).


Evaluation Metrics

I will report the following metrics, evaluated on the held-out test set (15% of data, ~30 examples):

Overall accuracy: Fraction of test examples correctly classified. Reported for both baseline and fine-tuned model. Useful as a top-line number but insufficient on its own because it can hide a model that ignores minority classes.

Per-class F1 score: The harmonic mean of precision and recall for each label. This is the primary metric for this task because:


The classes, while roughly balanced, are not perfectly equal. A model could achieve acceptable accuracy by performing poorly on one class.
The hot_take / analysis boundary is the hardest to learn. A high F1 on reaction but low F1 on hot_take reveals that the hard boundary wasn't learned — overall accuracy would mask this.


Confusion matrix: A 3×3 table showing predicted vs. actual labels. This reveals directional errors: does the model confuse analysis with hot_take more often than the reverse? That asymmetry tells me something specific about what the model learned.

Macro-averaged F1: The unweighted average of per-class F1 scores. This penalizes the model equally for failing on any class, which is the right behavior here since I care about all three distinctions.

I will not use weighted F1 as my primary metric because the classes are close enough in size that it would not meaningfully differ from macro F1, and macro F1 is easier to interpret.


Definition of Success

Minimum threshold for "good enough": Macro-averaged F1 ≥ 0.70 across all three classes, with no individual class F1 below 0.60. At this level, the classifier would be useful as a pre-screening tool in a community moderation context — it would flag likely reactions or hot takes for human review with acceptable accuracy.

Strong performance: Macro-averaged F1 ≥ 0.78, meaning the model has genuinely learned all three distinctions and not just the easy ones.

What would make it genuinely useful: If the analysis vs. hot_take F1 gap is under 0.10, the model has learned the hardest distinction in the taxonomy — that is the real test of whether the labels are working.

Failure condition: If the fine-tuned model does not meaningfully outperform the zero-shot LLM baseline (by at least 5 percentage points on macro F1), the fine-tuning added no value, which likely means labels are too noisy or the dataset is too small. This would require revisiting annotation before any further work.

The definition of success in the planning document is intentionally specific so that the outcome at evaluation time is unambiguous — either the model clears the threshold or it doesn't.


AI Tool Plan

Label stress-testing

Before I begin annotating, I will give Claude my three label definitions and my two edge case descriptions and ask it to generate 8–10 posts that sit at the boundary between analysis and hot_take specifically (since that is the hardest pair). I will then try to classify each generated post using my definitions. Any post I cannot cleanly classify will signal that my decision rule needs sharpening. I will refine the rule and repeat until I can classify all generated boundary cases with confidence. This happens before annotation begins.

Annotation assistance

I will use Claude to pre-label batches of 20–30 examples at a time by providing my full label definitions and asking for one label per post with a one-sentence rationale. I will review every pre-assigned label myself and correct any I disagree with. I will track which examples were pre-labeled in a separate column (prelabeled_by_ai, values: yes / no) in my CSV so I can report the proportion in my AI usage section and check whether pre-labeled examples have higher disagreement rates after my review.

Failure analysis

After running evaluation on the test set, I will paste all misclassified examples (true label + predicted label + post text) into Claude and ask it to identify common patterns — e.g., post length, presence of sarcasm, specific vocabulary, label pairs that dominate errors. I will then re-read all flagged examples myself to verify whether the patterns hold. I will discard any AI-identified pattern that I cannot confirm by reading the examples myself. The verified patterns will go into my README evaluation report.
Share
