# YouTube Video Downloader

This is a Python-based YouTube video downloader that automatically installs `yt-dlp` and `ffmpeg` if they are not already present. It allows users to select the best available video and audio quality in MP4 format.

## Features

- Automatically installs (if) missing dependencies (`yt-dlp` and `ffmpeg`).
- Downloads and extracts `ffmpeg` if not found in the system.
- Lists available MP4 video formats with resolution and FPS.
- Allows the user to select a preferred quality before downloading.
- Merges the best available audio with the selected video format.
- Ensures the downloaded file is properly closed after completion.

## Prerequisites

### Windows:
- Python 3.x installed with `pip` available in the system.

### Linux/macOS (not tested):
- Python 3.x installed with `pip`.
- `ffmpeg` will be downloaded automatically if missing.

## Installation & Setup

1. **Clone this repository (or download the script manually):**
   ```
   git clone https://github.com/Eslorex/Youtube-Media-Downloader.git
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
   If `requirements.txt` is not available, install `yt-dlp` manually:
   ```
   pip install yt-dlp
   ```

3. **Run the script:**
   ```
   python Youtube Media Downloader.py
   ```

## Usage

1. Run the script
2. Enter the YouTube video URL when prompted.
3. Choose the preferred video quality from the listed options.
4. Done.

## How It Works

- **Dependency Handling:**
  - If `yt-dlp` is missing, it installs it automatically.
  - If `ffmpeg` is missing, it downloads and extracts it in the script directory.

- **Video Selection:**
  - The script lists available MP4 formats with resolution and FPS.
  - The user selects a preferred format.
  - The best audio format (M4A) is selected and merged with the video.

- **Final Steps:**
  - Downloads the video and audio.
  - Merges them using `ffmpeg`.
  - Saves the final file as `title.mp4`.

## Example Run

```
Enter the YouTube video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ

Available quality options:
1. 1080p - mp4 (60 FPS)
2. 720p - mp4 (30 FPS)
3. 480p - mp4 (30 FPS)

Select a quality (enter number): 1

Downloading...
Merging audio...
Download completed successfully.
Video saved as: Rick Astley - Never Gonna Give You Up.mp4
```

## Notes

- If you receive a permission error while renaming the file, try restarting your system or manually unlocking it.
- The script is optimized for MP4 format to ensure compatibility.
- `ffmpeg` is installed in the same directory as the script for easy access.

## Troubleshooting

### "yt-dlp is not recognized" error
   - Run: `pip install yt-dlp`
   - Try: `python -m pip install yt-dlp`

### "ffmpeg not found" error
   - The script should automatically download `ffmpeg`. If it fails, manually download and extract it from:
     - **Windows:** [Gyan Dev FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/)
     - **macOS/Linux:** [FFmpeg Official](https://ffmpeg.org/download.html)

## License

This project is licensed under the MIT License.
