import pytest

import EigerMockServer


def test_initialize():
    server = EigerMockServer.init_detector()
    cmd = server.detector.command.initialize()