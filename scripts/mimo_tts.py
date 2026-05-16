#!/usr/bin/env python3
"""MiMo TTS wrapper - converts text to speech using Xiaomi MiMo API.

Supports:
- Voice selection: mimo_default, 冰糖, 茉莉, 苏打, 白桦, Mia, Chloe, Milo, Dean
- VoiceDesign: 通过文本描述设计音色
- Style control via user message
- Auto language detection for voice selection

Output: writes audio to {output_path}, prints the path to stdout.
"""
import sys, os, json, base64, urllib.request, re

# Voice mappings
VOICES = {
    "default": "mimo_default",
    "糖糖": "冰糖", "冰糖": "冰糖",
    "茉莉": "茉莉", "moli": "茉莉",
    "苏打": "苏打", "suda": "苏打",
    "白桦": "白桦", "baihua": "白桦",
    "mia": "Mia", "chloe": "Chloe",
    "milo": "Milo", "dean": "Dean",
}

def detect_language(text):
    """Detect if text is primarily Chinese or English."""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(re.findall(r'[a-zA-Z\u4e00-\u9fff]', text))
    if total_chars == 0:
        return "zh"
    return "zh" if chinese_chars / total_chars > 0.3 else "en"

def auto_select_voice(text):
    """Auto-select voice based on text language."""
    lang = detect_language(text)
    if lang == "zh":
        return "茉莉"  # Chinese female
    else:
        return "Mia"  # English female

def load_env_file():
    """Load .env file from Hermes config directory."""
    env_paths = [
        os.path.expanduser("~/AppData/Local/hermes/.env"),
        os.path.expanduser("~/.hermes/.env"),
    ]
    for path in env_paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, value = line.partition("=")
                        key = key.strip()
                        value = value.strip()
                        if key and key not in os.environ:
                            os.environ[key] = value
            break

def parse_voice_prefix(text):
    """Parse voice description from text using [voice: ...] prefix syntax.
    
    Supports:
      [voice: 描述]要说的话        → voicedesign mode
      [voice:冰糖]要说的话         → preset voice (no space after colon)
      [voice:mia]要说的话          → preset voice (english)
      要说的话                     → no prefix, auto mode
    
    Returns (voice_desc_or_name, clean_text, is_design).
    """
    # Match [voice: description] at start of text
    m = re.match(r'^\[voice:\s*(.+?)\]\s*', text)
    if m:
        desc = m.group(1).strip()
        clean_text = text[m.end():]
        # Check if it's a known preset voice name
        if desc.lower() in VOICES:
            return VOICES[desc.lower()], clean_text, False
        else:
            return desc, clean_text, True
    return None, text, False

def main():
    load_env_file()
    
    if len(sys.argv) < 3:
        print("Usage: mimo_tts.py <output_path> <text> [voice] [style] [--design]", file=sys.stderr)
        print("Voices: mimo_default, 冰糖, 茉莉, 苏打, 白桦, Mia, Chloe, Milo, Dean", file=sys.stderr)
        print("--design: 使用 voicedesign 模型，通过文本描述设计音色", file=sys.stderr)
        print("[voice:描述]文本  → 自动识别音色描述/预置音色", file=sys.stderr)
        sys.exit(1)

    output_path = sys.argv[1]
    text = sys.argv[2]
    
    # Check for --design flag
    use_design = "--design" in sys.argv
    
    # Parse [voice: ...] prefix from text
    prefix_voice, text, prefix_is_design = parse_voice_prefix(text)
    if prefix_is_design:
        use_design = True
    
    # Voice selection: env > arg3 > prefix > auto
    voice_env = os.environ.get("MIMO_TTS_VOICE", "")
    voice_arg = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "--design" else ""
    
    if use_design and prefix_voice:
        # VoiceDesign: prefix_voice is the description
        style = prefix_voice
        voice = ""  # no preset voice in design mode
    elif voice_arg and voice_arg.lower() in VOICES:
        voice = VOICES[voice_arg.lower()]
        style = ""
    elif voice_env and voice_env.lower() in VOICES:
        voice = VOICES[voice_env.lower()]
        style = ""
    elif voice_env:
        voice = voice_env
        style = ""
    elif voice_arg:
        voice = voice_arg
        style = ""
    elif prefix_voice:
        voice = prefix_voice
        style = ""
    else:
        voice = auto_select_voice(text)
        style = ""
    
    # Style/voice description from env or arg4 (overrides prefix)
    env_style = os.environ.get("MIMO_TTS_STYLE", "")
    if env_style:
        style = env_style
    elif not style and len(sys.argv) > 4 and sys.argv[4] != "--design":
        style = sys.argv[4]
    
    # Model selection
    if use_design:
        model = "mimo-v2.5-tts-voicedesign"
    else:
        model = os.environ.get("MIMO_TTS_MODEL", "mimo-v2.5-tts")
    
    api_key = os.environ.get("XIAOMI_API_KEY", "")
    base_url = os.environ.get("XIAOMI_BASE_URL", "https://api.xiaomimimo.com/v1")

    if not api_key:
        print("Error: XIAOMI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Detect output format from extension
    ext = os.path.splitext(output_path)[1].lower()
    fmt = {".wav": "wav", ".mp3": "mp3", ".ogg": "wav", ".opus": "wav"}.get(ext, "wav")

    # Build messages
    if use_design:
        # VoiceDesign mode: user message describes the voice (required), assistant message is the text
        # VoiceDesign doesn't use preset voices or voice parameter
        voice_desc = style if style else "用温柔甜美的年轻女性声音说话"
        messages = [
            {"role": "user", "content": voice_desc}
        ]
        # Only add assistant message if text is provided
        if text:
            messages.append({"role": "assistant", "content": text})
        # optimize_text_preview: when true, can skip assistant message
        audio_config = {"format": fmt, "optimize_text_preview": True}
    else:
        # Standard mode: style goes to user, text goes to assistant
        messages = []
        if style:
            messages.append({"role": "user", "content": style})
        else:
            messages.append({"role": "user", "content": "请朗读"})
        messages.append({"role": "assistant", "content": text})
        audio_config = {"format": fmt, "voice": voice}

    payload = json.dumps({
        "model": model,
        "messages": messages,
        "audio": audio_config
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())

    audio_b64 = result["choices"][0]["message"]["audio"]["data"]
    audio_bytes = base64.b64decode(audio_b64)

    # If target is ogg/opus and we got wav, try to convert with ffmpeg
    if ext in (".ogg", ".opus") and fmt == "wav":
        import subprocess, tempfile
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        try:
            subprocess.run(
                ["ffmpeg", "-y", "-i", tmp_path, "-acodec", "libopus", "-b:a", "128k", output_path],
                capture_output=True, timeout=30
            )
        finally:
            os.unlink(tmp_path)
    else:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)

    print(output_path)

if __name__ == "__main__":
    main()
