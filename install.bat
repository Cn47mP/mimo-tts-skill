@echo off
REM MiMo TTS Skill for Hermes Agent - Windows 一键安装脚本

echo ==========================================
echo   MiMo TTS Skill for Hermes Agent
echo ==========================================
echo.

set HERMES_DIR=%LOCALAPPDATA%\hermes
set SCRIPT_DIR=%~dp0

echo 📋 安装信息：
echo    Hermes 目录: %HERMES_DIR%
echo    源目录: %SCRIPT_DIR%
echo.

REM 创建必要的目录
if not exist "%HERMES_DIR%\scripts" mkdir "%HERMES_DIR%\scripts"
if not exist "%HERMES_DIR%\skills\media\mimo-tts" mkdir "%HERMES_DIR%\skills\media\mimo-tts"

REM 复制文件
echo 📦 复制文件...
copy /Y "%SCRIPT_DIR%scripts\mimo_tts.py" "%HERMES_DIR%\scripts\"
copy /Y "%SCRIPT_DIR%skills\SKILL.md" "%HERMES_DIR%\skills\media\mimo-tts\"

REM 处理 .env 文件
if not exist "%HERMES_DIR%\.env" (
    echo 📝 创建 .env 文件...
    copy /Y "%SCRIPT_DIR%.env.example" "%HERMES_DIR%\.env"
    echo    ⚠️  请编辑 %HERMES_DIR%\.env 文件，设置你的 XIAOMI_API_KEY
) else (
    echo 📝 .env 文件已存在，跳过创建
    echo    你可以参考 %SCRIPT_DIR%.env.example 查看可用配置
)

echo.
echo ✅ 安装成功！
echo.
echo 📝 后续步骤：
echo 1. 编辑 %HERMES_DIR%\.env 文件，设置 XIAOMI_API_KEY
echo 2. 在 Hermes 的 config.yaml 中添加 TTS provider 配置：
echo.
echo    tts:
echo      provider: mimo
echo      providers:
echo        mimo:
echo          type: command
echo          command: python %HERMES_DIR%\scripts\mimo_tts.py {output_path} {text}
echo          output_format: ogg
echo.
echo 3. 重启 Hermes Agent
echo.
pause
