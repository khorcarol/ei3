import struct


def bytes_to_float32(byte_list):
    # Ensure the byte list is exactly 4 integers
    if len(byte_list) != 4:
        raise ValueError("Input must be a list of exactly 4 integers")

    # Pack the integers into a bytes object
    byte_data = bytes(byte_list)

    # Unpack the bytes as a 32-bit float
    # '>f' for big-endian, '<f' for little-endian
    float_value = struct.unpack('>f', byte_data)[0]

    return float_value
