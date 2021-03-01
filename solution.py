#!/usr/bin/python3

import math
import sys

folder = ""
if len(sys.argv) > 1:
	folder = str(sys.argv[1])+"/"
SUB = [0, 1, 1, 0, 1, 0, 1, 0]
N_B = 32
N = 8 * N_B

pt = bytearray(open(folder+"bis.txt", "rb").read())
ct1 = bytearray(open(folder+"bis.txt.enc", "rb").read())
ct2 = bytearray(open(folder+"hint.gif.enc", "rb").read())
ct3 = bytearray(open(folder+"super_cipher.py.enc", "rb").read())

def bits2a(b):

    return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(b)] * 8))

# Next keystream
def step(x):
  x = (x & 1) << N+1 | x << 1 | x >> N-1
  y = 0
  for i in range(N):
    y |= SUB[(x >> i) & 7] << i
  return y

def getText(bytes):
    str = ""
    for x in bytes:
        str += chr(x)
    return str

def main():
    nPT = int.from_bytes(pt, 'little')
    nCT1 = int.from_bytes(ct1[:len(pt)], 'little')
    keystream = nPT ^ nCT1
    k = bytearray(keystream.to_bytes(len(pt), 'little'))

    nCT3 = int.from_bytes(ct3[:len(ct3)], 'little')
    b = bytearray((keystream ^ nCT3).to_bytes(len(ct3), 'little'))
    #print(getText(b))
    return k[:N_B]


def getKeystream(key, times):
    print(key)

def breakHINT():
    key = main()
    lCI2 = len(ct2)
    times = lCI2//N_B
    nKEY = int.from_bytes(key, 'little')
    xor = nKEY ^ int.from_bytes(ct2[:N_B], 'little')
    f = xor.to_bytes(N_B, 'little')
    for i in range(times):
        nKEY = step(nKEY)
        xor = nKEY ^ int.from_bytes(ct2[(i+1)*N_B:(i+2)*N_B], 'little')
        f += xor.to_bytes(N_B, 'little')

    return f

#f = breakHINT()
#open("output.gif", "wb").write(f)

zeroes = ["000", "011", "101", "111"]
ones = ["001", "010", "100", "110"]

def reverseF(stri):
  #print(str)
  for i in range(4-1, -1, -1):
    revert = ""
    if stri[0] == "1":
      revert = ones[i]
    else:
      revert = zeroes[i]
    for j in range(1, N):
      #print(str)
      if stri[j] == "1":
        for x in range(4):
          #print(revert[-2:], ones[x][:2])
          if revert[-2:] == ones[x][:2]:
            revert += ones[x][2]
            break
      else:
        for x in range(4):
          if revert[-2:] == zeroes[x][:2]:
            revert += zeroes[x][2]
            break
    #print("need: " + str(int(stri, 2)) + " " + stri)
    num = int(revert, 2) >>1
    ref = int(math.pow(2, N))
    if num & ref != ref:
      num = num & (ref-2)
    res = '{:08b}'.format(num).zfill(N)
    res = res[-N:]
    num = int(res, 2)
    if step(num) == int(stri, 2):
      return res


stri = '{:08b}'.format(int.from_bytes(main(), 'little')).zfill(N)

for i in range(N//2):
  stri = reverseF(stri)
  #print(stri)
print(bits2a(stri[24:])[::-1])
