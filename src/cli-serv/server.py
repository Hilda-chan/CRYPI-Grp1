import socket
import pickle
import os
import sys
import Pyfhel
import numpy as np
import cv2
#sys.path.append('../')
from prototype import readImg
import face_recognition

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
                data = conn.recv(65356)
                if not data:
                    break

                # Deserialize the received data
                received_data = pickle.loads(data)
                firstname = received_data['firstname']
                lastname = received_data['lastname']
                key = received_data['key']
                vector = received_data['vector']


                print(f'Received data: Firstname={firstname}, Lastname={lastname}, Key={key}, Vector={vector}')
        
                # Construct the directory path
                directory_path = f'data/LFW/{firstname}_{lastname}'

                # Check if the directory exists
                if os.path.exists(directory_path):
                    # List images in the directory
                    images = os.listdir(directory_path)
                    # Look for the specific image
                    image_path = None
                    for image in images:
                        if image.startswith(f'{firstname}_{lastname}_0001.jp'):
                            image_path = os.path.join(directory_path, image)
                            img = readImg(image_path)
                            HE = Pyfhel.Pyfhel()
                            ckks_params = {
                                'scheme': 'CKKS',
                                'n': 2**14,
                                'scale': 2**30,
                                'qi_sizes': [60, 30, 30, 30, 60]
                            }
                            HE.contextGen(**ckks_params)
                            HE.keyGen()
                            #v = getFaceVectors(img)

                            break
                    if image_path:
                        response = f'Image found for {firstname} {lastname}.'

                    else:
                        response = f'Directory found but not image for {firstname} {lastname}.'

                else:
                    response = f'Image not found for {firstname} {lastname}'        
                
                # Send the response back to the client
                conn.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    start_server()
