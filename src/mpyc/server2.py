import sys
import mpyc
import os
from mpyc.runtime import mpc
from server_encryptor import serv_encrypt

m = len(mpc.parties)

server = 0
client = 1

if m != 2:
    print('Invalid amount of parties. The number of parties must be 2.')
    sys.exit()

cli_vectors = []

# Secure fixed-point field
secfxp = mpc.SecFxp()

mpc.run(mpc.start())

# Receive client vectors from the client
print("Receiving client vectors from client")
sec_cli_vectors = mpc.transfer([secfxp(0)] * 128, senders=client)  # Assuming 128-d face vectors
sec_cli_vectors = mpc.run(sec_cli_vectors)
print("Client vectors received")

mpc.run(mpc.shutdown())

# Initialize minimum distance and matching username
min_distance = float('inf')
matched_username = ""

# Iterate over the database to find the minimum distance
data_path = './data/LFW/'
print(f"Starting to iterate over the database at {data_path}")

mpc.run(mpc.start())
person = 0
for root, dirs, files in os.walk(data_path):
    for person_dir in dirs:
        person += 1
        person_path = os.path.join(root, person_dir)
        print(f"Processing {person_path}")
        print(f"[DEBUG][PERSON]: {person}")
        
        for file in os.listdir(person_path):
            if file == "Sid_Caesar_0001.jpg":
                continue
            if file.endswith(".jpg") or file.endswith(".png"):
                image_path = os.path.join(person_path, file)
                try:
                    serv_vectors = serv_encrypt(image_path)                
                except ValueError as e:
                    print(f"Skipping {image_path}: {e}")
                    continue
                # Transfer server vectors to the client
                sec_serv_vectors = mpc.transfer([secfxp(x) for x in serv_vectors], senders=server)
                sec_serv_vectors = mpc.run(sec_serv_vectors)

                # Compute the Euclidean distance
                res = 0
                for i in range(len(sec_serv_vectors)):
                    tmp = sec_serv_vectors[i] - sec_cli_vectors[i]
                    res += (tmp * tmp)

                distance = mpc.run(mpc.output(res))
                print(f"Distance for {image_path}: {distance}")
                if distance < min_distance:
                    min_distance = distance
                    matched_username = person_dir
                print(f"[DEBUG][MATCH]: {matched_username}")
                print(f"[DEBUG][MIN_DIST]: {min_distance}")
        if person_dir == "Sid_Caesar":
            break

# Convert matched username to ASCII values
ascii_username = [ord(c) for c in matched_username]

# Send the minimum distance and matching username to the client
print(f"Minimum distance found: {min_distance} for {matched_username}")
mpc.transfer(secfxp(min_distance), receivers=client)
mpc.transfer([secfxp(x) for x in ascii_username], receivers=client)
mpc.run(mpc.shutdown())
