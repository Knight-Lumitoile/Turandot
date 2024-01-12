def perform_byte_xor(byte_array1, byte_array2):
    """Performs bitwise XOR on two byte arrays."""
    return bytes([byte1 ^ byte2 for byte1, byte2 in zip(byte_array1, byte_array2)])


def encrypt_file_xor(input_filename, output_filename, password):
    """Encrypts a file using XOR with a password."""
    with open(input_filename, 'rb') as input_file, open(output_filename, 'wb') as output_file:
        byte = input_file.read(1)
        counter = 0

        while byte:
            encrypted_byte = perform_byte_xor(byte, str.encode(password[counter]))
            output_file.write(encrypted_byte)

            counter += 1
            if counter == len(password):
                counter = 0

            byte = input_file.read(1)
