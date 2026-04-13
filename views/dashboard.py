import streamlit as st
import pandas as pd
import plotly.express as px

from utils.history_manager import load_history, clear_history
from utils.translations import t

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

    df = load_history()

    # Header
    st.markdown(f"""
        <div style='padding:28px 40px 20px 40px;
            border-bottom:1px solid {C["BORDER"]};'>
            <div style='font-size:1.2rem; font-weight:600;
                color:{C["TEXT"]};'>{t(lang,"dashboard_title")}</div>
            <div style='font-size:0.85rem; color:{C["TEXT2"]};
                margin-top:4px;'>{t(lang,"dashboard_sub")}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<div style='padding:28px 40px;'>",
        unsafe_allow_html=True
    )

    if df.empty:
        st.markdown(f"""
            <div style='background:{C["CARD"]};
                border:1px solid {C["BORDER"]};
                border-radius:16px; padding:60px;
                text-align:center;'>
                <div style='font-size:3rem; margin-bottom:16px;'>📭</div>
                <div style='color:{C["TEXT2"]}; font-size:0.95rem;
                    line-height:1.7;'>
                    {t(lang,"no_analysis")}
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Stats
    total = len(df)
    avg_w = round(
        pd.to_numeric(df["wellbeing_score"], errors="coerce")
        .fillna(0).mean(), 1
    )
    common_emo = (
        df["emotion"].mode()[0]
        if not df["emotion"].mode().empty else "-"
    )
    ei = EMOTION_ICONS.get(common_emo, "🎭")
    wc = C["ACCENT"]
    if avg_w >= 60: wc = "#6ec97a"
    elif avg_w <= 30: wc = "#e07070"

    st.markdown(f"""
        <div style='display:flex; gap:14px;
            flex-wrap:wrap; margin-bottom:24px;'>
            <div style='flex:1; min-width:130px;
                background:{C["CARD"]};
                border:1px solid {C["BORDER"]};
                border-top:3px solid {C["ACCENT"]};
                border-radius:14px; padding:20px;
                text-align:center;'>
                <div style='font-size:0.65rem; color:{C["TEXT2"]};
                    text-transform:uppercase; letter-spacing:1.5px;
                    font-weight:600; margin-bottom:10px;'>
                    {t(lang,"stats_total")}
                </div>
                <div style='font-size:2rem; font-weight:700;
                    color:{C["ACCENT"]};'>{total}</div>
            </div>
            <div style='flex:1; min-width:130px;
                background:{C["CARD"]};
                border:1px solid {C["BORDER"]};
                border-top:3px solid {wc};
                border-radius:14px; padding:20px;
                text-align:center;'>
                <div style='font-size:0.65rem; color:{C["TEXT2"]};
                    text-transform:uppercase; letter-spacing:1.5px;
                    font-weight:600; margin-bottom:10px;'>
                    {t(lang,"stats_avg")}
                </div>
                <div style='font-size:2rem; font-weight:700;
                    color:{wc};'>{avg_w}</div>
            </div>
            <div style='flex:1; min-width:130px;
                background:{C["CARD"]};
                border:1px solid {C["BORDER"]};
                border-top:3px solid #a07aba;
                border-radius:14px; padding:20px;
                text-align:center;'>
                <div style='font-size:0.65rem; color:{C["TEXT2"]};
                    text-transform:uppercase; letter-spacing:1.5px;
                    font-weight:600; margin-bottom:10px;'>
                    {t(lang,"stats_common")}
                </div>
                <div style='font-size:2rem;'>{ei}</div>
                <div style='font-size:0.82rem; color:{C["TEXT"]};
                    margin-top:4px; font-weight:600;'>
                    {common_emo.capitalize()}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Graphiques
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <div style='background:{C["CARD"]};
                border:1px solid {C["BORDER"]};
                border-radius:14px; padding:20px;
                margin-bottom:16px;'>
            <div style='font-size:0.65rem; color:{C["TEXT2"]};
                text-transform:uppercase; letter-spacing:1.5px;
                font-weight:600; margin-bottom:8px;'>
                {t(lang,"sentiments_chart")}
            </div>
        """, unsafe_allow_html=True)
        fig1 = px.pie(
            df, names="sentiment",
            color_discrete_sequence=[
                C["ACCENT"], "#e07070", C["TEXT2"]
            ],
            hole=0.55
        )
        fig1.update_layout(
            margin=dict(t=0,b=0,l=0,r=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=240,
            legend=dict(
                font=dict(size=11, color=C["TEXT"]),
                bgcolor="rgba(0,0,0,0)"
            )
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style='background:{C["CARD"]};
                border:1px solid {C["BORDER"]};
                border-radius:14px; padding:20px;
                margin-bottom:16px;'>
            <div style='font-size:0.65rem; color:{C["TEXT2"]};
                text-transform:uppercase; letter-spacing:1.5px;
                font-weight:600; margin-bottom:8px;'>
                {t(lang,"emotions_chart")}
            </div>
        """, unsafe_allow_html=True)
        emo_df = df["emotion"].value_counts().reset_index()
        emo_df.columns = ["emotion","count"]
        fig2 = px.bar(
            emo_df, x="emotion", y="count",
            color="emotion",
            color_discrete_sequence=[
                C["ACCENT"],"#e07070","#a07aba",
                "#e09060","#6ec97a"
            ]
        )
        fig2.update_layout(
            margin=dict(t=0,b=0,l=0,r=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False, height=240,
            xaxis=dict(showgrid=False, color=C["TEXT2"]),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(150,130,100,0.15)",
                color=C["TEXT2"]
            )
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Wellbeing trend
    st.markdown(f"""
        <div style='background:{C["CARD"]};
            border:1px solid {C["BORDER"]};
            border-radius:14px; padding:20px;
            margin-bottom:16px;'>
        <div style='font-size:0.65rem; color:{C["TEXT2"]};
            text-transform:uppercase; letter-spacing:1.5px;
            font-weight:600; margin-bottom:8px;'>
            {t(lang,"wellbeing_trend")}
        </div>
    """, unsafe_allow_html=True)

    df_p = df.copy()
    df_p["wellbeing_score"] = pd.to_numeric(
        df_p["wellbeing_score"], errors="coerce"
    ).fillna(0)
    fig3 = px.line(
        df_p, x="datetime", y="wellbeing_score",
        markers=True,
        color_discrete_sequence=[C["ACCENT"]]
    )
    fig3.update_layout(
        margin=dict(t=0,b=0,l=0,r=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=240,
        xaxis=dict(showgrid=False, color=C["TEXT2"]),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(150,130,100,0.15)",
            color=C["TEXT2"],
            range=[0,100]
        )
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Historique complet
    st.markdown(f"""
        <div style='background:{C["CARD"]};
            border:1px solid {C["BORDER"]};
            border-radius:14px; padding:20px;
            margin-bottom:16px;'>
        <div style='font-size:0.65rem; color:{C["TEXT2"]};
            text-transform:uppercase; letter-spacing:1.5px;
            font-weight:600; margin-bottom:16px;'>
            {t(lang,"full_history")}
        </div>
    """, unsafe_allow_html=True)

    for _, row in df.iloc[::-1].iterrows():
        sc = SENTIMENT_COLORS.get(str(row['sentiment']), C["TEXT2"])
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
                    {txt[:90]}{"..." if len(txt)>90 else ""}
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

    # Bouton effacer
    col_btn, _, _ = st.columns([1,2,2])
    with col_btn:
        if st.button(t(lang,"clear_history"),
                     use_container_width=True):
            clear_history()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)