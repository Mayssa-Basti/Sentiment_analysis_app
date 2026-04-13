import joblib
import re

VECTOR_PATH = "models/vectorizer.joblib"
SENTIMENT_PATH = "models/sentiment_model.joblib"
EMOTION_PATH = "models/emotion_model.joblib"

vectorizer = joblib.load(VECTOR_PATH)
sentiment_model = joblib.load(SENTIMENT_PATH)
emotion_model = joblib.load(EMOTION_PATH)

POSITIVE_WORDS = {
    "happy", "good", "great", "love", "joy", "peace", "better", "calm",
    "heureux", "heureuse", "bien", "super", "joie", "paix", "motivé",
    "motivée", "reconnaissant", "reconnaissante", "content", "contente",
    "sourire", "magnifique", "merveilleux", "merveilleuse", "excellent"
}

NEGATIVE_WORDS = {
    "sad", "bad", "angry", "terrible", "cry", "hate", "empty", "alone",
    "triste", "mal", "colère", "pleurer", "vide", "seul", "fatigué",
    "déprimé", "déprimée", "anxieux", "anxieuse", "peur", "stress"
}

INTENSIFIERS = {
    "so", "very", "really", "extremely", "too", "super",
    "tres", "très", "vraiment", "tellement", "trop", "fort"
}

POSITIVE_PHRASES = [
    "je suis heureux", "je suis heureuse", "je me sens bien",
    "je suis content", "je suis contente", "je suis motivé",
    "je suis motivée", "je suis reconnaissant", "je suis reconnaissante",
    "i am happy", "i feel good", "i am great", "i feel amazing",
    "i am excited", "i am proud", "i feel calm", "i feel peaceful"
]

SADNESS_WORDS = [
    "sad", "triste", "mal", "terrible", "down", "depressed",
    "bad day", "pas bien", "alone", "cry", "pleure",
    "didn't have a good day", "je me sens mal", "empty", "vide"
]

STRESS_WORDS = [
    "stressed", "stress", "anxious", "angoisse", "panic",
    "nervous", "overwhelmed", "pression", "débordé"
]

ANGER_WORDS = [
    "angry", "furious", "hate", "mad", "frustrated",
    "colère", "énervé", "déteste", "rage"
]

FEAR_WORDS = [
    "fear", "scared", "afraid", "panic", "unsafe",
    "peur", "anxieux", "panique", "danger"
]

def clean_text(text):
    return str(text).strip().lower()

def word_count(text):
    return len(re.findall(r"\b\w+\b", text))

def uppercase_ratio(text):
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    uppers = [c for c in letters if c.isupper()]
    return len(uppers) / len(letters)

def count_matches(text, vocab):
    txt = clean_text(text)
    return sum(1 for w in vocab if w in txt)

def compute_metrics(text):
    return {
        "word_count": word_count(text),
        "uppercase_ratio": uppercase_ratio(text),
        "positive_words": count_matches(text, POSITIVE_WORDS),
        "negative_words": count_matches(text, NEGATIVE_WORDS),
        "intensifiers": count_matches(text, INTENSIFIERS),
    }

def normalize_dict(d):
    total = sum(d.values())
    if total == 0:
        return d
    return {k: v / total for k, v in d.items()}

def apply_rules(text, sentiment_probs, emotion_probs):
    txt = clean_text(text)
    intensifier_count = count_matches(txt, INTENSIFIERS)

    # Positive phrases boost
    if any(p in txt for p in POSITIVE_PHRASES):
        sentiment_probs["positive"] = sentiment_probs.get("positive", 0) + 0.5
        emotion_probs["joy"] = emotion_probs.get("joy", 0) + 0.5

    # Positive words boost
    pos_count = count_matches(txt, POSITIVE_WORDS)
    if pos_count > 0:
        sentiment_probs["positive"] = sentiment_probs.get("positive", 0) + (0.15 * pos_count)
        emotion_probs["joy"] = emotion_probs.get("joy", 0) + (0.10 * pos_count)

    # Intensifier boost on positive
    if pos_count > 0 and intensifier_count > 0:
        sentiment_probs["positive"] = sentiment_probs.get("positive", 0) + (0.08 * intensifier_count)

    # Sadness
    if "sad" in txt or "triste" in txt:
        emotion_probs["sadness"] = emotion_probs.get("sadness", 0) + 0.15 + (0.08 * intensifier_count)

    if any(w in txt for w in SADNESS_WORDS):
        emotion_probs["sadness"] = emotion_probs.get("sadness", 0) + 0.25
        sentiment_probs["negative"] = sentiment_probs.get("negative", 0) + 0.22

    if any(w in txt for w in STRESS_WORDS):
        emotion_probs["stress"] = emotion_probs.get("stress", 0) + 0.22
        sentiment_probs["negative"] = sentiment_probs.get("negative", 0) + 0.12

    if any(w in txt for w in ANGER_WORDS):
        emotion_probs["anger"] = emotion_probs.get("anger", 0) + 0.25
        sentiment_probs["negative"] = sentiment_probs.get("negative", 0) + 0.18

    if any(w in txt for w in FEAR_WORDS):
        emotion_probs["fear"] = emotion_probs.get("fear", 0) + 0.25
        sentiment_probs["negative"] = sentiment_probs.get("negative", 0) + 0.18

    if "happy and sad" in txt or "heureux et triste" in txt:
        sentiment_probs["neutral"] = sentiment_probs.get("neutral", 0) + 0.25
        emotion_probs["sadness"] = emotion_probs.get("sadness", 0) + 0.10

    sentiment_probs = normalize_dict(sentiment_probs)
    emotion_probs = normalize_dict(emotion_probs)

    return sentiment_probs, emotion_probs

def predict_sentiment_and_emotion(text):
    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])

    sentiment_classes = sentiment_model.classes_
    sentiment_proba = sentiment_model.predict_proba(vec)[0]
    sentiment_probs = {cls: float(prob) for cls, prob in zip(sentiment_classes, sentiment_proba)}

    emotion_classes = emotion_model.classes_
    emotion_proba = emotion_model.predict_proba(vec)[0]
    emotion_probs = {cls: float(prob) for cls, prob in zip(emotion_classes, emotion_proba)}

    sentiment_probs, emotion_probs = apply_rules(text, sentiment_probs, emotion_probs)

    sentiment = max(sentiment_probs, key=sentiment_probs.get)
    emotion = max(emotion_probs, key=emotion_probs.get)

    wellbeing = round(
        (sentiment_probs.get("positive", 0) * 100)
        - (sentiment_probs.get("negative", 0) * 70)
        + (emotion_probs.get("joy", 0) * 20),
        1
    )
    wellbeing = max(0, min(100, wellbeing))
    metrics = compute_metrics(text)

    return {
        "sentiment": sentiment,
        "emotion": emotion,
        "wellbeing": wellbeing,
        "sentiment_probs": sentiment_probs,
        "emotion_probs": emotion_probs,
        "metrics": metrics
    }