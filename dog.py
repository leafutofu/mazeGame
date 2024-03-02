x = 1250
ap = 1920*0.3
bp = 1920*0.675

for i in range(100):
    value = 2*i+x
    llength = (1920-value)//2
    al = ap-llength
    bl = bp-llength
    f1 = al / value
    f2 = bl / value
    print(value, f1, f2)

