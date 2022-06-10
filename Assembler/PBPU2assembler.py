import os
import re
import sys

filePath = "helloWorld.asm"
f_name, f_ext = os.path.splitext(filePath);

try:
    t = open(filePath,"r")
    #t = open(sys.argv[1], "r")
    text = t.read()
    text = text.upper()
    text = re.sub(';.*?\n', '\n', text)
    text = text.replace(","," ")
    text = text.split()
    t.close()
except:
    print("No file given")
    exit()

final=[]

for i,e in enumerate(text):
    # Instructions
    if (e=="NOP"):
        final.append(0)
    if (e=="LDAN"):
        final.append(1)
        num = int(text[i+1],16)
        final.append(num)
    if (e=="LDAM"):
        final.append(2)
        temp = int(text[i+1],16)
        num = (int(temp) & 0b111100000000) >> 8
        final.append(num)
        num = (int(temp) & 0b000011110000) >> 4
        final.append(num)
        num = (int(temp) & 0b000000001111)
        final.append(num)
    if (e=="STA"):
        final.append(3)
        temp = int(text[i+1],16)
        num = (int(temp) & 0b111100000000) >> 8
        final.append(num)
        num = (int(temp) & 0b000011110000) >> 4
        final.append(num)
        num = (int(temp) & 0b000000001111)
        final.append(num)
    if (e=="SWAP"):
        final.append(4)
    if (e=="SHFT"):
        final.append(5)
    if (e=="ADD"):
        final.append(6)
    if (e=="SUB"):
        final.append(7)
    if (e=="AND"):
        final.append(8)
    if (e=="OR"):
        final.append(9)
    if (e=="XOR"):
        final.append(10)
    if (e=="IN"):
        final.append(11)
    if (e=="OUT"):
        final.append(12)
    if (e=="JP"):
        final.append(13)
        temp = int(text[i+1],16)
        num = (int(temp) & 0b111100000000) >> 8
        final.append(num)
        num = (int(temp) & 0b000011110000) >> 4
        final.append(num)
        num = (int(temp) & 0b000000001111)
        final.append(num)
    if (e=="JPC"):
        final.append(14)
        temp = text[i+1]
        num = (int(temp) & 0b111100000000) >> 8
        final.append(num)
        num = (int(temp) & 0b000011110000) >> 4
        final.append(num)
        num = (int(temp) & 0b000000001111)
        final.append(num)
    if (e=="JPZ"):
        final.append(15)
        temp = text[i+1]
        num = (int(temp) & 0b111100000000) >> 8
        final.append(num)
        num = (int(temp) & 0b000011110000) >> 4
        final.append(num)
        num = (int(temp) & 0b000000001111)
        final.append(num)
    if (e=="STR"): # String insertion
        for element in text[i+1]:
            final.append(ord(element) & 0b00001111)
            final.append((ord(element) & 0b11110000) >> 4)


output = open(f_name + ".pbpu2" ,'wb')

print(final)

for i in final:
    i = i.to_bytes(1, 'little')
    output.write(i)
output.close()

