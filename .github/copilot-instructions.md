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

## 🌌 Design Guide — Space Galaxy Theme

The current visual design is a **deep-space galaxy** aesthetic. Preserve and extend it when making UI changes.

### Palette (CSS variables in `app/static/css/app.css`)

| Variable | Value | Role |
|---|---|---|
| `--space-0` | `#020814` | Deepest bg (modal overlay, button text) |
| `--space-1` | `#050a18` | Body background base |
| `--space-2` | `#0a1628` | Card / cell backgrounds |
| `--cyan` | `#00e5ff` | Primary accent — titles, glows, CTAs |
| `--gold` | `#ffd700` | Win state — winning cells, modal, logo pulse |
| `--violet` | `#a855f7` | Free space — subtle third accent |
| `--green` | `#00ff88` | Marked cells |
| `--text-bright` | `#e8f4ff` | Primary readable text |
| `--text-mid` | `#8dafc8` | Secondary / body text |
| `--text-dim` | `#4a6a8a` | Hints, instructions |

### Typography

| Font | Import | Usage |
|---|---|---|
| **Orbitron** | Google Fonts | Headings, buttons, labels — sci-fi display |
| **Exo 2** | Google Fonts | Body text, how-to items — readable sci-fi |

### Animations (CSS-only, no JS)

| Name | Target | Effect |
|---|---|---|
| `nebulaDrift` | `body` bg | Slow breathing nebula gradient |
| `starDrift1/2` | `body::before/after` | Two layers of tiled star dots drifting |
| `logoPulse` | `.cosmic-logo` | Gold ✦ logo breathes with glow |
| `winPulse` | `.cell-winning` | Gold cells pulse on winning line |
| `goldPulse` | `.bingo-banner` | Banner glows on bingo |
| `modalReveal` | `.modal-card` | Scale+fade-in on bingo modal open |
| `starSpin` | `.modal-star` | ✦ star rotates in modal |
| `ringRotate` | `.modal-ring` | Conic gradient border orbits modal card |

### Key Component Classes

| Class | Description |
|---|---|
| `.title-cosmic` | Orbitron, cyan glow — main page title |
| `.cosmic-logo` | Gold pulsing ✦ symbol |
| `.subtitle-cosmic` | Spaced uppercase subtitle |
| `.card-glass` | Dark glassmorphism card with cyan border |
| `.btn-launch` | Cyan gradient CTA button with glow |
| `.btn-continue` | Same as btn-launch, used in modal |
| `.space-header` | Dark blurred header bar |
| `.space-header-title` | Orbitron header brand text |
| `.btn-back` | Dim text back/exit button |
| `.bingo-banner` | Gold banner strip with pulse animation |
| `.cell-default` | Default board cell — dark glass, cyan hover glow |
| `.cell-marked` | Marked cell — green tint + glow |
| `.cell-winning` | Winning line cell — gold pulse animation |
| `.cell-free` | Center free space — violet tint |
| `.modal-overlay` | Dark radial-gradient fullscreen overlay |
| `.modal-card` | Glassmorphism bingo win card |
| `.modal-ring` | Rotating conic gradient ring behind card |

### Rules for Extending the Design

- **Always use CSS variables** — never hardcode `#00e5ff` or `rgba(0,229,255,...)` directly
- **Glassmorphism pattern:** `background: rgba(10, 22, 40, 0.7); backdrop-filter: blur(Npx); border: 1px solid rgba(0,229,255,0.2);`
- **Glow pattern:** `box-shadow: 0 0 Npx var(--cyan-glow)` or `text-shadow: 0 0 20px var(--gold-glow)`
- **Keep animations CSS-only** — no JavaScript for visual effects
- **Use ✦ (U+2726)** as the star/bullet symbol throughout the UI (not ★ or •)

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
