import datetime;

def log(message):
    ct = datetime.datetime.now()
    s = ct.strftime('%m/%d/%Y %H:%M') 
    
    with open('log.txt', 'a') as file:
        file.write(f'[{s}] {message}\n')
