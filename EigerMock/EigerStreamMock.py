from EigerMockStructure import (
    EigerComponent,
    EigerCommand,
    EigerModule,
    EigerTask,
    EigerValueContainer,
)


def add_eiger_stream():
    module = EigerModule("stream")
    module.add_child(
        EigerValueContainer(name="version", access_mode="r", value="1.6.0")
    )
    module.add_child(add_command())
    module.add_child(add_config())
    module.add_child(add_status())
    return module


def add_command():
    command = EigerTask("command")
    initialize = EigerCommand("initialize")
    command.add_child(initialize)
    return command


def add_status():
    command = EigerTask("status")
    state = EigerValueContainer(name="state", access_mode="rw", value="na")
    command.add_child(state)
    return command


def add_config():
    config = EigerTask("config")
    initialize = EigerValueContainer(name="buffer_size", access_mode="rw", value=100)
    config.add_child(initialize)
    return config