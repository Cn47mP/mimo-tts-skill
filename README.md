# MiMo TTS Skill for Hermes Agent

小米 MiMo TTS 语音合成技能，适用于 [Hermes Agent](https://github.com/NousResearch/hermes-agent)。

## 功能

- **预置音色**：茉莉、冰糖、苏打、白桦、Mia、Chloe、Milo、Dean
- **VoiceDesign**：通过文本描述自定义音色（`[voice: ...]` 前缀语法）
- **语境匹配**：根据对话内容自动选择音色和语气
- **格式支持**：输出 Telegram 兼容的 `.ogg` (Opus) 格式

## 依赖

- **Python 3**（系统自带或独立安装）
- **ffmpeg**（用于 WAV → Opus 转换，必须在 PATH 中）
  - Windows：`winget install ffmpeg` 或从 [ffmpeg.org](https://ffmpeg.org/download.html) 下载
  - Linux：`sudo apt install ffmpeg` 或 `brew install ffmpeg`

## 文件结构

```
├── .env.example           # 环境变量模板
├── README.md              # 本文件
├── scripts/
│   └── mimo_tts.py        # TTS 调用脚本
└── skills/
    └── SKILL.md           # Hermes 技能文件（agent 使用）
```

## 安装

### 1. 复制脚本

```bash
cp scripts/mimo_tts.py ~/AppData/Local/hermes/scripts/
# Linux: cp scripts/mimo_tts.py ~/.hermes/scripts/
```

### 2. 复制技能文件

```bash
cp skills/SKILL.md ~/AppData/Local/hermes/skills/media/mimo-tts/SKILL.md
# Linux: mkdir -p ~/.hermes/skills/media/mimo-tts && cp skills/SKILL.md ~/.hermes/skills/media/mimo-tts/
```

### 3. 配置环境变量

```bash
cp .env.example ~/AppData/Local/hermes/.env
# Linux: cp .env.example ~/.hermes/.env
```

编辑 `.env`，填入你的 API Key：

```
XIAOMI_API_KEY=your_key_here
```

### 4. 配置 Hermes TTS provider

在 `config.yaml` 中添加：

```yaml
tts:
  provider: mimo
  providers:
    mimo:
      type: command
      command: python ~/AppData/Local/hermes/scripts/mimo_tts.py {output_path} {text}
      output_format: ogg
```

## 环境变量

| 变量 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `XIAOMI_API_KEY` | ✅ | — | 小米 MiMo API 密钥 |
| `XIAOMI_BASE_URL` | ❌ | `https://api.xiaomimimo.com/v1` | API 端点，可通过环境变量覆盖 |
| `MIMO_TTS_VOICE` | ❌ | 自动检测 | 默认音色（冰糖/茉莉/苏打/白桦/Mia/Chloe/Milo/Dean） |
| `MIMO_TTS_STYLE` | ❌ | — | 默认风格描述 |
| `MIMO_TTS_MODEL` | ❌ | `mimo-v2.5-tts` | 默认模型 |

## 使用

### 直接调用

```bash
# 基础用法（自动选择音色）
python mimo_tts.py <output_path> <text>

# 指定音色
python mimo_tts.py <output_path> <text> 茉莉

# VoiceDesign（前缀语法，推荐）
python mimo_tts.py <output_path> "[voice:一位年迈的老先生，嗓音沙哑沧桑]各位听众好。"

# VoiceDesign（命令行标志）
python mimo_tts.py <output_path> <text> "用低沉磁性的男声说话" --design
```

### 通过 Hermes Agent 使用

安装后，agent 会自动加载 `mimo-tts` 技能。用户说"发语音"、"朗读"、"TTS" 等即触发。

Agent 的标准调用流程（3 步）：

```
1. terminal  → 生成 .ogg 文件
2. send_message  → 发送 MEDIA 附件
3. terminal  → 清理临时文件
```

## 音色列表

### 中文音色

| 音色 ID | 性别 | 特点 |
|---------|------|------|
| 冰糖 | 女 | 甜美、温柔、活泼 |
| 茉莉 | 女 | 清新、自然、知性 |
| 苏打 | 男 | 阳光、活力、年轻 |
| 白桦 | 男 | 沉稳、成熟、可靠 |

### 英文音色

| 音色 ID | 性别 | 特点 |
|---------|------|------|
| Mia | 女 | 温暖、亲切、专业 |
| Chloe | 女 | 活泼、年轻、友好 |
| Milo | 男 | 深沉、磁性、成熟 |
| Dean | 男 | 清晰、标准、权威 |

## API

- **端点**：通过 `XIAOMI_BASE_URL` 环境变量设置（默认 `https://api.xiaomimimo.com/v1/chat/completions`）
- **模型**：`mimo-v2.5-tts`（预置音色）/ `mimo-v2.5-tts-voicedesign`（自定义音色）
- **密钥**：通过 `XIAOMI_API_KEY` 环境变量或 `.env` 文件设置

## 故障排除

| 问题 | 排查方向 |
|------|----------|
| `XIAOMI_API_KEY not set` | 检查 `.env` 文件是否存在且包含正确的 key |
| ffmpeg 报错 | 确认 `ffmpeg -version` 可正常执行 |
| 音频无声音 | 检查输出文件大小，确认 API 返回正常 |
| VoiceDesign 音色不对 | 描述尽量具体，避免模糊词（如"普通的"） |

## License

MIT
