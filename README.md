# IGD 챗봇 설문조사 시스템# IGD 챗봇 설문조사 시스템



인터넷 게임 중독(Internet Gaming Disorder) 설문조사를 위한 Flask 기반 웹 애플리케이션입니다.인터넷 게임 중독(Internet Gaming Disorder) 설문조사를 위한 Flask 기반 웹 애플리케이션입니다.



## ✨ 주요 기능## 🚀 빠른 시작 (Linux 환경)



- 📝 29문항 IGD 설문조사### 1. 환경 설정

- 🤖 GPT-4 기반 대화형 챗봇

- 🎤 음성인식 지원 (Web Speech API)```bash

- 💾 JSON 파일 기반 응답 저장# .env 파일 생성

- 🌐 CORS 지원 (외부 Frontend 연동)cp .env.example .env

- 📊 실시간 대화 기록

# .env 파일을 편집하여 OpenAI API 키 입력

---nano .env

# 또는

## 🚀 빠른 배포 (Railway - 추천)vim .env

```

### Railway로 5분만에 배포하기

### 2. 서버 실행

Railway는 무료로 웹 애플리케이션을 호스팅할 수 있는 플랫폼입니다.

```bash

**장점:**# 실행 권한 부여

- ✅ 무료 ($5/월 크레딧)chmod +x run.sh

- ✅ 자동 HTTPS (음성인식 작동)

- ✅ 고정 URL# 서버 실행

- ✅ 자동 재시작./run.sh

```

**배포 방법:** `RAILWAY_QUICKSTART.md` 참고

### 3. 접속 방법

**상세 가이드:** `RAILWAY_DEPLOY.md` 참고

서버 실행 후 표시되는 IP 주소로 접속하세요.

---

**로컬 접속:**

## 💻 로컬 개발- http://localhost:5000



### 필수 요구사항**외부 접속:** (다른 컴퓨터에서)

- http://[서버IP주소]:5000

- Python 3.9+- 예: http://192.168.1.100:5000

- OpenAI API 키

> 💡 서버 IP 주소는 `./run.sh` 실행 시 자동으로 표시됩니다.

### 설치 및 실행

## 📋 수동 설치 및 실행

```bash

# 1. 저장소 클론 또는 다운로드### 필수 요구사항

cd /path/to/project

- Python 3.7 이상

# 2. 패키지 설치- pip

pip install -r requirements.txt

### 설치

# 3. 환경 변수 설정

cp .env.example .env```bash

# .env 파일을 열어 OPENAI_API_KEY 설정# 1. Python 가상환경 생성 (선택사항이지만 권장)

python3 -m venv venv

# 4. 서버 실행source venv/bin/activate  # Linux/Mac

python3 main.py

# 2. 필요한 패키지 설치

# 5. 브라우저에서 접속pip install -r requirements.txt

# http://localhost:5001

```# 3. 환경 변수 설정

cp .env.example .env

---# .env 파일을 열어 OPENAI_API_KEY 값을 실제 키로 변경



## 📁 프로젝트 구조# 4. userinfo 디렉토리 생성 (자동으로 생성되지만, 미리 만들어도 됨)

mkdir -p userinfo

``````

.

├── main.py                   # Flask 애플리케이션### 실행

├── index.html                # 메인 HTML

├── script.js                 # Frontend JavaScript (음성인식 포함)```bash

├── style.css                 # 스타일시트# 개발 모드로 실행

├── requirements.txt          # Python 의존성python3 main.py

├── Procfile                  # Railway 실행 명령

├── runtime.txt               # Python 버전# 또는 프로덕션 모드로 실행 (더 안정적)

├── .env.example              # 환경 변수 예시gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 main:app

├── .gitignore                # Git 제외 파일```

├── RAILWAY_DEPLOY.md         # Railway 배포 가이드

├── RAILWAY_QUICKSTART.md     # 빠른 시작## 🔧 포트 변경

├── README.md                 # 이 문서

└── userinfo/                 # 사용자 응답 저장 (자동 생성)기본 포트는 5000입니다. 변경하려면:

```

1. `.env` 파일에서 `PORT=원하는포트번호` 설정

---2. 또는 `main.py` 마지막 줄 수정



## 🌐 API 엔드포인트## 🌐 외부 접속 설정



배포 후 Frontend 개발자에게 다음 정보를 전달하세요:### 방화벽 설정 (필요시)



**Base URL:** `https://your-app.up.railway.app````bash

# Ubuntu/Debian

### 사용 가능한 APIsudo ufw allow 5000/tcp



- `GET /` - 메인 페이지# CentOS/RHEL

- `POST /user-info` - 사용자 정보 저장sudo firewall-cmd --permanent --add-port=5000/tcp

- `POST /chat` - 질문/응답sudo firewall-cmd --reload

- `POST /reset` - 설문 초기화```

- `GET /history` - 대화 기록 조회

### 서버 IP 확인

### 예시

```bash

```javascript# Linux

// 사용자 정보 저장hostname -I

fetch('https://your-app.up.railway.app/user-info', {

    method: 'POST',# 또는

    headers: { 'Content-Type': 'application/json' },ip addr show

    body: JSON.stringify({```

        name: '홍길동',

        dob: '1990-01-01',## 📁 프로젝트 구조

        gender: 'male',

        gameAddictionScore: '5'```

    }).

});├── main.py              # Flask 애플리케이션 메인 파일

├── index.html           # 메인 HTML 페이지

// 채팅├── script.js            # 프론트엔드 JavaScript

fetch('https://your-app.up.railway.app/chat', {├── style.css            # 스타일시트

    method: 'POST',├── requirements.txt     # Python 의존성 패키지

    headers: { 'Content-Type': 'application/json' },├── .env                 # 환경 변수 (생성 필요)

    body: JSON.stringify({ user_input: '3' })├── .env.example         # 환경 변수 예시

});├── run.sh              # 실행 스크립트

```├── README.md           # 이 문서

└── userinfo/           # 사용자 응답 저장 폴더 (자동 생성)

---```



## 🔒 환경 변수## 💾 데이터 저장



### 로컬 개발사용자의 설문 응답은 `userinfo/[날짜]/[이름]_[생년월일].json` 형식으로 저장됩니다.



`.env` 파일:## ⚠️ 주의사항

```

OPENAI_API_KEY=sk-proj-...1. **OpenAI API 키**: 반드시 `.env` 파일에 유효한 OpenAI API 키를 설정해야 합니다.

PORT=50012. **방화벽**: 외부 접속을 위해 포트 5000을 열어야 할 수 있습니다.

FLASK_ENV=production3. **보안**: 프로덕션 환경에서는 HTTPS 설정을 권장합니다.

```

## 🛠 트러블슈팅

### Railway 배포

### 포트가 이미 사용 중인 경우

Railway Variables:

- `OPENAI_API_KEY`: OpenAI API 키```bash

- `FLASK_ENV`: `production`# 5000번 포트를 사용하는 프로세스 확인

lsof -i :5000

---

# 프로세스 종료

## 🎤 음성인식kill -9 [PID]

```

- Web Speech API 사용

- HTTPS 필수 (Railway 자동 제공)### Python 버전 확인

- 한국어 지원

- Chrome, Edge 권장```bash

python3 --version

---```



## 📚 추가 문서### 로그 확인



- Railway 배포: `RAILWAY_DEPLOY.md`서버 실행 시 터미널에 출력되는 로그를 확인하세요.

- 빠른 시작: `RAILWAY_QUICKSTART.md`

- Linux 설정: `LINUX_SETUP.md`## 📞 지원



---문제가 발생하면 터미널의 에러 메시지를 확인하세요.


## 🎯 배포 체크리스트

- [ ] Railway 가입
- [ ] 프로젝트 생성
- [ ] GitHub 저장소 연결
- [ ] 환경 변수 설정
- [ ] 배포 확인
- [ ] URL 테스트
- [ ] Frontend에 URL 전달

자세한 내용: `RAILWAY_QUICKSTART.md`
