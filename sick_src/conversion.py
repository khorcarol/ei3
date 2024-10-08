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


def bytes_to_int16(byte_list):

    if len(byte_list) != 2:
        raise ValueError("Input must be a list of exactly two bytes.")

    # Extract the two bytes
    byte1, byte2 = byte_list

    # Combine the bytes using bitwise operations
    result = (byte1 << 8) | byte2
    return result


def bytes_to_int16_be(byte_list):
    # Ensure the input is a list of exactly two bytes
    if len(byte_list) != 2:
        raise ValueError("Input must be a list of exactly two bytes.")

    # Extract the two bytes
    byte1, byte2 = byte_list

    # Combine the bytes using bitwise operations
    result = (byte1 << 8) | byte2

    # Check if the result is negative (if the 16th bit is set)
    if result & 0x8000:
        # Convert to a negative value by subtracting 2^16
        result -= 0x10000

    return result
