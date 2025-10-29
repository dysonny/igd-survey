# 🚂 Railway로 IGD 챗봇 배포하기

Railway는 무료로 웹 애플리케이션을 호스팅할 수 있는 플랫폼입니다.

## ✨ 장점
- ✅ **무료** (월 $5 크레딧 제공, 취미 프로젝트에 충분)
- ✅ **자동 HTTPS** (음성인식 작동)
- ✅ **고정 URL** (변경되지 않음)
- ✅ **GitHub 연동** 또는 직접 배포
- ✅ **자동 재시작**
- ✅ **간단한 설정**

---

## 🚀 Railway 배포 방법

### 방법 1: GitHub 연동 (추천)

#### 1단계: GitHub 저장소 생성

1. GitHub 접속: https://github.com
2. 새 저장소 생성 (New repository)
3. 이름: `igd-chatbot-survey`
4. Private 선택 (API 키 보호)
5. Create repository

#### 2단계: 코드 업로드

```bash
cd /Users/sondongyoung/Desktop/replit

# Git 초기화
git init

# .gitignore 확인 (이미 있음)
# userinfo/, venv/, .env 등이 제외됨

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: IGD Chatbot Survey"

# GitHub 저장소 연결 (YOUR_USERNAME을 본인 GitHub ID로)
git remote add origin https://github.com/YOUR_USERNAME/igd-chatbot-survey.git

# 업로드
git branch -M main
git push -u origin main
```

#### 3단계: Railway 배포

1. **Railway 가입**: https://railway.app
   - GitHub 계정으로 로그인

2. **New Project** 클릭

3. **Deploy from GitHub repo** 선택

4. 저장소 선택: `igd-chatbot-survey`

5. **환경 변수 설정**:
   - `OPENAI_API_KEY`: 본인의 OpenAI API 키
   - `PORT`: 자동 설정됨 (설정 불필요)
   - `FLASK_ENV`: `production`

6. **Deploy** 클릭!

7. 배포 완료 후 **Deployments** 탭에서 URL 확인:
   ```
   https://your-app-name.up.railway.app
   ```

---

### 방법 2: CLI로 직접 배포

#### 1단계: Railway CLI 설치

```bash
# macOS
brew install railway

# 또는 npm
npm i -g @railway/cli
```

#### 2단계: 로그인 및 배포

```bash
cd /Users/sondongyoung/Desktop/replit

# Railway 로그인
railway login

# 새 프로젝트 생성
railway init

# 환경 변수 설정
railway variables set OPENAI_API_KEY="your-api-key-here"
railway variables set FLASK_ENV="production"

# 배포
railway up

# URL 확인
railway open
```

---

## 📋 필수 파일 확인

다음 파일들이 프로젝트에 있어야 합니다:

✅ `main.py` - Flask 앱
✅ `requirements.txt` - Python 패키지
✅ `Procfile` - 실행 명령
✅ `runtime.txt` - Python 버전
✅ `.gitignore` - 제외 파일
✅ `.env.example` - 환경 변수 예시

---

## 🔒 보안 설정

### .gitignore 확인

`.env` 파일이 GitHub에 업로드되지 않도록 확인:

```
# .gitignore에 포함되어야 함
.env
userinfo/
venv/
__pycache__/
*.pyc
*.log
```

### Railway 환경 변수 설정

Railway 대시보드에서 설정:

1. 프로젝트 선택
2. **Variables** 탭
3. **New Variable** 클릭
4. 추가:
   - `OPENAI_API_KEY`: `sk-proj-...`
   - `FLASK_ENV`: `production`

---

## 🌐 배포 후 URL 공유

### Frontend 개발자에게 전달

```
IGD 챗봇 설문조사 API

Base URL: https://your-app.up.railway.app

엔드포인트:
- POST /user-info  (사용자 정보 저장)
- POST /chat       (질문/응답)
- POST /reset      (설문 초기화)
- GET  /history    (대화 기록)
- GET  /           (메인 페이지)

특징:
- HTTPS 지원 (음성인식 가능)
- CORS 허용
- 24/7 실행
```

---

## 📊 Railway 무료 플랜

- **월 $5 크레딧** 제공
- **500시간 실행 시간** (약 20일 연속 실행)
- **100GB 아웃바운드 네트워크**
- **1GB 메모리**
- **1GB 디스크**

충분히 사용 가능! 필요시 유료 플랜 업그레이드 가능.

---

## 🔄 업데이트 방법

### GitHub 연동 사용 시

```bash
# 코드 수정 후
git add .
git commit -m "Update chatbot"
git push

# Railway가 자동으로 재배포!
```

### CLI 사용 시

```bash
railway up
```

---

## 📝 배포 체크리스트

- [ ] GitHub 저장소 생성
- [ ] 코드 업로드 (git push)
- [ ] Railway 가입 및 로그인
- [ ] 프로젝트 생성
- [ ] GitHub 저장소 연결
- [ ] 환경 변수 설정 (OPENAI_API_KEY)
- [ ] 배포 확인
- [ ] URL 테스트
- [ ] Frontend 개발자에게 URL 전달

---

## 🛠 트러블슈팅

### 배포 실패

**로그 확인**:
```bash
railway logs
```

**흔한 문제**:
1. `requirements.txt` 누락 → 추가
2. 환경 변수 미설정 → Railway 대시보드에서 설정
3. 포트 오류 → `Procfile` 확인

### 앱이 시작되지 않음

1. Railway 대시보드 → **Deployments**
2. 로그 확인
3. 환경 변수 확인

### 500 에러

- OpenAI API 키 확인
- 로그에서 에러 메시지 확인

---

## 💡 추가 팁

### 커스텀 도메인 (선택)

Railway에서 본인 도메인 연결 가능:
- `survey.yourdomain.com`

### 데이터베이스 추가 (선택)

Railway에서 PostgreSQL 추가 가능:
- 현재는 JSON 파일 저장
- 필요시 DB 연동 가능

---

## 📞 도움말

- Railway 문서: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

---

## 🎯 요약

1. **GitHub에 코드 업로드**
2. **Railway 가입** (https://railway.app)
3. **GitHub 저장소 연결**
4. **환경 변수 설정** (API 키)
5. **배포!**
6. **URL 받아서 공유**

끝! 🎉
