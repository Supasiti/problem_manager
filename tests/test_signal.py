# tests for signal

import unittest
from services.signal import Signal

class TestSignal(unittest.TestCase):

    def setUp(self):
        self.signal      = Signal()
        self.signal_bool = Signal(bool)

        self.receiver  = Reciever(self.signal, self.signal_bool)

    def test_emit(self):
        self.signal.emit()
        self.signal_bool.emit(True)

        self.assertEqual(self.receiver.result_from_function, True)
        self.assertEqual(self.receiver.result_from_function_with_arg, True)

    def test_emit_fails(self):
        with self.assertRaises(AssertionError):
            self.signal.emit(True)

        with self.assertRaises(AssertionError):
            self.signal_bool.emit(1)

class Reciever():

    def __init__(self, signal, signal_bool):
        signal.connect(self.function)
        signal_bool.connect(self.function_with_arg)

        self.result_from_function = False
        self.result_from_function_with_arg = False

    def function(self):
        self.result_from_function = True

    def function_with_arg(self, arg:bool):
        self.result_from_function_with_arg = arg

    