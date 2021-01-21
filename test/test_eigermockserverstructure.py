import pytest
from EigerMockServerStructure import EigerComponent, ChildValidationException


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
