# MiMo TTS Skill for Hermes Agent

小米 MiMo TTS 语音合成技能，适用于 [Hermes Agent](https://github.com/NousResearch/hermes-agent)。

## 功能

- **预置音色**：茉莉、冰糖、苏打、白桦、Mia、Chloe、Milo、Dean
- **VoiceDesign**：通过文本描述自定义音色（`[voice: ...]` 前缀语法）
- **VoiceClone**：通过音频样本复刻任意音色
- **音频标签**：支持唱歌、情绪、方言、人设等多种风格控制
- **语境匹配**：根据对话内容自动选择音色和语气
- **格式支持**：输出 Telegram 兼容的 `.ogg` (Opus) 格式

## 依赖

- **Python 3**（系统自带或独立安装）
- **ffmpeg**（用于 WAV → Opus 转换，必须在 PATH 中）
  - Windows：`winget install ffmpeg` 或从 [ffmpeg.org](https://ffmpeg.org/download.html) 下载
  - Linux：`sudo apt install ffmpeg` 或 `brew install ffmpeg`

## 音频标签

### 基本用法
在文本前添加 `(标签)` 格式即可控制发音风格，例如：
```
(唱歌)原谅我这一生不羁放纵爱自由
(怅然)这么多年过去了，再走过那条街
(东北话)哎呀妈呀，这天儿也忒冷了
```

### 支持的标签类型

**基础情绪**：开心、悲伤、愤怒、恐惧、惊讶、兴奋、委屈、平静、冷漠、压抑的愤怒、带着哽咽的笑意、温柔但疲惫、狂躁中的温柔

**复合情绪**：怅然、欣慰、无奈、愧疚、释然、嫉妒、厌倦、忐忑、动情

**整体语调**：温柔、高冷、活泼、严肃、慵懒、俏皮、深沉、干练、凌厉

**音色定位**：磁性、醇厚、清亮、空灵、稚嫩、苍老、甜美、沙哑、醇雅

**人设腔调**：夹子音、御姐音、正太音、大叔音、台湾腔

**方言**：东北话、四川话、河南话、粤语

**角色扮演**：孙悟空、林黛玉

**语速与节奏**：吸气、深呼吸、叹气、长叹一口气、喘息、屏息

**情绪状态**：紧张、害怕、激动、疲惫、委屈、撒娇、心虚、震惊、不耐烦

**语音特征**：颤抖、声音颤抖、变调、破音、鼻音、气声、沙哑

**哭笑表达**：笑、轻笑、大笑、冷笑、抽泣、呜咽、哽咽、嚎啕大哭

**唱歌**：唱歌、sing、singing

### 标签示例
```
(紧张 深呼吸)呼……冷静，冷静。不就是一个面试吗……(语速加快 碎碎念)自我介绍已经背了五十遍了，应该没问题的。加油，你可以的……(小声)哎呀，领带歪没歪？
(极其疲惫 有气无力)师傅……到地方了叫我一声……(长叹一口气)我先眯一会儿，这班加得我魂儿都要散了。
(寒冷导致的急促呼吸)呼——呼——这、这大兴安岭的雪……(咳嗽)简直能把人骨头冻透了……别、别停下，走，快走。
(提高音量喊话)大姐！这鱼新鲜着呢！早上刚捞上来的！哎！那个谁，别乱翻，压坏了你赔啊？！
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

#### 基础用法（自动选择音色）
```bash
python mimo_tts.py <output_path> <text>
```

#### 指定音色
```bash
python mimo_tts.py <output_path> <text> 茉莉
```

#### VoiceDesign（前缀语法，推荐）
```bash
python mimo_tts.py <output_path> "[voice:一位年迈的老先生，嗓音沙哑沧桑]各位听众好。"
```

#### VoiceDesign（命令行标志）
```bash
python mimo_tts.py <output_path> <text> "用低沉磁性的男声说话" --design
```

#### VoiceClone（音频样本复刻）
```bash
python mimo_tts.py <output_path> <text> --clone <path_to_audio_sample.mp3>
```

#### VoiceClone + 风格控制
```bash
python mimo_tts.py <output_path> <text> "用温柔的语气说" --clone <path_to_audio_sample.mp3>
```

#### 唱歌模式
```bash
python mimo_tts.py <output_path> "(唱歌)原谅我这一生不羁放纵爱自由"
```

#### 情绪/方言控制
```bash
python mimo_tts.py <output_path> "(怅然)这么多年过去了，再走过那条街"
python mimo_tts.py <output_path> "(东北话)哎呀妈呀，这天儿也忒冷了"
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

## 模型列表

| 模型 ID | 功能 | 特点 |
|---------|------|------|
| `mimo-v2.5-tts` | 使用预置精品音色进行语音合成 | 支持唱歌，不支持音色设计与音色复刻 |
| `mimo-v2.5-tts-voicedesign` | 通过文本描述定制音色 | 通过文本描述自动生成音色，无需预置或音频样本，不支持唱歌模式、预置音色与音色复刻 |
| `mimo-v2.5-tts-voiceclone` | 基于音频样本复刻任意音色 | 通过音频样本精准复刻音色，实现任意声音的语音合成，不支持唱歌模式、预置音色与音色设计 |

## 如何写好音色描述（VoiceDesign）

### 关键维度
| 维度 | 示例 |
|------|------|
| 性别与年龄 | "young woman in her mid-20s"、"五十多岁的中年男性" |
| 音色/质感 | "deep and gravelly"、"丝滑醇厚、带着磁性" |
| 情绪/语气 | "warm and confident"、"温柔但带着一丝疲惫" |
| 语速/节奏 | "slow and deliberate"、"语速极快，像连珠炮" |

### 可选维度（增加丰富度）
- 角色/人设：narrator, podcast host, 评书先生, 深夜电台DJ
- 说话风格：casual and colloquial, 一本正经地, 压低嗓音像在密谋
- 场景描写：narrating a nature documentary, 在给投资人路演
- 年代参照：1940s film noir, 八十年代译制片配音

### 写法建议
1. **简洁描述型** — 用关键词或一句话快速勾勒声音轮廓
   ```
   Heavy Russian accent, gruff middle-aged male, blunt and matter-of-fact.
   ```

2. **专业描述型** — 通过场景、人设或多维度细节立体刻画声音
   ```
   Young female, extreme close-up with a binaural, ear-to-ear ASMR feel. 
   Audible breathing, subtle swallowing, and soft natural lip sounds. 
   She speaks very slowly, creating a deeply relaxing and immersive experience.
   ```
   ```
   一位年迈的老先生，说带北方口音的普通话，语速缓慢而沉稳，嗓音略带沙哑和沧桑感，
   仿佛一位饱经风霜的老爷爷在讲故事，充满岁月的智慧。
   ```

### 注意事项
- 长度：1-4 句即可，核心特征描述清楚比堆砌维度更重要
- 避免冲突：不要同时要求矛盾的特征（如"稚嫩的童声 + CEO气场"）
- 避免音质效果词：不要写混响、回声、EQ、压缩等后期处理相关描述
- 避免模糊词：不要用"普通的""正常的""外国的"等缺乏具体指向的描述
- 中英文均可：模型同时支持中英文音色描述，选择你最能精确表达的语言
- 合成文本要贴合音色：assistant 消息中的合成文本应与音色描述相匹配，才能获得最佳效果

## 故障排除

| 问题 | 排查方向 |
|------|----------|
| `XIAOMI_API_KEY not set` | 检查 `.env` 文件是否存在且包含正确的 key |
| ffmpeg 报错 | 确认 `ffmpeg -version` 可正常执行 |
| 音频无声音 | 检查输出文件大小，确认 API 返回正常 |
| VoiceDesign 音色不对 | 描述尽量具体，避免模糊词 |
| VoiceClone 失败 | 检查音频文件格式（支持 mp3 或 wav），确保文件存在 |
| HTTP/URL Error | 检查网络连接，确认 API Key 有效 |

## License

MIT
