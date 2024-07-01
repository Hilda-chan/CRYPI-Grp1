import sys
import mpyc
import os
from mpyc.runtime import mpc
from client_encryptor import toUsername, cli_encrypt
from server_encryptor import serv_encrypt

m = len(mpc.parties)

server = 0
client = 1

if m != 2:
    print('Invalid amount of parties. The number of parties must be 2.')
    sys.exit()

username = ''
picture_path = ''
cli_vectors = []

# Secure integer field
secfxp = mpc.SecFxp()

mpc.run(mpc.start())
### template start ###

shared_username = mpc.transfer(username, senders=client) # Get the username typed by the client
shared_username = mpc.run(shared_username) # Wait for the username to be entirely loaded

### template end ###
mpc.run(mpc.shutdown())

serv_vectors = serv_encrypt(shared_username)


mpc.run(mpc.start())
### template start ###

# Receive the two arrays
sec_serv_vectors = mpc.transfer([secfxp(x) for x in serv_vectors], senders=server)
sec_cli_vectors = mpc.transfer([secfxp(x) for x in cli_vectors], senders=client)

# Wait for the data to come
sec_serv_vectors = mpc.run(sec_serv_vectors)
sec_cli_vectors = mpc.run(sec_cli_vectors)

# Perform element-wise addition of the secure arrays
res = 0
for i in range (len(sec_serv_vectors)):
    tmp = sec_serv_vectors[i] - sec_cli_vectors[i]
    res += (tmp * tmp)

# Output the secure array result to the client
result = mpc.run(mpc.output(res, receivers=client))

### template ends ###
mpc.run(mpc.shutdown())