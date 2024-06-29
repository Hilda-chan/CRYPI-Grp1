import sys
from mpyc.runtime import mpc

m = len(mpc.parties)

if m != 2:
    print('Invalid amount of parties. The number of parties must be 2.')
    sys.exit()

server = 0
client = 1

if len(sys.argv) < 2:
    print('Usage: script.py <integers separated by space>')
    sys.exit()

if mpc.pid == server:
    serv_ints = list(map(int, sys.argv[1:]))
    print(f"Server inputs: {serv_ints}")
else:
    serv_ints = [0, 0, 0]  # no input for server

if mpc.pid == client:
    cli_ints = list(map(int, sys.argv[1:]))
    print(f"Client inputs: {cli_ints}")
else:
    cli_ints = [0, 0, 0]  # no input for client

# Secure integer field
secint = mpc.SecInt()

mpc.run(mpc.start())

### template start ###
# Input secure arrays from server and client
serv_array = mpc.input([secint(x) for x in serv_ints], senders=server)
cli_array = mpc.input([secint(x) for x in cli_ints], senders=client)

# Perform element-wise addition of the secure arrays
secure_sum_array = [serv_array[i] + cli_array[i] for i in range(len(serv_array))]

# Output the secure array result to the client
result = mpc.run(mpc.output(secure_sum_array, receivers=client))
### template ends ###

mpc.run(mpc.shutdown())

# Process the result
if mpc.pid == client:
    print(f'Result of secure array computation: {result}')

