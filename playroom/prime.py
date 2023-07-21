a = int(input())
is_prime = True

for i in range(2, a):
    if a == 1:
        is_prime = False
    if a % i == 0:
        is_prime = False
        break
if is_prime:
    print("YES")
else:
    print("NO")
