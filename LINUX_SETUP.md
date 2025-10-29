# Linux 서버 설치 및 실행 가이드

## 📋 준비사항

1. Linux 서버 (Ubuntu, CentOS 등)
2. Python 3.7 이상
3. OpenAI API 키

## 🔧 설치 방법

### 1단계: 파일 업로드

프로젝트 파일들을 Linux 서버로 복사합니다:

```bash
# 예: scp로 파일 전송
scp -r /path/to/replit username@server-ip:/home/username/igd-chatbot/

# 또는 서버에서 직접 Git clone (Git 사용 시)
git clone [repository-url] igd-chatbot
cd igd-chatbot
```

### 2단계: 환경 설정

```bash
# 프로젝트 디렉토리로 이동
cd igd-chatbot

# .env 파일 생성
cp .env.example .env

# .env 파일 편집하여 OpenAI API 키 입력
nano .env
# 또는
vim .env
```

**`.env` 파일 내용:**
```
OPENAI_API_KEY=sk-your-actual-api-key-here
PORT=5000
FLASK_ENV=production
```

### 3단계: 실행 권한 부여

```bash
chmod +x run.sh
```

### 4단계: 서버 실행

```bash
./run.sh
```

## 🌐 외부 접속 설정

### 서버 IP 확인

```bash
# 방법 1
hostname -I

# 방법 2
ip addr show | grep inet

# 방법 3
ifconfig
```

### 방화벽 설정 (필요시)

**Ubuntu/Debian:**
```bash
sudo ufw allow 5000/tcp
sudo ufw status
```

**CentOS/RHEL:**
```bash
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports
```

### 접속 URL 공유

서버 실행 후, frontend 개발자에게 다음 URL을 전달하세요:

```
http://[서버IP주소]:5000
```

예시:
- `http://192.168.1.100:5000` (로컬 네트워크)
- `http://123.45.67.89:5000` (공인 IP)

## 🔄 백그라운드 실행 (선택사항)

터미널을 닫아도 서버가 계속 실행되도록 하려면:

### 방법 1: nohup 사용

```bash
nohup python3 main.py > server.log 2>&1 &

# 프로세스 확인
ps aux | grep main.py

# 종료
kill [PID]
```

### 방법 2: screen 사용

```bash
# screen 설치 (필요시)
sudo apt-get install screen  # Ubuntu/Debian
sudo yum install screen       # CentOS/RHEL

# screen 세션 시작
screen -S igd-chatbot

# 서버 실행
./run.sh

# 세션에서 나가기: Ctrl+A, 그 다음 D

# 세션 재접속
screen -r igd-chatbot

# 세션 종료
screen -X -S igd-chatbot quit
```

### 방법 3: systemd 서비스 (권장)

`/etc/systemd/system/igd-chatbot.service` 파일 생성:

```ini
[Unit]
Description=IGD Chatbot Survey Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/igd-chatbot
Environment="PATH=/home/your-username/igd-chatbot/venv/bin"
ExecStart=/home/your-username/igd-chatbot/venv/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

서비스 활성화 및 시작:

```bash
sudo systemctl daemon-reload
sudo systemctl enable igd-chatbot
sudo systemctl start igd-chatbot

# 상태 확인
sudo systemctl status igd-chatbot

# 로그 확인
sudo journalctl -u igd-chatbot -f

# 중지
sudo systemctl stop igd-chatbot
```

## 📊 서버 상태 확인

```bash
# 포트 사용 확인
netstat -tuln | grep 5000
# 또는
lsof -i :5000

# 프로세스 확인
ps aux | grep python

# 로그 확인 (nohup 사용 시)
tail -f server.log
```

## 🛠 트러블슈팅

### 1. "Permission denied" 오류

```bash
chmod +x run.sh
```

### 2. 포트가 이미 사용 중

```bash
# 포트를 사용하는 프로세스 찾기
lsof -i :5000

# 프로세스 종료
kill -9 [PID]

# 또는 다른 포트 사용 (.env 파일에서 PORT 변경)
```

### 3. Python 패키지 설치 오류

```bash
# pip 업그레이드
pip install --upgrade pip

# 패키지 재설치
pip install -r requirements.txt --force-reinstall
```

### 4. 외부 접속 불가

- 방화벽 설정 확인
- 공유기 포트 포워딩 설정 (필요시)
- 서버가 실제로 실행 중인지 확인: `netstat -tuln | grep 5000`

## 📝 유용한 명령어

```bash
# 서버 재시작
sudo systemctl restart igd-chatbot

# 서버 로그 실시간 보기
tail -f server.log
# 또는
sudo journalctl -u igd-chatbot -f

# 디스크 사용량 확인 (userinfo 폴더)
du -sh userinfo/

# 저장된 응답 파일 개수 확인
find userinfo/ -name "*.json" | wc -l
```

## 🔒 보안 권장사항

1. **HTTPS 설정**: 프로덕션 환경에서는 nginx + Let's Encrypt 사용 권장
2. **API 키 보안**: `.env` 파일 권한 설정 `chmod 600 .env`
3. **방화벽**: 필요한 포트만 열기
4. **정기 업데이트**: 패키지 및 시스템 업데이트

## 📞 문제 해결

문제 발생 시:
1. 서버 로그 확인
2. 에러 메시지 복사
3. Python 버전 확인: `python3 --version`
4. 패키지 버전 확인: `pip list`
