import os
import platform
import subprocess
import sys
import urllib.request
import zipfile
import tarfile
import shutil

def install_package(package_name):
    """Install a package using pip."""
    subprocess.run([sys.executable, '-m', 'pip', 'install', package_name], check=True)


def is_ffmpeg_installed():
    """Check if ffmpeg is installed next to the script or in PATH."""
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))  
    ffmpeg_exe = os.path.join(base_dir, 'ffmpeg', 'bin', 'ffmpeg.exe')  
    if shutil.which("ffmpeg"):
        return True

    if os.path.exists(ffmpeg_exe) and os.access(ffmpeg_exe, os.X_OK):
        os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_exe)  
        return True

    return False  





def download_ffmpeg():
    """Download and install ffmpeg next to the script/exe, ensuring it's in the correct location."""
    system = platform.system()
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))  
    ffmpeg_dir = os.path.join(base_dir, 'ffmpeg')  
    bin_dir = os.path.join(ffmpeg_dir, 'bin')  

    if system == 'Windows':
        url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
        zip_path = os.path.join(base_dir, 'ffmpeg.zip')
    elif system == 'Darwin':  # macOS
        url = 'https://evermeet.cx/ffmpeg/ffmpeg-6.0.zip'
        zip_path = os.path.join(base_dir, 'ffmpeg.zip')
    elif system == 'Linux':
        url = 'https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-i686-static.tar.xz'
        zip_path = os.path.join(base_dir, 'ffmpeg.tar.xz')
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)

    os.makedirs(bin_dir, exist_ok=True) 

    print(f"Downloading ffmpeg from {url} to {zip_path}...")
    urllib.request.urlretrieve(url, zip_path)
    print("Download complete.")

    print("Extracting ffmpeg...")
    if zip_path.endswith('.zip'):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_dir)
    elif zip_path.endswith('.tar.xz'):
        with tarfile.open(zip_path, 'r:xz') as tar_ref:
            tar_ref.extractall(ffmpeg_dir)
    print("Extraction complete.")

  
    extracted_folder = None
    for item in os.listdir(ffmpeg_dir):
        item_path = os.path.join(ffmpeg_dir, item)
        if os.path.isdir(item_path) and "ffmpeg" in item.lower():
            extracted_folder = item_path
            break

    if extracted_folder:
        extracted_bin = os.path.join(extracted_folder, 'bin', 'ffmpeg.exe')
        if os.path.exists(extracted_bin):
            print(f"Moving ffmpeg.exe from {extracted_bin} to {bin_dir}...")
            shutil.move(extracted_bin, os.path.join(bin_dir, 'ffmpeg.exe'))
            shutil.rmtree(extracted_folder)  
            print("FFmpeg successfully moved to the correct location.")

    os.environ["PATH"] += os.pathsep + bin_dir
    print(f"ffmpeg installed and available at: {os.path.join(bin_dir, 'ffmpeg.exe')}")




import os

def main():
    try:
        import yt_dlp
    except ImportError:
        print("yt-dlp not found. Installing yt-dlp...")
        install_package('yt-dlp')

    if not is_ffmpeg_installed():
        print("ffmpeg not found. Installing ffmpeg...")
        download_ffmpeg()

    from yt_dlp import YoutubeDL

    url = input("Enter the YouTube video URL: ").strip()

    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

    formats = info_dict.get('formats', [])
    video_formats = []

    print("\nAvailable quality options:")
    for f in formats:
        resolution = f.get('format_note', 'Unknown')
        ext = f.get('ext', 'Unknown')
        fps = f.get('fps', 'N/A')
        video_codec = f.get('vcodec', 'none')

        if video_codec != 'none' and ext == "mp4" and resolution not in ["Unknown", "storyboard"]:
            video_formats.append(f)
            print(f"{len(video_formats)}. {resolution} - {ext} ({fps} FPS)")

    if not video_formats:
        print("No valid video formats found. Exiting.")
        return

    choice = input("\nSelect a quality (enter number): ").strip()
    try:
        choice = int(choice)
        selected_format = video_formats[choice - 1]
    except (ValueError, IndexError):
        print("Invalid choice. Exiting.")
        return

    video_format_id = selected_format['format_id']

    best_audio = None
    for f in formats:
        if f.get('acodec') != 'none' and f.get('vcodec') == 'none' and f.get('ext') == 'm4a':
            best_audio = f['format_id']
            break

    ydl_opts = {
        'format': f"{video_format_id}+{best_audio}" if best_audio else video_format_id,
        'merge_output_format': 'mp4',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegFixupM4a'
        }]
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(result)
            print("\nDownload completed successfully.")
            print(f"Video saved as: {file_path}")

            if os.path.exists(file_path):
                try:
                    os.rename(file_path, file_path)
                    print("File is properly closed.")
                except PermissionError:
                    print("File is locked. Restart your system or manually unlock it.")
                    
        except Exception as e:
            print(f"Error during download: {e}")







if __name__ == "__main__":
    main()
