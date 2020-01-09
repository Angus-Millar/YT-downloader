# ANGUS MILLAR 01/20
# YT PLAYLIST/VIDEO DOWNLOADER

"""
# Requires: youtube_dl module - (https://github.com/ytdl-org/youtube-dl/blob/master/README.md#readme)
# Requires: ffmpeg (Windows) -
    (https://m.wikihow.com/Install-FFmpeg-on-Windows)
# Requires: ffmpeg (Mac) -
    (http://jollejolles.com/install-ffmpeg-on-mac-os-x/)
"""

# Usage: python YT_download.py <YT playlist URL> <FORMAT (mp3 or mp4)>

from __future__ import unicode_literals
from youtube_dl import YoutubeDL
import time
import sys
import os
import platform

# Get playlist/video URL and desired download format
def get_URL():
    if len(sys.argv) != 3:
        sys.exit("\nWrong no. of arguments! \nUsage: python " + sys.argv[0] + " <YT playlist/video URL> <format (mp3 or mp4)>\n")
    else:
        URL = sys.argv[1]
        format = sys.argv[2]
    return URL, format
    
# Playlist dld folder on desktop
def desktop_folder():
    if platform.system() == 'Windows':
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    else:
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    return desktop
        
# mp3/mp4 formatting for dld
def dld_format(format, playlist_title):
    if (format == 'mp3' or format == '.mp3'):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '{}/{}/%(title)s.%(ext)s'.format(desktop, playlist_title),
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',}],
        }
    elif (format == 'mp4' or format == '.mp4'):
        ydl_opts = {
            'format': 'best',
            'outtmpl': '{}/{}/%(title)s.%(ext)s'.format(desktop, playlist_title),
        }
    else:
        sys.exit("\nWrong format! Valid formats: mp3 or mp4\n")
    return ydl_opts

# Extract info/URLs from playlist/video
def YT_info(URL):
    if "playlist" in URL:
        # Get info on YT playlist without downloading
        print("\n ---Collecting and downloading YT playlist---\n")
        ydl_playlist_opts = {'outtmpl': '%(id)s%(ext)s', 'quiet':True,}
        with YoutubeDL(ydl_playlist_opts) as ydl:
            result = ydl.extract_info(URL, download=False)
        if 'entries' in result:
            # Extract playlist title and video_url
            for i, item in enumerate(result['entries']):
                videos = [result['entries'][i]['webpage_url'].replace(",", "") for i in range(len(result))]
                folder = result['entries'][0]['playlist'].replace(",", "")
    else:
        # Get info on YT video
        print("\n ---Downloading YT video---\n")
        folder, videos = "YT_downloader", [URL]
    return folder, videos


# Code to run
if __name__ == "__main__":
    # User playlist/video URL and desired download format
    URL, format = get_URL()
    # Playlist dld folder on desktop
    desktop = desktop_folder()
    # YT playlist/video info
    folder, videos = YT_info(URL)
    # Download playlist/video into mp3 or mp4
    ydl_opts = dld_format(format, folder)
    with YoutubeDL(ydl_opts) as ydl:
        start = time.time()
        ydl.download(videos)
        end = time.time()
        print("\n---Time taken for download = {} seconds.---\n"
            .format(int(end - start)))
    


