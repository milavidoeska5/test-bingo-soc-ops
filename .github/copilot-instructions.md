# Copilot Workspace Instructions

## ✅ Pre-Commit Mandatory Checklist

**Before committing ANY changes:**
```bash
uv run ruff check .          # ✓ Must pass (linting)
uv run pytest                # ✓ Must pass (all tests)
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000  # ✓ Test in browser
```

---

## 🎮 Project Overview

**Soc Ops** — Social Bingo game (FastAPI + Jinja2 + HTMX). Players match questions to get 5 in a row.

| Tech | Details |
|------|---------|
| Backend | FastAPI (Python 3.13+), Pydantic, itsdangerous sessions |
| Frontend | Jinja2 templates, HTMX, custom CSS utilities |
| Testing | pytest, ruff linting |
| Package | uv (Python toolchain) |

**⚠️ Never use VS Code Simple Browser—HTMX needs a full browser. Start server, open `http://localhost:8000`.**


## 📁 Architecture

```
app/
├── main.py              # FastAPI routes & HTMX endpoints
├── game_logic.py        # Pure functions: board generation, bingo detection
├── game_service.py      # GameSession state management (cookies)
├── models.py            # Pydantic frozen models
├── data.py              # Question bank
├── templates/           # Jinja2 components
└── static/              # CSS utilities & HTMX

tests/                   # pytest (test_api.py, test_game_logic.py)
```

## 🎯 Key Patterns

| Aspect | Rule |
|--------|------|
| **Game Logic** | Pure functions in `game_logic.py`. Never mutate board—use `model_copy(update={})` |
| **State** | `GameSession` dataclass + in-memory store, sessions via signed cookies |
| **HTTP** | Endpoints return HTML fragments (not JSON). HTMX swaps responses into DOM |
| **Models** | Pydantic with `frozen=True` for immutable data; `@dataclass` for mutable state |
| **Testing** | pytest with class-based tests. Test status codes AND HTML content |
| **Caching** | `@functools.cache` for expensive operations |
| **Type Hints** | Required on all functions (`list[T]` not `List[T]`; Python 3.13+) |

---

## 🎨 Styling & Frontend

- **Component-based:** Jinja2 templates in `app/templates/`
- **HTMX:** Declarative interactivity (no JavaScript needed)
- **CSS:** Custom utilities (no external frameworks)
- **Design:** Distinctive, creative—avoid generic AI aesthetics. See [frontend-design.instructions.md](.github/instructions/frontend-design.instructions.md)

**CSS Quick Ref:** `.flex`, `.grid-cols-5`, `.p-4`, `.bg-accent`, `.text-lg`, `.font-bold`. Full list: [css-utilities.instructions.md](.github/instructions/css-utilities.instructions.md)

---

## 🎮 Game Rules

- **Board:** 5×5 grid, center is free space
- **Questions:** 24 unique (shuffled per game)
- **Win:** 5 in a row (horizontal, vertical, diagonal)
- **Key Functions:** `generate_board()`, `mark_square()`, `find_winning_line()`, `is_bingo()`

---

## ⚠️ Critical Rules

| Rule | Example |
|------|---------|
| **HTMX endpoints return HTML, not JSON** | `@app.post("/toggle/{i}")` returns `TemplateResponse` |
| **Never mutate board state** | ❌ `board.squares[i].marked = True` → ✅ `mark_square(board, i)` |
| **Sessions use signed cookies** | Don't leak session_id in URLs |
| **Type hints required** | `def foo(x: int) -> list[str]:` |
| **Test both status & HTML** | Check `response.status_code` and `response.text` contains expected content |

---

## 🔧 Common Tasks

**Add a game feature:** game_logic.py → test_game_logic.py → game_service.py → templates/ → main.py (routes)

**Update questions:** Edit `app/data.py` (no restart needed)

**Modify board display:** `app/templates/components/bingo_board.html`

**Run tests:** `uv run pytest` | `uv run pytest tests/test_api.py -v`

---

## 📚 Instruction Files

- [general.instructions.md](.github/instructions/general.instructions.md) — Dev practices
- [frontend-design.instructions.md](.github/instructions/frontend-design.instructions.md) — Design approach
- [css-utilities.instructions.md](.github/instructions/css-utilities.instructions.md) — CSS classes
- [README.md](../../README.md) — Lab guides & overview

---

**Last Updated:** May 2026 | **Lab:** Soc Ops — Social Bingo Game
