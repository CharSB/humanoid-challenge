import pytest
from pathlib import Path

from src.environment.grid import Grid
from src.environment.world import World
from src.environment.objects import ShortRock, TallRock, Key, Door

TEST_CONFIG = Path("configs/test_world.yaml")


@pytest.fixture
def basic_grid() -> Grid:
    return Grid(5, 5)


@pytest.fixture
def world() -> World:
    return World.from_yaml(TEST_CONFIG)


@pytest.fixture
def short_rock() -> ShortRock:
    return ShortRock()


@pytest.fixture
def tall_rock() -> TallRock:
    return TallRock()


@pytest.fixture
def red_key() -> Key:
    return Key("red")


@pytest.fixture
def blue_key() -> Key:
    return Key("blue")


@pytest.fixture
def red_door() -> Door:
    return Door("red")