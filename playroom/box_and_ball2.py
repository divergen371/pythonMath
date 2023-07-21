n = 6
a = [3, 2, 5, 5, 4, 3]

box = []
for i in range(1,n):
    if a[i-1] != a[i]:
        box.append(a[i-1])
    elif a[i-1] == a[i]:
        add = a[i-1] + a[i]
        del a[i]
        a.append(0)
        box.append(add)

for i in range(len(box)):
    print(box.pop())
