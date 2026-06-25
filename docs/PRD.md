# Zine Generator
### Product Requirements Document
**Author:** Jessica Kuang
**Version:** 1.0 — MVP
**Last Updated:** May 2026
**Status:** In Development

---

## 1. Executive Summary

Zine Generator is a personalized magazine platform that uses a user's own taste data — images, music, and reading habits — to generate a curated, beautifully designed zine delivered as a web experience and downloadable PDF. Unlike social media platforms that harvest user data to serve algorithmic feeds, Zine Generator returns that data directly to the user in the form of a coherent, creative artifact. The user owns their taste profile. They see exactly what's in it. And they get something beautiful back.

The product sits at the intersection of two converging trends: Gen Z's growing fatigue with opaque, exploitative social platforms, and a renewed appetite for analog-feeling, intentional media. It is not a feed. It is not an app you scroll. It is a creative third space — a personalized literary and style magazine that feels like it was made by a very chic, very attentive close friend.

---

## 2. Problem Statement

Social media promised self-discovery. It delivered surveillance.

Platforms like Instagram and TikTok built their value propositions on personalization — the idea that the more you engaged, the more the feed would reflect you. But the incentive structure was never about the user. It was about attention retention and ad revenue. The result is a 2026 landscape where:

- **67% of Gen Z view Instagram and Facebook as "data exploitative,"** contributing to declining engagement
- **83% of Gen Z adults have taken steps to limit their social media use,** with 82% associating social media with the word "addicting"
- **55% have taken at least one social media detox** in the past year to manage anxiety and digital fatigue
- The organic, user-generated feeds of 2012–2016 have been replaced by algorithmically promoted brand content, sponsored posts, and increasingly, AI-generated slop

What's been lost in this shift is the *self-discovery* function that early social media genuinely served — the sense that a platform was helping you figure out who you are and what you like, rather than just keeping you scrolling. That function has scattered across a dozen apps, each siloed, each requiring weeks of engagement before any meaningful personalization kicks in, none of them talking to each other.

Meanwhile, a user's taste identity — their aesthetic preferences, their music, their intellectual interests — is being reconstructed, incompletely and without consent, in server rooms they'll never see.

The insight is not that Gen Z doesn't want personalization. They do. **81% are concerned about data privacy yet 88% willingly share personal information for personalized experiences.** They're pragmatists who understand the trade-off. What they want is transparency — to know what's being used, why, and to get something genuinely valuable in return.

Zine Generator is built on that insight. And it makes a further argument: that AI, used well, doesn't have to be part of the problem. The same technology that powers algorithmic feeds and synthetic slop can be redirected — put in service of the user rather than in extraction from them. This is not AI replacing human taste. It is AI reflecting it back.

---

## 3. Target User

**Primary:** Gen Z users (18–28) with an active aesthetic identity — people who save things, pin things, curate playlists, and think about what their taste says about them. They are comfortable with technology learning their preferences; they are not comfortable with that learning happening invisibly.

**Secondary:** Older Millennials (28–35) who remember blogging, Tumblr, and early Pinterest — users with a nostalgic relationship to analog-feeling media and a personal history of taste curation online.

**Psychographic profile — the core user:**
- Thinks about aesthetics intentionally (Kibbe body types, color theory, capsule wardrobes)
- Uses multiple platforms for inspiration but finds none of them feel wholly *them*
- Has a sense that they're in a particular chapter of their life and wants media that reflects that
- Craves the "told a close friend all your preferences and they actually listened" feeling
- Is skeptical of platforms but not of technology itself — wants transparency, not abstraction

**They are not:**
- Passive consumers who want to be told what's trending
- Users who want infinite scroll
- People who are uncomfortable with AI understanding their preferences

---

## 4. Product Vision

A living taste graph — an interactive space that makes your aesthetic identity visible, explorable, and generative. Not a magazine you receive and put down. A world you navigate, play with, and return to as you change.

Your taste profile doesn't live in a document. It lives in a graph — nodes representing your archetypes, motifs, brands, curated reads, and palette, connected by edges that show exactly why each element belongs in your world. You don't read it. You explore it.

Each monthly issue refreshes the graph with new data — new Substack articles matched to your current profile, new brand discoveries, updated aesthetic clusters as your uploaded images evolve. The graph shows you not just who you are but who you're becoming.

The product has two layers:

**The mirror** — your taste graph as it stands today. Accurate, transparent, yours. Every node is explainable. Every edge shows its reasoning.

**The playground** — drag nodes together to discover emergent aesthetics. Move "dreamy ethereal" closer to "Damson Madder" and watch a new cluster form. The graph becomes a creative collaborator, not just a reflection.

The tagline: **"Like telling a close friend all your preferences — and they actually listened."**

---

## 5. Product Philosophy

There is a widespread and legitimate fear that AI will eliminate human creativity — that generative models will flood culture with synthetic content until authentic human expression becomes indistinguishable from or crowded out by machine output. This product is a direct response to that fear, and a counter-argument made in code.

Zine Generator is not AI generating culture. It is AI in service of human culture.

You are the creative director of your own zine. The AI is the production studio that makes it real.

Your images, your music, your words, your current chapter — these are the creative inputs. The AI does the labor of synthesis: clustering your aesthetic, extracting your palette, finding the Substack writers you'd love if you knew they existed, generating the editorial voice that ties it all together. The AI has no taste of its own here. It only reflects and amplifies yours. Without you, there is nothing to make.

Think about how a great magazine actually works. The editor doesn't invent the writer's voice or the photographer's eye. They curate, arrange, and present. The creative vision belongs to the humans involved. The editorial infrastructure serves it. This product works the same way — you bring the vision, AI handles the production work.

The Substack curation layer makes this concrete. The AI is not writing the articles in your zine. It is finding human writers whose work resonates with your taste profile and surfacing them to you. This is AI as a conduit — connecting humans to the writers, sounds, and aesthetics that reflect them — not AI as a replacement for human creativity.

This is what co-creation with AI should look like: the human authors the soul, the AI builds the connective tissue. The output is more human for having used it, not less.

**This product is a statement: AI is most powerful not when it replaces human creativity, but when it creates the conditions for humans to discover, express, and connect around their own.**

---

## 6. Goals and Non-Goals

### Goals (MVP)
- Allow users to upload images and answer an onboarding questionnaire to build their taste profile
- Connect Spotify to enrich music mood section with real listening data
- Curate 3 Substack articles per issue matched to the user's content interests
- Generate an interactive taste graph as the primary output — nodes for archetypes, motifs, brands, curated reads, and palette, with edges showing why each connection exists
- Allow users to click any node to inspect it and understand why it's in their world
- Refresh the graph monthly with new Substack curation, updated brand recommendations, and evolved aesthetic clusters
- Show users their taste profile clearly — what was inferred, what was stated, what it contains

### Non-Goals (MVP)
- Pinterest API integration (manual image upload only — Pinterest v2)
- Drag-to-explore emergent cluster generation (V2)
- Brand marketplace or paid promotions
- Data monetization layer
- Multi-user or social features
- Mobile app
- Static zine/PDF output (deprioritized in favor of interactive graph)

---

## 6. User Research

### Desk Research

The market context strongly validates the core problem:

Gen Z's relationship with social media in 2026 is defined by what researchers call "the tension between engagement and exhaustion." They use these platforms because they're infrastructure — discovery, commerce, community — but they increasingly resent the terms. The defining dynamic is not abandonment but ambivalence.

The authenticity crisis is the most relevant signal. Gen Z's skepticism is not a rejection of AI or personalization — it is specifically a rejection of *synthetic authenticity*: AI used to simulate human connection in a space where genuine human creativity and vulnerability are the primary currency of trust. This is the precise gap the zine occupies. It uses AI not to simulate a human voice, but to do the curatorial work that surfaces a real human voice — yours — and presents it back to you.

Perhaps most directly relevant: research indicates Gen Z is actively migrating toward Substack and Reddit, and craving IRL and "third space" experiences — bounded, intentional spaces that aren't social media feeds. The zine is a digital instantiation of exactly that desire.

### Primary Research *(to be completed)*

5–7 user interviews planned with Gen Z users (18–26) fitting the psychographic profile above. Interview guide focuses on:
- Current inspiration and self-discovery behaviors across platforms
- Relationship with data privacy and personalization trade-offs
- Response to the zine concept and format
- Willingness to connect platform accounts (Spotify, Pinterest)

*Findings to be incorporated in v1.1 of this document.*

---

## 7. User Stories

**As a user, I want to:**
- Upload images from my camera roll or Pinterest boards so the system can understand my visual aesthetic
- Answer a short onboarding questionnaire about where I am in my life right now, so the zine feels current rather than generic
- Connect my Spotify account so my music taste informs the listening companion section
- See my taste profile clearly — what archetypes were inferred, what my palette looks like, what keywords are being used to find Substack articles for me
- Edit or correct my taste profile if something feels off
- Generate a new issue and receive it as both a web page and a downloadable PDF
- Share my zine (or keep it private)
- Understand what data was used and how, at every step

---

## 8. Functional Requirements

### 8.1 Onboarding & Taste Profiling
- Image upload (20–50 images recommended)
- Short questionnaire: current chapter, style direction, active questions (fashion, beauty), content interests
- CLIP embedding pipeline runs on uploaded images
- K-means clustering identifies aesthetic archetypes
- Claude Vision labels each cluster with aesthetic language
- Color palette extracted from full image set
- Spotify OAuth connects and pulls top artists, genres, listening mood
- Taste profile assembled and displayed to user for review and editing

### 8.2 Content Curation
- Substack RSS feeds pulled from seed publication list
- Articles embedded and scored against taste profile keywords via cosine similarity
- Top 3 articles selected per issue
- Brand recommendations matched from curated catalog against aesthetic archetypes

### 8.3 Content Generation
- LLM (Claude) takes fully populated taste profile and generates:
  - Feature article (trend in user's aesthetic world)
  - Style recommendations (grounded in active questions and style direction)
  - Beauty edit (grounded in makeup language and active questions)
  - Self-reflective quiz (derived from identity tension)
  - Listening companion (grounded in music mood)
- Curated reads section populated from Substack curation step

### 8.4 Graph Rendering & Output
- D3.js force-directed graph renders taste profile as interactive network
- Node types: archetypes (large, dark), motifs (medium), brands (medium), curated reads (medium), palette (anchor node)
- Edge weights reflect strength of connection between nodes
- Click any node → inspect panel surfaces label, description, and why it was included
- Drag nodes to explore spatial relationships
- Web-hosted, shareable via URL
- Monthly refresh updates Substack articles, brand recommendations, and re-runs clustering on any new uploaded images

### 8.5 Transparency Layer
- Every edge in the graph is an explanation — hovering shows the connection reasoning
- Taste profile always visible and exportable as JSON
- Clear distinction between inferred data and stated data
- Node feedback: user can mark a node as "not me" to inform future clustering

---

## 9. Technical Architecture

```
[Input Layer]
  Image upload + onboarding questionnaire + Spotify OAuth
        ↓
[Taste Profiling Engine]
  CLIP embeddings → k-means clustering → Claude Vision labeling
  Color palette extraction (k-means on pixels)
  Spotify API → listening history → music mood
  Output: TasteProfile (Pydantic schema)
        ↓
[Content Curation Layer]
  Substack RSS → feedparser → sentence-transformer embeddings
  Cosine similarity against taste profile keywords → top 3 articles
  Brand catalog matching against aesthetic archetypes
        ↓
[Generation Layer]
  Claude API → generates 5 magazine sections from taste profile
  Curated reads injected from curation layer
        ↓
[Rendering Layer]
  HTML/CSS zine templates + user color palette
  WeasyPrint → PDF
  Web view for in-browser reading
        ↓
[Output]
  Shareable web link + downloadable PDF
  Taste profile visible and editable
```

**Core tech stack:** Python 3.11, PyTorch (MPS), CLIP, sentence-transformers, Pydantic, Anthropic API, Spotify API, feedparser, WeasyPrint, Streamlit

---

## 10. Success Metrics

### Quantitative (post-launch)
- Monthly active return rate (do users come back for issue 2, 3, 4?)
- Node interaction depth per session (how many nodes do users explore?)
- Substack article click-through rate (are curated reads actually resonating?)
- "Not me" feedback rate (are users correcting the graph — a signal of engagement, not failure)
- Session length (are users spending time exploring or bouncing?)

### Qualitative (MVP)
- User recognizes their archetypes immediately
- User discovers a brand or article they genuinely didn't know but feel is "them"
- User understands why each node is in their graph without being told
- User feels the graph reflects a current, specific version of themselves — not a generic aesthetic category
- User wants to come back next month to see what changed

### The north star feeling:
*"Wow, that's so me."*

### Open retention questions *(unresolved)*
- What triggers a user to generate a new issue — time-based (monthly) or event-based (you've added new images)?
- How do we communicate that the graph has refreshed without it feeling like a notification?
- Does the graph showing *change over time* — a ghost of last month's nodes — create the emotional pull to return?
- At what point does a user feel enough ownership of their graph to share it?

---

## 11. Privacy & Data Principles

These are non-negotiable and baked into the architecture, not bolted on afterward:

1. **Local by default.** The taste profile lives on the user's machine. No central database of aesthetic identities.
2. **Explicit over implicit.** Every piece of data used is visible to the user. Nothing happens in the background without disclosure.
3. **Stated vs. inferred.** The product clearly distinguishes between what the user told it and what it figured out. Users can correct inferences.
4. **Portability.** The taste profile is always exportable as a clean JSON. The user can take it, delete it, or build on it.
5. **No ads without consent.** Brand recommendations are editorially framed, clearly labeled, and only present if the user opts in.

---

## 12. Future Roadmap

**V2 — Generative exploration**
- Drag-to-explore: move nodes closer together to generate emergent aesthetic clusters
- "What if" branches — save alternative taste directions without overwriting your core profile
- Ghost nodes showing last month's positions — visualize how your taste has shifted
- Pinterest API (pull pins directly from boards)

**V3 — Social layer**
- Shareable public graph pages
- "Similar taste" discovery (opt-in, anonymized)
- Community reading section featuring independent Substack creators

**V4 — Data ownership marketplace**
- User-controlled taste profile licensing
- Brand pitch marketplace (brands pay to be considered, users choose)
- Collective anonymized taste pools with revenue sharing
- Full transparency dashboard showing what your profile is worth

---

## 13. Open Questions

- What's the right cadence for issue generation? (Weekly? Monthly? On-demand?)
- How do we handle users whose taste profile is genuinely eclectic with no coherent clusters?
- Should the questionnaire be conversational (chat-style) or form-based?
- How do we make the transparency layer feel empowering rather than overwhelming?
- At what point does local-first architecture become a barrier to sharing and social features?