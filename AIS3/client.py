import socket

SERVER_HOST = '127.0.0.1' 
SERVER_PORT = 5000
BUFFER_SIZE = 1024

def send_request(request, client_socket, data=None):
    try:
        client_socket.sendall(request.encode())
        response = client_socket.recv(BUFFER_SIZE).decode()
        print(response)
        if response == 'READY':
            if data:
                client_socket.sendall(data.encode())
                client_socket.sendall(b'DONE')
            return True
        elif response == 'EXIST':
            return True
        elif response == 'NOT_EXIST':
            return False
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("[*] Connected to server.")
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        return

    while True:
        print("1. Upload file")
        print("2. Download file")
        print("3. Modify file")
        print("4. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            filename = input("Enter filename to upload: ")
            if send_request("UPLOAD", client_socket, filename):
                with open(filename, 'rb') as f:
                    file_data = f.read(BUFFER_SIZE)
                    while file_data:
                        client_socket.sendall(file_data)
                        file_data = f.read(BUFFER_SIZE)
                    client_socket.sendall(b'DONE')
                print(client_socket.recv(BUFFER_SIZE).decode())
            else:
                print("File does not exist.")
        
        elif choice == '2':
            filename = input("Enter filename to download: ")
            if send_request("DOWNLOAD", client_socket, filename):
                data = client_socket.recv(BUFFER_SIZE).decode()
                while data != 'DONE':
                    print(data)
                    data = client_socket.recv(BUFFER_SIZE).decode()
            else:
                print("File does not exist on the server.")

        elif choice == '3':
            filename = input("Enter filename to modify: ")
            if send_request("MODIFY", client_socket, filename):
                row_number = input("Enter row number to modify: ")
                new_value = input("Enter new value: ")
                send_request("", client_socket, row_number)
                send_request("", client_socket, new_value)
                print(client_socket.recv(BUFFER_SIZE).decode())
            else:
                print("File does not exist on the server.")

        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

    client_socket.close()

if __name__ == "__main__":
    main()
