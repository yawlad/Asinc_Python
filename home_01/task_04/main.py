
strings_1 = ["разработка", "администрирование", "protocol", "standard"]
print("-"*50, end="\n")

for i in range(len(strings_1)):
    temp = (strings_1[i], strings_1[i].encode())
    strings_1[i] = temp
    print(temp[0], " : ", temp[1])

print("-"*50, end="\n")

for temp in strings_1:
    print(temp[1], " : ", temp[1].decode())