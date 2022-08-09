import socket
from threading import Thread


TCP_IP = 'localhost'
TCP_PORT = 8080


def send(sock):
	while True:
		try:
			message = input('Enter message or enter "stop" or execute Keyboard Interrupt to close client:\n')
			sock.send(message.encode('utf16'))

			if message == 'stop':
				print('Client stoped')
				break
			else:
				continue
				
		except EOFError:
			try: 
				sock.send('stop'.encode('utf16'))
				break
			except ConnectionResetError:
				break

	print('Sending is closed')


def receive(sock):
	while True:
		try:
			data = sock.recv(4096)
			if data.decode('utf16') == 'stop':
				print('Connection was broken by another client')
				break
			elif not data:
				break
			else:
				print(f'Received data: {data.decode("utf16")}')

		except KeyboardInterrupt:
			print('Receiving: keybord interruption')
			break

		except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
			print('Receivig: connection with server was interrupted')
			break

	print('Receiving is closed. Execute Keyboard Interrupt to close client')


def main_client():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		try:
			sock.connect((TCP_IP, TCP_PORT))

			sending_thread = Thread(target=send, args=(sock,))
			receiving_thread = Thread(target=receive, args=(sock,))

			sending_thread.start()
			receiving_thread.start()

			sending_thread.join()
			receiving_thread.join()

		except ConnectionRefusedError:
			print('Connection with server was refused')

		except KeyboardInterrupt:
			pass


if __name__ == '__main__':
	main_client()


