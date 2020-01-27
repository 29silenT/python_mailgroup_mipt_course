def hamming_distance(s1, s2) -> int:
    """Return the Hamming distance between equal-length sequences."""
    if len(s1) != len(s2):
        raise ValueError('Unequal lengths of input objects')
    return sum((x != y) for x, y in zip(s1, s2))


if __name__ == "__main__":
    print(f'Hamming distance {hamming_distance("yppah", "happy")}')
