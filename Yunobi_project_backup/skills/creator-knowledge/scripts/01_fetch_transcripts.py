#!/usr/bin/env python3
"""
Step 1: Fetch all transcripts from @kallawaymarketing YouTube channel.

Usage:
    # Method A: Fetch from YouTube directly (free, no API key)
    python scripts/01_fetch_transcripts.py

    # Method B: Parse a bulk file downloaded from downloadyoutubetranscripts.com
    python scripts/01_fetch_transcripts.py --parse-bulk data/raw-transcripts/bulk_file.txt

    # Method C: Fetch a single video for testing
    python scripts/01_fetch_transcripts.py --video-id VIDEO_ID

Output:
    data/raw-transcripts/*.txt (one file per video)
    data/raw-transcripts/manifest.json (metadata index)
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

DATA_DIR = Path("data/raw-transcripts")


def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_filename(title: str) -> str:
    """Convert video title to safe filename."""
    clean = re.sub(r'[^\w\s-]', '', title.lower())
    clean = re.sub(r'[\s]+', '-', clean.strip())
    return clean[:80]


def fetch_from_youtube(channel_handle: str = "kallawaymarketing"):
    """Method A: Use scrapetube + youtube-transcript-api (free, no API key)."""
    try:
        import scrapetube
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api.formatters import TextFormatter
    except ImportError:
        print("Install dependencies: pip install youtube-transcript-api scrapetube")
        sys.exit(1)

    print(f"Fetching video list from @{channel_handle}...")
    videos = list(scrapetube.get_channel(
        channel_url=f"https://www.youtube.com/@{channel_handle}"
    ))
    print(f"Found {len(videos)} videos")

    ytt_api = YouTubeTranscriptApi()
    formatter = TextFormatter()
    manifest = []
    
    for i, video in enumerate(videos):
        video_id = video['videoId']
        title = video.get('title', {}).get('runs', [{}])[0].get('text', video_id)
        view_count = video.get('viewCountText', {}).get('simpleText', 'N/A')
        duration = video.get('lengthText', {}).get('simpleText', 'N/A')
        
        filename = f"{i+1:03d}_{sanitize_filename(title)}.txt"
        filepath = DATA_DIR / filename
        
        if filepath.exists():
            print(f"  [{i+1}/{len(videos)}] SKIP (exists): {title[:60]}")
            manifest.append({
                "index": i + 1,
                "video_id": video_id,
                "title": title,
                "views": view_count,
                "duration": duration,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "file": filename
            })
            continue

        print(f"  [{i+1}/{len(videos)}] Fetching: {title[:60]}...")
        
        try:
            transcript = ytt_api.fetch(video_id)
            text = formatter.format_transcript(transcript)
            
            # Write with metadata header
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"TITLE: {title}\n")
                f.write(f"VIDEO_ID: {video_id}\n")
                f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
                f.write(f"VIEWS: {view_count}\n")
                f.write(f"DURATION: {duration}\n")
                f.write(f"---\n\n")
                f.write(text)
            
            manifest.append({
                "index": i + 1,
                "video_id": video_id,
                "title": title,
                "views": view_count,
                "duration": duration,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "file": filename
            })
            
            # Rate limit respect
            time.sleep(1)
            
        except Exception as e:
            print(f"    ERROR: {e}")
            manifest.append({
                "index": i + 1,
                "video_id": video_id,
                "title": title,
                "views": view_count,
                "duration": duration,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "file": None,
                "error": str(e)
            })
    
    # Save manifest
    manifest_path = DATA_DIR / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    success = len([m for m in manifest if m.get('file')])
    print(f"\nDone! {success}/{len(videos)} transcripts saved to {DATA_DIR}/")
    print(f"Manifest: {manifest_path}")


def parse_bulk_file(filepath: str):
    """Method B: Parse concatenated bulk download from downloadyoutubetranscripts.com."""
    print(f"Parsing bulk file: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Common delimiters used by bulk download tools
    # Try splitting by video title/URL patterns
    # Pattern 1: "Title: ...\nVideo ID: ...\nURL: ...\n---"
    # Pattern 2: "=== VIDEO TITLE ===" separators
    # Pattern 3: URL-based splitting "https://www.youtube.com/watch?v="
    
    # Auto-detect format
    if "Video ID:" in content or "VIDEO_ID:" in content:
        # Already has metadata headers
        sections = re.split(r'\n(?=(?:TITLE|Title):)', content)
    elif "===" in content:
        sections = re.split(r'\n={3,}\n', content)
    elif "https://www.youtube.com/watch?v=" in content:
        sections = re.split(r'\n(?=https://www\.youtube\.com/watch\?v=)', content)
    else:
        # Try splitting by double newlines with URL pattern
        sections = re.split(r'\n{3,}', content)
    
    manifest = []
    
    for i, section in enumerate(sections):
        section = section.strip()
        if not section or len(section) < 50:
            continue
        
        # Extract metadata if present
        title_match = re.search(r'(?:TITLE|Title):\s*(.+)', section)
        id_match = re.search(r'(?:VIDEO_ID|Video ID):\s*(.+)', section)
        url_match = re.search(r'(?:URL|Video URL):\s*(https://[^\s]+)', section)
        views_match = re.search(r'(?:VIEWS|Views|View Count):\s*(.+)', section)
        
        title = title_match.group(1).strip() if title_match else f"video_{i+1}"
        video_id = id_match.group(1).strip() if id_match else "unknown"
        url = url_match.group(1).strip() if url_match else ""
        views = views_match.group(1).strip() if views_match else "N/A"
        
        # Extract video_id from URL if not found
        if video_id == "unknown" and url:
            vid_match = re.search(r'v=([a-zA-Z0-9_-]{11})', url)
            if vid_match:
                video_id = vid_match.group(1)
        
        filename = f"{i+1:03d}_{sanitize_filename(title)}.txt"
        filepath_out = DATA_DIR / filename
        
        with open(filepath_out, 'w', encoding='utf-8') as f:
            f.write(section)
        
        manifest.append({
            "index": i + 1,
            "video_id": video_id,
            "title": title,
            "views": views,
            "url": url,
            "file": filename
        })
    
    # Save manifest
    manifest_path = DATA_DIR / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"Parsed {len(manifest)} transcripts to {DATA_DIR}/")
    print(f"Manifest: {manifest_path}")


def fetch_single_video(video_id: str):
    """Method C: Fetch a single video for testing."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api.formatters import TextFormatter
    except ImportError:
        print("Install: pip install youtube-transcript-api")
        sys.exit(1)
    
    print(f"Fetching transcript for {video_id}...")
    ytt_api = YouTubeTranscriptApi()
    formatter = TextFormatter()
    
    transcript = ytt_api.fetch(video_id)
    text = formatter.format_transcript(transcript)
    
    filepath = DATA_DIR / f"test_{video_id}.txt"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"VIDEO_ID: {video_id}\n")
        f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
        f.write(f"---\n\n")
        f.write(text)
    
    print(f"Saved to {filepath}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Kallaway transcripts")
    parser.add_argument("--parse-bulk", type=str, help="Parse a bulk download file")
    parser.add_argument("--video-id", type=str, help="Fetch a single video")
    parser.add_argument("--channel", type=str, default="kallawaymarketing", 
                        help="YouTube channel handle")
    args = parser.parse_args()
    
    ensure_dirs()
    
    if args.parse_bulk:
        parse_bulk_file(args.parse_bulk)
    elif args.video_id:
        fetch_single_video(args.video_id)
    else:
        fetch_from_youtube(args.channel)
