
strings_1 = ["разработка", "сокет", "декоратор"]
strings_2 = ["\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430", "\u0441\u043e\u043a\u0435\u0442", "\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440"]
print("-"*50, end="\n")

for s in strings_1:
    print(type(s), " : ", s)

print("-"*50, end="\n")

for s in strings_2:
    print(type(s), " : ", s)