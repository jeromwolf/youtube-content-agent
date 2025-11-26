import os
import json
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from openai import OpenAI
import re

class YouTubeContentAgent:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        self.llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o", openai_api_key=openai_api_key)
        self.client = OpenAI(api_key=openai_api_key)

# ... (skip to generate_metadata)

    def generate_metadata(self, script):
        """Generates SEO-optimized YouTube metadata (Title, Description, Tags) in JSON format."""
        system_prompt = """
        You are a YouTube Growth Hacker. Your goal is to generate metadata that maximizes Click-Through Rate (CTR) and Watch Time.
        
        You MUST return a valid JSON object with the following keys:
        - "title": <Click-baity, intriguing Korean title>
        - "description": <3-4 sentences summary + hashtags>
        - "tags": <Comma separated keywords>
        - "thumbnail_text": <A very short, punchy Korean phrase (2-5 words) to be written ON the thumbnail image. e.g. "충격적인 진실", "이것만 알면 끝">
        
        Do not include markdown formatting (```json). Just the raw JSON string.
        """
        
        user_prompt = f"""
        Based on this script, generate the best possible YouTube metadata:
        
        "{script[:10000]}"
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        try:
            # Clean up potential markdown code blocks if the LLM adds them
            content = response.content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
        except Exception as e:
            # Fallback if JSON parsing fails
            return {
                "title": "Error generating metadata",
                "description": response.content,
                "tags": "",
                "thumbnail_text": "Video Summary"
            }

    def generate_thumbnail(self, script, overlay_text=""):
        """Generates a high-quality thumbnail image using DALL-E 3."""
        try:
            # 1. Generate a prompt for DALL-E 3 based on the script
            prompt_generation_msg = [
                SystemMessage(content="You are an expert Art Director. Create a detailed text prompt for an AI image generator (DALL-E 3) to create a high-CTR YouTube thumbnail. Focus on visual elements, emotions, lighting, and composition."),
                HumanMessage(content=f"Create an image prompt for this video script: {script[:3000]}. \n\nIMPORTANT: The image MUST include the following text written clearly in Korean: '{overlay_text}'. The text should be large, bold, and easy to read.")
            ]
            dalle_prompt = self.llm.invoke(prompt_generation_msg).content
            
            # 2. Generate the image
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=dalle_prompt,
                size="1792x1024", # Landscape format for YouTube
                quality="standard",
                n=1,
            )
            
            return response.data[0].url
        except Exception as e:
            raise Exception(f"Thumbnail generation failed: {str(e)}")

    def extract_video_id(self, url):
        """Extracts the video ID from a YouTube URL."""
        video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        if video_id_match:
            return video_id_match.group(1)
        return None

    def get_transcript(self, video_id):
        """Fetches the transcript of the video."""
        try:
            # The installed version of youtube-transcript-api (v1.2.3) requires instantiation
            # and uses .fetch() instead of the static .get_transcript()
            api = YouTubeTranscriptApi()
            transcript_items = api.fetch(video_id)
            
            # The items are objects with a .text attribute
            return " ".join([item.text for item in transcript_items])
            
        except Exception as e:
            raise Exception(f"Could not retrieve transcript: {str(e)}")

    def generate_script(self, transcript):
        """Generates an engaging Korean YouTube script from the English transcript."""
        
        system_prompt = """
        You are a professional YouTube content creator and scriptwriter. 
        Your goal is to take an English transcript of a video and convert it into a highly engaging, helpful, and high-quality Korean YouTube script.
        
        **CRITICAL GOAL**: The user wants a **long-form, detailed video** (aiming for 5 to 10 minutes of reading time). 
        Do NOT summarize briefly. You must retain details, examples, and nuances from the original video.
        
        Guidelines:
        1. **Target Audience**: General Korean audience interested in self-improvement, tech, or knowledge.
        2. **Tone**: Energetic, professional yet friendly (Gu-eo-che). Like a top-tier Korean YouTuber (e.g., Syuka World, EO).
        3. **Length & Depth**: 
           - The script should be substantial. 
           - Expand on key points with explanations. 
           - Include specific examples mentioned in the transcript.
           - If the transcript is long, cover all major sections in detail.
        4. **Structure**:
           - **Hook**: Strong attention grabber (1 min).
           - **Body**: Detailed breakdown of points. Use transitional phrases to keep flow. (3-8 mins).
           - **Conclusion**: Summary and Call to Action (1 min).
        5. **Formatting**: Use clear markers like [Intro], [Body], [Outro].
        6. **Pronunciation**: Write English proper nouns in **Hangul** (Korean alphabet) to ensure correct pronunciation by TTS (e.g., write "Palantir" as "팔란티어", not "Palantir").
        """

        user_prompt = f"""
        Here is the English transcript of a YouTube video:
        
        "{transcript[:30000]}" 
        
        Please write a FULL, DETAILED script in Korean. 
        It should be long enough to create a 5-10 minute video.
        Don't leave out interesting details.
        Remember to write proper nouns in Hangul.
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = self.llm.invoke(messages)
        return response.content

    def fix_pronunciation(self, text):
        """Replaces words with their correct Hangul pronunciation."""
        # You can expand this dictionary as needed
        corrections = {
            "Palantir": "팔란티어",
            "palantir": "팔란티어",
            "팔란터": "팔란티어", # Fixing common mispronunciations/typos
            "AI": "에이아이",
            "GPT": "지피티",
            "LLM": "엘엘엠"
        }
        for term, replacement in corrections.items():
            text = text.replace(term, replacement)
        return text

    def generate_audio(self, text, voice="onyx"):
        """Generates audio from the script using OpenAI TTS, handling long text by chunking."""
        try:
            # Apply pronunciation fixes first
            text = self.fix_pronunciation(text)

            # OpenAI TTS has a 4096 char limit. We need to chunk the text.
            # Simple chunking by paragraphs or length.
            max_chars = 4000
            chunks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
            
            combined_audio = b""
            
            for chunk in chunks:
                if not chunk.strip():
                    continue
                response = self.client.audio.speech.create(
                    model="tts-1",
                    voice=voice,
                    input=chunk
                )
                combined_audio += response.content
                
            return combined_audio
        except Exception as e:
            raise Exception(f"Audio generation failed: {str(e)}")



    def generate_metadata(self, script):
        """Generates SEO-optimized YouTube metadata (Title, Description, Tags) in JSON format."""
        system_prompt = """
        You are a YouTube Growth Hacker. Your goal is to generate metadata that maximizes Click-Through Rate (CTR) and Watch Time.
        
        You MUST return a valid JSON object with the following keys:
        - "title": <Click-baity, intriguing Korean title>
        - "description": <3-4 sentences summary + hashtags>
        - "tags": <Comma separated keywords>
        - "thumbnail_text": <A very short, punchy Korean phrase (2-5 words) to be written ON the thumbnail image. e.g. "충격적인 진실", "이것만 알면 끝">
        
        Do not include markdown formatting (```json). Just the raw JSON string.
        """
        
        user_prompt = f"""
        Based on this script, generate the best possible YouTube metadata:
        
        "{script[:10000]}"
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        try:
            # Clean up potential markdown code blocks if the LLM adds them
            content = response.content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
        except Exception as e:
            # Fallback if JSON parsing fails
            return {
                "title": "Error generating metadata",
                "description": response.content,
                "tags": "",
                "thumbnail_text": "Video Summary"
            }

    def generate_thumbnail(self, script, overlay_text=""):
        """Generates a high-quality thumbnail image using DALL-E 3."""
        try:
            # 1. Generate a prompt for DALL-E 3 based on the script
            prompt_generation_msg = [
                SystemMessage(content="You are an expert Art Director. Create a detailed text prompt for an AI image generator (DALL-E 3) to create a high-CTR YouTube thumbnail. Focus on visual elements, emotions, lighting, and composition."),
                HumanMessage(content=f"""
                Create an image prompt for this video script: {script[:3000]}. 
                
                **CRITICAL REQUIREMENTS**:
                1. **NO YouTube UI**: Do NOT include any YouTube logos, play buttons, progress bars, or interface icons. The image should be a clean, cinematic illustration or photo.
                2. **TEXT OVERLAY**: The image MUST feature the text '{overlay_text}' written in **Korean**. 
                   - The text should be a **bold, cinematic title** integrated into the scene (e.g., neon sign, floating 3D text, or bold typography on a clear background).
                   - Ensure the text is large, legible, and the focal point.
                """)
            ]
            dalle_prompt = self.llm.invoke(prompt_generation_msg).content
            
            # 2. Generate the image
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=dalle_prompt,
                size="1792x1024", # Landscape format for YouTube
                quality="standard",
                n=1,
            )
            
            return response.data[0].url
        except Exception as e:
            raise Exception(f"Thumbnail generation failed: {str(e)}")

    def process_video(self, url):
        """Orchestrates the full flow."""
        video_id = self.extract_video_id(url)
        if not video_id:
            return {"error": "Invalid YouTube URL"}

        try:
            # 1. Get Transcript
            transcript = self.get_transcript(video_id)
            
            # 2. Generate Script
            script = self.generate_script(transcript)
            
            # 3. Generate Audio (Preview - first 4096 chars for now to save cost/complexity)
            # In a real app, we would chunk the script and stitch the audio.
            audio_data = self.generate_audio(script)
            
            return {
                "transcript": transcript,
                "script": script,
                "audio": audio_data
            }
        except Exception as e:
            return {"error": str(e)}
