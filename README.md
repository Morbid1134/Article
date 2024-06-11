# Audio and Video Processing Tool

This program processes audio and video files to normalize audio, extract audio from videos, transcribe the audio using the Whisper model, and generate an article summary using the Ollama model.

## Features

- **Audio Normalization**: Normalizes the audio levels of input files.
- **Audio Extraction**: Extracts audio from video files.
- **Transcription**: Transcribes audio to text using the Whisper model.
- **Article Generation**: Generates a summarized article from the transcript using the Ollama model.
- **Verbose Mode**: Provides detailed information about each processing step.

## Dependencies

- `sys`
- `os`
- `argparse`
- `typing`
- `pydub`
- `moviepy`
- `faster_whisper`
- `langchain_community.llms.ollama`

## Installation

1. **Install and navigate to repository**:
   ```bash
   git clone https://github.com/Morbid1134/article
   cd article
   ```
   
2. **Install required Python packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install additional system dependencies**:
    - For `pydub`, you may need to install FFmpeg:
      ```bash
      sudo apt-get install ffmpeg  # For Debian-based systems
      brew install ffmpeg          # For macOS
      ```

## Usage

```bash
python your_script.py [options] file1 file2 ...
```

### Options

- `-v`, `--verbose`: Print verbose info and errors.
- `-w`, `--whisper`: Change the Whisper model.
- `-o`, `--ollama`: Change the Ollama model.
- `-t`, `--transcript`: Create a transcript file.
- `-a`, `--article`: Create an article file.

## Examples

1. **Process a single audio file with transcript generation**:
    ```bash
    python your_script.py -t example_audio.wav
    ```

2. **Process multiple video files with transcript and article generation in verbose mode**:
    ```bash
    python your_script.py -v -t -a example_video1.mp4 example_video2.mov
    ```

## Functionality

### `parse_args()`

Parses command-line arguments.

### `normalize_audio(audio_path: str, verbose_mode: bool) -> str`

Normalizes the audio levels of the input file and saves the normalized audio.

### `extract_audio_from_video(video_path: str, verbose_mode: bool) -> str`

Extracts audio from the given video file and saves it as a WAV file.

### `save_text_to_file(text: str, output_file: str, verbose_mode: bool) -> None`

Saves the provided text to a file.

### `process_file(file: str, args) -> None`

Processes the given file, handling audio normalization, audio extraction from videos, transcription, and article generation.

### `main(args) -> None`

Main function that iterates through the provided files and processes each one.

## Notes

- Ensure your audio and video files are accessible and have appropriate permissions.
- The default Whisper model is `medium.en` and the default Ollama model is `llama3`.

## Troubleshooting

- **File not found**: Ensure the file path is correct and the file exists.
- **Dependencies not found**: Reinstall the required packages using the installation steps provided.
- **Verbose mode output**: Use the `-v` or `--verbose` option to get detailed output for debugging purposes.

For further assistance, refer to the documentation of the respective libraries used.
