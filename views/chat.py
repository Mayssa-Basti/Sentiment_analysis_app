import streamlit as st
from utils.chat_engine import generate_support_reply
from utils.safety import detect_self_harm
from utils.history_manager import save_analysis
from utils.analyzer_engine import predict_sentiment_and_emotion
from utils.translations import t
from datetime import datetime

EMOTION_ICONS = {
    "joy": "😊", "sadness": "😢",
    "anger": "😠", "fear": "😨", "stress": "😰",
}

def get_colors():
    if "theme_colors" not in st.session_state or not st.session_state.theme_colors:
        return {
            "BG": "#f5efe6", "BG2": "#ede4d8", "BG3": "#d9cfc4",
            "BORDER": "#c8b89a", "TEXT": "#2c2010", "TEXT2": "#7a6a55",
            "ACCENT": "#8a6a3a", "CARD": "#faf6f0",
            "BTN_BG": "#8a6a3a", "BTN_TEXT": "#f5efe6"
        }
    return st.session_state.theme_colors

def render():
    lang = st.session_state.get("lang", "FR")
    C = get_colors()

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Header
    st.markdown(f"""
        <div style='padding:28px 40px 20px 40px;
            border-bottom:1px solid {C["BORDER"]};'>
            <div style='font-size:1.2rem; font-weight:600;
                color:{C["TEXT"]};'>{t(lang,"chat_title")}</div>
            <div style='font-size:0.85rem; color:{C["TEXT2"]};
                margin-top:4px;'>{t(lang,"chat_sub")}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<div style='padding:28px 40px 10px 40px;'>",
        unsafe_allow_html=True
    )

    if not st.session_state.chat_messages:
        st.markdown(f"""
            <div style='display:flex; flex-direction:column;
                align-items:center; justify-content:center;
                min-height:340px; text-align:center;'>
                <div style='font-size:2.5rem; margin-bottom:16px;
                    color:{C["ACCENT"]};'>✦</div>
                <div style='font-size:1rem; color:{C["TEXT2"]};
                    line-height:1.7;'>
                    {t(lang,"chat_welcome")}
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f"""
                    <div style='display:flex; justify-content:flex-end;
                        margin-bottom:16px;'>
                        <div style='background:{C["BG3"]};
                            color:{C["TEXT"]};
                            border-radius:18px 18px 4px 18px;
                            padding:12px 18px; max-width:65%;
                            font-size:0.93rem; line-height:1.6;
                            border:1px solid {C["BORDER"]};'>
                            {msg["content"]}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                emotion   = msg.get("emotion", "")
                sentiment = msg.get("sentiment", "")
                wellbeing = msg.get("wellbeing", "")
                ei = EMOTION_ICONS.get(emotion, "✦")

                ec = {
                    "joy":C["ACCENT"],"sadness":"#e07070",
                    "anger":"#e07070","fear":"#a07aba",
                    "stress":"#e09060"
                }.get(emotion, C["TEXT2"])

                sc = {
                    "positive":C["ACCENT"],
                    "negative":"#e07070",
                    "neutral":C["TEXT2"]
                }.get(sentiment, C["TEXT2"])

                badge_html = ""
                if emotion:
                    badge_html = f"""
                        <div style='display:inline-flex;
                            align-items:center; gap:6px;
                            margin-bottom:10px;
                            background:{C["BG"]};
                            border:1px solid {C["BORDER"]};
                            border-radius:20px; padding:4px 12px;
                            font-size:0.72rem; font-weight:600;'>
                            <span style='color:{ec};'>
                                {ei} {emotion.capitalize()}
                            </span>
                            <span style='color:{C["BORDER"]};'>·</span>
                            <span style='color:{sc};'>
                                {sentiment.capitalize()}
                            </span>
                            <span style='color:{C["BORDER"]};'>·</span>
                            <span style='color:{C["TEXT2"]};'>
                                ⚡ {wellbeing}/100
                            </span>
                        </div>
                    """

                reply_text = msg["content"].replace(
                    "<","&lt;"
                ).replace(">","&gt;")

                st.markdown(f"""
                    <div style='display:flex;
                        justify-content:flex-start;
                        margin-bottom:16px;'>
                        <div style='background:{C["CARD"]};
                            border:1px solid {C["BORDER"]};
                            border-radius:18px 18px 18px 4px;
                            padding:14px 18px; max-width:70%;
                            font-size:0.93rem; line-height:1.6;
                            color:{C["TEXT"]};'>
                            {badge_html}
                            <div style='color:{C["TEXT"]};'>
                                {reply_text}
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Input
    st.markdown(f"""
        <div style='border-top:1px solid {C["BORDER"]};
            padding:16px 40px; background:{C["BG"]};'>
    """, unsafe_allow_html=True)

    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_btn = st.columns([6, 1])
        with col_input:
            user_input = st.text_input(
                "",
                placeholder=t(lang, "chat_placeholder"),
                label_visibility="collapsed",
                key="chat_input_field"
            )
        with col_btn:
            submitted = st.form_submit_button(
                "▶", use_container_width=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted and user_input.strip():
        text = user_input.strip()

        st.session_state.chat_messages.append({
            "role": "user", "content": text
        })

        result    = predict_sentiment_and_emotion(text)
        sentiment = result["sentiment"]
        emotion   = result["emotion"]
        wellbeing = result["wellbeing"]

        save_analysis(text, sentiment, emotion, wellbeing)

        st.session_state.chat_history.append({
            "text":      text,
            "emotion":   emotion,
            "sentiment": sentiment,
            "wellbeing": wellbeing,
            "time":      datetime.now().strftime("%H:%M")
        })

        if detect_self_harm(text):
            reply = t(lang, "risk_message")
        else:
            reply = generate_support_reply(text, lang)

        st.session_state.chat_messages.append({
            "role":      "assistant",
            "content":   reply,
            "emotion":   emotion,
            "sentiment": sentiment,
            "wellbeing": wellbeing
        })

        st.rerun()