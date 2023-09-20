import yt_dlp as youtube_dl 

def fetch_youtube_link(query):
    ydl_opts = {
        'default_search': 'ytsearch',
        'quiet': True,
        'format': 'bestaudio/best',
        'noplaylist': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(query, download=False)
        if 'entries' in result:
            video = result['entries'][0]
        else:
            video = result
    
    # 여기에서 video['id']를 사용하여 표준 YouTube 링크를 생성합니다.
    video_url = f"https://www.youtube.com/watch?v={video['id']}"
    return video_url  # 이제 URL만 반환합니다.
