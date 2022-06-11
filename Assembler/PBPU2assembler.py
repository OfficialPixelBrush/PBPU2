import os
import re
import sys

filePath = sys.argv[1]#"helloWorld.asm"
f_name, f_ext = os.path.splitext(filePath);

def checkIntHex(str):
    try:
        int(str,16)
        return True
    except ValueError:
        return False
    
def checkInt(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

try:
    t = open(filePath,"r")
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
labelName=[]
labelPos =[]
pos = 0 # for getting length of code

print("First Pass...")
# First pass to figure out where each Label will go
for i,e in enumerate(text):
    if e[0] == ':':
        labelName.append(re.sub(':', '', text[i]))
        labelPos.append(pos)
        text.remove(e)
    if (e=="NOP"):
        pos += 1
    if (e=="LDAN"):
        pos += 2
    if (e=="LDAM"):
        pos += 4
    if (e=="STA"):
        pos += 4
    if (e=="SWAP"):
        pos += 1
    if (e=="SHFT"):
        pos += 1
    if (e=="ADD"):
        pos += 1
    if (e=="SUB"):
        pos += 1
    if (e=="AND"):
        pos += 1
    if (e=="OR"):
        pos += 1
    if (e=="XOR"):
        pos += 1
    if (e=="IN"):
        pos += 1
    if (e=="OUT"):
        pos += 1
    if (e=="JP"):
        pos += 4
    if (e=="JPC"):
        pos += 4
    if (e=="JPZ"):
        pos += 4
    if (e=="STR"): # String insertion
        pos += len(text[i+1])*2

print("Second Pass...")
# Second Pass for actual compilation
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
        if checkIntHex(text[i+1]): # if it's a number, write number
            temp = int(text[i+1],16)
        else: # if it's not a number, it must be a label
            # tokenize operators
            token = re.split('(\W)', text[i+1])
            # turn labels into addresses
            for index,label in enumerate(token):
                if (not checkInt(label)) or (not checkIntHex(label)):
                    if (label != ( '+' or '-' or '*' or '/') ):
                        token[index] = str(labelName.index(label))
            temp = (eval(''.join(token)))
        num = (int(temp) & 0b111100000000) >> 8
        final.append(num)
        num = (int(temp) & 0b000011110000) >> 4
        final.append(num)
        num = (int(temp) & 0b000000001111)
        final.append(num)
            
    if (e=="STA"):
        final.append(3)
        if checkIntHex(text[i+1]): # if it's a number, write number
            temp = int(text[i+1],16)
        else: # if it's not a number, it must be a label
            # tokenize operators
            token = re.split('(\W)', text[i+1])
            # turn labels into addresses
            for index,label in enumerate(token):
                if (not checkInt(label)) or (not checkIntHex(label)):
                    if (label != ( '+' or '-' or '*' or '/') ):
                        token[index] = str(labelName.index(label))
            temp = (eval(''.join(token)))
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
        if checkIntHex(text[i+1]): # if it's a number, write number
            temp = int(text[i+1],16)
        else: # if it's not a number, it must be a label
            # tokenize operators
            token = re.split('(\W)', text[i+1])
            # turn labels into addresses
            for index,label in enumerate(token):
                if (not checkInt(label)) or (not checkIntHex(label)):
                    if (label != ( '+' or '-' or '*' or '/') ):
                        token[index] = str(labelName.index(label))
            temp = (eval(''.join(token)))
        num = (int(temp) & 0b111100000000) >> 8
        final.append(num)
        num = (int(temp) & 0b000011110000) >> 4
        final.append(num)
        num = (int(temp) & 0b000000001111)
        final.append(num)
    if (e=="JPC"):
        final.append(14)
        if checkIntHex(text[i+1]): # if it's a number, write number
            temp = int(text[i+1],16)
        else: # if it's not a number, it must be a label
            # tokenize operators
            token = re.split('(\W)', text[i+1])
            # turn labels into addresses
            for index,label in enumerate(token):
                if (not checkInt(label)) or (not checkIntHex(label)):
                    if (label != ( '+' or '-' or '*' or '/') ):
                        token[index] = str(labelName.index(label))
            temp = (eval(''.join(token)))
        num = (int(temp) & 0b111100000000) >> 8
        final.append(num)
        num = (int(temp) & 0b000011110000) >> 4
        final.append(num)
        num = (int(temp) & 0b000000001111)
        final.append(num)
    if (e=="JPZ"):
        final.append(15)
        if checkIntHex(text[i+1]): # if it's a number, write number
            temp = int(text[i+1],16)
        else: # if it's not a number, it must be a label
            # tokenize operators
            token = re.split('(\W)', text[i+1])
            # turn labels into addresses
            for index,label in enumerate(token):
                if (not checkInt(label)) or (not checkIntHex(label)):
                    if (label != ( '+' or '-' or '*' or '/') ):
                        token[index] = str(labelName.index(label))
            temp = (eval(''.join(token)))
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

for i in final:
    i = i.to_bytes(1, 'little')
    output.write(i)
output.close()
print("Finished.")
