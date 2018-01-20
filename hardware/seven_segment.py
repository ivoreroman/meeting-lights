from gpiozero import LEDBoard, OutputDeviceError, LEDCollection

class SevenSegmentDisplay(LEDBoard):
    """
    Extends :class:`LEDBoard` for a 7 segment LED display

    7 segment displays have either 7 or 8 pins, 7 pins for the digit display
    and an optional 8th pin for a decimal point. 7 segment displays
    typically have either a common anode or common cathode pin, when
    using a common anode display 'active_high' should be set to False.
    Instances of this class can be used to display characters or control
    individual leds on the display. For example::

        from gpiozero import SevenSegmentDisplay

        seven = SevenSegmentDisplay(1,2,3,4,5,6,7,8,active_high=False)
        seven.display("7")

    :param int \*pins:
        Specify the GPIO pins that the 7 segment display is attached to.
        Pins should be in the LED segment order A,B,C,D,E,F,G,decimal_point
        (the decimal_point is optional).

    :param bool pwm:
        If ``True``, construct :class:`PWMLED` instances for each pin. If
        ``False`` (the default), construct regular :class:`LED` instances. This
        parameter can only be specified as a keyword parameter.

    :param bool active_high:
        If ``True`` (the default), the :meth:`on` method will set all the
        associated pins to HIGH. If ``False``, the :meth:`on` method will set
        all pins to LOW (the :meth:`off` method always does the opposite). This
        parameter can only be specified as a keyword parameter.

    :param bool initial_value:
        If ``False`` (the default), all LEDs will be off initially. If
        ``None``, each device will be left in whatever state the pin is found
        in when configured for output (warning: this can be on). If ``True``,
        the device will be switched on initially. This parameter can only be
        specified as a keyword parameter.

    """
    def __init__(self, *pins, **kwargs):
        # 7 segment displays must have 7 or 8 pins
        if len(pins) < 7 or len(pins) > 8:
            raise ValueError('SevenSegmentDisplay must have 7 or 8 pins')
        # Don't allow 7 segments to contain collections
        for pin in pins:
            assert not isinstance(pin, LEDCollection)
        pwm = kwargs.pop('pwm', False)
        active_high = kwargs.pop('active_high', True)
        initial_value = kwargs.pop('initial_value', False)
        if kwargs:
            raise TypeError('unexpected keyword argument: %s' % kwargs.popitem()[0])

        self._layouts = {
            '1': (False, True, True, False, False, False, False),
            '2': (True, True, False, True, True, False, True),
            '3': (True, True, True, True, False, False, True),
            '4': (False, True, True, False, False, True, True),
            '5': (True, False, True, True, False, True, True),
            '6': (True, False, True, True, True, True, True),
            '7': (True, True, True, False, False, False, False),
            '8': (True, True, True, True, True, True, True),
            '9': (True, True, True, True, False, True, True),
            '0': (True, True, True, True, True, True, False),
            'A': (True, True, True, False, True, True, True),
            'B': (False, False, True, True, True, True, True),
            'C': (True, False, False, True, True, True, False),
            'D': (False, True, True, True, True, False, True),
            'E': (True, False, False, True, True, True, True),
            'F': (True, False, False, False, True, True, True),
            'G': (True, False, True, True, True, True, False),
            'H': (False, True, True, False, True, True, True),
            'I': (False, False, False, False, True, True, False),
            'J': (False, True, True, True, True, False, False),
            'K': (True, False, True, False, True, True, True),
            'L': (False, False, False, True, True, True, False),
            'M': (True, False, True, False, True, False, False),
            'N': (True, True, True, False, True, True, False),
            'O': (True, True, True, True, True, True, False),
            'P': (True, True, False, False, True, True, True),
            'Q': (True, True, False, True, False, True, True),
            'R': (True, True, False, False, True, True, False),
            'S': (True, False, True, True, False, True, True),
            'T': (False, False, False, True, True, True, True),
            'U': (False, False, True, True, True, False, False),
            'V': (False, True, True, True, True, True, False),
            'W': (False, True, False, True, False, True, False),
            'X': (False, True, True, False, True, True, True),
            'Y': (False, True, True, True, False, True, True),
            'Z': (True, True, False, True, True, False, True),
            '-': (False, False, False, False, False, False, True),
            ' ': (False, False, False, False, False, False, False),
            '=': (False, False, False, True, False, False, True)
        }

        super(SevenSegmentDisplay, self).__init__(*pins, pwm=pwm, active_high=active_high, initial_value=initial_value)

    def display(self, char):
        """
        Display a character on the 7 segment display

        :param string char:
            A single character to be displayed
        """
        char = str(char).upper()
        if len(char) > 1:
            raise ValueError('only a single character can be displayed')
        if char not in self._layouts:
            raise ValueError('there is no layout for character - %s' % char)
        layout = self._layouts[char]
        for led in range(7):
            self[led].value = layout[led]

    def display_hex(self, hexnumber):
        """
        Display a hex number (0-F) on the 7 segment display

        :param int hexnumber:
            The number to be displayed in hex
        """
        self.display(hex(hexnumber)[2:])

    @property
    def decimal_point(self):
        """
        Represents the status of the decimal point led
        """
        # does the 7seg display have a decimal point (i.e pin 8)
        if len(self) > 7:
            return self[7].value
        else:
            raise OutputDeviceError('there is no 8th pin for the decimal point')

    @decimal_point.setter
    def decimal_point(self, value):
        """
        Sets the status of the decimal point led
        """
        if len(self) > 7:
            self[7].value = value
        else:
            raise OutputDeviceError('there is no 8th pin for the decimal point')

    def set_char_layout(self, char, layout):
        """
        Create or update a custom character layout, which can be used with the
        `display` method.

        :param string char:
            A single character to be displayed

        :param tuple layout:
            A 7 bool tuple of LED values in the segment order A, B, C, D, E, F, G
        """
        char = str(char).upper()
        if len(char) != 1:
            raise ValueError('only a single character can be used in a layout')
        if len(layout) != 7:
            raise ValueError('a character layout must have 7 segments')
        self._layouts[char] = layout
