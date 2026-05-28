import streamlit as st
from langchain_community.llms import Ollama


st.set_page_config(
    page_title="AI Meeting Notes Summarizer",
    page_icon="📝",
    layout="centered"
)


if "reset_key" not in st.session_state:
    st.session_state["reset_key"] = 1

st.title("✉️ AI Meeting Notes Summarizer")
st.caption("🌐 Powered by Local Ollama LLM, LangChain & Streamlit")

st.markdown("""
### 📋 Description:
An AI Meeting Notes Summarizer is a tool that automates the transcription and documentation of your 
meetings. By processing text transcripts, it instantly extracts key takeaways, decisions, 
and action items, allowing teams to focus on the conversation rather than taking manual notes.
""")

st.divider()


with st.container(key=f"summarizer_wrapper_{st.session_state['reset_key']}"):


    st.subheader("📥 Provide Meeting Transcript")
    
    input_method = st.radio(" Type of input format:", ["Paste Text Transcript", "Upload Text File (.txt)"])
    transcript_text = ""

    if input_method == "Paste Text Transcript":
        transcript_text = st.text_area(
            "Paste the raw meeting transcript here in the space provided below :",
            placeholder="Speaker 1: Hello team...\nSpeaker 2: Regarding the database architecture setup...",
            height=200,
            key=f"text_area_{st.session_state['reset_key']}"
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload the transcript text file below:",
            type=["txt"],
            key=f"file_uploader_{st.session_state['reset_key']}"
        )
        if uploaded_file is not None:
            transcript_text = uploaded_file.read().decode("utf-8")


    if transcript_text.strip() != "":
        st.divider()
        st.subheader("🤖 Run AI Summarization for Notes!")
        
        if st.button("🚀 Generate Executive Summary", use_container_width=True):
            status_text = st.empty()
            progress_bar = st.progress(0)
            
            try:
                status_text.text(" Processing transcript structural layers...")
                progress_bar.progress(30)
                
                
                llm = Ollama(model="llama3")
                
                
                prompt = f"""
                You are an expert corporate secretary and business analyst. Analyze the following meeting transcript text and compile an executive summary record.
                
                MEETING TRANSCRIPT:
                {transcript_text}
                
                Your task is to extract information and structure it exactly into these four sections:
                
                ### 🎯 Executive Summary
                [Provide a concise, high-level paragraph summarizing the overall purpose and outcome of the meeting]
                
                ### 📌 Key Discussion Points
                * [Bullet point highlighting major discussion topic A]
                * [Bullet point highlighting major discussion topic B]
                * [Bullet point highlighting major discussion topic C]
                
                ### ✅ Action Items & Assignments
                * [Action Item 1] - Assigned to: [Name or Team Responsibilities, if mentioned, otherwise leave broad]
                * [Action Item 2] - Assigned to: [Name or Team Responsibilities]
                
                ### 🗓️ Next Steps / Deadlines
                * [List any follow-up dates, future sync milestones, or deadlines mentioned. If none, write "None explicitly stated"]
                
                Start your response directly with the sections. Do not include introductory conversational chit-chat greetings.
                """
                
                progress_bar.progress(60)
                summary_output = llm.invoke(prompt)
                
                progress_bar.progress(100)
                status_text.text("🎯 Completed successfully!")
                st.success("✅ Minutes of Meeting Generated!")
                
            
                st.divider()
                st.markdown(" 💻 Generated in Minutes!!!")
                st.markdown(summary_output)
                
            except Exception as e:
                st.error(f"❌ Processing Error: {e}")
                st.info("💡 Ensure your local application environment is active and you have running in your terminal background.")

st.write("")
if st.button("🗑️ Clear Dashboard & Reset", type="secondary", use_container_width=True):
    st.session_state["reset_key"] += 1
    
    for key in list(st.session_state.keys()):
        if key != "reset_key":
            del st.session_state[key]
            
    st.rerun()