from time import sleep


class ChildValidationException(Exception):
    pass


class AccessNotPermittedException(Exception):
    pass


class EigerComponent:
    """
    Base Class for inhertitating common methods over all components.
    """

    def __init__(self, name):
        self._name = name
        self._children = list()

    def get_name(self):
        """
        Return the name of the component.
        """
        return self._name

    def get_children(self):
        """
        Return a list of the children names.
        """
        return [child.get_name() for child in self._children]

    def _validate_child_duplicate(self, new_child):
        """
        Validate that the newly added `new_child` is not a duplicate or raise `ChildValidationException`.
        """
        for child in self._children:
            if child.get_name() == new_child.get_name():
                raise ChildValidationException(
                    f"A child with the name `{new_child.get_name()}` already exists."
                )

    def _validate_child(self, new_child):
        """
        This method is meant to be overwritten by implementations of EigerComponent.
        The method should validate if the `new_child` is a valid child for the compontent.
        """
        pass

    def _validate_no_attr_with_name(self, name):
        """
        Check if an attribute with `name` exists and raise a `ChildValidationException` if so.
        """
        try:
            getattr(self, name)
            raise ChildValidationException(
                f"An attribute `{name}` of `{self.get_name()}` already exists."
            )
        except AttributeError:
            pass

    def _add_child_attribute(self, new_child):
        """
        Add the attribute `new_child.get_name()` to this component in order to call it in a pythonic way.
        """
        self._validate_no_attr_with_name(new_child.get_name())
        setattr(self, new_child.get_name(), new_child)

    def add_child(self, new_child):
        """
        Add a child `new_child` to the component.
        """
        self._validate_child_duplicate(new_child)
        self._validate_child(new_child)
        self._children.append(new_child)
        self._add_child_attribute(new_child)


class EigerValue(EigerComponent):
    """
    Class representing lowest level values. Provides basic methods and access control.
    """

    def __init__(self, name=None, access_mode=None, value=None, setter=None):
        super(EigerValue, self).__init__(name)
        self._access_mode = access_mode
        self._value = value
        self._setter = setter

    def _check_read_access(self):
        self._check_access("r")

    def _check_write_access(self):
        self._check_access("w")

    def _check_access(self, access_mode):
        if self._access_mode.find(access_mode) == -1:
            raise AccessNotPermittedException(f"Read access not allowed.")

    def _get(self):
        if callable(self._value):
            value = self._value()
        else:
            value = self._value
        return value

    def get(self):
        """
        Return the value if read access is provided.
        """
        self._check_read_access()
        return self._get()

    def put(self, value):
        """
        Set the value if write access is provided.
        """
        self._check_write_access()
        if self._setter:
            return self._setter(value)
        else:
            self._value = value
            return None


class EigerValueContainer(EigerComponent):
    """
    Container for values. This is generally the level you might be addressing.
    """

    def __init__(
        self,
        *,
        name=None,
        access_mode=None,
        value=None,
        unit=None,
        allowed_values=None,
        value_type=None,
        setter=None,
    ):
        super(EigerValueContainer, self).__init__(name)
        self.add_child(
            EigerValue(
                name="value", access_mode=access_mode, value=value, setter=setter
            )
        )
        self.add_child(
            EigerValue(name="access_mode", access_mode="r", value=access_mode)
        )
        if unit is not None:
            self.add_child(EigerValue(name="unit", access_mode="r", value=unit))
        if allowed_values is not None:
            self.add_child(
                EigerValue(name="allowed_values", access_mode="r", value=allowed_values)
            )
        if value_type is not None:
            self.add_child(
                EigerValue(name="value_type", access_mode="r", value=value_type)
            )

    def get(self):
        """
        Return the stucture beneath this value. Generally this will be a dict
        containing `value`, `access_mode` and may contain further key-value
        pairs (e.g. `unit`, `allowed_value`, `value_type`).
        """
        return {child.get_name(): child.get() for child in self._children}

    def put(self, value):
        """
        Sets the (sub-)values to the given values as provided in a `dict`.
        """
        changes = []
        for key in value:
            change = getattr(self, key).put(value[key])
            try:
                changes.extend(change)
            except TypeError:
                pass
        return changes if len(changes) > 0 else [self.get_name()]


class EigerModule(EigerComponent):
    """
    Highest level component.
    """

    def __init__(self, *args, **kw_args):
        super(EigerModule, self).__init__(*args, **kw_args)


class EigerTask(EigerComponent):
    """
    Middle level component.
    """

    def __init__(self, *args, **kw_args):
        super(EigerTask, self).__init__(*args, **kw_args)
        self.add_child(EigerValue("keys", access_mode="r", value=self.get_children))


class EigerCommand(EigerComponent):
    """
    Component for commands. Allows to add custom callbacks at the start, call and
    end of execution.
    """

    def __init__(self, name=None, exec=None):
        super(EigerCommand, self).__init__(name=name)
        self._callback_call_func = None
        self._callback_start_func = None
        self._callback_end_func = None
        self.set_callback_call(exec)

    def _eval_callable_or_none(self, exec):
        if exec is None:
            return None
        elif not callable(exec):
            raise TypeError("Argument must be callable or None.")
        else:
            return exec

    def set_callback_call(self, exec):
        """
        Set a function that should be called during execution.
        Generally, a delay function is provided here.
        """
        self._callback_call_func = self._eval_callable_or_none(exec)

    def set_callback_start(self, exec):
        """
        Set a function that should be called before execution.
        Generally, a status change function is provided here.
        """
        self._callback_start_func = self._eval_callable_or_none(exec)

    def set_callback_end(self, exec):
        """
        Set a function that should be called after execution.
        Generally, a status change function is provided here.
        """
        self._callback_end_func = self._eval_callable_or_none(exec)

    def _callback_start(self):
        if self._callback_start_func is not None:
            return self._callback_start_func()

    def _callback_call(self):
        if self._callback_call_func is not None:
            return self._callback_call_func()

    def _callback_end(self):
        if self._callback_end_func is not None:
            return self._callback_end_func()

    def __call__(self):
        self._callback_start()
        self._callback_call()
        self._callback_end()
