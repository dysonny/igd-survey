# 🚀 빠른 시작 가이드

## Frontend 개발자에게 전달할 내용

### 접속 URL
서버 실행 후, 다음 형식의 URL로 접속 가능합니다:

```
http://[서버IP주소]:5000
```

예시:
- 로컬: `http://localhost:5000`
- 네트워크: `http://192.168.1.100:5000`
- 공인IP: `http://123.45.67.89:5000`

---

## Linux 서버에서 실행하기

### 한 줄 요약
```bash
chmod +x run.sh && ./run.sh
```

### 상세 단계

#### 1. 환경 설정 (최초 1회)
```bash
# .env 파일 생성
cp .env.example .env

# OpenAI API 키 입력
nano .env
```

`.env` 파일에 다음과 같이 입력:
```
OPENAI_API_KEY=sk-실제발급받은API키입력
PORT=5000
FLASK_ENV=production
```

#### 2. 서버 실행
```bash
./run.sh
```

#### 3. 서버 주소 확인
스크립트 실행 시 자동으로 표시되는 IP 주소를 확인하세요.

또는 수동으로 확인:
```bash
hostname -I
```

---

## 백그라운드 실행 (터미널 닫아도 계속 실행)

### 방법 1: nohup
```bash
nohup python3 main.py > server.log 2>&1 &
```

종료:
```bash
pkill -f main.py
```

### 방법 2: screen
```bash
screen -S igd
./run.sh
# Ctrl+A, D 키로 빠져나오기

# 재접속
screen -r igd
```

---

## 서버 상태 확인

```bash
./check_status.sh
```

---

## 트러블슈팅

### 포트가 이미 사용 중
```bash
lsof -i :5000
kill -9 [PID]
```

### 외부 접속 안 됨
```bash
# 방화벽 포트 열기 (Ubuntu)
sudo ufw allow 5000/tcp
```

---

## 필요한 것
- Linux 서버
- Python 3.7+
- OpenAI API 키

## 더 자세한 정보
- 전체 문서: `README.md`
- Linux 설정: `LINUX_SETUP.md`
