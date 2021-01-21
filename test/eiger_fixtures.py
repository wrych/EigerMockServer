import pytest


@pytest.fixture
def eiger(mocker):
    from EigerMock.EigerMock import init_detector

    mocker.patch("EigerMock.EigerStateMachine.EigerStateMachine._delay")
    return init_detector()