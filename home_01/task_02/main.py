
strings_1 = [b"class", b"function", b"method"]
print("-"*50, end="\n")

for s in strings_1:
    print(type(s), " : ", s, " : ", s.__len__())