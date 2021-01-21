from EigerMockStructure import EigerComponent
from EigerMock.EigerDetectorMock import add_eiger_detector
from EigerMock.EigerFileWriterMock import add_eiger_filewriter
from EigerMock.EigerMonitorMock import add_eiger_monitor
from EigerMock.EigerStreamMock import add_eiger_stream
from EigerMock.EigerStateMachine import EigerStateMachine


class EigerMockServer(EigerComponent):
    def __init__(self):
        super(EigerMockServer, self).__init__("EigerMockServer")


def init_detector():
    state_machine = EigerStateMachine()
    eiger_mock_server = EigerMockServer()
    eiger_mock_server.add_child(add_eiger_detector(state_machine))
    eiger_mock_server.add_child(add_eiger_filewriter())
    eiger_mock_server.add_child(add_eiger_monitor())
    eiger_mock_server.add_child(add_eiger_stream())
    return eiger_mock_server


if __name__ == "__main__":
    init_detector()
