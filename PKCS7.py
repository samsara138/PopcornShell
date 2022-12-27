# pkcs7 padding scheme

# Add padding to a byte string
def pad(data: bytes, length: int, echo=True) -> bytes:
    # Input should be in bytes format
    if type(data) is not bytes:
        if echo:
            print("Warning: parsing data to bytes")
        data = bytes(str(data), 'utf-8')

    # Data length shouldn't be longer than the final length
    if len(data) > length:
        if echo:
            print("Warning: data too long")
        return bytes()

    padding_len = length - len(data)
    paddings = bytes()
    # If the padding length is longer than 255 (cannot be held in one byte)
    # Add 255 * 0xff to the end
    while padding_len > 255:
        paddings += bytes.fromhex("ff") * 255
        padding_len -= 255

    # Create bytes format of the padding length
    padding_unit = '{:02x}'.format(padding_len)
    padding_unit = bytes.fromhex(padding_unit)
    # Put padding in front of the 0xff, if they exist
    paddings_buffer = padding_unit * padding_len
    paddings = paddings_buffer + paddings

    # Add paddings to data
    result = data + paddings
    return result


# Check if a byte string is padded
def is_padded(data: bytes, echo=True) -> (bool, int):
    # Input should be in bytes format
    if type(data) is not bytes:
        if echo:
            print("Warning: parsing data to bytes")
        data = bytes(str(data), 'utf-8')

    if len(data) == 0:
        if echo:
            print("Warning: empty data")
        return False, -1

    padding_length = 0
    padding_end_index = len(data) - 1
    padding_end = data[padding_end_index]
    if padding_end <= 0:
        return False, -1
    while True:
        padding_start_index = padding_end_index - padding_end
        padding_length += padding_end_index - padding_start_index

        for i in range(padding_end_index, padding_start_index, -1):
            if i < 0 or data[i] != padding_end:
                return False, -1
        if padding_end != 255:
            break
        padding_end_index = padding_start_index
        padding_end = data[padding_end_index]

    return True, padding_length


# Remove the padding of a data
def remove_padding(data: bytes, echo=True) -> bytes:
    # Input should be in bytes format
    if type(data) is not bytes:
        if echo:
            print("Warning: parsing data to bytes")
        data = bytes(str(data), 'utf-8')

    if len(data) == 0:
        if echo:
            print("Warning: empty data")
        return bytes()

    padding_info = is_padded(data)
    if not padding_info[0]:
        if echo:
            print("Warning: data is not padded")
        return bytes()

    return data[:len(data) - padding_info[1]]


# Test if this script is functioning correctly
def test(data, length):
    try:
        data_padded = pad(data, length, False)
    except:
        print("FAIL: Padding function crashed")
        return False

    try:
        padding_infoA = is_padded(data_padded, False)
        padding_infoB = is_padded(data, False)

        padding_length = length - len(data)
        assert padding_infoA[0] == (padding_length != 0), "FAIL: Is Padded function - padding exist (1)"
        if padding_length != 0:
            assert padding_infoA[1] == padding_length, "FAIL: Is Padded function - padding length"
        assert not padding_infoB[0], "FAIL: Is Padded function - padding exist (2)"
    except AssertionError:
        print("FAIL: Is Padded function failed")
        return False
    except:
        print("FAIL: Is Padded function crashed")
        return False

    try:
        data_removedA = remove_padding(data_padded, False)
        data_removedB = remove_padding(data, False)
        if padding_length != 0:
            assert data_removedA == data, "FAIL: Remove padding function - removed data doesn't match"
        assert len(data_removedB) == 0, "FAIL: Remove padding function - removing padding in non-padded data"
        return True
    except AssertionError:
        print("FAIL: Remove padding function failed")
        return False
    except:
        print("FAIL: Remove padding function crashed")


def main():
    tests = [(b"", 10), (b"", 1024),(b"1234", 10), (b"1234", 300), (b"1234", 300), (b"123456", 6), (b"123456789", 2048), ]
    for test_case in tests:
        print(f"Testing test case {test_case} ...... ", end="")
        result = "Passed" if test(test_case[0], test_case[1]) else "Failed"
        print(result)


if __name__ == '__main__':
    main()
