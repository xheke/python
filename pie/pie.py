from numpy import *

def getpi():
    s = 1000000
    sr = 0
    for j in range(s):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        z = x * x + y * y
        if( abs(x) == 1.0 or abs(y) == 1.0):
            print("-----------     ", x, y)
        if( z <= 1 ):
            sr = sr + 1
            #print(x, y, "ok")
        else:
            pass
            #print(x, y)

    px = 4.0 * sr / s
    print("OK:", px)

for x in range(20):
    getpi()
