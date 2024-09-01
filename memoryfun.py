import msvcrt
from colorama import Fore, Back, Style
import random, time

from colorama import init
init()

characters = ";ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.!,? "

output = ""

def out(c):
    global output
    print("\t->%s" % (c))
    output += c

def getcharnum(chr):
    for i, c in enumerate(characters):
        if c == chr:
            return i
    return 0
        
def getnumchar(num):
    return characters[num]

def colorbydist(dist):
    if dist == 0:
        return Fore.WHITE
    if dist < 2:
        return Fore.RED
    if dist < 4:
        return Fore.YELLOW
    if dist < 8:
        return Fore.GREEN
    if dist < 16:
        return Fore.CYAN
    return Fore.BLUE


alloc = 63
calloc = 7
mem = []
cmem = []
for x in range(0,alloc):
    mem.append(0)
for x in range(0,calloc):
    cmem.append(0)
ptr = 0
res = -1
retln = 0
pushed = 0
counter = 0
heap_sel = ''
heap_ptr = 0
heap_mem = {}

labels = {}
consts = {}

code = """CONST text Skyyf je negr!
LENCONST text
PUSHR 0
SET 0
LABEL loop
CMPVAL *0
RAISE
GETCONST text !0
PRINTCH
LOWER
INC
EXEQ
JMP loop"""

code3 = """CONST a Hello, world!
PTR 15
LENCONST a
PTR 0
SET 0
RAISE
LABEL loop
GETCONST a !0
PUSHPTR
PTR 0
CMPVAL !15
JE cont
INC
POPPTR
RAISE
JMP loop
LABEL cont
PTR 0
SET 0
RAISE
LABEL print
CMPVAL 0
EXEQ
PRINTCH
SET 0
RAISE
JMP print
"""


code2 = """LABEL loop
GETCH
CMPVAL 53
RAISE
JNE loop
LOWER
SET 0
PUSHPTR
CALL printcall
POPPTR
EXIT
LABEL printcall
PTR 0
LABEL print
CMPVAL 0
JE printend
PRINTCH
SET 0
RAISE
JMP print
LABEL printend
RET"""



code1 = """SETCHARS h e l l o ,
RAISE
SETSPACE
RAISE
SETCHARS w o r l d !

PTR 0
LABEL loop
CMPVAL 0
EXEQ
PRINTCH
SET 0
RAISE
JMP loop"""
lines = code.splitlines()
line = 0

for i, mmm in enumerate(lines):
    f = mmm.split(" ")
    if f[0] == "LABEL":
        labels[f[1]] = i

print(labels)

print("ALLOCATED %d Bytes (4B/int)" % ((alloc+1)*4))
while True:
    memstr = ""
    cmemstr = ""
    counter += 1
    thisline = lines[line].split(" ")
    opcode = thisline[0]
    for i, arg in enumerate(thisline):
        if arg.startswith("!"):
            thisline[i] = mem[int(arg[1:])]
        if arg.startswith("*"):
            thisline[i] = cmem[int(arg[1:])]
    for x in range(0,alloc):
        #memstr += random.choice([Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE])
        memstr += colorbydist(abs(x-ptr))
        memstr += str(mem[x]) + " "
        memstr += Style.RESET_ALL
    for x in range(0,calloc):
        if cmem[x] != 0:
            cmemstr += [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE][x % 4]
        else:
            cmemstr+= Style.RESET_ALL
        cmemstr+= str(cmem[x]) + " "
    print("\tREG: %s" % (cmemstr))
    print("\tSTACK: %s" % (memstr))
    print("\tLINE: %d PTR: %d INTs: %d OUT: %s" % (line, ptr, counter, output))
    print("%s" % (lines[line]))
    if opcode == "":
        line += 1
        continue

    match opcode:
        case "PRINT":
            out(mem[ptr])
        case "PRINTCH":
            out(getnumchar(mem[ptr]))
        case "LABEL":
            labels[thisline[1]] = line
        case "JMP":
            line = labels[thisline[1]]
            continue
        case "JE":
            if res == 0:
                line = labels[thisline[1]]
                continue
        case "JNE":
            if res != 0:
                line = labels[thisline[1]]
                continue
        case "CMPVAL":
            res = mem[ptr] - int(thisline[1])
        case "EXEQ":
            if res == 0:
                break
        case "SETCHARS":
            for c in thisline[1:]:
                mem[ptr] = getcharnum(c)
                ptr += 1
            ptr -= 1
        case "SETSPACE":
            mem[ptr] = getcharnum(" ")
        case "RAISE":
            ptr += 1
        case "LOWER":
            ptr -= 1
        case "PTR":
            ptr = int(thisline[1])
        case "SET":
            mem[ptr] = int(thisline[1])
        case "GETCH":
            mem[ptr] = getcharnum(msvcrt.getch().decode())
        case "EXIT":
            break
        case "CALL":
            retln = line
            line = labels[thisline[1]]
        case "RET":
            line = retln
        case "PUSHPTR":
            pushed = ptr
        case "POPPTR":
            ptr = pushed
        case "HEAP_ALLOC":
            if thisline[1] not in heap_mem:
                buffer = []
                for x in range(0,int(thisline[2]) - 1):
                    buffer.append(0)
                heap_mem[thisline[1]] = buffer
        case "HEAP_FREE":
            heap_mem.pop(thisline[1])
        case "HEAP_FOCUS":
            if thisline[1] in heap_mem:
                heap_sel = thisline[1]
        case "HEAP_PTR":
            heap_ptr = int(thisline[1])
        case "HEAP_SET":
            heap_mem[heap_sel][heap_ptr] = int(thisline[1])
        case "HEAP_RAISE":
            heap_ptr += 1
        case "HEAP_LOWER":
            heap_ptr -= 1
        case "CONST":
            consts[thisline[1]] = " ".join(thisline[2:])
        case "GETCONST":
            mem[ptr] = getcharnum(consts[thisline[1]][int(thisline[2])])
        case "LENCONST":
            mem[ptr] = len(consts[thisline[1]]) - 1
        case "SUB":
            mem[ptr] -= int(thisline[1])
        case "ADD":
            mem[ptr] += int(thisline[1])
        case "INC":
            mem[ptr] += 1
        case "DEC":
            mem[ptr] -= 1
        case "PUSHR":
            cmem[int(thisline[1])] = mem[ptr]
        case "POPR":
            mem[ptr] = cmem[int(thisline[1])]
    line += 1
    #msvcrt.getch()
    time.sleep(0.05)
    
print("PROGRAM END")
print(f"Resulting output: '{output}'")