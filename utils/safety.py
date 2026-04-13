def detect_self_harm(text: str) -> bool:
    txt = text.lower().strip()

    danger_phrases = [
        "i want to die",
        "i want to kill myself",
        "kill myself",
        "end my life",
        "suicide",
        "i don't want to live",
        "je veux mourir",
        "je vais me tuer",
        "me tuer",
        "finir ma vie",
        "je n'en peux plus",
        "je veux en finir",
        "j'ai envie de mourir"
    ]

    return any(p in txt for p in danger_phrases)