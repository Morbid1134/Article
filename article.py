import sys
import os
import argparse
from typing import List
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from faster_whisper import WhisperModel
from langchain_community.llms.ollama import Ollama

# Initialize models
model_size = "medium.en"
model = WhisperModel(model_size, device="cpu", compute_type="int8")
summarizer = Ollama(model="llama3", temperature=0)

class verbose:
    """ANSI color codes for terminal output."""
    STOP = '\033[0m'
    UNDERLINE = '\033[4m'
    BOLD = '\033[1m'
    INFO = f'\033[92m{BOLD} [INFO] {STOP}'
    WARNING = f'\033[93m{BOLD} [WARNING] {STOP}'
    ERROR = f'\033[91m{BOLD} [ERROR] {STOP}'

def parse_args():
    parser = argparse.ArgumentParser(description="Process audio/video files.")
    parser.add_argument("files", metavar="file", type=str, nargs="+", help="Input files (audio or video)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose info and errors")
    parser.add_argument("-w", "--whisper", action="store", help="Change whisper model")
    parser.add_argument("-o", "--ollama", action="store", help="Change ollama model")
    parser.add_argument("-t", "--transcript", action="store_true", help="Create transcript file")
    parser.add_argument("-a", "--article", action="store_true", help="Create article file")
    return parser.parse_args()

def normalize_audio(audio_path: str, verbose_mode: bool) -> str:
    try:
        if verbose_mode:
            print(f"{verbose.INFO} Normalizing audio...")
        sound = AudioSegment.from_file(audio_path)
        change_in_dBFS = -20.0 - sound.dBFS
        normalized_sound = sound.apply_gain(change_in_dBFS)
        normalized_audio_path = f"{os.path.splitext(audio_path)[0]}_normalized.wav"
        normalized_sound.export(normalized_audio_path, format="wav")
        if verbose_mode:
            print(f"{verbose.INFO} Normalized audio saved to {verbose.UNDERLINE}{normalized_audio_path}{verbose.STOP}")
        return normalized_audio_path
    except Exception as e:
        if verbose_mode:
            print(f"{verbose.ERROR} Failed to normalize audio: {e}")
        sys.exit(1)

def extract_audio_from_video(video_path: str, verbose_mode: bool) -> str:
    try:
        if verbose_mode:
            print(f"{verbose.INFO} Extracting audio from video...")
        audio_path = f"{os.path.splitext(video_path)[0]}_extracted_audio.wav"
        with VideoFileClip(video_path) as video:
            video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        if verbose_mode:
            print(f"{verbose.INFO} Audio extracted to {verbose.UNDERLINE}{audio_path}{verbose.STOP}")
        return audio_path
    except Exception as e:
        if verbose_mode:
            print(f"{verbose.ERROR} Failed to extract audio from video: {e}")
        sys.exit(1)

def save_text_to_file(text: str, output_file: str, verbose_mode: bool) -> None:
    try:
        if verbose_mode:
            print(f"{verbose.INFO} Saving text to file...")
        with open(output_file, 'w') as file:
            file.write(text)
        if verbose_mode:
            print(f"{verbose.INFO} Text saved to {verbose.UNDERLINE}{output_file}{verbose.STOP}")
    except Exception as e:
        if verbose_mode:
            print(f"{verbose.ERROR} Failed to save text: {e}")
        sys.exit(1)

def process_file(file: str, args) -> None:


    if args.whisper:
        model = WhisperModel(args.whisper, device="cpu", compute_type="int8")
        if args.verbose:
            print(f"{verbose.INFO} Whisper model changed to {args.whisper}")

    if args.ollama:
        global summarizer
        summarizer = Ollama(model=args.ollama, temperature=0)
        if args.verbose:
            print(f"{verbose.INFO} Ollama model changed to {args.ollama}")

    try:
        if args.verbose:
            print(f"{verbose.INFO} Processing file: {verbose.UNDERLINE}{file}{verbose.STOP}")
        file_extension = os.path.splitext(file)[1].lower()
        base_name = os.path.splitext(os.path.basename(file))[0]

        if file_extension in ['.mp4', '.mov', '.avi', '.mkv']:
            if args.verbose:
                print(f"{verbose.INFO} File is a video. Extracting audio...")
            file = extract_audio_from_video(file, args.verbose)
        
        normalized_file = normalize_audio(file, args.verbose)
        
        segments, _ = model.transcribe(normalized_file, beam_size=5)
        transcript = " ".join([segment.text for segment in segments])
        
        article = summarizer.invoke(f'With the transcript of a video, create a digestible article with all the crucial information that the viewer should know. TRANSCRIPT: "{transcript}"')
        
        if args.transcript or args.article:
            if args.transcript:
                transcript_file = f"{base_name}_transcript.md"
                save_text_to_file(transcript, transcript_file, args.verbose)
            if args.article:
                article_file = f"{base_name}_article.md"
                save_text_to_file(article, article_file, args.verbose)

        if file_extension in ['.mp4', '.mov', '.avi', '.mkv']:
            os.remove(file)
            if args.verbose:
                print(f"{verbose.INFO} Deleted extracted audio file.")
        os.remove(normalized_file)
        if args.verbose:
            print(f"{verbose.INFO} Deleted normalized audio file.")

        if args.verbose:
            print(f"{verbose.INFO} Process for {verbose.UNDERLINE}{file}{verbose.STOP} completed successfully.")
        
    except Exception as e:
        if args.verbose:
            print(f"{verbose.ERROR} An error occurred while processing {verbose.UNDERLINE}{file}{verbose.STOP}: {e}")
        sys.exit(1)

def main(args) -> None:
    for file in args.files:
        if not os.path.isfile(file):
            if args.verbose:
                print(f"{verbose.ERROR} The file {verbose.UNDERLINE}{file}{verbose.STOP} does not exist.")
            continue
        process_file(file, args)

if __name__ == "__main__":
    args = parse_args()
    main(args)
