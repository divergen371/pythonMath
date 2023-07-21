n, k = [int(x) for x in input().split()]
counter = 0
while k >= n:
    n *= 2
    counter += 1


print(counter)
