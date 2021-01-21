from EigerMockStructure import (
    EigerComponent,
    EigerCommand,
    EigerModule,
    EigerTask,
    EigerValueContainer,
    EigerValue,
)


def add_eiger_detector(state_machine):
    module = EigerModule("detector")
    module.add_child(
        EigerValueContainer(name="version", access_mode="r", value="1.6.0")
    )
    module.add_child(add_command(state_machine))
    module.add_child(add_config(state_machine))
    module.add_child(add_status(state_machine))
    return module


def add_command(state_machine):
    command = EigerTask("command")
    command.add_child(add_initialize_command(state_machine))
    command.add_child(add_arm_command(state_machine))
    command.add_child(add_trigger_command(state_machine))
    command.add_child(add_disarm_command(state_machine))
    return command


def add_initialize_command(state_machine):
    initialize = EigerCommand("initialize")
    initialize.set_callback_start(state_machine.initialize)
    initialize.set_callback_call(state_machine.init)
    initialize.set_callback_end(state_machine.idle)
    return initialize


def add_arm_command(state_machine):
    arm = EigerCommand("arm")
    arm.set_callback_start(state_machine.configure)
    arm.set_callback_call(state_machine.delay)
    arm.set_callback_end(state_machine.ready)
    return arm


def add_trigger_command(state_machine):
    trigger = EigerCommand("trigger")
    trigger.set_callback_start(state_machine.acquire)
    trigger.set_callback_call(state_machine.delay)
    trigger.set_callback_end(state_machine.ready)
    return trigger


def add_disarm_command(state_machine):
    disarm = EigerCommand("disarm")
    disarm.set_callback_start(state_machine.configure)
    disarm.set_callback_call(state_machine.delay)
    disarm.set_callback_end(state_machine.idle)
    return disarm


def add_status(state_machine):
    status = EigerTask("status")
    state = EigerValueContainer(
        name="state", access_mode="rw", value=state_machine.get_state
    )
    state.add_child(
        EigerValue(name="critical_values", access_mode="r", value=["na", "error"])
    )
    status.add_child(state)
    return status


def add_config(state_machine):
    config = EigerTask("config")
    config.add_child(
        EigerValueContainer(
            name="countrate_correction_applied",
            access_mode="rw",
            value=True,
            value_type="bool",
        )
    )
    config.add_child(
        EigerValueContainer(
            name="flatfield_correction_applied",
            access_mode="rw",
            value=True,
            value_type="bool",
        )
    )
    config.add_child(
        EigerValueContainer(
            name="pixel_mask_applied",
            access_mode="rw",
            value=True,
            value_type="bool",
        )
    )
    config.add_child(
        EigerValueContainer(
            name="detector_number",
            access_mode="r",
            value="E-02-0100",
            value_type="string",
        )
    )
    config.add_child(
        EigerValueContainer(
            name="count_time", access_mode="rw", value=1.0, unit="s", value_type="float"
        )
    )
    config.add_child(
        EigerValueContainer(
            name="frame_time", access_mode="rw", value=1.0, unit="s", value_type="float"
        )
    )
    config.add_child(
        EigerValueContainer(name="nimages", access_mode="rw", value=1, value_type="int")
    )
    config.add_child(
        EigerValueContainer(
            name="ntrigger", access_mode="rw", value=1, value_type="int"
        )
    )
    config.add_child(
        EigerValueContainer(
            name="trigger_mode",
            access_mode="rw",
            value="ints",
            allowed_values=["ints", "exts"],
            value_type="string",
        )
    )
    config.add_child(
        EigerValueContainer(
            name="auto_summation",
            access_mode="rw",
            value=False,
            value_type="bool",
        )
    )
    config.add_child(
        EigerValueContainer(
            name="element",
            access_mode="rw",
            value=state_machine.get_element,
            allowed_values=[el for el in state_machine.ELEMENTS],
            value_type="string",
            setter=state_machine.set_element,
        )
    )
    config.add_child(
        EigerValueContainer(
            name="photon_energy",
            access_mode="rw",
            value=state_machine.get_photon_energy,
            unit="eV",
            value_type="float",
            setter=state_machine.set_photon_energy,
        )
    )
    config.add_child(
        EigerValueContainer(
            name="threshold_energy",
            access_mode="rw",
            value=state_machine.get_threshold_energy,
            unit="eV",
            value_type="float",
            setter=state_machine.set_threshold_energy,
        )
    )
    config.add_child(
        EigerValueContainer(
            name="sensor_material", access_mode="rw", value="Si", value_type="string"
        )
    )
    config.add_child(
        EigerValueContainer(
            name="sensor_thickness",
            access_mode="r",
            value="0.000320",
            unit="m",
            value_type="float",
        )
    )
    return config