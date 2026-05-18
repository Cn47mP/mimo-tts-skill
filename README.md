# MiMo TTS Skill for Hermes Agent

为 Hermes Agent 设计的小米 MiMo TTS 语音合成技能，支持 Telegram bot。

## 特性

- 8种预置音色（4中4英）
- VoiceDesign：文本描述自定义音色
- VoiceClone：音频样本克隆声音
- 唱歌模式、方言支持、情绪控制
- Telegram 优化的 .ogg 输出

## 给 Hermes Agent 的说明

### 如果你需要安装/配置此技能

请参考 [skills/SKILL.md](file:///workspace/skills/SKILL.md) 中的「安装与配置」章节，你可以自动完成所有配置步骤。

### 项目结构

```
.
├── scripts/
│   └── mimo_tts.py      # TTS 主脚本
├── skills/
│   └── SKILL.md         # 技能定义（包含自动安装步骤）
├── .env.example         # 环境变量示例
└── README.md            # 本文件
```

## 核心文件说明

- **[mimo_tts.py](file:///workspace/scripts/mimo_tts.py)** - TTS 脚本，负责与 MiMo API 通信
- **[SKILL.md](file:///workspace/skills/SKILL.md)** - Hermes 技能定义，包含完整使用说明和配置步骤
- **[.env.example](file:///workspace/.env.example)** - 环境变量模板

## 环境变量

在 `.env` 中配置：

| 变量 | 必需 | 说明 |
|------|------|------|
| `XIAOMI_API_KEY` | ✅ | MiMo API 密钥 |
| `XIAOMI_BASE_URL` | ❌ | 自定义 API 端点 |
| `MIMO_TTS_VOICE` | ❌ | 默认音色 |
| `MIMO_TTS_DEFAULT_FORMAT` | ❌ | 默认输出格式 |

## 依赖

- Python 3.6+
- ffmpeg

## 许可证

MIT
