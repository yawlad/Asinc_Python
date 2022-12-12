import subprocess

for adress in ['yandex.ru', 'youtube.com']:   
    print("-"*25,f"{adress}", "-"*25, end="\n") 
    data = ['ping', adress]
    ping = subprocess.Popen(args=data, stdout=subprocess.PIPE)
    for s in ping.stdout:
        print (s.decode('cp866'))


