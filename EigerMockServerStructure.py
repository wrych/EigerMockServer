class ChildValidationException(Exception):
    pass


class EigerComponent:
    def __init__(self, name):
        self._name = name
        self._children = list()

    def get_name(self):
        """
        Return the name of the component.
        """
        return self._name

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


class EigerModule(EigerComponent):
    def __init__(self, *args, **kw_args):
        super(EigerModule, self).__init__(*args, **kw_args)


class EigerTask(EigerComponent):
    def __init__(self, *args, **kw_args):
        super(EigerTask, self).__init__(*args, **kw_args)


class EigerCommand:
    def __call__(self):
        pass