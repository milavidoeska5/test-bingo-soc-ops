import random
from dataclasses import dataclass, field

from app.game_logic import (
    check_bingo,
    check_scavenger_hunt_complete,
    generate_board,
    get_scavenger_hunt_progress,
    get_winning_square_ids,
    toggle_square,
)
from app.models import BingoLine, BingoSquareData, GameMode, GameState


@dataclass
class GameSession:
    """Holds the state for a single game session."""

    game_state: GameState = GameState.START
    mode: GameMode = GameMode.BINGO
    board: list[BingoSquareData] = field(default_factory=list)
    card_shuffle_deck: list[str] = field(default_factory=list)
    card_shuffle_current_text: str = ""
    card_shuffle_flip_state: bool = False
    card_shuffle_draw_count: int = 0
    winning_line: BingoLine | None = None
    show_completion_modal: bool = False

    @property
    def winning_square_ids(self) -> set[int]:
        return get_winning_square_ids(self.winning_line)

    @property
    def has_bingo(self) -> bool:
        return self.game_state == GameState.BINGO

    @property
    def is_scavenger_hunt(self) -> bool:
        return self.mode == GameMode.SCAVENGER_HUNT

    @property
    def is_card_deck_shuffle(self) -> bool:
        return self.mode == GameMode.CARD_DECK_SHUFFLE

    @property
    def scavenger_hunt_progress(self) -> tuple[int, int]:
        return get_scavenger_hunt_progress(self.board)

    @property
    def scavenger_hunt_completed_count(self) -> int:
        return self.scavenger_hunt_progress[0]

    @property
    def scavenger_hunt_total_count(self) -> int:
        return self.scavenger_hunt_progress[1]

    @property
    def scavenger_hunt_progress_percent(self) -> int:
        completed, total = self.scavenger_hunt_progress
        if total == 0:
            return 0
        return int((completed / total) * 100)

    @property
    def completion_title(self) -> str:
        if self.is_scavenger_hunt:
            return "Scavenger Hunt Complete"
        return "BINGO!"

    @property
    def completion_subtitle(self) -> str:
        if self.is_scavenger_hunt:
            completed, total = self.scavenger_hunt_progress
            return f"{completed} / {total} complete"
        return "Mission Complete!"

    def _card_shuffle_questions(self) -> list[str]:
        return [square.text for square in self.board if not square.is_free_space]

    def _rebuild_card_shuffle_deck(self) -> None:
        self.card_shuffle_deck = self._card_shuffle_questions()
        random.shuffle(self.card_shuffle_deck)

    def _prime_card_shuffle_prompt(self) -> None:
        if not self.is_card_deck_shuffle or self.game_state != GameState.PLAYING:
            return
        if not self.card_shuffle_deck:
            self._rebuild_card_shuffle_deck()
        if not self.card_shuffle_deck:
            return

        self.card_shuffle_current_text = self.card_shuffle_deck.pop()

    def draw_next_card_shuffle_prompt(self) -> None:
        if not self.is_card_deck_shuffle or self.game_state != GameState.PLAYING:
            return

        if self.card_shuffle_flip_state:
            self.card_shuffle_flip_state = False
        else:
            if not self.card_shuffle_deck:
                self._rebuild_card_shuffle_deck()
            if not self.card_shuffle_deck:
                return
            self.card_shuffle_current_text = self.card_shuffle_deck.pop()
            self.card_shuffle_draw_count += 1
            self.card_shuffle_flip_state = True

    def start_game(self, mode: GameMode = GameMode.BINGO) -> None:
        self.mode = mode
        self.board = generate_board()
        self.card_shuffle_deck = []
        self.card_shuffle_current_text = ""
        self.card_shuffle_flip_state = False
        self.card_shuffle_draw_count = 0
        self.winning_line = None
        self.game_state = GameState.PLAYING
        self.show_completion_modal = False

        if self.is_card_deck_shuffle:
            self._prime_card_shuffle_prompt()

    def _complete_game(self, winning_line: BingoLine | None = None) -> None:
        self.winning_line = winning_line
        self.game_state = GameState.BINGO
        self.show_completion_modal = True

    def handle_square_click(self, square_id: int) -> None:
        if self.game_state != GameState.PLAYING:
            return
        self.board = toggle_square(self.board, square_id)

        if self.is_scavenger_hunt:
            if check_scavenger_hunt_complete(self.board):
                self._complete_game()
            return

        if self.winning_line is None:
            bingo = check_bingo(self.board)
            if bingo is not None:
                self._complete_game(bingo)

    def reset_game(self) -> None:
        self.game_state = GameState.START
        self.mode = GameMode.BINGO
        self.board = []
        self.card_shuffle_deck = []
        self.card_shuffle_current_text = ""
        self.card_shuffle_flip_state = False
        self.card_shuffle_draw_count = 0
        self.winning_line = None
        self.show_completion_modal = False

    def dismiss_modal(self) -> None:
        self.show_completion_modal = False
        self.game_state = GameState.PLAYING


# In-memory session store keyed by session ID
_sessions: dict[str, GameSession] = {}


def get_session(session_id: str) -> GameSession:
    """Get or create a game session for the given session ID."""
    if session_id not in _sessions:
        _sessions[session_id] = GameSession()
    return _sessions[session_id]
