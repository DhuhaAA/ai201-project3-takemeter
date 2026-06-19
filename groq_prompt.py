# ─────────────────────────────────────────────────────────────────────────────
# GROQ BASELINE PROMPT  —  paste into Section 5 of the Colab notebook
# ─────────────────────────────────────────────────────────────────────────────
#
# Instructions:
#   1. Open the starter Colab notebook and navigate to Section 5.
#   2. Add your Groq API key via Colab Secrets (key name: GROQ_API_KEY).
#   3. Replace the placeholder prompt string in the Section 5 cell with the
#      CLASSIFICATION_PROMPT string defined below.
#   4. Make sure label_map in Section 1 is set to:
#         label_map = {"analysis": 0, "hot_take": 1, "reaction": 2}
#   5. Run the baseline cells. The notebook expects the model to return exactly
#      one of the three label strings — the prompt enforces this.
#
# ─────────────────────────────────────────────────────────────────────────────

CLASSIFICATION_PROMPT = """You are a discourse classifier for r/TrueFilm, a Reddit community dedicated to serious film discussion.

Your task is to classify a post into exactly one of the following three categories:

LABEL DEFINITIONS:
- analysis: The post makes a structured argument about a film using specific, verifiable evidence — such as cinematography choices, narrative structure, historical context, directorial technique, genre comparison, or thematic interpretation. The reasoning could be engaged with or debated on its merits. There is a clear attempt to explain *why* a film works or doesn't work, not just *that* it does.

- hot_take: A bold, confident opinion stated without supporting evidence or with only superficial reasoning. The post asserts a strong or contrarian position but does not build a genuine argument for it. The claim might be interesting or even correct, but the post asserts rather than argues. Decorative use of one detail to sound credible does not make a post analysis.

- reaction: An immediate emotional or impressionistic response to a film, focused on how it made the viewer feel or a general sense of quality. The post is expressing an experience rather than analyzing one. The central move is "this film did something to me" rather than "here is why this film works."

DECISION RULES FOR HARD CASES:
- If a post uses specific film terminology (mise-en-scène, cinematography, etc.) but the core move is still expressing a feeling rather than constructing an argument, label it reaction.
- If a post cites one specific detail (a scene, a stat, a technique) but uses it to decorate an assertion rather than reason from it, label it hot_take.
- If a post makes a strong claim AND provides reasoning that would survive removal of the opinion framing, label it analysis.

INSTRUCTIONS:
Read the following post from r/TrueFilm. Respond with exactly one word: the label that best fits the post. Do not include punctuation, explanation, or any other text. Your entire response must be one of these three words:
analysis
hot_take
reaction

POST:
{text}"""

# ─────────────────────────────────────────────────────────────────────────────
# HOW THE NOTEBOOK USES THIS PROMPT
# ─────────────────────────────────────────────────────────────────────────────
#
# The Section 5 cell will call:
#     prompt = CLASSIFICATION_PROMPT.format(text=post_text)
# and send it to the Groq API. The notebook then parses the response by
# stripping whitespace and checking if it exactly matches one of the labels.
#
# If you see >10% unparseable responses:
#   - Check that your label_map keys match the label strings exactly
#     ("hot_take" not "hot take", "analysis" not "Analysis")
#   - Add a .lower().strip() call when parsing if the model capitalizes
#
# Recommended Groq model for the baseline: "llama3-70b-8192"
# It is fast, free-tier accessible, and accurate on classification tasks.
# Set temperature=0 for deterministic outputs.
#
# Example Groq API call for Section 5:
# ─────────────────────────────────────────────────────────────────────────────
#
# from groq import Groq
# import os
#
# client = Groq(api_key=os.environ["GROQ_API_KEY"])
#
# def classify_post(text):
#     prompt = CLASSIFICATION_PROMPT.format(text=text)
#     response = client.chat.completions.create(
#         model="llama3-70b-8192",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0,
#         max_tokens=10,
#     )
#     return response.choices[0].message.content.strip().lower()
#
# ─────────────────────────────────────────────────────────────────────────────
