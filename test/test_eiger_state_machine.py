import pytest

from EigerMock.EigerStateMachine import EigerStateMachine


@pytest.fixture
def state_machine():
    return EigerStateMachine()


def test_check_default_state(state_machine):
    assert state_machine.get_state() == "na"


def test_change_state(state_machine):
    state_machine._change_state("initialize")
    assert state_machine.get_state() == "initialize"


def test_set_threshold_energy(state_machine):
    value = 5000
    photon_energy = state_machine.get_photon_energy()
    state_machine.set_threshold_energy(value)
    assert state_machine.get_threshold_energy() == value
    assert state_machine.get_photon_energy() == photon_energy


def test_set_photon_energy(state_machine):
    value = 11200
    state_machine.set_photon_energy(value)
    assert state_machine.get_photon_energy() == value
    assert state_machine.get_threshold_energy() == value / 2