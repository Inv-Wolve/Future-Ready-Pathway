import json
import subprocess
import os

# Paths
INPUT_FILE = "./MindMaze/js/content.json"
OUTPUT_FILE = "./MindMaze/js/analysis.json"
MODEL = "phi3"

# Helper to call Ollama locally
def ask_ollama(prompt, model=MODEL):
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode("utf-8"),
            capture_output=True,
            check=True
        )
        return result.stdout.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        return f"Error generating explanation: {e}"

# Prompts the AI model which i downloaded locally to do as told
def build_prompt(text, is_human):
    return f"""
You are a friendly linguistics expert.
The following text is labeled as {"HUMAN" if is_human else "AI"}:

{text}

Explain in **simple, easy-to-understand language** how someone could tell if it is AI-generated or human-written.
Keep it slightly detailed but not overwhelming. Highlight tone, vocabulary, repetition, punctuation, and flow.
Return only the explanation text.
"""

# Load JSON (file type)
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

results = []
for i, item in enumerate(data, start=1):
    prompt = build_prompt(item["text"], item["is_human"])
    explanation = ask_ollama(prompt)
    results.append({
        "text": item["text"],
        "is_human": item["is_human"],
        "explanation": explanation
    })
    if i % 50 == 0:
        print(f"Processed {i}/{len(data)} entries...")

# Save output
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"✅ Done! Analysis saved to {OUTPUT_FILE}")