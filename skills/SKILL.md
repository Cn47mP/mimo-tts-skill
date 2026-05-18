---
name: mimo-tts
description: "小米 MiMo TTS 语音合成技能，支持多种音色、自定义音色、方言、情绪和唱歌模式"
version: 2.2.0
author: Hermes
tags: [tts, voice, audio, xiaomi, mimo, telegram]
---

# MiMo TTS 语音合成技能

## 安装与配置（Hermes Agent 可自动执行）

### 如果此技能未安装，请按以下步骤操作：

1. **复制脚本文件**
   - 将 `mimo_tts.py` 复制到 Hermes 的 scripts 目录
   - 目录位置：
     - Linux/macOS: `~/.hermes/scripts/`
     - Windows: `%LOCALAPPDATA%\hermes\scripts\`
   - 确保脚本有执行权限

2. **复制技能文件**
   - 将此 SKILL.md 复制到：`~/.hermes/skills/media/mimo-tts/`
   - Windows: `%LOCALAPPDATA%\hermes\skills\media\mimo-tts\`

3. **配置环境变量**
   - 检查 `.env` 文件是否存在于 Hermes 目录
   - 如果不存在，从 `.env.example` 复制
   - 确保设置了 `XIAOMI_API_KEY`

4. **配置 TTS provider**
   - 在 Hermes 的 `config.yaml` 中添加：
     ```yaml
     tts:
       provider: mimo
       providers:
         mimo:
           type: command
           command: python ~/.hermes/scripts/mimo_tts.py {output_path} {text}
           output_format: ogg
     ```

5. **重启 Hermes Agent**

## 触发条件

用户说以下内容时触发：
- "发语音"、"用语音说"、"朗读"
- "TTS"、"语音合成"
- "唱歌"、"唱首歌"
- "用东北话说"、"用四川话说"
- "用茉莉说"、"用冰糖说"
- "[voice:描述]"

## 使用方法

### 1. 基础使用
直接要求用户要说的内容：
- "用语音说：你好"
- "朗读：今天天气真好"

### 2. 指定音色
- "用茉莉说：你好"
- "用冰糖唱首歌"
- "用Mia说：Hello"

### 3. 自定义音色（VoiceDesign）
- "[voice:温柔的御姐音]你好呀"
- "[voice:沙哑的老年男声]你好，年轻人"

### 4. 情绪/方言/唱歌
- "(开心)今天真棒！"
- "(东北话)哎呀妈呀"
- "(唱歌)原谅我这一生不羁放纵爱自由"

## 音色列表

### 中文
- 冰糖 - 甜美温柔女声 ✅ 默认
- 茉莉 - 清新自然女声
- 苏打 - 阳光活力男声
- 白桦 - 沉稳成熟男声

### 英文
- Mia - 温暖亲切女声 ✅ 默认
- Chloe - 活泼年轻女声
- Milo - 深沉磁性男声
- Dean - 清晰标准男声

## 工作流程（必须按此执行）

当用户触发技能时，按以下步骤执行：

1. **生成音频**
   - 使用 TTS provider 生成音频
   - 保存到临时文件（必须是绝对路径）
   - 推荐路径：`$TMPDIR/tts_$(date +%s).ogg`

2. **发送语音**
   - 通过 send_message 发送 MEDIA 类型消息

3. **清理文件**
   - 删除临时音频文件

## 注意事项

- ⚠️ 不要解释流程，直接执行
- ⚠️ 不要问"要发语音吗？"，直接生成并发送
- ⚠️ 音频路径必须使用绝对路径
- ⚠️ 输出格式优先使用 .ogg（Telegram 优化）
- 中文歌词唱歌效果最好
