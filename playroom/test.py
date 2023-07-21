num = int(input())
num_list = input().split()
sorted_list = sorted(num_list)
for i in range(num):
    for j in range(int(num_list[i])):
        if (j + 1) == int(num_list[i]):
            print(sorted_list[j])
        else:
            print(sorted_list[j], end=" ")
