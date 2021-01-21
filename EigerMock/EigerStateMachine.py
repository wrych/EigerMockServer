from time import sleep


class InvalidStateException(Exception):
    pass


class EigerStateMachine:
    ALLOWED_STATES = ("na", "initialize", "ready", "acquire", "idle", "configure")
    ELEMENTS = {"Cu": 8048.0, "Mo": 17450.0}

    def __init__(self):
        self._state = "na"
        self._init()

    def _init(self):
        self.set_element("Cu")

    def get_state(self):
        """
        Return the `state` of the detector.
        """
        return self._state

    def get_element(self):
        """
        Return the currently set `element` of the detector.
        If a custom `photon_energy` is set, this will return an empty string.
        """
        return self._element

    def get_threshold_energy(self):
        """
        Return the currently set `threshold_energy` of the detector.
        """
        return self._threshold_energy

    def get_photon_energy(self):
        """
        Return the currently set `photon_energy` of the detector.
        """
        return self._photon_energy

    def set_element(self, value):
        """
        Sets the the `photon_energy` to the k-alpha energy of given `element`.
        This will also set the `threshold_energy` to half of the `photon_energy`.
        Please note that this Mock does not implement any sanity checks for the `threshold_energy`.
        """
        changes = self.set_photon_energy(self.ELEMENTS[value])
        self._element = value
        return changes

    def set_threshold_energy(self, value):
        """
        Sets the `threshold_value` to the given `value`.
        Please note that this Mock does not implement any sanity checks for the `threshold_energy`.
        """
        value = float(value)
        self._threshold_energy = value
        return ["threshold_energy"]

    def set_photon_energy(self, value):
        """
        Sets the the `photon_energy` to the given `value`.
        This will also set the `threshold_energy` to half of the `photon_energy`.
        Please note that this Mock does not implement any sanity checks for the
        `photon_energy` or `threshold_energy`.
        """
        value = float(value)
        self._photon_energy = value
        self._threshold_energy = value / 2
        self._element = ""
        return ["threshold_energy", "photon_energy", "element"]

    def _validate_state(self, new_state):
        if not new_state in self.ALLOWED_STATES:
            raise InvalidStateException(
                f"State `{new_state}` is not in allowed states."
            )

    def _change_state(self, new_state):
        self._validate_state(new_state)
        self._state = new_state

    def idle(self):
        """
        Sets the detector's state to `idle`.
        """
        self._change_state("idle")

    def configure(self):
        """
        Sets the detector's state to `configure`.
        """
        self._change_state("configure")

    def ready(self):
        """
        Sets the detector's state to `ready`.
        """
        self._change_state("ready")

    def initialize(self):
        """
        Sets the detector's state to `initialize`.
        """
        self._change_state("initialize")

    def acquire(self):
        """
        Sets the detector's state to `acquire`.
        """
        self._change_state("acquire")

    def init(self):
        """
        Reset (some) values to default.
        """
        self._init()
        self._delay(2.5)

    def delay(self):
        """
        Delays command execution by a small time to make things feel more realistic.
        """
        self._delay(0.2)

    def _delay(self, delay):
        sleep(delay)
