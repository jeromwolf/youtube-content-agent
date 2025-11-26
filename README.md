# YouTube Content Agent 🎬

This agent helps you create high-quality Korean YouTube content from English videos.

## Features
- **Transcript Extraction**: Automatically pulls English transcripts from YouTube videos.
- **AI Scriptwriting**: Uses GPT-4o to summarize and rewrite the content into an engaging Korean script.
- **Voiceover Generation**: Uses OpenAI's TTS (Text-to-Speech) to generate professional-grade voiceovers.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Agent**:
    ```bash
    streamlit run app.py
    ```

3.  **Usage**:
    - Enter your OpenAI API Key in the sidebar.
    - Paste a YouTube URL.
    - Click "Generate Content".
    - Download the script and audio!

## Notes
- You need an OpenAI API Key with access to GPT-4 and TTS models.
- The audio generation is limited to the first 4096 characters in this version to manage costs.
