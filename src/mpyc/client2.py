import sys
import mpyc
import os
from mpyc.runtime import mpc
from client_encryptor import cli_encrypt

m = len(mpc.parties)

server = 0
client = 1

if m != 2:
    print('Invalid amount of parties. The number of parties must be 2.')
    sys.exit()

if len(sys.argv) < 2:
    print('The path to the picture is required')
    sys.exit()

picture_path = sys.argv[1]
if not os.path.exists(picture_path):
    print("Invalid picture path")
    sys.exit()

print(f"Reading image from {picture_path}")
cli_vectors = cli_encrypt("", picture_path)
print("Image read and face vectors obtained")

# Secure fixed-point field
secfxp = mpc.SecFxp()

mpc.run(mpc.start())

# Transfer client vectors to server
print("Transferring client vectors to server")
sec_cli_vectors = mpc.transfer([secfxp(x) for x in cli_vectors], senders=client)
sec_cli_vectors = mpc.run(sec_cli_vectors)
print("Client vectors transferred")

mpc.run(mpc.shutdown())

# Process the result
mpc.run(mpc.start())
# Receive the minimum distance and the corresponding username from the server
min_distance = mpc.transfer(secfxp(0), senders=server)
ascii_username = mpc.transfer([secfxp(0)] * 100, senders=server)  # Assuming max username length of 100

min_distance = mpc.run(min_distance)
ascii_username = mpc.run(ascii_username)
mpc.run(mpc.shutdown())

# Convert the list of ASCII values back to a string
matched_username = ''.join(chr(int(x)) for x in ascii_username).strip('\x00')

print(f"Minimum distance: {min_distance}, Matched username: {matched_username}")

if min_distance < 0.36:
    print(f'Welcome {matched_username.replace("_", " ")}')
else:
    print('You are not recognized, try again')
