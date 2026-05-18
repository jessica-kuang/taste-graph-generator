import json
import numpy as np
import feedparser
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# load model
def load_model():
    print("loading sentence transformer...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model

# fetch articles from rss
def fetch_articles(seed_path: str):
    with open(seed_path) as f:
        seed_data = json.load(f)

    articles = []
    for pub in seed_data["publications"]:
        print(f"fetching {pub['name']}...")
        try:
            feed = feedparser.parse(pub["url"])
            for entry in feed.entries[:5]:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                link = entry.get("link", "")
                published = entry.get("published", "")

                # cleaned summary - strip html tags roughly
                import re
                summary_clean = re.sub(r'<[^>]+>', '', summary)[:500]

                if title and summary_clean:
                    articles.append({
                        "title": title,
                        "summary": summary_clean,
                        "link": link,
                        "published": published,
                        "publication": pub["name"],
                        "text": f"{title}. {summary_clean}"
                    })
        except Exception as e:
            print(f"error fetching {pub['name']}: {e}")
    print(f"fetched {len(articles)} articles total")
    return articles
# load taste profile keywords
def load_profile_keywords(cluster_labels_path: str, palette_path: str):
    with open(cluster_labels_path) as f:
        cluster_data = json.load(f)
    
    with open(palette_path) as f:
        palette_data = json.load(f)

    # extract all meaningful keywords from taste profile
    keywords = []
    
    for label in cluster_data["labels"].values():
        keywords.append(label["archetype"])
        keywords.extend(label["motifs"])
        keywords.append(label["mood"])

    keywords.append(palette_data["palette_mood"])
    keywords.append(palette_data["palette_name"])

    # combine into one profile string
    profile_text = " ".join(keywords)
    print(f"profile keywords: {profile_text[:200]}...")
    return profile_text

# score articles
def score_articles(articles, profile_text, model):
    # embed all article texts
    article_texts = [a["text"] for a in articles]
    article_embeddings = model.encode(article_texts, show_progress_bar=True)
    # embed profile
    profile_embedding = model.encode([profile_text])
    # cosine similarity
    scores = cosine_similarity(profile_embedding, article_embeddings)[0]
    # attach scores to articles
    for i, article in enumerate(articles):
        article["score"] = float(scores[i])

    return articles

# select top articles
def select_top_articles(articles, n=3):
    sorted_articles = sorted(articles, key=lambda x: x["score"], reverse=True)
    top = sorted_articles[:n]

    print(f"\n--- top {n} curated reads ---")
    for i, article in enumerate(top):
        print(f"{i+1}. [{article['publication']}] {article['title']}")
        print(f"   score: {article['score']:.3f}")
        print(f"   {article['link']}")

    return top

# save results
def save_curated_reads(articles, output_path: str):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(articles, f, indent=2)
    print(f"saved {output_path}")

# main
if __name__ == "__main__":
    model = load_model()
    articles = fetch_articles("substack/seed_publications.json")
    profile_text = load_profile_keywords(
        "data/profiles/cluster_labels.json",
        "data/profiles/palette.json"
    )

    scored = score_articles(articles, profile_text, model)
    top_articles = select_top_articles(scored, n=3)
    save_curated_reads(top_articles, "data/profiles/curated_reads.json")