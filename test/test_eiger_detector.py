import pytest

from eiger_fixtures import eiger


def test_eiger_detector_version(eiger):
    assert eiger.detector.version.value.get() == "1.6.0"
    assert eiger.detector.version.get()["value"] == "1.6.0"
    assert eiger.detector.version.get()["access_mode"] == "r"


def test_eiger_state_changes_after_initialize(eiger):
    assert eiger.detector.status.state.value.get() == "na"
    eiger.detector.command.initialize()
    print(eiger.detector.status.state.value.get())
    assert eiger.detector.status.state.value.get() == "idle"


def test_set_threshold_energy(eiger):
    value = 6000
    eiger.detector.config.threshold_energy.put({"value": value})
    assert eiger.detector.config.threshold_energy.value.get() == value
    eiger.detector.config.threshold_energy.value.put(value + 1)
    assert eiger.detector.config.threshold_energy.value.get() == value + 1


def test_set_photon_energy(eiger):
    value = 6000
    eiger.detector.config.photon_energy.put({"value": value})
    assert eiger.detector.config.photon_energy.value.get() == value
    assert eiger.detector.config.threshold_energy.value.get() == value / 2
    assert eiger.detector.config.element.value.get() == ""
    eiger.detector.config.photon_energy.value.put(value + 2)
    assert eiger.detector.config.photon_energy.value.get() == value + 2
    assert eiger.detector.config.threshold_energy.value.get() == (value + 2) / 2


def test_set_element(eiger):
    element = "Mo"
    assert eiger.detector.config.element.value.put(element) == [
        "threshold_energy",
        "photon_energy",
        "element",
    ]
    assert eiger.detector.config.photon_energy.value.get() == 17450.0
    assert eiger.detector.config.threshold_energy.value.get() == 17450.0 / 2
    assert eiger.detector.config.element.value.get() == element
