import datetime

now = datetime.datetime.now()
timestamp = now.strftime("%d-%m-%y %H:%M:%S")
print(type(now))
print(type(timestamp))
