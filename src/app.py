import streamlit as st

from src.pipelines.pipeline import run_research_pipeline

st.set_page_config(page_title="Multi-Agent Research", page_icon="🔎", layout="wide")

st.title("🔎 Multi-Agent Research Assistant")
st.caption("Search agent → Reader agent → Writer → Critic")

topic = st.text_input("Research topic", placeholder="e.g. latest advances in AI agents")

if st.button("Run research", type="primary", disabled=not topic.strip()):
    with st.spinner("Agents are working... this can take a minute"):
        try:
            state = run_research_pipeline(topic.strip())
        except Exception as e:
            st.error(f"Pipeline failed: {e}")
            st.stop()

    st.subheader("📄 Report")
    st.markdown(state["report"])

    st.subheader("🧐 Critic feedback")
    st.markdown(state["feedback"])

    with st.expander("Search results"):
        st.markdown(state["search_results"])

    with st.expander("Scraped content"):
        st.markdown(state["scraped_content"])
