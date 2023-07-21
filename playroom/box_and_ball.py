from queue import LifoQueue

n = 6
a = [3, 2, 5, 5, 4, 3]


box = LifoQueue()
for i in range(1, n):
    if a[i - 1] != a[i]:
        box.put(a[i-1])
    elif a[i - 1] == a[i]:
        add = a[i - 1] + a[i]
        box.put(add)

for i in range(box.qsize()):
    print(box.get())
