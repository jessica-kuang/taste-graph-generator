import json
from pathlib import Path

# load brand catalog
def load_catalog(catalog_path: str):
    with open(catalog_path) as f:
        data = json.load(f)
    return data["brands"]

# load taste profile
def load_taste_signals(cluster_labels_path: str):
    with open(cluster_labels_path) as f:
        cluster_data = json.load(f)

    archetypes = []
    motifs = []

    for label in cluster_data["labels"].values():
        archetypes.append(label["archetype"].lower())
        motifs.extend([m.lower() for m in label["motifs"]])

    return archetypes, motifs

# score a single brand
def score_brand(brand, archetypes, motifs):
    score = 0
    for tag in brand.get("aesthetic_tags", []):
        if any(tag.lower() in arch or arch in tag.lower() for arch in archetypes):
            score += 2

    for tag in brand.get("motif_tags", []):
        if any(tag.lower() in motif or motif in tag.lower() for motif in motifs):
            score += 1

    return score

# match brands
def match_brands(brands, archetypes, motifs, top_n: int = 2):
    scored = []
    for brand in brands:
        s = score_brand(brand, archetypes, motifs)
        scored.append({**brand, "score": s})
    
    # group by category
    categories = {}
    for brand in scored:
        cat = brand["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(brand)

    # sort each category and take top n
    results = {}
    for cat, cat_brands in categories.items():
        sorted_brands = sorted(cat_brands, key=lambda x: x["score"], reverse=True)
        results[cat] = sorted_brands[:top_n]
    
    return results

# display results
def display_matches(matches):
    print(f"\n--- brand recs---")
    for category, brands in matches.items():
        print(f"n\{category.upper()}")
        for brand in brands:
            print(f"   {brand['name']} (score: {brand['score']})")
            print(f"   {brand['description']}")
            print(f"   {brand['url']}")


def save_matches(matches, output_path: str):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(matches, f, indent=2)
    print(f"saved brand matches to {output_path}")

# main
if __name__ == "__main__":
    brands = load_catalog("brands/brand_catalog.json")
    archetypes, motifs = load_taste_signals("data/profiles/cluster_labels.json")

    print(f"archetypes: {archetypes}")
    print(f"motifs: {motifs[:5]}...")

    matches = match_brands(brands, archetypes, motifs)
    display_matches(matches)
    save_matches(matches, "data/profiles/brand_matches.json")