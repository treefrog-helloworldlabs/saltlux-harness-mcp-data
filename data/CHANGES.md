# auth-api 변경 기록

## 0.2.0 (2026-10-15 배포)
- feat: 로그인 실패 5회가 넘으면 해당 이메일을 10분간 잠근다
- feat: refresh token 재발급 때 이전 refresh token 을 폐기한다(토큰 회전)
- fix: 이미 가입된 이메일로 가입하면 500 대신 409 를 돌려준다
- refactor: 요청 로거를 미들웨어 파일로 분리 (동작 변화 없음)
- breaking: `/auth/token` 경로 제거 → `/auth/refresh` 사용

## 0.1.0 (2026-09-24 배포)
- feat: 회원가입·로그인·토큰 재발급 API
