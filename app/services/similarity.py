from __future__ import annotations


def simhash_to_int(simhash: str) -> int:
    simhash = simhash.strip().lower()
    return int(simhash, 16)


def hamming_distance(simhash_a: str, simhash_b: str) -> int:
    int_a = simhash_to_int(simhash_a)
    int_b = simhash_to_int(simhash_b)
    return (int_a ^ int_b).bit_count()

