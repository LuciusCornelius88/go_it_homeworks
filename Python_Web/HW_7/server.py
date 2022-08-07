import socket 
from threading import Thread

TCP_IP = 'localhost'
TCP_PORT = 8080


connections = []
threads = []


def check_connections():
	global connections
	global s_sock

	while True:
		if s_sock.fileno() == -1:
			break

		for conn in connections:
			if conn and conn.fileno() == -1:
				connections.remove(conn)
				print(f'Connection {conn} was deleted')
				print(f'Actual connections: {connections}')

	print('Check connections loop is finished')


def set_timeout(lim_connections):
	global connections
	global s_sock

	while True:
		if s_sock.fileno() == -1:
			break

		if len(connections) >= lim_connections and s_sock.timeout:
			s_sock.settimeout(None)
			print('Number of connections is acceptible and timeout was removed')
		elif len(connections) < lim_connections and not s_sock.timeout:
			s_sock.settimeout(15)
			print(f'Number of connections is less then limit and timeout was set to {s_sock.timeout}')

	print('Timeout setter loop is finished')


def handle_connection(connection, address):
	while True:
		try:
			data = connection.recv(4096)
			print(f'Received {data.decode("utf16")}')

			if data.decode('utf16') == 'stop':
				print(f'Receiving data from {address} is stoped')
				connection.close()
				break

			connection.send('OK: your message is sent'.encode('utf16'))

			an_connection = list(filter(lambda x: x != connection, connections))[0]
			print(an_connection)
			an_connection.send(data)

			print(f'Data sent')
		except ConnectionAbortedError:
			print(f'Connection with {address} was interrupted')
			break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_sock:
	s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s_sock.bind((TCP_IP, TCP_PORT))

	lim_connections = 2

	s_sock.listen(lim_connections)
	print(f'Server is listening for minimum {lim_connections} connections...')

	connections_checker = Thread(target=check_connections)
	timeout_setter = Thread(target=set_timeout, args=(lim_connections,))

	threads.append(connections_checker)
	threads.append(timeout_setter)

	connections_checker.start()
	timeout_setter.start()

	try:
		while True:
			conn, addr = s_sock.accept()
			connections.append(conn)
			print(f'Connected to {addr}')

			client_thread = Thread(target=handle_connection, args=(conn, addr))
			threads.append(client_thread)

			client_thread.start()

	except KeyboardInterrupt:
		print('Keybord interruption')
	except TimeoutError:
		print('Time of waiting for connections is out')

[conn.close() for conn in connections]
[thread.join() for thread in threads]
	
print('Session is closed')





