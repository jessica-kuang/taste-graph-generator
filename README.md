# Taste Graph Generator
### A personalized taste graph powered by your own data

---

Social media promised self-discovery. It delivered surveillance.

The Edit is a generative AI application that infers your visual aesthetic identity from images you actually love — Pinterest saves, photos, mood boards — and renders it as an interactive taste graph you can explore. Curated Substack articles, brand recommendations, and aesthetic archetypes surface as nodes connected by edges that show exactly why they belong in your world.

This is not a feed. It is not infinite scroll. It is a bounded, intentional space that reflects who you are and who you're becoming — refreshed monthly as you change.

**You are the creative director. The AI is the production studio.**

---

## What it does

Upload 20–50 images that feel like you. The pipeline does the rest:

- Infers your aesthetic archetypes from visual patterns across your images
- Extracts your dominant color palette and gives it a name
- Curates Substack articles semantically matched to your taste profile
- Recommends brands aligned to your aesthetic world
- Generates personalized descriptions for every node — specific and observed, not categorical
- Renders everything as an interactive D3.js force-directed graph served via Flask

Click any node to understand why it's in your world. Drag nodes to explore spatial relationships. Come back next month to see how you've changed.

---

## The pipeline

```
data/uploads/          ← your images go here
      ↓
embedder.py            ← CLIP encodes images as 512-dim vectors
      ↓
profiler.py            ← k-means clusters vectors, Claude Vision labels each cluster
      ↓
palette.py             ← k-means on pixels extracts your dominant color palette
      ↓
substack.py            ← RSS fetch → sentence-transformer embeddings → cosine similarity → top 3 articles
      ↓
brands.py              ← semantic tag matching against curated brand catalog
      ↓
generator.py           ← Claude generates personalized node descriptions from full taste profile
      ↓
app.py                 ← Flask serves the interactive D3 graph at localhost:5000
```

---

## Tech stack

| Layer | Tools |
|---|---|
| Image embeddings | CLIP (ViT-B/32) via HuggingFace |
| Aesthetic clustering | k-means, scikit-learn |
| Vision labeling | Claude claude-sonnet-4-20250514 (Anthropic API) |
| Color extraction | k-means on pixel RGB values |
| Text embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Content generation | Claude claude-sonnet-4-20250514 (Anthropic API) |
| Graph visualization | D3.js (force-directed) |
| Web framework | Flask |
| Data validation | Pydantic v2 |
| RSS parsing | feedparser |

---

## Setup

**Requirements:** Python 3.11, conda (Miniforge recommended for Apple Silicon)

```bash
# clone the repo
git clone https://github.com/jessica-kuang/zine-generator.git
cd zine-generator

# create environment
conda create -n zine-env python=3.11
conda activate zine-env

# install dependencies
pip install -r requirements.txt

# install CLIP
pip install git+https://github.com/openai/CLIP.git
```

**Add your images** to `data/uploads/` — aim for 20–50 images that feel like you. Screenshots, saved photos, Pinterest exports, anything.

**Add Substack publications** you love to `substack/seed_publications.json`:
```json
{
  "publications": [
    {"name": "Publication Name", "url": "https://handle.substack.com/feed"}
  ]
}
```

---

## Running the pipeline

Run each module in order:

```bash
python src/embedder.py      # embed your images
python src/profiler.py      # cluster and label your aesthetic
python src/palette.py       # extract your color palette
python src/substack.py      # curate articles
python src/brands.py        # match brands
python src/generator.py     # generate node content
python app.py               # launch the graph at localhost:5000
```

---

## Product thinking

This project came with a full product process — not just code.

A PRD lives in `docs/PRD.md` covering problem framing, target user, product philosophy, functional requirements, success metrics, and roadmap. User interviews informed a key pivot: early prototypes used a static zine layout, but research surfaced that users wanted low-effort discovery and spontaneity — leading to the interactive graph as the primary output.

The philosophy behind the product:

> *"AI is most powerful not when it replaces human creativity, but when it creates the conditions for humans to discover, express, and connect around their own."*

The AI here is a conduit — connecting you to writers, brands, and aesthetics that reflect you. Your images, your taste, your data. The graph just makes it visible.

---

## Roadmap

**V2 — Spontaneous discovery**
Web search integration so the system surfaces brands and publications you've never heard of, matched semantically to your taste profile. True serendipity grounded in who you are.

**V2 — Generative exploration**
Drag nodes together to generate emergent aesthetic clusters. Move "dreamy ethereal" closer to a brand and watch new recommendations form. The graph becomes a creative collaborator.

**V2 — Spotify integration**
Connect your listening history to enrich the music mood layer of your taste profile.

**V3 — Hosted and shareable**
Each user gets a URL. Share your taste graph or keep it private.

**V4 — Data ownership marketplace**
User-controlled taste profile licensing. Brands pay to be considered. You choose what to share and get compensated for it.

---

## Project structure

```
zine-generator/
├── src/
│   ├── schema.py          # Pydantic taste profile model
│   ├── embedder.py        # CLIP image embedding pipeline
│   ├── profiler.py        # aesthetic clustering + Claude Vision labeling
│   ├── palette.py         # color palette extraction
│   ├── substack.py        # RSS curation with semantic matching
│   ├── brands.py          # brand recommendation matching
│   └── generator.py       # LLM node content generation
├── templates/
│   └── graph.html         # D3.js interactive graph
├── brands/
│   └── brand_catalog.json # curated brand database
├── substack/
│   └── seed_publications.json
├── data/
│   ├── uploads/           # your input images
│   ├── embeddings/        # saved CLIP vectors
│   └── profiles/          # generated taste profile JSON files
├── docs/
│   └── PRD.md             # full product requirements document
└── app.py                 # Flask web application
```

---

*Built by Jessica Kuang · 2026*
