@echo off
chcp 65001 >nul
echo ========================================
echo   AI智能体模块 - 一键启动脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.10+
    pause
    exit /b 1
)
echo ✅ Python环境正常

echo.
echo [2/4] 安装依赖...
if not exist ".env" (
    echo ⚠️  未找到.env文件，正在从.env.example复制...
    copy .env.example .env
    echo ⚠️  请编辑.env文件，填入讯飞API密钥后重新运行
    notepad .env
    pause
    exit /b 0
)

pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
echo ✅ 依赖安装完成

echo.
echo [3/4] 检查配置...
findstr /c:"your_api_key" .env >nul
if not errorlevel 1 (
    echo ⚠️  检测到API密钥未配置，请编辑.env文件填入真实密钥
    notepad .env
    echo 配置完成后请重新运行本脚本
    pause
    exit /b 0
)
echo ✅ 配置检查完成

echo.
echo [4/4] 启动服务器...
echo.
echo ========================================
echo   服务器启动中，请稍候...
echo   访问地址: http://localhost:8000
echo   API文档:  http://localhost:8000/docs
echo   按 Ctrl+C 停止服务
echo ========================================
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause