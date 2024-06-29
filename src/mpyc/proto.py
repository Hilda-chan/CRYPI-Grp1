import sys
from mpyc.runtime import mpc

m = len(mpc.parties)

if m != 2:
    print('Invalid amount of parties. The number of parties must be 2.')
    sys.exit()

server = 0
client = 1

x = ''
if mpc.pid == 1:
    given_name = input("Firstname_Lastname: ")
    print(given_name)


if len(sys.argv) < 2:
    print('Usage: script.py <integers separated by space>')
    sys.exit()

if mpc.pid == server:
    serv_array = list(map(int, sys.argv[1:]))
    print(f"Server inputs: {serv_array}")
else:
    serv_array = []  # no input for server

if mpc.pid == client:
    name = [ord(c) for c in given_name]
    cli_array = list(map(int, sys.argv[1:]))
    print(f"Client inputs: {cli_array}")
else:
    name = ''
    cli_array = []  # no input for client

# Secure integer field
secint = mpc.SecInt()

mpc.run(mpc.start())

### template start ###
# Input secure arrays from server and client


sec_serv_array = mpc.transfer([secint(x) for x in serv_array], senders=server)
sec_cli_array = mpc.transfer([secint(x) for x in cli_array], senders=client)
#sec_name = mpc.transfer([secint(x) for x in name], senders=client)
user_name = mpc.transfer(name, senders=client)

# Wait for the data to come
sec_serv_array = mpc.run(sec_serv_array)
sec_cli_array = mpc.run(sec_cli_array)
#sec_name = mpc.run(sec_name)
user_name = mpc.run(user_name)

# Perform element-wise addition of the secure arrays
secure_sum_array = [sec_serv_array[i] + sec_cli_array[i] for i in range(min(len(sec_serv_array), len(sec_cli_array)))]


# Output the secure array result to the client
result = mpc.run(mpc.output(secure_sum_array, receivers=client))
### template ends ###

mpc.run(mpc.shutdown())

# Process the result
name = ''.join(map(chr, user_name))
print(f'Hello {name}')
if mpc.pid == client:
    print(f'Result of secure array computation: {result}')

