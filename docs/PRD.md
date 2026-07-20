# Taste Graph Generator
### Product Requirements Document
**Author:** Jessica Kuang
**Version:** 2.0, Graph MVP
**Last Updated:** July 2026
**Status:** MVP Complete

---

## 1. Executive Summary

Taste Graph Generator is a personalized aesthetic identity platform that uses a user's own image data to generate an interactive taste graph: a bounded, explorable network of archetypes, motifs, brands, curated reads, and color palette, all connected by edges that explain why each element belongs in the user's world. Unlike social media platforms that harvest user data to serve algorithmic feeds, Taste Graph Generator returns that data directly to the user as a coherent, navigable reflection of who they are.

The product sits at the intersection of two converging trends: Gen Z's growing fatigue with opaque, exploitative social platforms, and a renewed appetite for analog feeling, intentional media. It is not a feed. It is not an app you scroll. It is a creative third space, a personalized graph that feels like it was made by a very chic, very attentive close friend who actually looked at your photos.

---

## 2. Problem Statement

Social media promised self-discovery. It delivered surveillance.

Platforms like Instagram and TikTok built their value propositions on personalization, the idea that the more you engaged, the more the feed would reflect you. But the incentive structure was never about the user. It was about attention retention and ad revenue. The result is a 2026 landscape where:

- **67% of Gen Z view Instagram and Facebook as "data exploitative,"** contributing to declining engagement
- **83% of Gen Z adults have taken steps to limit their social media use,** with 82% associating social media with the word "addicting"
- **55% have taken at least one social media detox** in the past year to manage anxiety and digital fatigue
- The organic, user-generated feeds of 2012 to 2016 have been replaced by algorithmically promoted brand content, sponsored posts, and increasingly, AI-generated slop

What's been lost in this shift is the *self-discovery* function that early social media genuinely served: the sense that a platform was helping you figure out who you are and what you like, rather than just keeping you scrolling. That function has scattered across a dozen apps, each siloed, each requiring weeks of engagement before any meaningful personalization kicks in, none of them talking to each other.

Meanwhile, a user's taste identity, their aesthetic preferences, their intellectual interests, is being reconstructed, incompletely and without consent, in server rooms they'll never see.

The insight is not that Gen Z doesn't want personalization. They do. **81% are concerned about data privacy yet 88% willingly share personal information for personalized experiences.** They're pragmatists who understand the trade-off. What they want is transparency: to know what's being used, why, and to get something genuinely valuable in return.

Taste Graph Generator is built on that insight. And it makes a further argument: that AI, used well, doesn't have to be part of the problem. The same technology that powers algorithmic feeds and synthetic slop can be redirected, put in service of the user rather than in extraction from them. This is not AI replacing human taste. It is AI reflecting it back.

---

## 3. Target User

**Primary:** Gen Z users (18 to 28) with an active aesthetic identity, people who save things, pin things, curate mood boards, and think about what their taste says about them. They are comfortable with technology learning their preferences; they are not comfortable with that learning happening invisibly.

**Secondary:** Older Millennials (28 to 35) who remember blogging, Tumblr, and early Pinterest, users with a nostalgic relationship to analog feeling media and a personal history of taste curation online.

**Psychographic profile, the core user:**
- Thinks about aesthetics intentionally (Kibbe body types, color theory, capsule wardrobes)
- Uses multiple platforms for inspiration but finds none of them feel wholly *them*
- Has a sense that they're in a particular chapter of their life and wants media that reflects that
- Craves the "told a close friend all your preferences and they actually listened" feeling
- Is skeptical of platforms but not of technology itself, wants transparency, not abstraction

**They are not:**
- Passive consumers who want to be told what's trending
- Users who want infinite scroll
- People who are uncomfortable with AI understanding their preferences

---

## 4. Product Vision

A living taste graph, an interactive space that makes your aesthetic identity visible, explorable, and generative. Not a magazine you receive and put down. A world you navigate, play with, and return to as you change.

Your taste profile doesn't live in a document. It lives in a graph: nodes representing your archetypes, motifs, brands, curated reads, and palette, connected by edges that show exactly why each element belongs in your world. You don't read it. You explore it.

Each monthly refresh updates the graph with new data: new Substack articles matched to your current profile, new brand discoveries, updated aesthetic clusters as your uploaded images evolve. The graph shows you not just who you are but who you're becoming.

The product has two layers:

**The mirror**, your taste graph as it stands today. Accurate, transparent, yours. Every node is explainable. Every edge shows its reasoning.

**The playground** (V2), drag nodes together to discover emergent aesthetics. Move "dreamy ethereal" closer to a brand and watch a new cluster form. The graph becomes a creative collaborator, not just a reflection.

The tagline: **"Like telling a close friend all your preferences, and they actually listened."**

---

## 5. Product Philosophy

There is a widespread and legitimate fear that AI will eliminate human creativity, that generative models will flood culture with synthetic content until authentic human expression becomes indistinguishable from or crowded out by machine output. This product is a direct response to that fear, and a counter argument made in code.

Taste Graph Generator is not AI generating culture. It is AI in service of human culture.

You are the creative director of your own graph. The AI is the production studio that makes it real.

Your images and your current chapter are the creative inputs. The AI does the labor of synthesis: clustering your aesthetic, extracting your palette, finding the Substack writers you'd love if you knew they existed, generating the descriptions that tie it all together. The AI has no taste of its own here. It only reflects and amplifies yours. Without you, there is nothing to make.

Think about how a great editor actually works. They don't invent the writer's voice or the photographer's eye. They curate, arrange, and present. The creative vision belongs to the humans involved. The editorial infrastructure serves it. This product works the same way: you bring the vision, AI handles the production work.

The Substack curation layer makes this concrete. The AI is not writing the articles surfaced in your graph. It is finding human writers whose work resonates with your taste profile and connecting you to them. This is AI as a conduit, connecting humans to the writers, brands, and aesthetics that reflect them, not AI as a replacement for human creativity.

This is what co-creation with AI should look like: the human authors the soul, the AI builds the connective tissue. The output is more human for having used it, not less.

**This product is a statement: AI is most powerful not when it replaces human creativity, but when it creates the conditions for humans to discover, express, and connect around their own.**

---

## 6. Goals and Non-Goals

### Goals (MVP, shipped)
- Allow users to upload images to build their taste profile
- Infer aesthetic archetypes and recurring motifs from uploaded images via CLIP embedding and k-means clustering, labeled with Claude Vision
- Extract and name a dominant color palette from the image set
- Curate 3 Substack articles per profile, matched semantically to the user's aesthetic
- Recommend brands from a curated catalog, matched to inferred archetypes
- Generate an interactive taste graph as the primary output, nodes for archetypes, motifs, brands, curated reads, and palette, with edges showing why each connection exists
- Allow users to click any node to inspect it and understand why it's in their world
- Serve the graph locally via Flask with a D3.js force directed layout

### Goals (near term, not yet shipped)
- Onboarding questionnaire capturing current chapter, style direction, and content interests to enrich node generation beyond image data alone
- Monthly refresh flow that re-runs clustering on newly added images and re-curates articles and brands

### Non-Goals (MVP)
- Pinterest API integration (manual image upload only, Pinterest is V2)
- Spotify integration and music mood layer (V2)
- Drag-to-explore emergent cluster generation (V2)
- Brand marketplace or paid promotions
- Data monetization layer
- Multi-user or social features
- Mobile app
- Static zine or PDF output (deprioritized in favor of the interactive graph, see Section 7)

---

## 7. User Research

### Desk Research

The market context strongly validates the core problem:

Gen Z's relationship with social media in 2026 is defined by what researchers call "the tension between engagement and exhaustion." They use these platforms because they're infrastructure: discovery, commerce, community, but they increasingly resent the terms. The defining dynamic is not abandonment but ambivalence.

The authenticity crisis is the most relevant signal. Gen Z's skepticism is not a rejection of AI or personalization, it is specifically a rejection of *synthetic authenticity*: AI used to simulate human connection in a space where genuine human creativity and vulnerability are the primary currency of trust. This is the precise gap the taste graph occupies. It uses AI not to simulate a human voice, but to do the curatorial work that surfaces a real human voice, yours, and presents it back to you.

Perhaps most directly relevant: research indicates Gen Z is actively migrating toward Substack and Reddit, and craving IRL and "third space" experiences, bounded, intentional spaces that aren't social media feeds. The taste graph is a digital instantiation of exactly that desire.

### Primary Research and the Zine to Graph Pivot

Early prototypes of this product were built around a static zine layout: a generated magazine with sections for style, beauty, a feature article, and a listening companion, exportable as a PDF. User interviews conducted during that phase surfaced a key finding: users wanted low effort discovery and spontaneity more than a finished, linear document. A magazine is something you read once and put down. It didn't match how this audience actually behaves with taste, which is exploratory, associative, and a little bit obsessive.

That research led directly to the interactive graph as the primary output. Instead of a document with fixed sections, the taste profile became a network you click through and drag around, with every node explainable and no fixed reading order. The zine format and its PDF export are retained as a non-goal for the MVP rather than removed from the roadmap entirely, since a shareable static artifact may still have value once the graph experience is validated.

Further interviews (5 to 7 users, ages 18 to 26, fitting the psychographic profile in Section 3) are planned to validate the graph format directly: response to the interaction model, willingness to connect additional accounts (Spotify, Pinterest) for richer input, and reactions to the transparency layer. *Findings to be incorporated in v2.1 of this document.*

---

## 8. User Stories

**As a user, I want to:**
- Upload images from my camera roll or Pinterest boards so the system can understand my visual aesthetic
- See my taste profile clearly: what archetypes were inferred, what my palette looks like, what's being used to find Substack articles and brands for me
- Explore my taste graph by clicking and dragging nodes to see how everything connects
- Understand why each node is in my graph without being told
- Generate an updated graph as I add new images, and see how my taste has shifted
- Understand what data was used and how, at every step

---

## 9. Functional Requirements

### 9.1 Taste Profiling
- Image upload (20 to 50 images recommended)
- CLIP embedding pipeline runs on uploaded images
- K-means clustering identifies aesthetic archetypes and recurring motifs
- Claude Vision labels each cluster with aesthetic language
- Color palette extracted from the full image set and given a name
- Taste profile assembled from clusters, palette, and matched content

### 9.2 Content Curation
- Substack RSS feeds pulled from seed publication list
- Articles embedded via sentence-transformers and scored against the taste profile via cosine similarity
- Top 3 articles selected per profile
- Brand recommendations matched from curated catalog against aesthetic archetypes

### 9.3 Content Generation
- LLM (Claude) takes the assembled taste profile and generates:
  - A description for each archetype node, specific and observed, not categorical
  - A description for each brand node explaining why it belongs in the user's world
  - A description for each curated read explaining its relevance
  - A short feature reflecting the user's aesthetic world as a whole

### 9.4 Graph Rendering and Output
- D3.js force directed graph renders the taste profile as an interactive network
- Node types: palette (anchor), archetypes, motifs, brands, curated reads
- Edges connect nodes to the archetype or palette they stem from
- Click any node to open an inspect panel with its label and description
- Drag nodes to explore spatial relationships
- Served locally via Flask at localhost:5000

### 9.5 Transparency Layer
- Every edge in the graph is an explanation, the connection reasoning is visible on inspection
- Taste profile data is stored locally as JSON and never leaves the user's machine
- Clear distinction between inferred data (archetypes, palette) and curated data (brands, reads)

---

## 10. Technical Architecture

```
[Input Layer]
  Image upload to data/uploads/
        v
[Taste Profiling Engine]
  embedder.py: CLIP embeddings (ViT-B/32)
  profiler.py: k-means clustering, Claude Vision labeling
  palette.py: k-means on pixel RGB values, palette naming
  Output: taste profile artifacts (JSON)
        v
[Content Curation Layer]
  substack.py: RSS via feedparser, sentence-transformer embeddings,
  cosine similarity against cluster labels, top 3 articles selected
  brands.py: semantic tag matching against brand_catalog.json
        v
[Generation Layer]
  generator.py: Claude API generates node descriptions and feature text
  from the full taste profile
        v
[Rendering Layer]
  app.py: Flask serves templates/graph.html
  graph.html: D3.js force directed graph, fetches /api/profile
        v
[Output]
  Interactive graph at localhost:5000
  Taste profile visible as JSON in data/profiles/
```

**Core tech stack:** Python 3.11, CLIP (ViT-B/32), scikit-learn, sentence-transformers (all-MiniLM-L6-v2), Pydantic v2, Anthropic API (Claude), feedparser, D3.js, Flask

---

## 11. Success Metrics

### Quantitative (post-launch)
- Monthly active return rate (do users come back after refreshing their graph?)
- Node interaction depth per session (how many nodes do users explore?)
- Substack article click-through rate (are curated reads actually resonating?)
- Session length (are users spending time exploring or bouncing?)

### Qualitative (MVP)
- User recognizes their archetypes immediately
- User discovers a brand or article they genuinely didn't know but feel is "them"
- User understands why each node is in their graph without being told
- User feels the graph reflects a current, specific version of themselves, not a generic aesthetic category
- User wants to come back next month to see what changed

### The north star feeling:
*"Wow, that's so me."*

### Open retention questions (unresolved)
- What triggers a user to refresh their graph: time based (monthly) or event based (you've added new images)?
- How do we communicate that the graph has refreshed without it feeling like a notification?
- Does the graph showing *change over time*, a ghost of last month's nodes, create the emotional pull to return?
- At what point does a user feel enough ownership of their graph to share it?

---

## 12. Privacy and Data Principles

These are non-negotiable and baked into the architecture, not bolted on afterward:

1. **Local by default.** The taste profile lives on the user's machine. No central database of aesthetic identities.
2. **Explicit over implicit.** Every piece of data used is visible to the user. Nothing happens in the background without disclosure.
3. **Stated vs. inferred.** The product clearly distinguishes between what the user told it and what it figured out. Users can correct inferences.
4. **Portability.** The taste profile is always exportable as a clean JSON. The user can take it, delete it, or build on it.
5. **No ads without consent.** Brand recommendations are editorially framed, clearly labeled, and only present if the user opts in.

---

## 13. Future Roadmap

**V2, Spontaneous discovery**
Web search integration so the system surfaces brands and publications the user has never heard of, matched semantically to their taste profile.

**V2, Generative exploration**
Drag-to-explore: move nodes closer together to generate emergent aesthetic clusters. "What if" branches to save alternative taste directions without overwriting the core profile. Ghost nodes showing last month's positions to visualize how taste has shifted.

**V2, Spotify integration**
Connect listening history to enrich a music mood layer of the taste profile. Pinterest API to pull pins directly from boards instead of manual upload.

**V3, Hosted and shareable**
Each user gets a URL. Share your taste graph or keep it private. "Similar taste" discovery, opt-in and anonymized.

**V4, Data ownership marketplace**
User-controlled taste profile licensing. Brands pay to be considered, users choose. Collective anonymized taste pools with revenue sharing. Full transparency dashboard showing what a profile is worth.

---

## 14. Open Questions

- What's the right cadence for graph refresh? (Weekly? Monthly? On-demand, triggered by new uploads?)
- How do we handle users whose taste profile is genuinely eclectic with no coherent clusters?
- Should there be a short onboarding questionnaire, or should the graph be inferred from images alone?
- How do we make the transparency layer feel empowering rather than overwhelming?
- At what point does local-first architecture become a barrier to sharing and social features?
- Is there still a place for a static, shareable artifact (zine or PDF export) once the graph experience is validated?
