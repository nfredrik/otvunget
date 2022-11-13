from dataclasses import dataclass
import pytest
from sleep_controller import SleepController

@pytest.fixture()
def config():
    @dataclass
    class Config:
        backoff_start: int = 5
        backoff_multiple:int =  2
        backoff_stop: int = 100

    return  Config()

def test_sleep_controller(config):
    sleep_controller = SleepController(config)
    assert sleep_controller.current_backoff() < 10


def test_sleep_reset(config):
    sleep_controller = SleepController(config)
    sleep_controller.current_backoff()
    sleep_controller.current_backoff()
    sleep_controller.current_backoff()
    assert sleep_controller.current_backoff() > 10
    sleep_controller.reset()
    assert sleep_controller.current_backoff() == 5

def test_sleep_controller_reached_max(config):
    sleep_controller = SleepController(config)
    sleep_controller.current_backoff()
    for _ in range(100):
        sleep_controller.current_backoff()

    assert sleep_controller.current_backoff() == 100

