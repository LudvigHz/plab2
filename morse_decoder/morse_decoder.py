import serial

from constants import LEGAL_SIGNALS, MORSE_CODES, SYMBOL_BREAK, WORD_BREAK


class Morse_decoder:
    """
    Morse code decoder. Reads data from serial port and decodes into text.
    Serial input needs to be separeted by newline, one signal per line
    """

    def __init__(self, port="/dev/ttyUSB0", baudrate=9600, time=1):
        self.serial_port = port
        self.current_symbol = ""
        self.current_word = ""
        self.serial = serial.Serial(port, baudrate, timeout=time)

    def start_decoding(self):
        print("starting decoder!")
        while True:
            self.read_one_signal()

    def read_one_signal(self):
        # Read a line from the serial port
        try:
            signal = self.serial.readline().decode("utf-8").strip()
            self.process_signal(signal)
        except Exception as e:
            return

    def process_signal(self, signal):
        # Processes the signal read from serial
        if signal not in LEGAL_SIGNALS:
            # If the signal is not defined, return
            return
        if signal == SYMBOL_BREAK:
            # Run symbol end handler
            self.handle_symbol_end()
        elif signal == WORD_BREAK:
            self.handle_word_end()
        else:
            # Update the current symbol if the signal is 0 or 1
            self.update_current_symbol(signal)

    def update_current_symbol(self, signal):
        self.current_symbol += signal

    def handle_symbol_end(self):
        # Decode the symbol from the string of 0 and 1,
        # if the symbol is not a defined morse code, except the symbol as an
        # unknown code (?)
        try:
            decoded_symbol = MORSE_CODES[self.current_symbol]
        except:
            decoded_symbol = "?"
        # Reset the current symbol code
        self.current_symbol = ""

        # And update the current word with the decoded symbol
        self.update_current_word(decoded_symbol)
        print(decoded_symbol, end="", flush=True)

    def update_current_word(self, symbol):
        self.current_word += symbol

    def handle_word_end(self):
        # handle word end: print the end and reset the current word
        self.handle_symbol_end()
        print("", end=" ", flush=True)
        self.current_word = ""
