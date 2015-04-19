import socket

UDP_IP= "<VPN ip address goes here>"
UDP_PORT = 11774

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 48 < ord(c) < 127)
    return ''.join(stripped)

def find_split_string(string):
	out = ''
	for c in string:
		if 32 == ord(c) or 47 < ord(c) < 58 or 64 < ord(c) < 91 or 96 < ord(c) < 123 :
			out = out + c
		elif ord(c) > 0:
			break
	return out
	
i = 0

strings = []

f = open("out.txt", "w")

while True:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((UDP_IP, UDP_PORT))
	data, addr = sock.recvfrom(4096)
	
	k = 0
	while k < len(data):
		for x in range(k, len(data)):
			found = find_split_string(data[k:len(data)])
			if len(found) > 3:
				strings.append(found)
				k = k + len(found) * 2
			else:
				k = k + 1
	if len(strings) > 1:
		f.write('capture ' + str(i) + ':\n')
		f.write('\t' + strings[1][1:len(strings[1])] + '\n')
		for s in range(2, len(strings)):
			f.write('\t' + strings[s] + '\n')
	strings = []
	i = i+1
f.close()
