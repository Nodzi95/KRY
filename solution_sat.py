#!/usr/bin/python3

from z3 import *
import sys

folder = ""
if len(sys.argv) > 1:
	folder = str(sys.argv[1])+"/"

N_B = 32
N = 8 * N_B
pt = int.from_bytes(open(folder+"bis.txt", "rb").read(N_B), "little")
ct = int.from_bytes(open(folder+"bis.txt.enc", "rb").read(N_B), "little")


var = []
for i in range(N):
	var.append(Bool(str(i)))


def bits2a(b):
    return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(b)] * 8))


def get_SAT(bit, x1, x2, x3):
	if bit:
		return Or(And(Not(x3), Not(x2), x1), And(Not(x1), x2, Not(x3)), And(x3, Not(x2), Not(x1)), And(x3, x2, Not(x1)))
	else:
		return Or(And(Not(x1), Not(x2), Not(x3)), And(Not(x3), x2, x1), And(x1, Not(x2), x3), And(x1, x2, x3))

def get_prev(x):
	SAT = get_SAT(x & 1, var[0], var[1], var[2])
	for i in range(1, N):
		SAT = And(get_SAT((x >> i) & 1, var[i], var[(i+1)%N], var[(i+2)%N]), SAT)
	s = Solver()
	s.add(SAT)
	s.check()
	mod = s.model()
	bits = ""
	for i in range( N):
		if is_true(mod[var[N-1-i]]):
			bits = bits + "1"
		else:
			bits = bits + "0"
	
	return int(bits, 2)
key = pt ^ ct

for i in range(N//2):
	key = get_prev(key)

key = "{:08b}".format(key, 'little').zfill(N)
bits = bits2a(key)
print(bits[:16][::-1] + bits[16:][::-1][:13])
