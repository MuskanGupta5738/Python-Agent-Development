
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
    page_title="KnowledgeIQ | AI Knowledge Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- PREMIUM UI THEME ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #242044;
    --muted: #77758f;
    --purple: #7964dc;
    --lavender: #eeeaff;
    --border: #eae7f5;
    --surface: #ffffff;
}

.stApp {
    background: #f8f7fc;
    color: var(--ink);
    font-family: 'DM Sans', sans-serif;
}

header[data-testid="stHeader"] {
    background: rgba(248,247,252,0.92);
}

.block-container {
    max-width: 1450px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #f0edfc;
    border-right: 1px solid #e4def9;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

h1, h2, h3 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #28234c !important;
    letter-spacing: -0.7px;
}

p, label, span {
    font-family: 'DM Sans', sans-serif;
}

.brand {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 25px;
    font-weight: 800;
    color: #352765;
    letter-spacing: -1px;
}

.brand span { color: #8069e5; }

.eyebrow {
    color: #8069e5;
    text-transform: uppercase;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 9px;
}

.hero {
    background: linear-gradient(115deg, #33275e 0%, #57449a 58%, #8875e8 100%);
    border-radius: 24px;
    padding: 34px 36px;
    color: white;
    margin: 8px 0 26px 0;
    box-shadow: 0 14px 34px rgba(80,62,145,0.15);
}

.hero h1 {
    color: white !important;
    font-size: 34px;
    line-height: 1.25;
    margin: 0 0 12px 0;
}

.hero p {
    color: #e8e1ff;
    font-size: 15px;
    line-height: 1.8;
    max-width: 700px;
    margin-bottom: 0;
}

.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.13);
    color: #f3efff;
    padding: 7px 12px;
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 30px;
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 18px;
}

.section-label {
    font-size: 19px;
    font-weight: 800;
    color: #30294f;
    margin: 10px 0 15px 0;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.metric-card {
    background: white;
    border: 1px solid #eae6f5;
    border-radius: 17px;
    padding: 21px;
    min-height: 133px;
    box-shadow: 0 5px 18px rgba(44,32,90,0.035);
}

.metric-icon {
    font-size: 23px;
    margin-bottom: 12px;
}

.metric-label {
    font-size: 12px;
    color: #77758f;
    font-weight: 600;
}

.metric-value {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #302750;
    font-size: 26px;
    font-weight: 800;
    margin-top: 5px;
}

.feature-card {
    background: white;
    border: 1px solid #eae6f5;
    border-radius: 18px;
    padding: 23px;
    min-height: 190px;
    margin-bottom: 12px;
}

.feature-icon {
    width: 43px;
    height: 43px;
    border-radius: 13px;
    background: #eeeaff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    margin-bottom: 16px;
}

.feature-title {
    color: #302750;
    font-weight: 800;
    font-size: 16px;
    margin-bottom: 8px;
}

.feature-desc {
    color: #77758f;
    font-size: 13px;
    line-height: 1.7;
}

.info-panel {
    background: #f0edff;
    border: 1px solid #e0d8ff;
    border-radius: 16px;
    padding: 20px 23px;
    margin: 12px 0 22px 0;
}

.info-panel strong {
    color: #49388b;
}

.sidebar-note {
    color: #77718e;
    font-size: 12px;
    line-height: 1.7;
}

.stButton > button {
    background: #7964dc;
    color: white;
    border: 1px solid #7964dc;
    border-radius: 10px;
    padding: 0.55rem 1rem;
    font-weight: 700;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: #6650c6;
    color: white;
    border-color: #6650c6;
}

.stTextInput input, .stTextArea textarea {
    background: white;
    border: 1px solid #ded9ed;
    border-radius: 10px;
    color: #302750;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #7964dc;
    box-shadow: 0 0 0 1px #7964dc;
}

[data-testid="stDataFrame"] {
    border: 1px solid #eae6f5;
    border-radius: 12px;
    overflow: hidden;
}

hr {
    border-color: #e3def1;
}

.footer {
    color: #89869e;
    font-size: 12px;
    text-align: center;
    padding-top: 30px;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown(
        '<div class="brand">Knowledge<span>IQ.</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("AI Knowledge Intelligence")

    st.divider()
    st.markdown("##### WORKSPACE")

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
    )

    st.divider()
    st.markdown("##### SYSTEM STATUS")

    if st.button("↻  Check backend connection", use_container_width=True):
        try:
            result = health_check()
            st.session_state["backend_status"] = "Connected"
            st.session_state["backend_response"] = result
        except RuntimeError as error:
            st.session_state["backend_status"] = "Offline"
            st.session_state["backend_error"] = str(error)

    status = st.session_state.get("backend_status", "Not checked")

    if status == "Connected":
        st.success("Backend connected")
        if "backend_response" in st.session_state:
            with st.expander("Health response"):
                st.json(st.session_state["backend_response"])
    elif status == "Offline":
        st.error("Backend unavailable")
        st.caption(st.session_state.get("backend_error", ""))
    else:
        st.info("Connection not checked")

    st.markdown("---")
    st.markdown(
        '<div class="sidebar-note">Knowledge management<br>'
        'Search · Audit · Insights · Recommendations</div>',
        unsafe_allow_html=True,
    )


# ---------- REUSABLE HELPERS ----------
def show_error(error):
    st.error(str(error))


def show_results_table(results):
    if results:
        st.dataframe(
            pd.DataFrame(results),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No results returned. Try again after checking your data.")


def metric_card(icon, label, value, note):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_card(icon, title, description):
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- OVERVIEW ----------
if page == "Overview":
    st.markdown('<div class="eyebrow">YOUR KNOWLEDGE WORKSPACE</div>',
                unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero">
            <div class="hero-tag">✦ AI-POWERED KNOWLEDGE INTELLIGENCE</div>
            <h1>Turn customer questions<br>into better answers.</h1>
            <p>
                Discover relevant help articles, uncover repeated customer
                questions, audit outdated content and identify knowledge gaps
                — all in one workspace.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">Workspace at a glance</div>',
                unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    # These are feature indicators, not actual dataset counts.
    with c1:
        metric_card("📚", "Article Search", "Ready", "Semantic matching")
    with c2:
        metric_card("💬", "Query Insights", "Ready", "Similar questions")
    with c3:
        metric_card("🔎", "Content Audit", "Ready", "Duplicate & outdated")
    with c4:
        metric_card("✦", "Recommendations", "Ready", "Knowledge gaps")

    st.markdown('<div class="section-label">Explore your workspace</div>',
                unsafe_allow_html=True)

    a, b, c = st.columns(3)

    with a:
        feature_card(
            "⌕", "Find the right article",
            "Search customer questions and discover the most relevant "
            "knowledge base content."
        )
        if st.button("Open article search →", key="go_search",
                     use_container_width=True):
            st.session_state["page_choice"] = "Article Search"
            st.rerun()

    with b:
        feature_card(
            "◈", "Understand query patterns",
            "Find repeated customer questions and identify common support needs."
        )
        if st.button("Explore similar queries →", key="go_queries",
                     use_container_width=True):
            st.session_state["page_choice"] = "Similar Queries"
            st.rerun()

    with c:
        feature_card(
            "✧", "Improve your knowledge base",
            "Review content issues and discover topics that may need new articles."
        )
        if st.button("View recommendations →", key="go_recommendations",
                     use_container_width=True):
            st.session_state["page_choice"] = "Recommendations"
            st.rerun()

    st.markdown(
        """
        <div class="info-panel">
            <strong>✦ Intelligence behind the scenes</strong><br>
            TF-IDF and cosine similarity help compare text. Article freshness
            rules and recurring query patterns support content audits and
            knowledge-gap recommendations.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- ARTICLE SEARCH ----------
elif page == "Article Search":
    st.markdown('<div class="eyebrow">DISCOVER CONTENT</div>',
                unsafe_allow_html=True)
    st.title("Article Search")
    st.write("Ask a question to find matching knowledge base articles.")

    with st.form("search_form"):
        question = st.text_input(
            "Your question",
            placeholder="e.g. Where is my order?",
        )
        submitted = st.form_submit_button(
            "⌕  Search articles",
            use_container_width=True,
        )

    if submitted:
        if not question.strip():
            st.warning("Please enter a question first.")
        else:
            with st.spinner("Finding relevant articles..."):
                try:
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
                                    f"Article ID: "
                                    f"{article.get('article_id', 'N/A')}"
                                )
                                st.write(
                                    article.get("content", "No content available.")
                                )
                                similarity = article.get("similarity")
                                if similarity is not None:
                                    st.progress(
                                        max(0.0, min(1.0, float(similarity))),
                                        text=f"Similarity: {float(similarity):.0%}",
                                    )
                    else:
                        st.info("No relevant articles found.")

                except (RuntimeError, ValueError, TypeError) as error:
                    show_error(error)


# ---------- SIMILAR QUERIES ----------
elif page == "Similar Queries":
    st.markdown('<div class="eyebrow">CUSTOMER INSIGHTS</div>',
                unsafe_allow_html=True)
    st.title("Similar Queries")
    st.write("Explore customer questions that have similar wording or meaning.")

    if st.button("↻  Load query insights"):
        with st.spinner("Loading similar queries..."):
            try:
                data = get_similar_queries()
                show_results_table(data.get("results", []))
            except RuntimeError as error:
                show_error(error)


# ---------- ARTICLE AUDIT ----------
elif page == "Article Audit":
    st.markdown('<div class="eyebrow">CONTENT QUALITY</div>',
                unsafe_allow_html=True)
    st.title("Article Audit")
    st.write("Review potentially duplicate or outdated knowledge base articles.")

    if st.button("⌕  Run content audit"):
        with st.spinner("Auditing articles..."):
            try:
                data = get_article_audit()
                show_results_table(data.get("results", []))
            except RuntimeError as error:
                show_error(error)


# ---------- RECOMMENDATIONS ----------
elif page == "Recommendations":
    st.markdown('<div class="eyebrow">CONTINUOUS IMPROVEMENT</div>',
                unsafe_allow_html=True)
    st.title("Knowledge Gap Recommendations")
    st.write("Find topics that may need clearer queries or new help articles.")

    with st.form("recommendation_form"):
        question = st.text_input(
            "Customer question",
            placeholder="e.g. How can I track my order?",
        )
        submitted = st.form_submit_button(
            "✦  Generate recommendations",
            use_container_width=True,
        )

    if submitted:
        if not question.strip():
            st.warning("Please enter a customer question.")
        else:
            with st.spinner("Analysing knowledge gaps..."):
                try:
                    data = get_recommendations(question.strip())

                    st.markdown("### Rewritten query")
                    st.markdown(
                        f"""
                        <div class="info-panel">
                            <strong>{data.get('rewritten_query', 'Not provided')}</strong>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown("### Suggested improvements")
                    recommendations = data.get("recommendations", [])

                    if recommendations:
                        show_results_table(recommendations)
                    else:
                        st.info("No recommendations returned.")

                except RuntimeError as error:
                    show_error(error)


# ---------- FOOTER ----------
st.markdown(
    """
    <div class="footer">
        KnowledgeIQ · Knowledge Base Improvement Advisory Agent<br>
        Built with Streamlit · Connected through FastAPI REST APIs
    </div>
    """,
    unsafe_allow_html=True,
)
