# 🚀 Findation Backend

애플 파인데이션 프로그램 팀 **Findation**의 백엔드 레포지토리입니다.  
이 프로젝트는 Django REST Framework를 기반으로 RESTful API 서버를 구현하며, 클라이언트 앱과 통신합니다.

---

## 📦 Python 패키지 관리

패키지는 `requirements.txt` 파일을 통해 관리합니다.

### ✅ 설치 명령어

아래 커맨드를 통해 한번에 패키지를 설치할 수 있습니다

```bash
pip install -r requirements.txt
```

새로운 패키지를 설치한 뒤에는 아래 커맨드를 통해 requirements.txt를 갱신해 주세요:

```bash
pip freeze > requirements.txt
```

## 💬 커밋 메시지 규칙

커밋 메시지는 다음의 규칙에 따라 작성합니다.
커밋 예약어는 모두 대문자로 작성하며, 메시지의 앞에 붙입니다.

### ✅ 커밋 메시지 예시

| 커밋 태그  | 설명                                                  |
| ---------- | ----------------------------------------------------- |
| `FEAT`     | 새로운 기능에 대한 커밋                               |
| `FIX`      | 버그 수정에 대한 커밋                                 |
| `BUILD`    | 빌드 관련 파일 수정 / 모듈 설치 또는 삭제에 대한 커밋 |
| `CHORE`    | 그 외 자잘한 수정에 대한 커밋                         |
| `DOCS`     | 문서 수정에 대한 커밋                                 |
| `STYLE`    | 코드 스타일 혹은 포맷 등에 관한 커밋                  |
| `REFACTOR` | 코드 리팩토링에 대한 커밋                             |
| `TEST`     | 테스트 코드 수정에 대한 커밋                          |
| `PERF`     | 성능 개선에 대한 커밋                                 |

```bash
FEAT: add user login API
FIX: fix push token saving logic
TEST: add unit test for login API
PERF: improve query performance for user list
```
