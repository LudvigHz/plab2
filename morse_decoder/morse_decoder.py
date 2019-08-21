import serial

from constants import LEGAL_SIGNALS, MORSE_CODES, SYMBOL_BREAK, WORD_BREAK


class Morse_decoder:
    """
    Morse code decoder. Reads data from serial port and decodes into text.
    Serial input needs to be separeted by newline, one signal per line
    """

    def __init__(self, port="/dev/ttyUSB0", baudrate=9600, timeout=0.1):
        self.serial_port = port
        self.current_symbol = ""
        self.current_word = ""
        self.serial = serial.Serial(port, baudrate, timeout)

    def start_decoding(self):
        while True:
            self.read_one_signal()

    def read_one_signal(self):
        try:
            signal = self.serial.readline()
            print("Read:            " + signal)
            self.process_signal(signal)
        except Exception as e:
            return

    def process_signal(self, signal):
        if signal not in LEGAL_SIGNALS:
            return
        if signal == SYMBOL_BREAK:
            self.handle_symbol_end()
        elif signal == WORD_BREAK:
            self.handle_word_end()
        else:
            self.update_current_symbol(signal)
        print("current sym   " + self.current_symbol)
        print("current word   " + self.current_word)

    def update_current_symbol(self, signal):
        self.current_symbol += signal

    def handle_symbol_end(self):
        try:
            decoded_symbol = MORSE_CODES[self.current_symbol]
        except:
            decoded_symbol = "?"
        self.current_symbol = ""

        self.update_current_word(decoded_symbol)

    def update_current_word(self, symbol):
        self.current_word += symbol

    def handle_word_end(self):
        self.handle_symbol_end()
        print(self.current_word, end=" ")
        self.current_word = ""
