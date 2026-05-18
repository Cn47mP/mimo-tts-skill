#!/bin/bash
# MiMo TTS Skill for Hermes Agent - 一键安装脚本

set -e

echo "=========================================="
echo "  MiMo TTS Skill for Hermes Agent"
echo "=========================================="
echo ""

# 检测操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    HERMES_DIR="$HOME/.hermes"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    HERMES_DIR="$HOME/.hermes"
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* || "$OSTYPE" == "win32" ]]; then
    HERMES_DIR="$HOME/AppData/Local/hermes"
else
    echo "❌ 不支持的操作系统: $OSTYPE"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📋 安装信息："
echo "   Hermes 目录: $HERMES_DIR"
echo "   源目录: $SCRIPT_DIR"
echo ""

# 创建必要的目录
mkdir -p "$HERMES_DIR/scripts"
mkdir -p "$HERMES_DIR/skills/media/mimo-tts"

# 复制文件
echo "📦 复制文件..."
cp "$SCRIPT_DIR/scripts/mimo_tts.py" "$HERMES_DIR/scripts/"
chmod +x "$HERMES_DIR/scripts/mimo_tts.py"
cp "$SCRIPT_DIR/skills/SKILL.md" "$HERMES_DIR/skills/media/mimo-tts/"

# 处理 .env 文件
if [ ! -f "$HERMES_DIR/.env" ]; then
    echo "📝 创建 .env 文件..."
    cp "$SCRIPT_DIR/.env.example" "$HERMES_DIR/.env"
    echo "   ⚠️  请编辑 $HERMES_DIR/.env 文件，设置你的 XIAOMI_API_KEY"
else
    echo "📝 .env 文件已存在，跳过创建"
    echo "   你可以参考 $SCRIPT_DIR/.env.example 查看可用配置"
fi

echo ""
echo "✅ 安装成功！"
echo ""
echo "📝 后续步骤："
echo "1. 编辑 $HERMES_DIR/.env 文件，设置 XIAOMI_API_KEY"
echo "2. 在 Hermes 的 config.yaml 中添加 TTS provider 配置："
echo ""
echo "   tts:"
echo "     provider: mimo"
echo "     providers:"
echo "       mimo:"
echo "         type: command"
echo "         command: python $HERMES_DIR/scripts/mimo_tts.py {output_path} {text}"
echo "         output_format: ogg"
echo ""
echo "3. 重启 Hermes Agent"
echo ""
