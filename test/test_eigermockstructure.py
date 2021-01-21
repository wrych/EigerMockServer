import pytest
import pytest_mock

from EigerMockStructure import (
    EigerComponent,
    EigerCommand,
    EigerTask,
    ChildValidationException,
    EigerValueContainer,
    AccessNotPermittedException,
)


def test_eiger_component_add_child():
    a = EigerComponent("aaa")
    child_name = "bbb"
    b = EigerComponent(child_name)
    a.add_child(b)
    assert getattr(a, child_name).get_name() == child_name


def test_add_duplicate_child():
    a = EigerComponent("aaa")
    b = EigerComponent("bbb")
    with pytest.raises(ChildValidationException):
        a.add_child(b)
        a.add_child(b)


def test_get_value():
    value = "test_123"
    a = EigerValueContainer(name="test", access_mode="rw", value=value)
    assert a.value.get() == value


def test_value_unit():
    unit = "s"
    a = EigerValueContainer(name="test", access_mode="w", value="test_123", unit=unit)
    assert a.unit.get() == "s"


def test_get_raises_no_access():
    a = EigerValueContainer(name="test", access_mode="w", value="test_123")
    with pytest.raises(AccessNotPermittedException):
        a.value.get()


@pytest.mark.parametrize("mode", ["r", "rw", "w"])
def test_value_has_access_mode(mode):
    a = EigerValueContainer(name="test", access_mode=mode, value="test_123")
    assert a.access_mode.get() == mode


def test_value_function():
    value = "abc"

    def func():
        return value

    a = EigerValueContainer(name="test", access_mode="r", value=func)
    assert a.value.get() == value


def test_task_keys():
    parameters = ["aaa", "bbb", "ccc"]
    a = EigerTask("test_abc")
    for parameter in parameters:
        a.add_child(EigerValueContainer(name=parameter, access_mode="rw"))
    assert not set(a.keys.get()) ^ set(parameters + ["keys"])


def test_allowed_values():
    allowed_values = ["aaa", "bbb", "ccc"]
    a = EigerValueContainer(
        name="test", access_mode="rw", value="test_123", allowed_values=allowed_values
    )
    assert a.allowed_values.get() == allowed_values


def test_set_value():
    new_value = "test_xxx"
    a = EigerValueContainer(name="test", access_mode="rw", value="test_123")
    a.put({"value": new_value})
    assert a.value.get() == new_value


def test_value_type():
    value_type = "bool"
    a = EigerValueContainer(
        name="test", access_mode="rw", value=True, value_type=value_type
    )
    assert a.value_type.get() == value_type


def test_setter_called_with_value(mocker):
    m = mocker.Mock()
    value = 22
    a = EigerValueContainer(name="test", access_mode="rw", value=True, setter=m)
    a.put({"value": value})
    m.assert_called_once_with(value)


def test_callback(mocker):
    a = EigerCommand(name="test")
    x = mocker.Mock()
    a.set_callback_start(x)
    y = mocker.Mock()
    a.set_callback_call(y)
    z = mocker.Mock()
    a.set_callback_end(z)
    a()
    x.assert_called()
    y.assert_called()
    z.assert_called()