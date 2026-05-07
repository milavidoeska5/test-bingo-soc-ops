import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestHomePage:
    def test_home_returns_200(self, client: TestClient) -> None:
        response = client.get("/")
        assert response.status_code == 200

    def test_home_offers_scavenger_hunt_mode(self, client: TestClient) -> None:
        response = client.get("/")

        assert "Scavenger Hunt" in response.text
        assert 'value="scavenger_hunt"' in response.text

    def test_home_contains_start_screen(self, client: TestClient) -> None:
        response = client.get("/")
        assert "Soc Ops" in response.text
        assert "Launch Mission" in response.text
        assert "How to Play" in response.text

    def test_home_sets_session_cookie(self, client: TestClient) -> None:
        response = client.get("/")
        assert "session" in response.cookies


class TestStartGame:
    def test_start_returns_game_board(self, client: TestClient) -> None:
        # First visit to get session
        client.get("/")
        response = client.post("/start")
        assert response.status_code == 200
        assert "FREE SPACE" in response.text
        assert "Exit" in response.text

    def test_start_scavenger_hunt_returns_checklist_view(
        self, client: TestClient
    ) -> None:
        client.get("/")
        response = client.post("/start", data={"mode": "scavenger_hunt"})

        assert response.status_code == 200
        assert "Scavenger Hunt" in response.text
        assert "0 / 24 complete" in response.text
        assert "FREE SPACE" not in response.text


class TestScavengerHunt:
    def test_toggle_updates_scavenger_hunt_progress(self, client: TestClient) -> None:
        client.get("/")
        client.post("/start", data={"mode": "scavenger_hunt"})

        response = client.post("/toggle/0")

        assert response.status_code == 200
        assert "1 / 24 complete" in response.text
        assert "progress-meter-fill" in response.text

    def test_completing_scavenger_hunt_shows_completion_modal(
        self, client: TestClient
    ) -> None:
        client.get("/")
        client.post("/start", data={"mode": "scavenger_hunt"})

        response = None
        for square_id in range(25):
            if square_id == 12:
                continue
            response = client.post(f"/toggle/{square_id}")

        assert response is not None
        assert response.status_code == 200
        assert "Scavenger Hunt Complete" in response.text
        assert "24 / 24 complete" in response.text

    def test_board_has_25_squares(self, client: TestClient) -> None:
        client.get("/")
        response = client.post("/start")
        # Count the toggle buttons (squares with hx-post="/toggle/")
        assert response.text.count('hx-post="/toggle/') == 24  # 24 + 1 free space


class TestToggleSquare:
    def test_toggle_marks_square(self, client: TestClient) -> None:
        client.get("/")
        client.post("/start")
        response = client.post("/toggle/0")
        assert response.status_code == 200
        # The response should contain the game screen with a marked square
        assert "FREE SPACE" in response.text


class TestResetGame:
    def test_reset_returns_start_screen(self, client: TestClient) -> None:
        client.get("/")
        client.post("/start")
        response = client.post("/reset")
        assert response.status_code == 200
        assert "Launch Mission" in response.text
        assert "How to Play" in response.text


class TestDismissModal:
    def test_dismiss_returns_game_screen(self, client: TestClient) -> None:
        client.get("/")
        client.post("/start")
        response = client.post("/dismiss-modal")
        assert response.status_code == 200
        assert "FREE SPACE" in response.text
