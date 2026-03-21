from pydantic import BaseModel
from typing import List, Optional

# visual components input
class VisualIdentity(BaseModel):
    primary_archetypes: List[str]
    rejected_aesthetics: List[str]
    dominant_palette: List[str]
    palette_mood: str
    recurring_motifs: List[str]
    texture_language: List[str]
    confidence: float

# text input components
class SelfConcept(BaseModel):
    energy: str
    values_signals: List[str]
    current_chapter: str
    identity_tension: Optional[str] = None
    user_prompt: Optional[str] = None

class FashionInterests(BaseModel):
    style_direction: str
    active_questions: List[str]

class BeautyInterests(BaseModel):
    makeup_language: List[str]
    active_questions: List[str]

class CultureInterests(BaseModel):
    topic_affinities: List[str]
    reading_level: str
    substack_keywords: List[str]

class MusicMood(BaseModel):
    descriptors: List[str]
    reference_artists: List[str]

class ContentInterests(BaseModel):
    fashion: FashionInterests
    beauty: BeautyInterests
    culture: CultureInterests
    music: MusicMood

class MagazineVoice(BaseModel):
    tone: str
    persona_name: str
    writing_style: str
    avoids: List[str]

class TasteProfile(BaseModel):
    user_handle: str
    issue_number: int = 1
    visual_identity: VisualIdentity
    self_concept: SelfConcept
    content_interests: ContentInterests
    magazine_voice: MagazineVoice

# check this works!
if __name__ == "__main__":
    test_profile = TasteProfile(
        user_handle="jessica",
        issue_number=1,
        visual_identity=VisualIdentity(
            primary_archetypes=["dark romantic", "quiet luxury"],
            rejected_aesthetics=["maximalist", "streetwear"],
            dominant_palette=["#2C1B18", "#C9B99A", "#F5F0E8"],
            palette_mood="warm, muted, candlelit",
            recurring_motifs=["lace", "tailored silhouettes"],
            texture_language=["soft", "structured", "aged"],
            confidence=0.83
        ),
        self_concept=SelfConcept(
            energy="introspective, intentional",
            values_signals=["elegance", "privacy", "craft"],
            current_chapter="transitioning toward more structure",
            identity_tension="softness vs ambition",
            user_prompt="I want to feel more put together but still romantic"
        ),
        content_interests=ContentInterests(
            fashion=FashionInterests(
                style_direction="feminine tailoring with romantic details",
                active_questions=["how to build a capsule wardrobe"]
            ),
            beauty=BeautyInterests(
                makeup_language=["soft glam", "skin-first"],
                active_questions=["which lip colors suit warm undertones"]
            ),
            culture=CultureInterests(
                topic_affinities=["psychology of aesthetics", "creative identity"],
                reading_level="longform, essayistic",
                substack_keywords=["style", "femininity", "self-development"]
            ),
            music=MusicMood(
                descriptors=["melancholic", "cinematic"],
                reference_artists=["Lana Del Rey", "Sufjan Stevens"]
            )
        ),
        magazine_voice=MagazineVoice(
            tone="like a conversation with a very chic older sister",
            persona_name="the editor",
            writing_style="essayistic, second-person, occasionally poetic",
            avoids=["listicle energy", "hype language", "toxic positivity"]
        )
    )
    print(test_profile.model_dump_json(indent=2))