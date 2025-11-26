# YouTube Content Agent 🎬

This agent helps you create high-quality Korean YouTube content from English videos.

## 🚀 Project Background & Vision

**"Too much information, too little time."**

English content on YouTube is exploding with valuable information, but consuming it all—especially with language barriers—is time-consuming. We need a way to quickly digest high-quality global knowledge.

**AI ON** is a project designed to bridge this gap. It acts as an **AI Curator**, selecting excellent content and providing concise, engaging summaries in Korean.

### Key Goals:
- **Efficiency**: Drastically reduce the time needed to consume English video content through smart summarization.
- **Expansion**: While starting with YouTube, the roadmap includes expanding to **academic papers** and technical documentation.
- **Service Vision**: To build an "AI ON" service that delivers the world's best knowledge to you, translated and summarized instantly.

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
