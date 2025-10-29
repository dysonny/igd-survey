# 🚂 Railway 빠른 배포 가이드

## 5분만에 배포하기!

### 1️⃣ Railway 가입 (30초)
https://railway.app → "Start a New Project" → GitHub 로그인

### 2️⃣ 프로젝트 생성 (1분)
- "Deploy from GitHub repo" 클릭
- 저장소 선택 (또는 새로 만들기)

### 3️⃣ 환경 변수 설정 (1분)
Variables 탭에서:
- `OPENAI_API_KEY` = `sk-proj-...` (본인 키)
- `FLASK_ENV` = `production`

### 4️⃣ 배포! (2분)
자동 배포 시작 → 완료!

### 5️⃣ URL 받기
Settings → Public Networking → Generate Domain
```
https://your-app.up.railway.app
```

## 🎉 완료!

이 URL을 Frontend 개발자에게 전달하세요.

---

## 📝 더 자세한 내용은?
`RAILWAY_DEPLOY.md` 참고

## ❓ GitHub 저장소가 없다면?
Railway에서 "Empty Project" 선택 후 CLI로 배포 (RAILWAY_DEPLOY.md 참고)
