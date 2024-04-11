import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re
import openai

# Set up OpenAI API key
openai.api_key = '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'

# Function to retrieve transcript from YouTube video using its ID
def get_video_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([line['text'] for line in transcript_list])
        return transcript
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Function to save transcript to a file
def save_transcript(transcript):
    try:
        with open('transcript.txt', 'w') as f:
            f.write(transcript)
        # st.success("Transcript saved to transcript.txt")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Function to chunk the transcript into smaller parts
def chunk_transcript(transcript, chunk_size):
    chunks = []
    words = re.findall(r'\b\w+\b', transcript)
    num_words = len(words)
    for i in range(0, num_words, chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# Function to generate summary using OpenAI API
def generate_summary(transcript_chunk):
    prompt = f"Summarize the following educational video transcript and give a complete summary in 300 words only:\n{transcript_chunk}\n\nSummary:"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=300
    )
    summary = response.choices[0].text.strip()
    return summary

# Function to main summary generation process
def generate_summary_process(transcript):
    word_count = len(re.findall(r'\b\w+\b', transcript))
    if word_count > 3747:
        chunk_size = 3300
        transcript_chunks = chunk_transcript(transcript, chunk_size)
        final_summary = ""
        for chunk in transcript_chunks:
            summary = generate_summary(chunk)
            final_summary += summary + " "
        return final_summary
    else:
        print("no need to chunk\n")
        return generate_summary(transcript)

# Streamlit app
def main():
    st.title("EduPrep AI 🤖")
    st.markdown("<small>Educational Video Summary Generator</small>", unsafe_allow_html=True)
    
    # Text input for video URL
    video_url = st.text_input("Paste the URL of the educational video:")
    
    # Button to generate summary
    if st.button("Generate Summary"):
        if video_url:
            try:
                video_id = video_url.split("=")[-1]
                transcript = get_video_transcript(video_id)
                if transcript:
                    summary = generate_summary_process(transcript)
                    st.subheader("Summary:")
                    st.write(summary)
                    save_transcript(transcript)
                else:
                    st.error("Failed to retrieve the transcript.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please input the video URL first.")

if __name__ == "__main__":
    main()
