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

def _brand_item_schema():
    return {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "url": {"type": "string"},
            "description": {"type": "string"},
        },
        "required": ["name", "url", "description"],
        "additionalProperties": False,
    }

# catches stray control characters (e.g. a tab mid-word) from occasional
# decoder glitches on accented characters, seen once in testing
def _has_control_chars(value) -> bool:
    if isinstance(value, str):
        return any(ord(c) < 0x20 for c in value)
    if isinstance(value, dict):
        return any(_has_control_chars(v) for v in value.values())
    if isinstance(value, list):
        return any(_has_control_chars(v) for v in value)
    return False

# search the web for real brands matching this specific taste profile
def discover_brands(profile_text: str, client: anthropic.Anthropic, max_attempts: int = 3) -> dict:
    prompt = f"""Someone's aesthetic taste profile, inferred from their own images:

{profile_text}

Search the web to find real, currently active brands that genuinely fit this
person's specific aesthetic, not generic recommendations. Find 2 fashion
brands, 2 beauty brands, and 2 lifestyle/home brands. Verify each brand is
real and currently operating, and find its actual website URL.

For each brand, write 1-2 sentences explaining why it fits THIS profile
specifically, connecting it to the archetypes and motifs above, not a
generic description of the brand."""

    tools = [{"type": "web_search_20260209", "name": "web_search", "max_uses": 8}]
    # output_config.format constrains generation at the token level, so the
    # response is guaranteed valid JSON, unlike asking nicely in the prompt
    # (which broke once a description happened to contain an unescaped quote)
    output_config = {
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "fashion": {"type": "array", "items": _brand_item_schema()},
                    "beauty": {"type": "array", "items": _brand_item_schema()},
                    "lifestyle": {"type": "array", "items": _brand_item_schema()},
                },
                "required": ["fashion", "beauty", "lifestyle"],
                "additionalProperties": False,
            },
        }
    }

    for attempt in range(max_attempts):
        messages = [{"role": "user", "content": prompt}]
        response = client.messages.create(
            model="claude-sonnet-5", max_tokens=2000, tools=tools, output_config=output_config, messages=messages
        )
        while response.stop_reason == "pause_turn":
            # server-side search hit its per-turn iteration cap before finishing;
            # resend to let it continue where it left off
            messages = [{"role": "user", "content": prompt}, {"role": "assistant", "content": response.content}]
            response = client.messages.create(
                model="claude-sonnet-5", max_tokens=2000, tools=tools, output_config=output_config, messages=messages
            )

        text_blocks = [b.text for b in response.content if b.type == "text"]
        if not text_blocks:
            raise RuntimeError(f"no text in response, stop_reason={response.stop_reason}")
        matches = json.loads(text_blocks[-1])

        if not _has_control_chars(matches):
            return matches
        print(f"discovery attempt {attempt + 1} had a stray control character, retrying...")

    raise RuntimeError(f"discover_brands produced control characters after {max_attempts} attempts")

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
