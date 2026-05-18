# MiMo TTS Skill for Hermes Agent

为 Hermes Agent 打造的小米 MiMo TTS 语音合成技能，完美配合 Telegram bot 使用。

## ✨ 特性

- 🎯 **预置音色** - 8种高品质音色（4中4英）
- 🎨 **VoiceDesign** - 用文字描述自定义音色
- 🔊 **VoiceClone** - 基于音频样本克隆声音
- 🎵 **唱歌模式** - 支持中文歌词演唱
- 🌍 **方言支持** - 东北话、四川话、粤语等
- 😊 **情绪控制** - 开心、悲伤、温柔等多种情绪
- 📱 **Telegram 优化** - 默认输出 .ogg 格式

## 🚀 快速安装

### 方法 1：一键安装脚本（推荐）

**Linux/macOS:**
```bash
cd /path/to/this/project
chmod +x install.sh
./install.sh
```

**Windows:**
```cmd
cd \path\to\this\project
install.bat
```

### 方法 2：手动安装

1. **复制文件**
   ```bash
   # 复制脚本
   cp scripts/mimo_tts.py ~/.hermes/scripts/
   # Windows: copy scripts\mimo_tts.py %LOCALAPPDATA%\hermes\scripts\
   
   # 复制技能文件
   mkdir -p ~/.hermes/skills/media/mimo-tts
   cp skills/SKILL.md ~/.hermes/skills/media/mimo-tts/
   # Windows: mkdir %LOCALAPPDATA%\hermes\skills\media\mimo-tts
   #          copy skills\SKILL.md %LOCALAPPDATA%\hermes\skills\media\mimo-tts\
   ```

2. **配置环境变量**
   ```bash
   cp .env.example ~/.hermes/.env
   # Windows: copy .env.example %LOCALAPPDATA%\hermes\.env
   ```
   
   编辑 `~/.hermes/.env` 文件，设置你的 API Key：
   ```
   XIAOMI_API_KEY=your_api_key_here
   ```

3. **配置 Hermes**
   
   在 Hermes 的 `config.yaml` 中添加：
   ```yaml
   tts:
     provider: mimo
     providers:
       mimo:
         type: command
         command: python ~/.hermes/scripts/mimo_tts.py {output_path} {text}
         output_format: ogg
   ```
   
   可参考项目中的 [config.example.yaml](file:///workspace/config.example.yaml)

4. **重启 Hermes Agent**

## 📖 使用方法

### 在 Telegram 中使用

对 Hermes bot 说：

| 功能 | 示例 |
|------|------|
| 基础语音 | "用语音说：你好" |
| 指定音色 | "用茉莉说：今天天气真好" |
| 唱歌 | "唱首歌：原谅我这一生不羁放纵爱自由" |
| 方言 | "用东北话说：哎呀妈呀" |
| 自定义音色 | "[voice:温柔的御姐音]你好呀" |
| 情绪 | "(开心)今天真是太棒了" |

### 直接调用脚本

```bash
# 基础使用
python ~/.hermes/scripts/mimo_tts.py output.ogg "你好，世界"

# 指定音色
python ~/.hermes/scripts/mimo_tts.py output.ogg "你好" 茉莉

# VoiceDesign
python ~/.hermes/scripts/mimo_tts.py output.ogg "[voice:沙哑的男声]你好"

# 唱歌
python ~/.hermes/scripts/mimo_tts.py output.ogg "(唱歌)歌词内容"

# VoiceClone
python ~/.hermes/scripts/mimo_tts.py output.ogg "你好" -- clone sample.mp3
```

## 🎤 音色列表

### 中文音色
| 音色 | 特点 |
|------|------|
| 冰糖 | 甜美温柔女声 ✅ 默认 |
| 茉莉 | 清新自然女声 |
| 苏打 | 阳光活力男声 |
| 白桦 | 沉稳成熟男声 |

### 英文音色
| 音色 | 特点 |
|------|------|
| Mia | 温暖亲切女声 ✅ 默认 |
| Chloe | 活泼年轻女声 |
| Milo | 深沉磁性男声 |
| Dean | 清晰标准男声 |

## 🏷️ 常用音频标签

### 情绪
开心、悲伤、愤怒、惊讶、兴奋、委屈、平静、温柔、高冷

### 方言
东北话、四川话、河南话、粤语、台湾腔

### 特殊
唱歌、sing、夹子音、御姐音、正太音、大叔音

## ⚙️ 环境变量

在 `~/.hermes/.env` 中可配置：

| 变量 | 说明 |
|------|------|
| `XIAOMI_API_KEY` | （必需）小米 MiMo API 密钥 |
| `XIAOMI_BASE_URL` | （可选）自定义 API 端点 |
| `MIMO_TTS_VOICE` | （可选）默认音色 |
| `MIMO_TTS_STYLE` | （可选）默认风格 |
| `MIMO_TTS_MODEL` | （可选）默认模型 |
| `MIMO_TTS_DEFAULT_FORMAT` | （可选）默认输出格式 |

## 📋 项目结构

```
.
├── scripts/
│   └── mimo_tts.py          # TTS 主脚本
├── skills/
│   └── SKILL.md             # Hermes 技能定义
├── install.sh               # Linux/macOS 安装脚本
├── install.bat              # Windows 安装脚本
├── config.example.yaml      # Hermes 配置示例
├── .env.example             # 环境变量示例
└── README.md                # 本文件
```

## 🔧 依赖

- Python 3.6+
- ffmpeg（用于音频格式转换）
  - Ubuntu/Debian: `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: 从 https://ffmpeg.org/download.html 下载

## 📝 注意事项

1. 获取 API Key：访问 https://platform.xiaomimimo.com
2. Telegram 优先使用 .ogg 格式，音质好且体积小
3. 确保脚本有执行权限：`chmod +x ~/.hermes/scripts/mimo_tts.py`
4. 音频路径必须使用绝对路径

## 🆘 故障排除

### 问题：API Key 未设置
**解决**：检查 `~/.hermes/.env` 文件，确保 `XIAOMI_API_KEY` 已正确配置

### 问题：ffmpeg 未找到
**解决**：安装 ffmpeg 并确保它在系统 PATH 中

### 问题：技能未加载
**解决**：确保 `SKILL.md` 放在正确位置并重启 Hermes Agent

## 📄 许可证

MIT License
