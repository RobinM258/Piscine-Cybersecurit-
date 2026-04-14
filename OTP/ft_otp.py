import sys
from binascii import unhexlify
import hmac
import hashlib
import struct
import time



def isHexa(str):
    for i in range(len(str)):
        if (str[i] >= '0' and str[i] <= '9' 
            or str[i] >= 'a' and str[i] <= 'f' 
            or str[i] >= 'A' and str[i] <= 'F'):
            return True
        else:
            return False
            
def Generate():
    global now
    count = int(now / 30)
    try:
        with open("ft_otp.key", "rb") as binary_file:
            raw = binary_file.read()
        bytes = struct.pack(">Q", count)
        h = hmac.new(raw, bytes, hashlib.sha1).digest()
        offset = h[19] & 0x0F
        raw_octet = h[offset : offset + 4]
        raw_code = struct.unpack(">I", raw_octet)[0]
        raw_code = raw_code & 0x7fffffff
        code = raw_code % 1000000
        print(code)
    except:
        print("Error")

def main():
    for i in range(len(sys.argv)):
        if (sys.argv[i] == "-g" and len(sys.argv) > i + 1):
            try:
                with open(sys.argv[i + 1], 'r', encoding='utf-8') as fichier:
                    contenu = fichier.read()
                if (len(contenu) == 64 and isHexa(contenu) == True):
                    raw = bytes.fromhex(contenu)
                    with open("ft_otp.key", "wb") as binary_file:
                        binary_file.write(raw)
                        print("Key was successfully saved in ft_otp.key.")
                else:
                    print("./ft_otp: error: key must be 64 hexadecimal characters.")
            except:
                print("Error")
        elif (sys.argv[i] == "-k" and len(sys.argv) > i + 1):
            Generate()
        elif (i == 0):
            continue

    
if len(sys.argv) < 2:
    print("Please use: ./spider [-gk] URL")
    sys.exit(1)
global now
now = time.time()
main()
