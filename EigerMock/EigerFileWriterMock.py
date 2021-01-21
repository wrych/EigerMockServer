from EigerMockStructure import (
    EigerComponent,
    EigerCommand,
    EigerModule,
    EigerTask,
    EigerValueContainer,
)


def add_eiger_filewriter():
    module = EigerModule("filewriter")
    module.add_child(
        EigerValueContainer(name="version", access_mode="r", value="1.6.0")
    )
    module.add_child(
        EigerValueContainer(
            name="files", access_mode="r", value=["test_1_master.h5", "test_1_00001.h5"]
        )
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
    command.add_child(EigerValueContainer(name="state", access_mode="rw", value="na"))
    command.add_child(EigerValueContainer(name="error", access_mode="rw", value="na"))
    command.add_child(EigerValueContainer(name="time", access_mode="rw", value="na"))
    command.add_child(
        EigerValueContainer(name="buffer_free", access_mode="rw", value="na")
    )
    return command


def add_config():
    config = EigerTask("config")
    config.add_child(
        EigerValueContainer(name="name_pattern", access_mode="rw", value="series_$id")
    )
    config.add_child(
        EigerValueContainer(name="compression_enabled", access_mode="rw", value=True)
    )
    config.add_child(
        EigerValueContainer(name="nimages_per_file", access_mode="rw", value=1000)
    )
    config.add_child(
        EigerValueContainer(
            name="mode",
            access_mode="rw",
            value="enabled",
            allowed_values=["enabled", "disabled"],
        )
    )
    return config