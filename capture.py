import socket
import mysql.connector
from mysql.connector import errorcode

UDP_IP= "<IP address goes here>"
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
type = {'name':'', 'mode':''}

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
	if len(strings) > 2:
		type = {'name':strings[1][1:len(strings[1])], 'mode':strings[2]}
		try:
			cnx = mysql.connector.connect([REDACTED])
		except mysql.connector.Error as err:
		  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		  elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		  else:
			print(err)
		else:
			cursor = cnx.cursor()
			clear_servers = ("DELETE FROM NameMode WHERE name = %(name)s")
			cursor.execute(clear_servers, type)
			add_server = ("INSERT INTO NameMode (name,mode) VALUES (%(name)s, %(mode)s)")
			cursor.execute(add_server, type)
			cnx.commit()
			cursor.close()
			cnx.close()

	strings = []
	i = i+1
