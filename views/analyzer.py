import json
import streamlit as st
import plotly.express as px
import pandas as pd

from utils.analyzer_engine import predict_sentiment_and_emotion
from utils.history_manager import save_analysis, load_history
from utils.pdf_export import create_pdf_report
from utils.translations import t
from utils.safety import detect_self_harm

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

    SENTIMENT_COLORS = {
        "positive": C["ACCENT"],
        "negative": "#e07070",
        "neutral":  C["TEXT2"]
    }
    EMOTION_COLORS = {
        "joy":    C["ACCENT"], "sadness": "#e07070",
        "anger":  "#e07070",   "fear":    "#a07aba",
        "stress": "#e09060",
    }

    # Header
    st.markdown(f"""
        <div style='padding:28px 40px 20px 40px;
            border-bottom:1px solid {C["BORDER"]};'>
            <div style='font-size:1.2rem; font-weight:600;
                color:{C["TEXT"]};'>{t(lang,"analyzer_title")}</div>
            <div style='font-size:0.85rem; color:{C["TEXT2"]};
                margin-top:4px;'>{t(lang,"analyzer_sub")}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<div style='padding:28px 40px;'>",
        unsafe_allow_html=True
    )

    if "main_text" not in st.session_state:
        st.session_state.main_text = ""

    st.markdown(f"""
        <div style='background:{C["CARD"]};
            border:1px solid {C["BORDER"]};
            border-radius:16px; padding:20px 24px;
            margin-bottom:20px;'>
    """, unsafe_allow_html=True)

    with st.form(key="analyzer_form", clear_on_submit=False):
        original_text = st.text_area(
            "",
            value=st.session_state.get("main_text", ""),
            height=150,
            placeholder="Ex: Je me sens vraiment bien aujourd'hui...",
            label_visibility="collapsed",
            key="analyzer_input"
        )
        col1, col2 = st.columns([4, 1])
        with col1:
            analyze_clicked = st.form_submit_button(
                "🔍 " + t(lang, "analyze_btn"),
                use_container_width=True
            )
        with col2:
            clear_clicked = st.form_submit_button(
                "🗑️ " + t(lang, "clear_btn"),
                use_container_width=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    if clear_clicked:
        st.session_state.main_text = ""
        st.rerun()

    if analyze_clicked and original_text.strip():
        st.session_state.main_text = original_text
        result    = predict_sentiment_and_emotion(original_text)
        sentiment = result["sentiment"]
        emotion   = result["emotion"]
        wellbeing = result["wellbeing"]
        s_probs   = result["sentiment_probs"]
        e_probs   = result["emotion_probs"]
        metrics   = result["metrics"]

        save_analysis(original_text, sentiment, emotion, wellbeing)

        if detect_self_harm(original_text):
            st.error(t(lang, "danger_alert"))

        sc = SENTIMENT_COLORS.get(sentiment, C["TEXT2"])
        ec = EMOTION_COLORS.get(emotion, C["TEXT2"])
        ei = EMOTION_ICONS.get(emotion, "🎭")

        wc = C["ACCENT"]
        if wellbeing >= 60: wc = "#6ec97a"
        elif wellbeing <= 30: wc = "#e07070"

        # Résultat
        st.markdown(f"""
            <div style='display:flex; gap:14px;
                flex-wrap:wrap; margin-bottom:20px;'>
                <div style='flex:1; min-width:130px;
                    background:{C["CARD"]};
                    border:1px solid {C["BORDER"]};
                    border-top:3px solid {sc};
                    border-radius:14px; padding:18px;
                    text-align:center;'>
                    <div style='font-size:0.65rem; color:{C["TEXT2"]};
                        text-transform:uppercase; letter-spacing:1.5px;
                        margin-bottom:10px; font-weight:600;'>
                        {t(lang,"sentiment_label")}
                    </div>
                    <div style='font-size:1.3rem; font-weight:700;
                        color:{sc};'>{sentiment.upper()}</div>
                </div>
                <div style='flex:1; min-width:130px;
                    background:{C["CARD"]};
                    border:1px solid {C["BORDER"]};
                    border-top:3px solid {ec};
                    border-radius:14px; padding:18px;
                    text-align:center;'>
                    <div style='font-size:0.65rem; color:{C["TEXT2"]};
                        text-transform:uppercase; letter-spacing:1.5px;
                        margin-bottom:10px; font-weight:600;'>
                        {t(lang,"emotion")}
                    </div>
                    <div style='font-size:1.3rem; font-weight:700;
                        color:{ec};'>{ei} {emotion.upper()}</div>
                </div>
                <div style='flex:1; min-width:130px;
                    background:{C["CARD"]};
                    border:1px solid {C["BORDER"]};
                    border-top:3px solid {wc};
                    border-radius:14px; padding:18px;
                    text-align:center;'>
                    <div style='font-size:0.65rem; color:{C["TEXT2"]};
                        text-transform:uppercase; letter-spacing:1.5px;
                        margin-bottom:10px; font-weight:600;'>
                        {t(lang,"wellbeing_label")}
                    </div>
                    <div style='font-size:1.3rem; font-weight:700;
                        color:{wc};'>{wellbeing}/100</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Graphiques
        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown(f"""
                <div style='background:{C["CARD"]};
                    border:1px solid {C["BORDER"]};
                    border-radius:14px; padding:20px;
                    margin-bottom:16px;'>
                <div style='font-size:0.65rem; color:{C["TEXT2"]};
                    text-transform:uppercase; letter-spacing:1.5px;
                    font-weight:600; margin-bottom:8px;'>
                    {t(lang,"proba_sentiment")}
                </div>
            """, unsafe_allow_html=True)
            fig = px.pie(
                pd.DataFrame({
                    "label": list(s_probs.keys()),
                    "prob":  list(s_probs.values())
                }),
                names="label", values="prob",
                color_discrete_sequence=[
                    C["ACCENT"], "#e07070", C["TEXT2"]
                ],
                hole=0.55
            )
            fig.update_layout(
                margin=dict(t=0,b=0,l=0,r=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=220,
                legend=dict(
                    font=dict(size=11, color=C["TEXT"]),
                    bgcolor="rgba(0,0,0,0)"
                )
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_r:
            st.markdown(f"""
                <div style='background:{C["CARD"]};
                    border:1px solid {C["BORDER"]};
                    border-radius:14px; padding:20px;
                    margin-bottom:16px;'>
                <div style='font-size:0.65rem; color:{C["TEXT2"]};
                    text-transform:uppercase; letter-spacing:1.5px;
                    font-weight:600; margin-bottom:8px;'>
                    {t(lang,"detail_emotions")}
                </div>
            """, unsafe_allow_html=True)
            fig2 = px.bar(
                pd.DataFrame({
                    "emotion": list(e_probs.keys()),
                    "prob":    list(e_probs.values())
                }),
                x="emotion", y="prob", color="emotion",
                color_discrete_sequence=[
                    C["ACCENT"],"#e07070","#a07aba",
                    "#e09060","#6ec97a"
                ]
            )
            fig2.update_layout(
                margin=dict(t=0,b=0,l=0,r=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False, height=220,
                xaxis=dict(showgrid=False, color=C["TEXT2"]),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(150,130,100,0.15)",
                    color=C["TEXT2"]
                )
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Métriques
        st.markdown(f"""
            <div style='background:{C["CARD"]};
                border:1px solid {C["BORDER"]};
                border-radius:14px; padding:20px;
                margin-bottom:16px;'>
            <div style='font-size:0.65rem; color:{C["TEXT2"]};
                text-transform:uppercase; letter-spacing:1.5px;
                font-weight:600; margin-bottom:16px;'>
                {t(lang,"text_metrics")}
            </div>
        """, unsafe_allow_html=True)

        mc = st.columns(5)
        items = [
            (t(lang,"word_count"),      metrics["word_count"]),
            (t(lang,"uppercase_ratio"), round(metrics["uppercase_ratio"],2)),
            (t(lang,"positive_words"),  metrics["positive_words"]),
            (t(lang,"negative_words"),  metrics["negative_words"]),
            (t(lang,"intensifiers"),    metrics["intensifiers"]),
        ]
        for col, (label, val) in zip(mc, items):
            col.markdown(f"""
                <div style='text-align:center; padding:12px 8px;
                    background:{C["BG2"]};
                    border-radius:10px;
                    border:1px solid {C["BORDER"]};'>
                    <div style='font-size:0.65rem; color:{C["TEXT2"]};
                        margin-bottom:6px; line-height:1.3;'>
                        {label}
                    </div>
                    <div style='font-size:1.2rem; font-weight:700;
                        color:{C["ACCENT"]};'>{val}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Export PDF
        pdf_path = "report.pdf"
        create_pdf_report(pdf_path, {
            "text": original_text,
            "sentiment": sentiment,
            "emotion": emotion,
            "wellbeing": wellbeing,
            "probs": json.dumps(s_probs, indent=2)
        })
        with open(pdf_path, "rb") as f:
            st.download_button(
                label=t(lang, "export_pdf"),
                data=f,
                file_name="emotioncare_report.pdf",
                mime="application/pdf"
            )

    # Historique
    hist = load_history()
    if not hist.empty:
        st.markdown(f"""
            <div style='background:{C["CARD"]};
                border:1px solid {C["BORDER"]};
                border-radius:14px; padding:20px;
                margin-top:8px;'>
            <div style='font-size:0.65rem; color:{C["TEXT2"]};
                text-transform:uppercase; letter-spacing:1.5px;
                font-weight:600; margin-bottom:16px;'>
                {t(lang,"recent_history")}
            </div>
        """, unsafe_allow_html=True)

        SCOL = {
            "positive": C["ACCENT"],
            "negative": "#e07070",
            "neutral":  C["TEXT2"]
        }

        for _, row in hist.tail(5).iloc[::-1].iterrows():
            sc = SCOL.get(str(row['sentiment']), C["TEXT2"])
            ei = EMOTION_ICONS.get(str(row['emotion']), "✦")
            txt = str(row['text'])
            st.markdown(f"""
                <div style='padding:12px 16px; margin-bottom:8px;
                    border-radius:10px; background:{C["BG2"]};
                    border-left:3px solid {sc};
                    border-top:1px solid {C["BORDER"]};
                    border-right:1px solid {C["BORDER"]};
                    border-bottom:1px solid {C["BORDER"]};'>
                    <div style='font-size:0.7rem; color:{C["TEXT2"]};
                        margin-bottom:4px;'>
                        🕐 {row['datetime']}
                    </div>
                    <div style='font-size:0.88rem; color:{C["TEXT"]};
                        margin-bottom:6px;'>
                        {txt[:80]}{"..." if len(txt)>80 else ""}
                    </div>
                    <div style='display:flex; gap:12px;
                        font-size:0.75rem;'>
                        <span style='color:{sc}; font-weight:600;'>
                            {str(row['sentiment']).upper()}
                        </span>
                        <span style='color:{C["TEXT2"]};'>
                            {ei} {row['emotion']}
                        </span>
                        <span style='color:{C["TEXT2"]};'>
                            ⚡ {row['wellbeing_score']}/100
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)