def test(a: int) -> bool:
    if a == 0:
        return True
    else:
        return False


def test2(a: int) -> bool:
    return a == 0


print(test(0))
print(test2(0))
