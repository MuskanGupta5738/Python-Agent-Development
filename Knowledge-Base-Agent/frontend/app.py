
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
    page_title="KnowledgeIQ | Knowledge Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

:root {
    --purple: #7964dc;
    --deep: #33275e;
    --ink: #29234a;
    --muted: #77738f;
    --border: #e8e3f4;
}

.stApp {
    background: #f8f7fc;
    color: var(--ink);
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1450px;
    padding: 2rem 2.5rem 3rem 2.5rem;
}

[data-testid="stSidebar"] {
    background: #efebfb !important;
    border-right: 1px solid #e2dcf5;
}

[data-testid="stSidebar"] > div {
    background: transparent;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #382c65 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    color: #382c65 !important;
    font-weight: 600;
}

.brand {
    color: #35275f;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 3px;
}

.brand span {
    color: #8069e5 !important;
}

.brand-caption {
    color: #71658f !important;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 20px;
}

.eyebrow {
    color: #7964dc;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 10px;
}

.hero {
    background: linear-gradient(115deg, #33275e, #57449a 60%, #8875e8);
    color: white;
    border-radius: 22px;
    padding: 35px;
    margin: 12px 0 27px 0;
    box-shadow: 0 12px 30px rgba(62, 45, 117, 0.15);
}

.hero-tag {
    display: inline-block;
    padding: 7px 12px;
    border: 1px solid rgba(255,255,255,.25);
    background: rgba(255,255,255,.12);
    border-radius: 30px;
    color: white;
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 17px;
}

.hero h1 {
    color: white !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 35px;
    line-height: 1.25;
    margin: 0 0 12px 0;
}

.hero p {
    color: #eee8ff !important;
    font-size: 15px;
    line-height: 1.8;
    max-width: 760px;
    margin-bottom: 0;
}

.section-title {
    color: #302750;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 20px;
    font-weight: 800;
    margin: 24px 0 15px 0;
}

.metric-card {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 20px;
    min-height: 140px;
    box-shadow: 0 5px 18px rgba(44,32,90,.035);
}

.metric-icon {
    font-size: 23px;
    margin-bottom: 10px;
}

.metric-label {
    color: var(--muted);
    font-size: 12px;
    font-weight: 600;
}

.metric-value {
    color: #302750;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 25px;
    font-weight: 800;
    margin: 5px 0;
}

.feature-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 23px;
    min-height: 175px;
    margin-bottom: 12px;
}

.feature-icon {
    background: #eeeaff;
    border-radius: 12px;
    width: 43px;
    height: 43px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    margin-bottom: 15px;
}

.feature-title {
    color: #302750;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 8px;
}

.feature-desc {
    color: #77738f;
    font-size: 13px;
    line-height: 1.7;
}

.info-panel {
    background: #f0edff;
    border: 1px solid #e0d8ff;
    border-radius: 15px;
    padding: 19px 22px;
    margin: 20px 0;
    color: #49388b;
    line-height: 1.8;
}



/* Buttons: visible text and premium purple styling */
.stButton > button,
.stFormSubmitButton > button,
[data-testid="stFormSubmitButton"] button {
    background: #7964dc !important;
    color: #ffffff !important;
    border: 1px solid #7964dc !important;
    border-radius: 11px !important;
    min-height: 46px;
    padding: 0.65rem 1.25rem;
    font-size: 15px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(121, 100, 220, 0.16);
    transition: all 0.2s ease;
}

.stButton > button p,
.stFormSubmitButton > button p,
[data-testid="stFormSubmitButton"] button p {
    color: #ffffff !important;
    font-weight: 700 !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
[data-testid="stFormSubmitButton"] button:hover {
    background: #5f49bd !important;
    color: #ffffff !important;
    border-color: #5f49bd !important;
    box-shadow: 0 6px 18px rgba(95, 73, 189, 0.24);
}

/* Top header */
header[data-testid="stHeader"] {
    background: #f8f7fc !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
}

/* Input labels */
.stTextInput label,
.stTextInput label p {
    color: #382c65 !important;
    font-weight: 700 !important;
}

/* Input text and placeholder */
.stTextInput input {
    background: #ffffff !important;
    color: #29234a !important;
    border: 1px solid #dcd5ef !important;
    border-radius: 11px !important;
    min-height: 46px;
}

.stTextInput input::placeholder {
    color: #9189a8 !important;
    opacity: 1;
}

.stTextInput input:focus {
    border-color: #7964dc !important;
    box-shadow: 0 0 0 2px rgba(121, 100, 220, 0.13) !important;
}








.stButton > button:hover {
    background: #6550c4;
    border-color: #6550c4;
}

.stTextInput input {
    background: white;
    border: 1px solid #ded8ee;
    border-radius: 10px;
    color: #302750;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 12px;
}

.footer {
    color: #89849e;
    font-size: 12px;
    text-align: center;
    padding-top: 30px;
}

#MainMenu, footer {
    visibility: hidden;
}


/* ===== GLOBAL READABILITY FIX ===== */

/* Main page text */
.stApp,
.stApp p,
.stApp label,
.stApp li {
    color: #302750;
}

/* Input labels and entered text */
.stTextInput label,
.stTextInput label p,
.stTextArea label,
.stTextArea label p {
    color: #302750 !important;
    font-weight: 700 !important;
}

.stTextInput input,
.stTextArea textarea {
    background: #ffffff !important;
    color: #302750 !important;
    border: 1px solid #d8d0ed !important;
    caret-color: #7964dc !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #827a9b !important;
    opacity: 1 !important;
}

/* All buttons: search, audit, recommendations */
.stApp button,
.stApp button p {
    color: #ffffff !important;
}

.stApp button[kind="primary"],
.stApp button[kind="secondary"],
.stFormSubmitButton button,
.stButton button {
    background: #7964dc !important;
    color: #ffffff !important;
    border-color: #7964dc !important;
    border-radius: 11px !important;
    font-weight: 700 !important;
}

.stApp button:hover {
    background: #5f49bd !important;
    color: #ffffff !important;
}

/* Warning, info, error and success messages */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid #e0d8f4 !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div {
    color: #302750 !important;
}

/* Info messages */
[data-testid="stAlert"][kind="info"] {
    background: #eeeaff !important;
}

/* Warning messages */
[data-testid="stAlert"][kind="warning"] {
    background: #fff5d9 !important;
}

/* Error messages */
[data-testid="stAlert"][kind="error"] {
    background: #fff0f0 !important;
}

/* Success messages */
[data-testid="stAlert"][kind="success"] {
    background: #e7f7ed !important;
}

/* Data tables */
[data-testid="stDataFrame"] {
    background: #ffffff !important;
    border: 1px solid #e8e3f4 !important;
    border-radius: 12px !important;
}

/* Keep the top header light */
header[data-testid="stHeader"] {
    background: #f8f7fc !important;
}

/* Footer should use full available width */
.custom-footer,
.footer {
    display: block;
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
    margin: 40px auto 0;
    text-align: center !important;
    overflow-wrap: anywhere;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown(
        '<div class="brand">Knowledge<span>IQ.</span></div>'
        '<div class="brand-caption">AI Knowledge Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("##### WORKSPACE")

    page = st.radio(
        "Navigation",
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
    st.markdown("##### SYSTEM STATUS")

    if st.button("↻  Check backend connection",
                 use_container_width=True):
        try:
            st.session_state["health"] = health_check()
            st.session_state["backend_error"] = None
        except RuntimeError as exc:
            st.session_state["health"] = None
            st.session_state["backend_error"] = str(exc)

    if st.session_state.get("health") is not None:
        st.success("Backend connected")
    elif st.session_state.get("backend_error"):
        st.error("Backend unavailable")
        st.caption(st.session_state["backend_error"])
    else:
        st.info("Connection not checked")

    st.divider()
    st.caption("Search · Audit · Insights · Recommendations")


# ---------------- HELPERS ----------------
def show_error(error):
    st.error(str(error))


def show_table(results):
    if results:
        st.dataframe(
            pd.DataFrame(results),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No results returned. Try again after checking the data.")


def metric_card(icon, label, value, description):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{description}</div>
    </div>
    """, unsafe_allow_html=True)


def feature_card(icon, title, description):
    st.markdown(f"""
    <div class="feature-card">
        <div class="feature-icon">{icon}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-desc">{description}</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------- OVERVIEW ----------------
if page == "Overview":
    st.markdown(
        '<div class="eyebrow">YOUR KNOWLEDGE WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="hero">
        <div class="hero-tag">✦ AI-POWERED KNOWLEDGE INTELLIGENCE</div>
        <h1>Turn customer questions<br>into better answers.</h1>
        <p>Discover relevant help articles, uncover repeated customer
        questions, audit outdated content and identify knowledge gaps
        — all in one workspace.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Workspace at a glance</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("📚", "Article Search", "Ready", "Semantic matching")
    with c2:
        metric_card("💬", "Query Insights", "Ready", "Similar questions")
    with c3:
        metric_card("🔎", "Content Audit", "Ready", "Duplicate & outdated")
    with c4:
        metric_card("✦", "Recommendations", "Ready", "Knowledge gaps")

    st.markdown(
        '<div class="section-title">Explore your workspace</div>',
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3)

    with a:
        feature_card(
            "⌕", "Find the right article",
            "Search customer questions and discover relevant knowledge."
        )
        if st.button("Open article search →", key="open_search",
                     use_container_width=True):
            st.session_state["page"] = "Article Search"
            st.rerun()

    with b:
        feature_card(
            "◈", "Understand query patterns",
            "Explore similar questions and common support needs."
        )
        if st.button("Explore similar queries →", key="open_queries",
                     use_container_width=True):
            st.session_state["page"] = "Similar Queries"
            st.rerun()

    with c:
        feature_card(
            "✧", "Improve your knowledge base",
            "Review content issues and discover missing topics."
        )
        if st.button("View article audit →", key="open_audit",
                     use_container_width=True):
            st.session_state["page"] = "Article Audit"
            st.rerun()

    st.markdown("""
    <div class="info-panel">
        <strong>✦ Intelligence behind the scenes</strong><br>
        TF-IDF and cosine similarity compare text. Article freshness rules
        and recurring query patterns support content audits and
        knowledge-gap recommendations.
    </div>
    """, unsafe_allow_html=True)


# ---------------- ARTICLE SEARCH ----------------
elif page == "Article Search":
    st.markdown('<div class="eyebrow">DISCOVER CONTENT</div>',
                unsafe_allow_html=True)
    st.title("Article Search")
    st.write("Ask a question to find matching knowledge base articles.")

    with st.form("search_form"):
        question = st.text_input(
            "Your question",
            placeholder="Where is my order?",
        )
        submitted = st.form_submit_button("⌕  Search articles")

    if submitted:
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Finding relevant articles..."):
                    data = search_articles(question.strip())

                results = data.get("results", [])
                st.markdown("### Search results")
                st.caption(f"{len(results)} result(s) returned")

                if results:
                    for article in results:
                        with st.container(border=True):
                            st.markdown(
                                f"#### {article.get('title', 'Untitled')}"
                            )
                            st.caption(
                                f"Article ID: {article.get('article_id', 'N/A')}"
                            )
                            st.write(article.get("content", "No content available."))

                            score = article.get("similarity")
                            if score is not None:
                                score = max(0.0, min(1.0, float(score)))
                                st.progress(score, text=f"Similarity: {score:.0%}")
                else:
                    st.info("No relevant articles found.")

            except (RuntimeError, ValueError, TypeError) as exc:
                show_error(exc)


# ---------------- SIMILAR QUERIES ----------------
elif page == "Similar Queries":
    st.markdown('<div class="eyebrow">CUSTOMER INSIGHTS</div>',
                unsafe_allow_html=True)
    st.title("Similar Queries")
    st.write("Explore customer questions with similar wording or meaning.")

    if st.button("↻  Load similar queries"):
        try:
            with st.spinner("Loading query insights..."):
                data = get_similar_queries()
            show_table(data.get("results", []))
        except RuntimeError as exc:
            show_error(exc)


# ---------------- ARTICLE AUDIT ----------------
elif page == "Article Audit":
    st.markdown('<div class="eyebrow">CONTENT QUALITY</div>',
                unsafe_allow_html=True)
    st.title("Article Audit")
    st.write("Review potentially duplicate or outdated knowledge articles.")

    if st.button("⌕  Run article audit"):
        try:
            with st.spinner("Auditing articles..."):
                data = get_article_audit()
            show_table(data.get("results", []))
        except RuntimeError as exc:
            show_error(exc)


# ---------------- RECOMMENDATIONS ----------------
elif page == "Recommendations":
    st.markdown('<div class="eyebrow">CONTINUOUS IMPROVEMENT</div>',
                unsafe_allow_html=True)
    st.title("Knowledge Gap Recommendations")
    st.write("Discover topics that may need clearer queries or new help articles.")

    with st.form("recommendation_form"):
        question = st.text_input(
            "Customer question",
            placeholder="How can I track my order?",
        )
        submitted = st.form_submit_button("✦  Generate recommendations")

    if submitted:
        if not question.strip():
            st.warning("Please enter a customer question.")
        else:
            try:
                with st.spinner("Analysing knowledge gaps..."):
                    data = get_recommendations(question.strip())

                st.markdown("### Rewritten query")
                st.markdown(
                    f'<div class="info-panel"><strong>'
                    f'{data.get("rewritten_query", "Not provided")}'
                    f'</strong></div>',
                    unsafe_allow_html=True,
                )

                st.markdown("### Suggested improvements")
                show_table(data.get("recommendations", []))

            except RuntimeError as exc:
                show_error(exc)


# ---------------- FOOTER ----------------

st.markdown("""
<div class="custom-footer">
    <div class="footer-brand">KnowledgeIQ<span>.</span></div>
    <div class="footer-description">
        Smarter knowledge. Better customer experiences.
    </div>
    <div class="footer-divider"></div>
    <div class="footer-bottom">
        Knowledge Base Improvement Advisory Agent<br>
        Powered by Streamlit &amp; FastAPI
    </div>
</div>
""", unsafe_allow_html=True)






