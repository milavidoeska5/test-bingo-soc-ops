🌐 [Português (BR)](README.pt_BR.md) | [Español](README.es.md)

<div align="center">

# 🎲 Soc Ops

### Social Bingo for In-Person Mixers

[![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![HTMX](https://img.shields.io/badge/HTMX-1.x-blue)](https://htmx.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Find people who match the questions. Get 5 in a row. Win bragging rights.** 🏆

[🚀 Get Started](#-getting-started) · [📚 Lab Guide](#-lab-guide) · [🛠️ Tech Stack](#%EF%B8%8F-tech-stack) · [🤝 Contributing](CONTRIBUTING.md)

</div>

---

## ✨ What is Soc Ops?

**Soc Ops** is a fast-paced, real-world **Social Bingo** game designed for team mixers, meetups, and events. Instead of numbers, each square contains a prompt — *"speaks more than 2 languages"*, *"has a hidden talent"*, *"can juggle"* — and you have to find real people in the room who match!

```
┌─────────────────────────────────────────────────────┐
│  🎯  bikes    │  🌍  lived   │  🐾  has a  │  ☕  prefers  │  🎵  plays   │
│     to work   │   abroad     │    pet      │  tea over ☕ │  instrument  │
├───────────────┼──────────────┼─────────────┼─────────────┼──────────────┤
│  🗣️  speaks  │  🏃  ran a  │  🌟  met a  │  🤹  can   │  🪂  been   │
│  2+ languages │   marathon   │  celebrity  │   juggle    │  skydiving   │
├───────────────┼──────────────┼─────────────┼─────────────┼──────────────┤
│  🍳  loves   │  🌱  has a  │  ✨  FREE  │  🌏  been  │  ✋  left-  │
│    cooking    │    garden    │    SPACE    │   to Asia   │   handed     │
├───────────────┼──────────────┼─────────────┼─────────────┼──────────────┤
│  👯  has a   │  🎮  plays  │  🧘  does  │  🎩  hidden │  🌶️  loves  │
│     twin      │  video games │     yoga    │    talent   │  spicy food  │
├───────────────┼──────────────┼─────────────┼─────────────┼──────────────┤
│  📺  been    │  🏆  collects│  📖  read  │  🤟  knows │  💡  unique  │
│     on TV     │   uniquely   │  book/month │  sign lang. │   hobby      │
└─────────────────────────────────────────────────────┘
```

---

## 🎮 How to Play

| Step | Action |
|------|--------|
| **1** | Open the app on your phone or browser |
| **2** | Mingle — find real people who match each square |
| **3** | Tap a square when you find a match |
| **4** | Get **5 in a row** (horizontal, vertical, or diagonal) to win! |

> 💡 The center square is a **FREE SPACE** — already marked for you!

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) + Python 3.13 |
| **Templating** | [Jinja2](https://jinja.palletsprojects.com/) |
| **Interactivity** | [HTMX](https://htmx.org/) — no JavaScript needed |
| **Sessions** | Signed cookies via `itsdangerous` |
| **Styling** | Custom CSS utilities |
| **Testing** | pytest + ruff |
| **Toolchain** | [uv](https://docs.astral.sh/uv/) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) installed

### Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/milavidoeska5/test-bingo-soc-ops.git
cd test-bingo-soc-ops

# 2. Install dependencies
uv sync

# 3. Run the app
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open **http://localhost:8000** in your browser and start playing! 🎉

### Run Tests

```bash
uv run pytest          # run all tests
uv run ruff check .    # lint
```

> 💡 **DevContainer users:** Everything is pre-configured — just open in VS Code and go!

---

## 📚 Lab Guide

This project is also a **hands-on GitHub Copilot Agent workshop**. Follow the lab parts to learn context engineering, agentic development, and AI-assisted design.

> ⏱️ Total time: ~1 hour | Level: Intermediate

| Part | Title | Time | Description |
|------|-------|------|-------------|
| [**00**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=00-overview) | Overview & Checklist | — | Prerequisites and setup |
| [**01**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=01-setup) | Setup & Context Engineering | 15 min | Teach AI about your codebase |
| [**02**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=02-design) | Design-First Frontend | 15 min | Redesign the UI with creative themes |
| [**03**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=03-quiz-master) | Custom Quiz Master | 10 min | Create your own quiz themes |
| [**04**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=04-multi-agent) | Multi-Agent Development | 20 min | Build features with TDD agents |

> 📝 Lab guides are also available in the [`workshop/`](workshop/) folder for offline reading.

Head to **[Part 00: Overview](https://copilot-dev-days.github.io/agent-lab-python/step.html?step=00-overview)** to begin.

---

## 🏗️ Project Structure

```
app/
├── main.py           # FastAPI routes & HTMX endpoints
├── game_logic.py     # Pure functions: board generation, bingo detection
├── game_service.py   # GameSession state management
├── models.py         # Pydantic frozen models
├── data.py           # Question bank (24 prompts)
├── templates/        # Jinja2 components
└── static/           # CSS utilities & HTMX

tests/                # pytest test suite
workshop/             # Offline lab guides
```

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
