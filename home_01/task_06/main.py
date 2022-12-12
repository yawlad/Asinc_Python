import locale

print("-"*50,end="\n\n") 
print("Default coding: ", locale.getpreferredencoding(), end="\n\n")
print("-"*50,end="\n\n") 


with open("home_01/task_06/test_file.txt", encoding="utf-8") as file:
    for line in file:
        print(line)