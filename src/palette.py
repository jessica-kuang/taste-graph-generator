import numpy as np
import anthropic
from PIL import Image
from pathlib import Path
from sklearn.cluster import KMeans
import json

# same pixels from image
def sample_pixels(image_path: str, n_samples: int = 1000):
    img = Image.open(image_path)
    # always flatten to RGB
    if img.mode == "RGBA":
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    else:
        img = img.convert("RGB")

    pixels = np.array(img).reshape(-1, 3)
    indices = np.random.choice(len(pixels), min(n_samples, len(pixels)), replace=False)
    return pixels[indices]

# extract palette
def extract_palette(image_paths: list, n_colors: int = 6):
    all_pixels = []

    for path in image_paths:
        try:
            pixels = sample_pixels(path)
            all_pixels.append(pixels)
        except Exception as e:
            print(f"skipping {path}: {e}")

    all_pixels = np.vstack(all_pixels)
    print(f"running k-means on {len(all_pixels)} pixels...")

    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(all_pixels)

    # convert cluster centers to hex
    colors = kmeans.cluster_centers_.astype(int)
    hex_codes = [
        "#{:02X}{:02X}{:02X}".format(r, g, b)
        for r, g, b in colors
    ]

    # sort by frequency
    labels = kmeans.labels_
    counts = np.bincount(labels)
    sorted_indices = np.argsort(-counts)
    hex_codes = [hex_codes[i] for i in sorted_indices]

    return hex_codes

# get palette mood from claude
def describe_palette(hex_codes: list, archetypes: list, client: anthropic.Anthropic):
    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=150,
        messages=[
            {
                "role": "user",
                "content": f"""Given these dominant colors from someone's aesthetic inspiration images: {hex_codes}
                And their aesthetic archetypes: {archetypes}
                Respond with ONLY a JSON object:
                {{
                    "palette_mood": "3-5 word evocative description of the overall color mood",
                    "palette_name": "a poetic name for this palette (2-3 words)"
                }}
                No other text, just the JSON."""
            }
        ]
    )
    response_text = message.content[0].text.strip()
    if response_text.startswith("```"):
        response_text = response_text.strip("`")
        response_text = response_text.removeprefix("json").strip()
    return json.loads(response_text)

# load image paths
def load_image_paths(embeddings_dir: str, handle: str):
    paths_file = Path(embeddings_dir) / f"{handle}_image_paths.txt"
    return paths_file.read_text().strip().split("\n")

# main
if __name__ == "__main__":
    client = anthropic.Anthropic()

    # load image paths
    image_paths = load_image_paths("data/embeddings", "jessica")
    print(f"extracting palette from {len(image_paths)} images...")

    # extract palette
    hex_codes = extract_palette(image_paths)
    print(f"dominant colors: {hex_codes}")

    # load archetypes from cluster labels
    with open("data/profiles/cluster_labels.json") as f:
        cluster_data = json.load(f)

    archetypes = [v["archetype"] for v in cluster_data["labels"].values()]

    # get mood description
    palette_data = describe_palette(hex_codes, archetypes, client)
    print(f"palette mood: {palette_data['palette_mood']}")
    print(f"palette name: {palette_data['palette_name']}")

    # save 
    output = {
        "hex_codes": hex_codes,
        "palette_mood": palette_data["palette_mood"],
        "palette_name": palette_data["palette_name"]
    }

    output_path = Path("data/profiles/palette.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nsaved palette to {output_path}")