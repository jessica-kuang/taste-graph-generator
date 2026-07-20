import json
import re
import numpy as np
import anthropic
import feedparser
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# load model
def load_model():
    print("loading sentence transformer...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model

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

# search the web for real Substack publications matching this taste profile
def discover_publications(profile_text: str, client: anthropic.Anthropic, max_attempts: int = 3) -> list:
    prompt = f"""Someone's aesthetic and intellectual taste profile, inferred from
their own images:

{profile_text}

Search the web to find 5-6 real, currently active Substack publications this
person would genuinely love reading, ones they likely haven't heard of, not
the most obvious mainstream picks. Verify each publication is real and still
publishing."""

    tools = [{"type": "web_search_20260209", "name": "web_search", "max_uses": 8}]
    # output_config.format guarantees valid JSON at the token level, unlike
    # asking nicely in the prompt (which broke on both an unescaped quote and,
    # separately, a stray control character mid-word)
    output_config = {
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "publications": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "url": {"type": "string"},
                            },
                            "required": ["name", "url"],
                            "additionalProperties": False,
                        },
                    }
                },
                "required": ["publications"],
                "additionalProperties": False,
            },
        }
    }

    for attempt in range(max_attempts):
        messages = [{"role": "user", "content": prompt}]
        response = client.messages.create(
            model="claude-sonnet-5", max_tokens=3000, tools=tools, output_config=output_config, messages=messages
        )
        while response.stop_reason == "pause_turn":
            # server-side search hit its per-turn iteration cap before finishing;
            # resend to let it continue where it left off
            messages = [{"role": "user", "content": prompt}, {"role": "assistant", "content": response.content}]
            response = client.messages.create(
                model="claude-sonnet-5", max_tokens=3000, tools=tools, output_config=output_config, messages=messages
            )

        text_blocks = [b.text for b in response.content if b.type == "text"]
        if not text_blocks:
            raise RuntimeError(f"no text in response, stop_reason={response.stop_reason}")
        result = json.loads(text_blocks[-1])

        if not _has_control_chars(result):
            return result["publications"]
        print(f"discovery attempt {attempt + 1} had a stray control character, retrying...")

    raise RuntimeError(f"discover_publications produced control characters after {max_attempts} attempts")

# fetch articles from rss
def fetch_articles(publications: list):
    articles = []
    for pub in publications:
        feed_url = pub["url"].rstrip("/") + "/feed"
        print(f"fetching {pub['name']}...")
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                link = entry.get("link", "")
                published = entry.get("published", "")

                # cleaned summary - strip html tags roughly
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
    client = anthropic.Anthropic()
    model = load_model()

    profile_text = load_profile_keywords(
        "data/profiles/cluster_labels.json",
        "data/profiles/palette.json"
    )

    articles = []
    for attempt in range(3):
        print("discovering substack publications...")
        publications = discover_publications(profile_text, client)
        print(f"discovered: {[p['name'] for p in publications]}")

        articles = fetch_articles(publications)
        if articles:
            break
        print(f"attempt {attempt + 1}: every discovered publication's feed was empty, retrying discovery...")

    if not articles:
        raise RuntimeError("no articles fetched after 3 discovery attempts, all feeds came back empty")

    scored = score_articles(articles, profile_text, model)
    top_articles = select_top_articles(scored, n=3)
    save_curated_reads(top_articles, "data/profiles/curated_reads.json")
