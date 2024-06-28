import socket
import pickle

def send_data_to_server(firstname, lastname, key, vector, host='localhost', port=65432):
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the server
        s.connect((host, port))
        
        # Prepare the data to be sent
        data = {
            'firstname': firstname,
            'lastname': lastname,
            'key': key,
            'vector': vector
        }
        
        # Serialize the data
        serialized_data = pickle.dumps(data)
        
        # Send the serialized data to the server
        s.sendall(serialized_data)
        
        # Receive the response from the server
        response = s.recv(65536)
        
        # Decode and print the response
        print('Received from server:', response.decode('utf-8'))

if __name__ == "__main__":
    # Example data
    firstname = 'Hello'
    lastname = 'World'
    key = '123482659'
    vector = [[1, 2, 3], [4, 5, 6]]
    
    send_data_to_server(firstname, lastname, key, vector)

