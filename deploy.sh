#!/bin/bash
# MacOS용 배포 스크립트

# 1. Python 설치
# Homebrew가 설치되어 있는지 확인
if ! command -v brew &> /dev/null
then
    echo "Homebrew가 설치되어 있지 않습니다. Homebrew를 설치합니다."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Python이 설치되어 있는지 확인
if ! command -v python3 &> /dev/null
then
    echo "Python3가 설치되어 있지 않습니다. Python3를 설치합니다."
    brew install python
else
    echo "Python3가 이미 설치되어 있습니다."
fi

# 2. 가상 환경 설정
PROJECT_DIR="$(pwd)"
VENV_DIR="$PROJECT_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "가상 환경을 생성합니다."
    python3 -m venv "$VENV_DIR"
else
    echo "가상 환경이 이미 존재합니다."
fi

# 가상 환경 활성화
source "$VENV_DIR/bin/activate"

# 3. 패키지 설치
if [ -f "requirements.txt" ]; then
    echo "필요한 패키지를 설치합니다."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "requirements.txt 파일이 없습니다. 패키지 설치를 건너뜁니다."
fi

# 4. Redis 설치 및 실행 (옵션)
if ! command -v redis-server &> /dev/null
then
    echo "Redis가 설치되어 있지 않습니다. Redis를 설치합니다."
    brew install redis
fi

# Redis 서버 시작
if ! pgrep redis-server > /dev/null 2>&1; then
    echo "Redis 서버를 시작합니다."
    redis-server --daemonize yes
else
    echo "Redis 서버가 이미 실행 중입니다."
fi

# 5. Appium 설치 및 실행 (옵션)
if ! command -v appium &> /dev/null
then
    echo "Appium이 설치되어 있지 않습니다. Appium을 설치합니다."
    npm install -g appium
else
    echo "Appium이 이미 설치되어 있습니다."
fi

# Appium 서버 시작 (새 터미널 창에서 실행)
osascript <<EOF
tell application "Terminal"
    do script "appium"
end tell
EOF

# 6. Celery 워커 실행 (새 터미널 창에서 실행)
osascript <<EOF
tell application "Terminal"
    do script "source $VENV_DIR/bin/activate && celery -A celery_app worker --loglevel=info"
end tell
EOF

# 7. Flask 서버 실행
echo "Flask 서버를 시작합니다."
python3 autotest_server.py