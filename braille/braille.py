import serial
import time

from braille_map import BRAILLE_MAP


PORT = "COM5"       # Change this to your ESP32 COM port
BAUD_RATE = 115200


def letter_to_bits(letter):

    letter = letter.upper()

    if letter not in BRAILLE_MAP:
        raise ValueError("Enter a letter from A-Z")

    active_dots = BRAILLE_MAP[letter]

    bits = []

    for dot in range(1, 7):
        bits.append(1 if dot in active_dots else 0)

    return bits


def send_letter(esp32, letter):

    bits = letter_to_bits(letter)

    pattern = ''.join(str(bit) for bit in bits)

    print("Letter:", letter.upper())
    print("Pattern:", pattern)

    esp32.write(pattern.encode())


esp32 = serial.Serial(PORT, BAUD_RATE)

time.sleep(2)

while True:

    letter = input("\nEnter letter (Q to quit): ").strip()

    if letter.upper() == "Q":
        break

    if len(letter) != 1 or not letter.isalpha():
        print("Please enter a single letter.")
        continue

    send_letter(esp32, letter)

esp32.close()