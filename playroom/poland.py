n = 7

stack = []


def add():
    y, x = stack.pop(), stack.pop()
    stack.append(x + y)


def sub():
    y, x = stack.pop(), stack.pop()
    stack.append(x - y)


for i in ["1", "2", "+", "3", "4", "+", "-"]:
    if i == "+":
        add()
    elif i == "-":
        sub()
    else:
        stack.append(int(i))

print(stack.pop())
