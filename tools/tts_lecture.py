#!/usr/bin/env python3
"""Generate audio-guide files in the "calm lecturer" voice (see VOICE_GUIDE.md).

Usage:
    export ELEVENLABS_API_KEY=...            # never commit the key
    python3 tools/tts_lecture.py scripts.json out_dir/ [--lang de]

scripts.json maps output names to texts, for example:
    {"01-intro": "[calm] Hello, dear friends. [pauses] ...",
     "02-campo": "[calm] Ecco. [long pause] Piazza del Campo. ..."}

Each text becomes out_dir/<name>.mp3, exactly as ElevenLabs delivers it
(MP3 44.1 kHz 192 kbps, no post-processing).
"""
import argparse
import concurrent.futures as cf
import json
import os
import sys
import time
import urllib.error
import urllib.request

VOICE_ID = "cgSgspJ2msm6clMCkdW9"          # Jessica
MODEL_ID = "eleven_v4"
SETTINGS = {"stability": 0.45, "similarity_boost": 0.75}
OUTPUT_FORMAT = "mp3_44100_192"
PARALLEL = 3                               # Creator plan allows 5 concurrent requests
MAX_CHARS = 2300                           # longer requests sometimes time out


def synthesize(text, out_path, api_key, lang=None, retries=5):
    body = {"text": text, "model_id": MODEL_ID, "voice_settings": SETTINGS}
    if lang:
        body["language_code"] = lang
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format={OUTPUT_FORMAT}"
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"xi-api-key": api_key, "Content-Type": "application/json"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = r.read()
            with open(out_path, "wb") as f:
                f.write(data)
            return "ok"
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf8", "ignore")[:300]
            if "quota" in msg.lower() or "credit" in msg.lower():
                return "OUT OF CREDITS: " + msg
            if e.code in (401, 403):
                return f"HTTP {e.code}: {msg}"
            last = f"HTTP {e.code}: {msg}"
        except Exception as e:  # timeouts, connection resets
            last = str(e)
        time.sleep(6 * (attempt + 1))
    return "FAILED: " + last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scripts")
    ap.add_argument("out_dir")
    ap.add_argument("--lang", help="optional language code, e.g. en, de, ru, it")
    args = ap.parse_args()
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("Set ELEVENLABS_API_KEY first.")
    scripts = json.load(open(args.scripts, encoding="utf8"))
    os.makedirs(args.out_dir, exist_ok=True)
    for name, text in scripts.items():
        if len(text) > MAX_CHARS:
            print(f"warning: {name} has {len(text)} characters; consider splitting it", file=sys.stderr)
    total = sum(len(t) for t in scripts.values())
    print(f"{len(scripts)} files, {total} characters (≈ {total} credits)")

    def job(item):
        name, text = item
        out = os.path.join(args.out_dir, f"{name}.mp3")
        if os.path.exists(out) and os.path.getsize(out) > 20000:
            return name, "exists"
        return name, synthesize(text, out, key, args.lang)

    with cf.ThreadPoolExecutor(PARALLEL) as ex:
        for name, status in ex.map(job, scripts.items()):
            print(f"{name}: {status}", flush=True)


if __name__ == "__main__":
    main()
