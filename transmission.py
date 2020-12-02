from binascii import hexlify, unhexlify


def text_to_bits(text, encoding='ascii', errors='surrogatepass'):
    bits = bin(int(hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def transmission_mask(bits):
    transmission = []
    # start transmission mask
    for i in range(16):
        transmission.append(1)

    # transmission with double poll rate
    for bit in bits:
        transmission.append(int(bit))
        transmission.append(int(bit))

    # transmission end mask
    for i in range(16):
        transmission.append(0)
    return transmission


def print_bits(bits):
    print()
    i = 0
    internal_counter = 0
    while i < len(bits):
        print(bits[i], end="")
        i += 1
        internal_counter += 1
        if internal_counter == 8:
            print(end=" ")
        if internal_counter == 16:
            print()
            internal_counter = 0
    print()


def convert_ascii_to_transmission_bits(text):
    bit_array = text_to_bits(text)
    bit_array = transmission_mask(bit_array)

    return bit_array
