
import html
import streamlit as st
import pandas as pd

from api_client import (
    health_check,
    search_articles,
    get_similar_queries,
    get_article_audit,
    get_recommendations,
)

st.set_page_config(
    page_title="KnowledgeIQ | Knowledge Workspace",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== DESIGN & CSS ====================
st.markdown("""
<style>
:root {
    color-scheme: light;
}

.stApp,
[data-testid="stAppViewContainer"] {
    background: #f8f7fc !important;
    color: #302750 !important;
}

[data-testid="stHeader"] {
    background: #f8f7fc !important;
    color: #302750 !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
}

.block-container {
    max-width: 1350px;
    padding-top: 2.5rem;
    padding-bottom: 2rem;
}

h1, h2, h3, h4,
.stApp p,
.stApp label,
.stApp [data-testid="stMarkdownContainer"] {
    color: #302750;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #eeeafb !important;
    border-right: 1px solid #ded7f3;
}

[data-testid="stSidebar"] > div {
    background: #eeeafb !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h4,
[data-testid="stSidebar"] [data-testid="stRadio"] label,
[data-testid="stSidebar"] [data-testid="stRadio"] label p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #382c65 !important;
}

.brand {
    font-size: 29px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #33275e !important;
    padding-top: 12px;
}

.brand span {
    color: #7964dc !important;
}

.brand-sub {
    color: #695b91 !important;
    font-size: 13px;
    margin-bottom: 26px;
}

.side-heading {
    color: #514080 !important;
    font-weight: 800;
    font-size: 12px;
    letter-spacing: 1.4px;
    margin: 20px 0 10px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 7px 8px;
    border-radius: 9px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #e1dafa;
}

/* HERO */
.eyebrow {
    color: #6952cc !important;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    margin: 4px 0 12px;
}

.hero {
    background: linear-gradient(115deg, #33275e, #5c49a3 65%, #8976e8);
    border-radius: 24px;
    padding: 42px 45px;
    margin: 12px 0 32px;
    box-shadow: 0 12px 30px rgba(51, 39, 94, 0.12);
}

.hero h1 {
    color: #ffffff !important;
    font-size: 40px;
    line-height: 1.25;
    margin: 18px 0;
}

.hero p {
    color: #f3efff !important;
    font-size: 16px;
    line-height: 1.8;
    max-width: 760px;
}

.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 30px;
    color: #ffffff !important;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 700;
}

/* CARDS */
.card {
    background: #ffffff;
    border: 1px solid #e7e1f4;
    border-radius: 17px;
    padding: 22px;
    min-height: 140px;
    margin-bottom: 15px;
    box-shadow: 0 6px 18px rgba(51,39,94,0.04);
}

.card-icon {
    font-size: 25px;
    margin-bottom: 12px;
}

.card-label {
    font-size: 13px;
    color: #6e638c !important;
    font-weight: 600;
}

.card-value {
    font-size: 25px;
    color: #33275e !important;
    font-weight: 800;
    margin: 6px 0;
}

.card-desc {
    font-size: 13px;
    color: #71658f !important;
    line-height: 1.6;
}

.section-title {
    font-size: 22px;
    color: #302750 !important;
    font-weight: 800;
    margin: 22px 0 14px;
}

/* ALL BUTTONS */
.stButton > button,
.stFormSubmitButton > button,
[data-testid="stFormSubmitButton"] button {
    background: #7964dc !important;
    color: #ffffff !important;
    border: 1px solid #7964dc !important;
    border-radius: 11px !important;
    font-weight: 700 !important;
    min-height: 46px;
    padding: 10px 18px;
}

.stButton > button *,
.stFormSubmitButton > button *,
[data-testid="stFormSubmitButton"] button * {
    color: #ffffff !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #6049c1 !important;
    border-color: #6049c1 !important;
}

/* INPUTS */
[data-testid="stTextInput"] label,
[data-testid="stTextInput"] label p {
    color: #35275f !important;
    font-weight: 700 !important;
}

[data-testid="stTextInput"] input {
    background: #ffffff !important;
    color: #302750 !important;
    border: 1px solid #d9d2ed !important;
    border-radius: 10px !important;
    min-height: 44px;
}

[data-testid="stTextInput"] input::placeholder {
    color: #817796 !important;
    opacity: 1 !important;
}

/* ALERTS */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid #e0d8f4 !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
    color: #302750 !important;
}

[data-testid="stAlert"][kind="info"] {
    background: #eeeaff !important;
}

[data-testid="stAlert"][kind="warning"] {
    background: #fff5d9 !important;
}

[data-testid="stAlert"][kind="error"] {
    background: #fff0f0 !important;
}

[data-testid="stAlert"][kind="success"] {
    background: #e7f7ed !important;
}

/* TABLES */
[data-testid="stDataFrame"] {
    background: #ffffff !important;
    border: 1px solid #e7e1f4 !important;
    border-radius: 12px;
}

/* FOOTER */
.footer-panel {
    background: #f0ecfc;
    border: 1px solid #e2daf7;
    border-radius: 18px;
    padding: 25px 16px;
    margin-top: 45px;
    text-align: center;
    width: 100%;
    box-sizing: border-box;
}

.footer-title {
    font-size: 22px;
    font-weight: 800;
    color: #33275e !important;
}

.footer-title span {
    color: #7964dc !important;
}

.footer-copy {
    font-size: 13px;
    color: #655a85 !important;
    line-height: 1.9;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)


# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown(
        '<div class="brand">Knowledge<span>IQ.</span></div>'
        '<div class="brand-sub">AI Knowledge Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="side-heading">WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigate",
        [
            "Overview",
            "Article Search",
            "Similar Queries",
            "Article Audit",
            "Recommendations",
        ],
        label_visibility="collapsed",
        key="page",
    )

    st.divider()

    st.markdown(
        '<div class="side-heading">SYSTEM STATUS</div>',
        unsafe_allow_html=True,
    )

    if st.button("↻ Check backend connection",
                 use_container_width=True):
        try:
            st.session_state["health"] = health_check()
            st.session_state["health_error"] = None
        except Exception as exc:
            st.session_state["health"] = None
            st.session_state["health_error"] = str(exc)

    if st.session_state.get("health") is not None:
        st.success("Backend connected")
    elif st.session_state.get("health_error"):
        st.error("Backend unavailable")
        st.caption(st.session_state["health_error"])
    else:
        st.info("Connection not checked")

    st.caption("Search · Audit · Insights · Recommendations")


# ==================== HELPER FUNCTIONS ====================
def safe(value):
    return html.escape(str(value))


def show_error(exc):
    st.error(f"Backend request failed: {exc}")


def show_rows(rows):
    if isinstance(rows, list) and rows:
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No records returned.")


def show_card(icon, label, value, description):
    st.markdown(
        f'<div class="card">'
        f'<div class="card-icon">{safe(icon)}</div>'
        f'<div class="card-label">{safe(label)}</div>'
        f'<div class="card-value">{safe(value)}</div>'
        f'<div class="card-desc">{safe(description)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ==================== OVERVIEW ====================
if page == "Overview":
    st.markdown(
        '<div class="eyebrow">YOUR KNOWLEDGE WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="hero">
        <div class="hero-tag">✦ AI-POWERED KNOWLEDGE INTELLIGENCE</div>
        <h1>Turn customer questions<br>into better answers.</h1>
        <p>Discover relevant help articles, identify repeated customer
        questions, audit outdated content and uncover knowledge gaps —
        all in one workspace.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Workspace at a glance</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    cards = [
        ("📚", "Article Search", "Ready", "Find relevant articles"),
        ("💬", "Query Insights", "Ready", "Similar questions"),
        ("🔎", "Content Audit", "Ready", "Outdated and duplicate articles"),
        ("✨", "Recommendations", "Ready", "Knowledge gaps"),
    ]

    for col, item in zip(cols, cards):
        with col:
            show_card(*item)

    st.markdown(
        '<div class="section-title">Explore your workspace</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    features = [
        ("🔍", "Article Search",
         "Find matching knowledge base content.", "Article Search"),
        ("💬", "Similar Queries",
         "Discover recurring customer questions.", "Similar Queries"),
        ("🛠️", "Article Audit",
         "Review outdated or duplicate content.", "Article Audit"),
    ]

    for col, item in zip(cols, features):
        with col:
            show_card(item[0], item[1], "Explore", item[2])
            if st.button(
                "Open " + item[1] + " →",
                key="go_" + item[3],
                use_container_width=True,
            ):
                st.session_state["page"] = item[3]
                st.rerun()

    st.info(
        "Cards show feature availability, not live statistics. "
        "Check the backend connection to verify the API."
    )


# ==================== ARTICLE SEARCH ====================
elif page == "Article Search":
    st.markdown(
        '<div class="eyebrow">DISCOVER CONTENT</div>',
        unsafe_allow_html=True,
    )
    st.title("Article Search")
    st.write("Ask a question to find matching knowledge base articles.")

    with st.form("search_form"):
        question = st.text_input(
            "Your question",
            placeholder="Where is my order?",
        )
        submitted = st.form_submit_button("🔍 Search articles")

    if submitted:
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Searching articles..."):
                    response = search_articles(question.strip())

                results = response.get("results", [])
                st.subheader("Search results")

                if not results:
                    st.info("No matching articles found.")

                for article in results:
                    with st.container(border=True):
                        st.subheader(str(article.get("title", "Untitled")))
                        st.caption(
                            "Article ID: "
                            + str(article.get("article_id", "N/A"))
                        )
                        st.write(article.get("content", ""))

                        score = article.get("similarity")
                        if score is not None:
                            score = max(0.0, min(1.0, float(score)))
                            st.progress(
                                score,
                                text=f"Similarity: {score:.1%}",
                            )
            except Exception as exc:
                show_error(exc)


# ==================== SIMILAR QUERIES ====================
elif page == "Similar Queries":
    st.markdown(
        '<div class="eyebrow">CUSTOMER INSIGHTS</div>',
        unsafe_allow_html=True,
    )
    st.title("Similar Queries")
    st.write("Find customer questions that may be asking the same thing.")

    if st.button("Load similar queries"):
        try:
            response = get_similar_queries()
            show_rows(response.get("results", []))
        except Exception as exc:
            show_error(exc)


# ==================== ARTICLE AUDIT ====================
elif page == "Article Audit":
    st.markdown(
        '<div class="eyebrow">CONTENT QUALITY</div>',
        unsafe_allow_html=True,
    )
    st.title("Article Audit")
    st.write("Check for outdated and duplicate knowledge base articles.")

    if st.button("Run article audit"):
        try:
            response = get_article_audit()
            show_rows(response.get("results", []))
        except Exception as exc:
            show_error(exc)


# ==================== RECOMMENDATIONS ====================
elif page == "Recommendations":
    st.markdown(
        '<div class="eyebrow">CONTINUOUS IMPROVEMENT</div>',
        unsafe_allow_html=True,
    )
    st.title("Knowledge Gap Recommendations")
    st.write("Find opportunities to improve the knowledge base.")

    with st.form("recommend_form"):
        question = st.text_input(
            "Customer question",
            placeholder="How can I track my order?",
        )
        submitted = st.form_submit_button("✦ Generate recommendations")

    if submitted:
        if not question.strip():
            st.warning("Please enter a customer question.")
        else:
            try:
                with st.spinner("Generating recommendations..."):
                    response = get_recommendations(question.strip())

                st.subheader("Rewritten query")
                st.info(str(response.get("rewritten_query", "Not provided")))

                st.subheader("Suggested improvements")
                show_rows(response.get("recommendations", []))
            except Exception as exc:
                show_error(exc)


# ==================== FOOTER ====================
st.markdown("""
<div class="footer-panel">
    <div class="footer-title">Knowledge<span>IQ.</span></div>
    <div class="footer-copy">
        Smarter knowledge. Better customer experiences.<br>
        Knowledge Base Improvement Advisory Agent<br>
        Built with Streamlit · Connected through FastAPI REST APIs
    </div>
</div>
""", unsafe_allow_html=True)
