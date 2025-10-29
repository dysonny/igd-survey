#!/bin/bash

# 서버 상태 확인 스크립트

echo "=========================================="
echo "IGD 챗봇 서버 상태 확인"
echo "=========================================="

# 포트 설정
PORT=${PORT:-5000}

echo ""
echo "1. 포트 사용 확인..."
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ 포트 $PORT 이 사용 중입니다."
    echo ""
    echo "프로세스 정보:"
    lsof -i :$PORT
else
    echo "❌ 포트 $PORT 이 사용되지 않습니다."
    echo "   서버가 실행 중이 아닙니다."
fi

echo ""
echo "=========================================="
echo "2. Python 프로세스 확인..."
PROCESS=$(ps aux | grep "[m]ain.py")
if [ -n "$PROCESS" ]; then
    echo "✅ Python 서버가 실행 중입니다."
    echo "$PROCESS"
else
    echo "❌ Python 서버가 실행 중이 아닙니다."
fi

echo ""
echo "=========================================="
echo "3. 네트워크 인터페이스 정보..."
echo ""
echo "🌐 접속 가능한 IP 주소들:"
hostname -I | awk '{for(i=1;i<=NF;i++) print "   http://"$i":'$PORT'"}'

echo ""
echo "=========================================="
echo "4. .env 파일 확인..."
if [ -f .env ]; then
    echo "✅ .env 파일이 존재합니다."
    if grep -q "OPENAI_API_KEY=your_openai_api_key_here" .env 2>/dev/null || \
       grep -q "OPENAI_API_KEY=$" .env 2>/dev/null || \
       ! grep -q "OPENAI_API_KEY=" .env 2>/dev/null; then
        echo "⚠️  경고: OpenAI API 키가 설정되지 않았을 수 있습니다."
    else
        echo "✅ OpenAI API 키가 설정되어 있습니다."
    fi
else
    echo "❌ .env 파일이 없습니다."
    echo "   cp .env.example .env 명령으로 생성하세요."
fi

echo ""
echo "=========================================="
echo "5. userinfo 디렉토리 확인..."
if [ -d "userinfo" ]; then
    echo "✅ userinfo 디렉토리가 존재합니다."
    FILE_COUNT=$(find userinfo -name "*.json" 2>/dev/null | wc -l)
    echo "   저장된 응답 파일 수: $FILE_COUNT"
else
    echo "⚠️  userinfo 디렉토리가 없습니다 (자동 생성됩니다)."
fi

echo ""
echo "=========================================="
echo "6. 필수 패키지 확인..."
if [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null
fi

PACKAGES=("flask" "openai" "pytz" "python-dotenv")
for package in "${PACKAGES[@]}"; do
    if pip show $package >/dev/null 2>&1; then
        VERSION=$(pip show $package | grep Version | awk '{print $2}')
        echo "✅ $package ($VERSION)"
    else
        echo "❌ $package (설치되지 않음)"
    fi
done

echo ""
echo "=========================================="
echo "완료!"
echo "=========================================="
