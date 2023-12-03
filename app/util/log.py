import datetime;

def log(message):
    ct = datetime.datetime.now()
    s = ct.strftime('%Y-%m-%d %H:%M:%S') 
    
    with open('log.txt', 'a') as file:
        file.write(f'{s} {message}\n')