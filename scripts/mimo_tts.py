#!/usr/bin/env python3
"""MiMo TTS wrapper - converts text to speech using Xiaomi MiMo API.

Supports:
- Voice selection: mimo_default, 冰糖, 茉莉, 苏打, 白桦, Mia, Chloe, Milo, Dean
- VoiceDesign: 通过文本描述设计音色
- VoiceClone: 通过音频样本复刻音色
- Style control via user message
- Audio tag control (singing, emotions, dialects, etc.)
- Auto language detection for voice selection

Output: writes audio to {output_path}, prints the path to stdout.
"""
import sys, os, json, base64, urllib.request, re, subprocess, tempfile

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

def encode_audio_file(file_path):
    """Encode audio file to base64 with data URI prefix for VoiceClone."""
    if not os.path.exists(file_path):
        print(f"Error: Audio file not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    ext = os.path.splitext(file_path)[1].lower()
    mime_type = "audio/mpeg" if ext == ".mp3" else "audio/wav"
    
    with open(file_path, "rb") as f:
        audio_data = f.read()
    
    b64_data = base64.b64encode(audio_data).decode("utf-8")
    return f"data:{mime_type};base64,{b64_data}"

def main():
    load_env_file()
    
    if len(sys.argv) < 3:
        print("Usage: mimo_tts.py <output_path> <text> [voice/style] [--design] [--clone <audio_file>]", file=sys.stderr)
        print("Voices: mimo_default, 冰糖, 茉莉, 苏打, 白桦, Mia, Chloe, Milo, Dean", file=sys.stderr)
        print("--design: 使用 voicedesign 模型，通过文本描述设计音色", file=sys.stderr)
        print("--clone <audio_file>: 使用 voiceclone 模型，通过音频样本复刻音色", file=sys.stderr)
        print("[voice:描述]文本  → 自动识别音色描述/预置音色", file=sys.stderr)
        print("\n环境变量：", file=sys.stderr)
        print("  MIMO_TTS_DEFAULT_FORMAT: 默认输出格式 (wav/mp3/ogg/opus)", file=sys.stderr)
        print("\n音频标签示例：", file=sys.stderr)
        print("  (唱歌)原谅我这一生不羁放纵爱自由", file=sys.stderr)
        print("  (怅然)这么多年过去了，再走过那条街", file=sys.stderr)
        print("  (东北话)哎呀妈呀，这天儿也忒冷了", file=sys.stderr)
        sys.exit(1)

    output_path = sys.argv[1]
    text = sys.argv[2]
    
    # Check for flags
    use_design = "--design" in sys.argv
    use_clone = "--clone" in sys.argv
    clone_audio_file = None
    
    if use_clone:
        try:
            clone_idx = sys.argv.index("--clone")
            if clone_idx + 1 < len(sys.argv):
                clone_audio_file = sys.argv[clone_idx + 1]
            else:
                print("Error: --clone requires an audio file path", file=sys.stderr)
                sys.exit(1)
        except ValueError:
            pass
    
    # Parse [voice: ...] prefix from text
    prefix_voice, text, prefix_is_design = parse_voice_prefix(text)
    if prefix_is_design and not use_clone:
        use_design = True
    
    # Voice selection: env > arg3 > prefix > auto
    voice_env = os.environ.get("MIMO_TTS_VOICE", "")
    # Find non-flag arguments
    non_flag_args = []
    for arg in sys.argv[3:]:
        if arg not in ("--design", "--clone"):
            non_flag_args.append(arg)
    voice_arg = non_flag_args[0] if len(non_flag_args) > 0 and not use_clone else ""
    
    # Model selection and voice/style setup
    if use_clone and clone_audio_file:
        model = "mimo-v2.5-tts-voiceclone"
        style = ""
        voice = ""  # No preset voice in clone mode
    elif use_design:
        model = "mimo-v2.5-tts-voicedesign"
        if prefix_voice:
            style = prefix_voice
        else:
            style = non_flag_args[0] if len(non_flag_args) > 0 else ""
        voice = ""  # No preset voice in design mode
    else:
        model = os.environ.get("MIMO_TTS_MODEL", "mimo-v2.5-tts")
        if voice_arg and voice_arg.lower() in VOICES:
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
    
    # Style/voice description from env (overrides prefix)
    env_style = os.environ.get("MIMO_TTS_STYLE", "")
    if env_style and not use_clone:
        style = env_style
    elif not style and len(non_flag_args) > 1 and not use_clone:
        style = non_flag_args[1]
    
    api_key = os.environ.get("XIAOMI_API_KEY", "")
    base_url = os.environ.get("XIAOMI_BASE_URL", "https://api.xiaomimimo.com/v1")
    default_format = os.environ.get("MIMO_TTS_DEFAULT_FORMAT", "").lower()

    if not api_key:
        print("Error: XIAOMI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Detect output format from extension or use default from environment
    ext = os.path.splitext(output_path)[1].lower()
    
    # If no extension, use default format from env or fall back to .wav
    if not ext and default_format:
        ext = f".{default_format}"
        output_path = f"{output_path}{ext}"
    
    fmt = {".wav": "wav", ".mp3": "mp3", ".ogg": "wav", ".opus": "wav"}.get(ext, "wav")

    # Build messages and audio config
    messages = []
    audio_config = {}
    
    if use_clone and clone_audio_file:
        # VoiceClone mode: user message contains base64 audio + optional style
        audio_data_uri = encode_audio_file(clone_audio_file)
        user_content = {"audio": audio_data_uri}
        if style:
            user_content["text"] = style
        messages = [
            {"role": "user", "content": user_content}
        ]
        if text:
            messages.append({"role": "assistant", "content": text})
        audio_config = {"format": fmt, "optimize_text_preview": True}
    elif use_design:
        # VoiceDesign mode: user message describes the voice (required), assistant message is the text
        voice_desc = style if style else "用温柔甜美的年轻女性声音说话"
        messages = [
            {"role": "user", "content": voice_desc}
        ]
        # Only add assistant message if text is provided
        if text:
            messages.append({"role": "assistant", "content": text})
        audio_config = {"format": fmt, "optimize_text_preview": True}
    else:
        # Standard mode: style goes to user, text goes to assistant
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

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
        
        # Check for errors in response
        if "error" in result:
            print(f"API Error: {result['error'].get('message', 'Unknown error')}", file=sys.stderr)
            sys.exit(1)
        
        audio_b64 = result["choices"][0]["message"]["audio"]["data"]
        audio_bytes = base64.b64decode(audio_b64)

        # If target is ogg/opus and we got wav, try to convert with ffmpeg
        if ext in (".ogg", ".opus") and fmt == "wav":
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name
            try:
                subprocess.run(
                    ["ffmpeg", "-y", "-i", tmp_path, "-acodec", "libopus", "-b:a", "128k", output_path],
                    capture_output=True, timeout=30, check=True
                )
            except subprocess.CalledProcessError as e:
                print(f"FFmpeg conversion failed: {e}", file=sys.stderr)
                # Fallback to writing raw wav if conversion fails
                with open(output_path, "wb") as f:
                    f.write(audio_bytes)
            finally:
                os.unlink(tmp_path)
        else:
            with open(output_path, "wb") as f:
                f.write(audio_bytes)

        print(output_path)
        
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        try:
            error_body = e.read().decode("utf-8")
            print(f"Error details: {error_body}", file=sys.stderr)
        except:
            pass
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"Invalid API response format: missing key {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()