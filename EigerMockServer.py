from EigerMockServerStructure import (
    EigerComponent,
    EigerCommand,
    EigerModule,
    EigerTask,
)


class EigerMockServer(EigerComponent):
    def __init__(self):
        super(EigerMockServer, self).__init__("EigerMockServer")


class EigerDetector(EigerModule):
    def __init__(self):
        super(EigerDetector, self).__init__("detector")


class EigerDetectorCommand(EigerTask):
    def __init__(self):
        super(EigerDetectorCommand, self).__init__("command")


class EigerDetectorCommandInitialize(EigerComponent, EigerCommand):
    def __init__(self):
        super(EigerDetectorCommandInitialize, self).__init__("initialize")


def init_detector():
    eiger_mock_server = EigerMockServer()

    eiger_detector = EigerDetector()
    eiger_mock_server.add_child(eiger_detector)

    eiger_detector_command = EigerDetectorCommand()
    eiger_detector.add_child(eiger_detector_command)

    eiger_detector_command_initialize = EigerDetectorCommandInitialize()
    eiger_detector_command.add_child(eiger_detector_command_initialize)

    return eiger_mock_server


if __name__ == "__main__":
    init_detector()
