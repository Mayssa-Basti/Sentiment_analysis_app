def generate_support_reply(user_text: str, lang="FR") -> str:
    txt = user_text.lower()

    if lang == "FR":
        if any(w in txt for w in ["triste", "mal", "vide", "seul", "pleurer"]):
            return (
                "Je suis désolé que tu traverses ça. "
                "Ce que tu ressens est important. "
                "Si tu veux, tu peux me dire ce qui t'a le plus pesé aujourd'hui, "
                "et on peut essayer de le démêler ensemble, étape par étape."
            )

        if any(w in txt for w in ["stress", "pression", "angoisse", "anxieux", "débordé"]):
            return (
                "Ça ressemble à une vraie surcharge émotionnelle. "
                "Dis-moi ce qui te stresse le plus en ce moment : "
                "les études, la famille, le travail, ou autre chose ?"
            )

        if any(w in txt for w in ["heureux", "bien", "content", "motivé"]):
            return (
                "C'est agréable à entendre 🌷 "
                "Qu'est-ce qui t'a aidé à te sentir comme ça aujourd'hui ?"
            )

        return (
            "Je suis là pour discuter avec toi. "
            "Tu peux me parler librement de ce que tu ressens, "
            "de ta journée ou de ce qui te pèse."
        )

    else:
        if any(w in txt for w in ["sad", "bad", "empty", "alone", "cry"]):
            return (
                "I'm sorry you're going through this. "
                "What you're feeling matters. "
                "If you want, tell me what felt heaviest today, "
                "and we can unpack it together step by step."
            )

        if any(w in txt for w in ["stress", "anxious", "pressure", "overwhelmed"]):
            return (
                "That sounds like real emotional overload. "
                "Tell me what is stressing you most right now: "
                "studies, family, work, or something else?"
            )

        if any(w in txt for w in ["happy", "good", "motivated", "great"]):
            return (
                "That's nice to hear 🌷 "
                "What helped you feel that way today?"
            )

        return (
            "I'm here to talk with you. "
            "You can speak freely about how you feel, "
            "your day, or whatever is on your mind."
        )