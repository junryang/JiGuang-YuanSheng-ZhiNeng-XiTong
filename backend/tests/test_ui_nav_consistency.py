import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


_NAV_CORE_LINKS = (
    "agents.html",
    "collab.html",
    "marketing.html",
    "skills.html",
    "memory.html",
    "tasks.html",
    "chat.html",
)


@pytest.mark.parametrize(
    ("path", "must_include"),
    [
        ("/ui/login.html", _NAV_CORE_LINKS),
        ("/ui/agents.html", _NAV_CORE_LINKS[1:]),
        ("/ui/collab.html", _NAV_CORE_LINKS[2:]),
        ("/ui/marketing.html", ("agents.html", "skills.html", "collab.html", "memory.html", "tasks.html", "chat.html")),
        ("/ui/skills.html", ("agents.html", "marketing.html", "collab.html", "memory.html", "tasks.html", "chat.html")),
        ("/ui/memory.html", ("agents.html", "collab.html", "marketing.html", "skills.html", "tasks.html", "chat.html")),
        ("/ui/tasks.html", ("agents.html", "collab.html", "marketing.html", "skills.html", "memory.html", "chat.html")),
        ("/ui/chat.html", ("agents.html", "collab.html", "marketing.html", "skills.html", "memory.html", "tasks.html")),
        ("/ui/project.html?id=proj-nav-smoke", ("agents.html", "collab.html", "marketing.html", "skills.html", "memory.html", "tasks.html", "chat.html")),
    ],
)
def test_ui_nav_core_links(path: str, must_include: tuple[str, ...]):
    r = client.get(path)
    assert r.status_code == 200
    for link in must_include:
        assert link.encode("utf-8") in r.content


def _assert_nav_order(content: bytes, ordered_links: tuple[str, ...]) -> None:
    txt = content.decode("utf-8")
    last = -1
    for link in ordered_links:
        cur = txt.find(link)
        assert cur >= 0, f"missing link: {link}"
        assert cur > last, f"link order mismatch: {link}"
        last = cur


@pytest.mark.parametrize(
    ("path", "ordered_links"),
    [
        ("/ui/", _NAV_CORE_LINKS),
        ("/ui/login.html", _NAV_CORE_LINKS),
        ("/ui/agents.html", _NAV_CORE_LINKS[1:]),
        ("/ui/collab.html", ("agents.html", "marketing.html", "skills.html", "memory.html", "tasks.html", "chat.html")),
        ("/ui/marketing.html", ("agents.html", "collab.html", "skills.html", "memory.html", "tasks.html", "chat.html")),
        ("/ui/skills.html", ("agents.html", "collab.html", "marketing.html", "memory.html", "tasks.html", "chat.html")),
        ("/ui/memory.html", ("agents.html", "collab.html", "marketing.html", "skills.html", "tasks.html", "chat.html")),
        ("/ui/tasks.html", ("agents.html", "collab.html", "marketing.html", "skills.html", "memory.html", "chat.html")),
        ("/ui/chat.html", ("agents.html", "collab.html", "marketing.html", "skills.html", "memory.html", "tasks.html")),
        ("/ui/project.html?id=proj-nav-order", ("agents.html", "collab.html", "marketing.html", "skills.html", "memory.html", "tasks.html", "chat.html")),
    ],
)
def test_ui_nav_core_links_order(path: str, ordered_links: tuple[str, ...]):
    r = client.get(path)
    assert r.status_code == 200
    _assert_nav_order(r.content, ordered_links)


@pytest.mark.parametrize(
    ("path", "ordered_links"),
    [
        ("/ui/", ("docs", "redoc", "login.html")),
        ("/ui/collab.html", ("docs", "redoc", "login.html")),
        ("/ui/agents.html", ("docs", "redoc")),
        ("/ui/tasks.html", ("docs", "redoc")),
        ("/ui/memory.html", ("docs", "redoc")),
        ("/ui/chat.html", ("docs", "redoc")),
        ("/ui/project.html?id=proj-nav-aux", ("docs", "redoc")),
    ],
)
def test_ui_nav_aux_links_order(path: str, ordered_links: tuple[str, ...]):
    r = client.get(path)
    assert r.status_code == 200
    _assert_nav_order(r.content, ordered_links)
