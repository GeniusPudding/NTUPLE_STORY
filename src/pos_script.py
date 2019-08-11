f = open('NTU PIECE/src/pos.txt')
r = f.read()
rr = r.split('\n')
rr = [s.split(' ')[-2:] for s in rr]
rr = [(float(t[0][1:-1]),float(t[1][:-1]) ) for t in rr]
res = [0]*10
for i,t in enumerate(rr):
	res[i//4] += t[1]
	res[6+i%4] += t[0]
for i in range(10):
	if i < 6:
		res[i] = res[i]/4
	else:
		res[i] = res[i]/6

print(res)