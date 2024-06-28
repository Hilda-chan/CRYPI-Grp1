import socket
import pickle

def start_server(host='localhost', port=65432):
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the socket to the host and port
        s.bind((host, port))
        # Listen for incoming connections
        s.listen()
        print(f'Server listening on {host}:{port}')

        while True:
            # Accept a connection from the client
            conn, addr = s.accept()
            with conn:
                print(f'Connected by {addr}')
                
                # Receive the data from the client
                data = conn.recv(1024)
                if not data:
                    break

                # Deserialize the received data
                received_data = pickle.loads(data)
                name = received_data['name']
                key = received_data['key']
                vector = received_data['vector']


                print(f'Received data: Name={name}, Key={key}, Vector={vector}')
                
        
        
                # Prepare the response
                if (name == "Hello World"):
                    response = f'Welcome {name}'
                else:
                    response = f'Dude, you ain\'t the one'
                
                # Send the response back to the client
                conn.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    start_server()

