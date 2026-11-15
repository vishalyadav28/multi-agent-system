import streamlit as st

from src.agent.agents import writer_chain, critic_chain
from src.pipelines.pipeline import gather_research

st.set_page_config(page_title="Multi-Agent Research", page_icon="🔎")

st.title("🔎 Multi-Agent Research Assistant")
st.caption("Search agent → Reader agent → Writer → Critic")

if "messages" not in st.session_state:
    st.session_state.messages = []


def show_details(msg):
    with st.expander("🧐 Critic feedback"):
        st.markdown(msg["feedback"])
    with st.expander("Search results"):
        st.markdown(msg["search_results"])
    with st.expander("Scraped content"):
        st.markdown(msg["scraped_content"])


# Replay chat history (Streamlit reruns the whole script on every interaction)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            show_details(msg)

if topic := st.chat_input("Ask me to research any topic..."):
    topic = topic.strip()
    st.session_state.messages.append({"role": "user", "content": topic})
    with st.chat_message("user"):
        st.markdown(topic)

    with st.chat_message("assistant"):
        try:
            with st.status("Researching... this can take a minute", expanded=True) as status:
                state = gather_research(topic, on_step=st.write)
                status.update(label="Research gathered", state="complete", expanded=False)

            report = st.write_stream(writer_chain.stream({"topic": topic, "research": state["research"]}))

            with st.expander("🧐 Critic feedback", expanded=True):
                feedback = st.write_stream(critic_chain.stream({"report": report}))
        except Exception as e:
            st.error(f"Pipeline failed: {e}")
            st.stop()

        msg = {"role": "assistant", "content": report, "feedback": feedback,
               "search_results": state["search_results"], "scraped_content": state["scraped_content"]}
        with st.expander("Search results"):
            st.markdown(msg["search_results"])
        with st.expander("Scraped content"):
            st.markdown(msg["scraped_content"])
    st.session_state.messages.append(msg)
