
from Crypto.Util.strxor import strxor
from Crypto.Random import get_random_bytes


with open("ciphertext1.enc", 'rb') as f:
    c1 = f.read()

with open("ciphertext2.enc", 'rb') as f:
    c2 = f.read()

cx = strxor(c1,c2)

temp1 = b"cs409{"
temp2 = strxor(temp1,cx[0:6])

otherstring = temp2
flag = temp1
numberleft = len(cx) - len(flag)

while(numberleft > 0):
    print(f"current guess of other string is {otherstring}")
    print(f"current guess of flag is {flag}")
    print(f"nunber of characters left to guess is {numberleft}")
    #guessing phase
    while(True):
        trial = input("what substring to append and try: ")
        trial_bytes = trial.encode('utf-8')
        if(len(flag) + len(trial_bytes) > len(cx)):
            print("TOO LONG!!!!!! CHOOSE A DIFFERENT ONE")
            continue
        ch = int(input("which to add it to 1.) otherstring 2.) flag : "))
        if(ch==1):
            othertemp = otherstring + trial_bytes
            flagtemp = strxor(othertemp,cx[0:len(othertemp)])
        else:
            flagtemp = flag + trial_bytes
            othertemp = strxor(flagtemp,cx[0:len(flagtemp)])
        response = input(f"this is flag obtained \"{flagtemp}\" this is otherstring \"{othertemp}\" should we confirm this? (Y/N): ")
        if(response == "Y"):
            otherstring = othertemp
            flag = flagtemp
            numberleft = len(cx) - len(flag)
            break
