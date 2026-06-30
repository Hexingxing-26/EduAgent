#!/bin/bash

echo "========================================"
echo "  AI智能体模块 - 一键启动脚本"
echo "========================================"
echo ""

cd "$(dirname "$0")"

echo "[1/4] 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python，请先安装Python 3.10+"
    exit 1
fi
python3 --version
echo "✅ Python环境正常"

echo ""
echo "[2/4] 安装依赖..."
if [ ! -f ".env" ]; then
    echo "⚠️  未找到.env文件，正在从.env.example复制..."
    cp .env.example .env
    echo "⚠️  请编辑.env文件，填入讯飞API密钥后重新运行"
    exit 0
fi

pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi
echo "✅ 依赖安装完成"

echo ""
echo "[3/4] 检查配置..."
if grep -q "your_api_key" .env; then
    echo "⚠️  检测到API密钥未配置，请编辑.env文件填入真实密钥"
    echo "配置完成后请重新运行本脚本"
    exit 0
fi
echo "✅ 配置检查完成"

echo ""
echo "[4/4] 启动服务器..."
echo ""
echo "========================================"
echo "  服务器启动中，请稍候..."
echo "  访问地址: http://localhost:8000"
echo "  API文档:  http://localhost:8000/docs"
echo "  按 Ctrl+C 停止服务"
echo "========================================"
echo ""

python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload