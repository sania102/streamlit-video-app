import streamlit as st
import tempfile
import moviepy.editor as mp
import requests
import time
from gtts import gTTS
import os

# AssemblyAI API Key
API_KEY_ASSEMBLYAI = "c7a5b10e31c14fc5817aab0d707c40d2"

# Function to transcribe audio using AssemblyAI
def transcribe_audio_with_assemblyai(audio_path):
    headers = {
        'authorization': API_KEY_ASSEMBLYAI,
        'content-type': 'application/json'
    }

    # Upload the audio to AssemblyAI
    upload_url = 'https://api.assemblyai.com/v2/upload'
    with open(audio_path, 'rb') as audio_file:
        response = requests.post(upload_url, headers=headers, data=audio_file)
    audio_url = response.json()['upload_url']

    # Request transcription
    transcribe_url = "https://api.assemblyai.com/v2/transcript"
    transcript_request = {'audio_url': audio_url}
    response = requests.post(transcribe_url, headers=headers, json=transcript_request)
    transcript_id = response.json()['id']

    # Poll for completion
    status = 'processing'
    while status != 'completed':
        time.sleep(5)
        response = requests.get(f"{transcribe_url}/{transcript_id}", headers=headers)
        status = response.json()['status']

    return response.json()['text']

# GPT-4: Correct transcription using Azure OpenAI (you can replace this if needed)
def gpt4_correct_transcription(transcription):
    # For now, we’ll just return the transcription as-is.
    return transcription

# Text-to-Speech: Function to convert text to speech using gTTS (Google Text-to-Speech)
def text_to_speech_gtts(text):
    # Convert text to speech
    tts = gTTS(text)
    audio_file_path = 'output.mp3'
    tts.save(audio_file_path)  # Save to a file

    return audio_file_path

# Function to replace audio in video using MoviePy
def replace_audio_in_video(video_path, audio_path):
    output_directory = os.path.dirname(video_path)  # Use the same directory as the input video
    output_path = os.path.join(output_directory, "output_with_new_audio.mp4")  # Specify a valid name

    video_clip = mp.VideoFileClip(video_path)  # Load video
    audio_clip = mp.AudioFileClip(audio_path)  # Load new audio

    # Set new audio to video
    final_clip = video_clip.set_audio(audio_clip)

    try:
        final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')  # Use the same codecs
    except Exception as e:
        st.error(f"Error during video processing: {str(e)}")  # Display error if it occurs
        return None

    return output_path

# Main Streamlit App
def main():
    st.title("Video Audio Transcription and Correction App (AssemblyAI + gTTS)")

    video_file = st.file_uploader("Upload a video", type=["mp4"])

    if video_file is not None:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(video_file.read())
        temp_file.close()

        st.video(temp_file.name)

        if st.button("Transcribe and Correct Audio"):
            st.write("Transcribing with AssemblyAI...")
            transcription = transcribe_audio_with_assemblyai(temp_file.name)
            st.write("Original Transcription:", transcription)

            st.write("Correcting transcription using GPT-4...")
            corrected_transcription = gpt4_correct_transcription(transcription)
            st.write("Corrected Transcription:", corrected_transcription)

            st.write("Generating new audio using gTTS Text-to-Speech...")
            audio_path = text_to_speech_gtts(corrected_transcription)

            st.write("Replacing audio in the video...")
            output_video = replace_audio_in_video(temp_file.name, audio_path)

            if output_video:
                st.video(output_video)
                st.success(f"Processed video with corrected audio is ready!")

if __name__ == "__main__":
    main()
