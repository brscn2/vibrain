from app.services.similarity import hamming_distance, simhash_to_int


def test_simhash_to_int_hex_conversion():
    assert simhash_to_int("ff") == 255
    assert simhash_to_int("0F") == 15


def test_hamming_distance():
    assert hamming_distance("ff00", "ff00") == 0
    assert hamming_distance("ff00", "00ff") == bin(0xFF00 ^ 0x00FF).count("1")

