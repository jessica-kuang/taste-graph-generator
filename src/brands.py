import json
from pathlib import Path

import anthropic

# build a flat description of the taste profile for prompting
def load_taste_profile(cluster_labels_path: str, palette_path: str):
    with open(cluster_labels_path) as f:
        cluster_data = json.load(f)
    with open(palette_path) as f:
        palette_data = json.load(f)

    archetypes = []
    motifs = []
    moods = []
    for label in cluster_data["labels"].values():
        archetypes.append(label["archetype"])
        motifs.extend(label["motifs"])
        moods.append(label["mood"])

    return (
        f"Archetypes: {', '.join(archetypes)}\n"
        f"Recurring motifs: {', '.join(motifs[:10])}\n"
        f"Mood: {'; '.join(moods)}\n"
        f"Color palette: {palette_data['palette_name']} ({palette_data['palette_mood']})"
    )

# search the web for real brands matching this specific taste profile
def discover_brands(profile_text: str, client: anthropic.Anthropic) -> dict:
    prompt = f"""Someone's aesthetic taste profile, inferred from their own images:

{profile_text}

Search the web to find real, currently active brands that genuinely fit this
person's specific aesthetic, not generic recommendations. Find 2 fashion
brands, 2 beauty brands, and 2 lifestyle/home brands. Verify each brand is
real and currently operating, and find its actual website URL.

For each brand, write 1-2 sentences explaining why it fits THIS profile
specifically, connecting it to the archetypes and motifs above, not a
generic description of the brand.

Respond with ONLY a JSON object, nothing else, in this exact format:
{{
  "fashion": [{{"name": "...", "url": "...", "description": "..."}}, ...],
  "beauty": [{{"name": "...", "url": "...", "description": "..."}}, ...],
  "lifestyle": [{{"name": "...", "url": "...", "description": "..."}}, ...]
}}"""

    tools = [{"type": "web_search_20260209", "name": "web_search", "max_uses": 8}]
    messages = [{"role": "user", "content": prompt}]

    response = client.messages.create(model="claude-sonnet-5", max_tokens=2000, tools=tools, messages=messages)
    while response.stop_reason == "pause_turn":
        # server-side search hit its per-turn iteration cap before finishing;
        # resend to let it continue where it left off
        messages = [{"role": "user", "content": prompt}, {"role": "assistant", "content": response.content}]
        response = client.messages.create(model="claude-sonnet-5", max_tokens=2000, tools=tools, messages=messages)

    text_blocks = [b.text for b in response.content if b.type == "text"]
    if not text_blocks:
        raise RuntimeError(f"no text in response, stop_reason={response.stop_reason}")
    text = text_blocks[-1].strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.removeprefix("json").strip()
    return json.loads(text)

# save results
def save_matches(matches, output_path: str):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(matches, f, indent=2)
    print(f"saved brand matches to {output_path}")

# main
if __name__ == "__main__":
    client = anthropic.Anthropic()
    profile_text = load_taste_profile("data/profiles/cluster_labels.json", "data/profiles/palette.json")
    print("discovering brands...")

    matches = discover_brands(profile_text, client)
    for category, brands in matches.items():
        print(f"\n{category.upper()}")
        for brand in brands:
            print(f"  {brand['name']} — {brand['url']}")

    save_matches(matches, "data/profiles/brand_matches.json")
