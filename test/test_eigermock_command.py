import pytest

from eiger_fixtures import eiger


def test_initialize(eiger):
    cmd = eiger.detector.command.initialize()