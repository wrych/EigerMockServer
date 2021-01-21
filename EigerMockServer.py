class ChildValidationException(Exception)

class EigerComponent:
    def __init__(self, name):
        self._name = name
        self._children = list()

    def _validate_child(self, child):
        pass

    def add_child(self, child):
        self._validate_child(child)
        self._children.append(child)


class EigerModule(EigerComponent):
    def __init__(self, *args, **kw_args):
        super(self, EigerModule).__init__(*args, **kw_args)


class EigerTask(EigerComponent):
    def __init__(self, *args, **kw_args):
        super(self, EigerTask).__init__(*args, **kw_args)


class EigerMockServer(EigerComponent):
    def __init__(self):
        pass

class Einer


if __name__ == "__main__":
    detector_command = EigerTask("command")
    detector = EigerModule("detector")
    detector.add_child(detector_command)
    EigerMockServer()
