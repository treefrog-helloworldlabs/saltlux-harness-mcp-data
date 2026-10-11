"""team-docs MCP 서버 — 플랫폼개발팀 문서를 읽기만 하는 MCP (Streamable HTTP).

배포: Render 웹 서비스(render.yaml). 로컬 확인:
    pip install -r requirements.txt
    python server.py              # http://127.0.0.1:8000/mcp
    PORT=9000 python server.py    # 포트 변경

도구는 읽기 셋뿐이다 — list_files · read_file · search.
쓰기·삭제 도구가 없으므로 수강생이 무엇을 요청해도 data/ 는 바뀌지 않는다.
대상은 이 파일 옆 data/ 하위뿐이며, 그 밖의 경로는 거부한다.
"""

import os
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from starlette.requests import Request
from starlette.responses import PlainTextResponse

DATA = (Path(__file__).parent / "data").resolve()
TEXT_SUFFIXES = {".md", ".txt", ".csv", ".json"}
MAX_CHARS = 20_000

server = MCPServer(
    "team-docs",
    instructions="플랫폼개발팀 문서(공지·규정·용어집·변경 기록)를 읽기 전용으로 제공한다.",
)


def _inside(rel: str) -> Path:
    """data/ 기준 상대경로를 실제 경로로 바꾼다. data/ 밖이면 거부한다."""
    rel = (rel or "").strip().lstrip("/\\")
    p = (DATA / rel).resolve()
    if p != DATA and DATA not in p.parents:
        raise ValueError("data 폴더 밖의 경로는 읽을 수 없다")
    return p


def _rel(p: Path) -> str:
    return p.relative_to(DATA).as_posix()


@server.tool()
def list_files(folder: str = "") -> str:
    """팀 문서 목록을 돌려준다. folder: data 기준 하위 폴더(예: "규정"). 비우면 전체."""
    try:
        base = _inside(folder)
    except ValueError as e:
        return str(e)
    if not base.is_dir():
        return f"폴더가 없다: {folder}"
    files = sorted(f for f in base.rglob("*") if f.is_file() and f.suffix in TEXT_SUFFIXES)
    if not files:
        return "문서가 없다."
    return "\n".join(f"{_rel(f)}\t{f.stat().st_size}B" for f in files)


@server.tool()
def read_file(path: str) -> str:
    """팀 문서 하나의 내용을 돌려준다. path: list_files 가 돌려준 경로(예: "규정/보안-규정.md")."""
    try:
        p = _inside(path)
    except ValueError as e:
        return str(e)
    if not p.is_file():
        return f"파일이 없다: {path}"
    if p.suffix not in TEXT_SUFFIXES:
        return f"텍스트 문서만 읽을 수 있다: {path}"
    return p.read_text(encoding="utf-8")[:MAX_CHARS]


@server.tool()
def search(keyword: str) -> str:
    """모든 팀 문서에서 키워드가 들어 있는 줄을 찾아 '경로:줄번호: 내용'으로 돌려준다."""
    keyword = (keyword or "").strip()
    if not keyword:
        return "키워드를 넣어야 한다."
    hits = []
    for f in sorted(DATA.rglob("*")):
        if not (f.is_file() and f.suffix in TEXT_SUFFIXES):
            continue
        for no, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if keyword.lower() in line.lower():
                hits.append(f"{_rel(f)}:{no}: {line.strip()}")
    return "\n".join(hits[:100]) if hits else f"'{keyword}'가 들어 있는 줄이 없다."


@server.custom_route("/", methods=["GET"])
async def health(_: Request) -> PlainTextResponse:
    """깨우기·상태 확인용. 브라우저로 열면 한 줄이 보인다."""
    count = sum(1 for f in DATA.rglob("*") if f.is_file())
    return PlainTextResponse(f"team-docs MCP ok — 문서 {count}개, 연결 주소는 /mcp\n")


if __name__ == "__main__":
    server.run(
        "streamable-http",
        host=os.environ.get("HOST", "0.0.0.0" if "PORT" in os.environ else "127.0.0.1"),
        port=int(os.environ.get("PORT", "8000")),
        stateless_http=True,
    )
