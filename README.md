# team-docs MCP (read-only)

플랫폼개발팀 문서(`data/`)를 읽기 전용으로 제공하는 MCP 서버다. Streamable HTTP, 경로 `/mcp`.

- 도구: `list_files` · `read_file` · `search` — 쓰기 도구는 없다
- 대상: `data/` 하위 텍스트 문서만
- 연결: `claude mcp add --transport http team-docs https://<서비스 주소>/mcp`

로컬 실행: `pip install -r requirements.txt && python server.py` → `http://127.0.0.1:8000/mcp`
