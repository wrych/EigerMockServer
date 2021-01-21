import pytest

import EigerMockServer


def test_initialize():
    server = EigerMockServer.EigerMockServer()
    cmd = server.detector.command.initialize()