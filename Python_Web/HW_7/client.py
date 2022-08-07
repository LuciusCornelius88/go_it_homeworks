import socket
from threading import Thread


TCP_IP = 'localhost'
TCP_PORT = 8080


def send(sock):
	while True:
		try:
			print('Enter message or enter "stop" or execute Keyboard Interrupt to close client: ')
			message = input()
			sock.send(message.encode('utf16'))

			if message == 'stop':
				print('Client stoped')
				break
			else:
				continue
				
		except EOFError:
			try: 
				sock.send('stop'.encode('utf16'))
				print('EOF error')
				break
			except ConnectionResetError:
				break

	print('Sending is closed')


def receive(sock):
	while True:
		try:
			data = sock.recv(4096)
			if not data:
				break
			print(f'Received data: {data.decode("utf16")}')

		except KeyboardInterrupt:
			print('Receiving: keybord interruption')
			break

		except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
			print('Receivig: connection with server was interrupted')
			break

	print('Receiving is closed. Execute Keyboard Interrupt to close client')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	sock.connect((TCP_IP, TCP_PORT))

	sending_thread = Thread(target=send, args=(sock,))
	receiving_thread = Thread(target=receive, args=(sock,))

	sending_thread.start()
	receiving_thread.start()

	try:
		sending_thread.join()
		receiving_thread.join()
	except KeyboardInterrupt:
		pass


