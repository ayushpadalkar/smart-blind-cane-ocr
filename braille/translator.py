from braille_map import BRAILLE_MAP


def letter_to_dots(letter):
    letter = letter.upper()

    if letter not in BRAILLE_MAP:
        raise ValueError(f"Unsupported character: {letter}")

    return BRAILLE_MAP[letter]


def dots_to_bits(dots):
    bits = []

    for dot in range(1, 7):
        if dot in dots:
            bits.append(1)
        else:
            bits.append(0)

    return bits


def letter_to_bits(letter):
    dots = letter_to_dots(letter)
    return dots_to_bits(dots)