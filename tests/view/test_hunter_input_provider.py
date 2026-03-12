import random
from unittest.mock import patch

import pytest

from src.models.board import Point
from src.models.common import Action, CellState
from src.models.ship import Destroyer
from src.models.turn import Turn
from src.models.turn_result import TurnResult
from src.view.input_providers.hunter_input_provider import HunterInputProvider


@pytest.fixture
def provider():
    return HunterInputProvider()


@pytest.fixture
def alive_ship():
    ship = Destroyer()
    return ship


@pytest.fixture
def destroyed_ship():
    ship = Destroyer()
    ship.hit_points = 0
    return ship

@pytest.fixture
def mock_random(monkeypatch):
    def mock_randint(a, b):
        # Всегда возвращает 5
        return 5
    monkeypatch.setattr(random, 'randint', mock_randint)


class TestHunterInputProviderGetInput:
    def test_get_input_returns_turn_with_shot_action(self, provider):
        # arrange
        # (provider from fixture)

        # act
        turn = provider.get_input()

        # assert
        assert turn.action == Action.SHOT

    def test_get_input_returns_turn_with_valid_point(self, provider):
        # arrange
        # (provider from fixture)

        # act
        turn = provider.get_input()

        # assert
        assert turn.point is not None
        assert 0 <= turn.point.row <= 9
        assert 0 <= turn.point.column <= 9

    def test_get_input_does_not_repeat_shots(self, provider):
        # arrange
        fired_points = set()

        # act
        for _ in range(100):
            turn = provider.get_input()
            fired_points.add(turn.point)

        # assert
        assert len(fired_points) == 100

    def test_get_input_uses_hunt_queue_first(self, provider):
        # arrange
        expected_point = Point(3, 3)
        provider._hunt_queue.append(expected_point)

        # act
        turn = provider.get_input()

        # assert
        assert turn.point == expected_point
        assert turn.action == Action.SHOT

    def test_get_input_skips_already_fired_point_in_hunt_queue(self, provider, mock_random):
        # arrange
        already_fired = Point(3, 3)
        shot_point = Point(5, 5)

        provider._shots_fired.add(already_fired)
        provider._hunt_queue.append(already_fired)

        # act
        turn = provider.get_input()

        # assert
        assert turn.point == shot_point

    def test_get_input_falls_back_to_random_when_hunt_queue_empty(self, provider):
        # arrange
        # (provider from fixture)

        # act
        with patch('src.view.input_providers.hunter_input_provider.random.randint', side_effect=[5, 7]):
            turn = provider.get_input()

        # assert
        assert turn.point == Point(5, 7)

    def test_get_input_adds_point_to_shots_fired(self, provider):
        # arrange
        # (provider from fixture)

        # act
        with patch('src.view.input_providers.hunter_input_provider.random.randint', side_effect=[2, 3]):
            turn = provider.get_input()

        # assert
        assert turn.point in provider._shots_fired

    def test_get_input_retries_until_finding_unfired_point(self, provider):
        # arrange
        provider._shots_fired.add(Point(0, 0))
        provider._shots_fired.add(Point(1, 1))

        # act
        with patch('src.view.input_providers.hunter_input_provider.random.randint', 
                   side_effect=[0, 0, 1, 1, 2, 2]):
            turn = provider.get_input()

        # assert
        assert turn.point == Point(2, 2)


class TestHunterInputProviderNotifyResult:
    def test_notify_result_does_nothing_when_point_is_none(self, provider, alive_ship):
        # arrange
        turn_result = TurnResult(
            turn=Turn(Action.SHOT, None),
            ship=alive_ship,
            result=CellState.HIT
        )

        # act
        provider.notify_result(turn_result)

        # assert
        assert len(provider._hunt_queue) == 0

    def test_notify_result_does_nothing_when_ship_is_none(self, provider):
        # arrange
        turn_result = TurnResult(
            turn=Turn(Action.SHOT, Point(5, 5)),
            ship=None,
            result=CellState.MISS
        )

        # act
        provider.notify_result(turn_result)

        # assert
        assert len(provider._hunt_queue) == 0

    def test_notify_result_adds_neighbors_to_hunt_queue_when_ship_alive(self, provider, alive_ship):
        # arrange
        turn_result = TurnResult(
            turn=Turn(Action.SHOT, Point(5, 5)),
            ship=alive_ship,
            result=CellState.HIT
        )

        # act
        provider.notify_result(turn_result)

        # assert
        assert len(provider._hunt_queue) == 4
        assert Point(4, 5) in provider._hunt_queue
        assert Point(6, 5) in provider._hunt_queue
        assert Point(5, 4) in provider._hunt_queue
        assert Point(5, 6) in provider._hunt_queue

    def test_notify_result_excludes_already_fired_neighbors_from_hunt_queue(self, provider, alive_ship):
        # arrange
        provider._shots_fired.add(Point(4, 5))
        provider._shots_fired.add(Point(5, 4))
        turn_result = TurnResult(
            turn=Turn(Action.SHOT, Point(5, 5)),
            ship=alive_ship,
            result=CellState.HIT
        )

        # act
        provider.notify_result(turn_result)

        # assert
        assert len(provider._hunt_queue) == 2
        assert Point(6, 5) in provider._hunt_queue
        assert Point(5, 6) in provider._hunt_queue

    def test_notify_result_clears_hunt_queue_when_ship_destroyed(self, provider, destroyed_ship):
        # arrange
        provider._hunt_queue.append(Point(1, 1))
        provider._hunt_queue.append(Point(2, 2))
        turn_result = TurnResult(
            turn=Turn(Action.SHOT, Point(5, 5)),
            ship=destroyed_ship,
            result=CellState.HIT
        )

        # act
        provider.notify_result(turn_result)

        # assert
        assert len(provider._hunt_queue) == 0

    def test_notify_result_adds_surroundings_to_shots_fired_when_ship_destroyed(self, provider, destroyed_ship):
        # arrange
        turn_result = TurnResult(
            turn=Turn(Action.SHOT, Point(5, 5)),
            ship=destroyed_ship,
            result=CellState.HIT
        )

        # act
        provider.notify_result(turn_result)

        # assert
        expected_surroundings = {
            Point(4, 4), Point(4, 5), Point(4, 6),
            Point(5, 4), Point(5, 6),
            Point(6, 4), Point(6, 5), Point(6, 6)
        }
        for point in expected_surroundings:
            assert point in provider._shots_fired

    def test_notify_result_handles_corner_point_when_ship_alive(self, provider, alive_ship):
        # arrange
        turn_result = TurnResult(
            turn=Turn(Action.SHOT, Point(0, 0)),
            ship=alive_ship,
            result=CellState.HIT
        )

        # act
        provider.notify_result(turn_result)

        # assert
        assert len(provider._hunt_queue) == 2
        assert Point(1, 0) in provider._hunt_queue
        assert Point(0, 1) in provider._hunt_queue

    def test_notify_result_handles_edge_point_when_ship_destroyed(self, provider, destroyed_ship):
        # arrange
        turn_result = TurnResult(
            turn=Turn(Action.SHOT, Point(0, 5)),
            ship=destroyed_ship,
            result=CellState.HIT
        )

        # act
        provider.notify_result(turn_result)

        # assert
        expected_surroundings = {
            Point(0, 4), Point(0, 6),
            Point(1, 4), Point(1, 5), Point(1, 6)
        }
        for point in expected_surroundings:
            assert point in provider._shots_fired


class TestHunterInputProviderIntegration:
    def test_hunt_mode_targets_ship_neighbors_after_hit(self, provider, alive_ship):
        # arrange
        hit_point = Point(5, 5)
        provider._shots_fired.add(hit_point)
        turn_result = TurnResult(
            turn=Turn(Action.SHOT, hit_point),
            ship=alive_ship,
            result=CellState.HIT
        )

        # act
        provider.notify_result(turn_result)
        next_turn = provider.get_input()

        # assert
        neighbors = {Point(4, 5), Point(6, 5), Point(5, 4), Point(5, 6)}
        assert next_turn.point in neighbors

    def test_returns_to_random_mode_after_ship_destroyed(self, provider, destroyed_ship):
        # arrange
        provider._hunt_queue.append(Point(3, 3))
        turn_result = TurnResult(
            turn=Turn(Action.SHOT, Point(5, 5)),
            ship=destroyed_ship,
            result=CellState.HIT
        )

        # act
        provider.notify_result(turn_result)

        # assert
        assert len(provider._hunt_queue) == 0

    def test_multiple_hits_accumulate_in_hunt_queue(self, provider):
        # arrange
        ship = Destroyer()
        ship.hit_points = 3
        
        # act
        first_hit = TurnResult(
            turn=Turn(Action.SHOT, Point(5, 5)),
            ship=ship,
            result=CellState.HIT
        )
        provider.notify_result(first_hit)
        first_queue_size = len(provider._hunt_queue)
        
        provider._shots_fired.add(Point(5, 6))
        second_hit = TurnResult(
            turn=Turn(Action.SHOT, Point(5, 6)),
            ship=ship,
            result=CellState.HIT
        )
        provider.notify_result(second_hit)
        second_queue_size = len(provider._hunt_queue)

        # assert
        assert first_queue_size == 4
        assert second_queue_size > 0
