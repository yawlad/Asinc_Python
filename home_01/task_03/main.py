
strings_1 = ["attribute", "класс", "функция", "type"]
print("-"*50, end="\n")

for s in strings_1:
    try:
        s.encode('ASCII') # Данное выражение равносильно b'{s}'
    except Exception as exception:
        print(exception, " : ", s)
        