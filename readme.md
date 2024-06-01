# Shinkai C2

## Notes:
- If the response from the client is an empty string, it gonna hang the server. To resolve that, set the ouput from subprocess on the client side to '/r' (carriage return string). So the response from the client is not an enpty string and /r also usefull to not print a blank new line on the server ouput

## Added:
- Terminate all connection with 'terminate' command then display the information message.
- Terminate all connection when exit from the app.
- Kill one connection.
- Add file transfer functionality

## Bugs:
- The server close when all client closed. It should be continue to listen for incoming connection. (Fixed by removing the *break* in *terminate function*)