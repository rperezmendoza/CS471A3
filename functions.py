import commands

'''
get_file_size (might want a shorter name)
takes a file name
returns the size of the data to be sent over tcp
including file size + file name + delimiter character
'''
def get_file_size (file_name):
    file = open(file_name, "r")
    file_data = file.read()
    if file_data:
        file_size = len(file_data)
    file.close()
    return (file_size + len(file_name) +1)

'''
putFile Client side version
Takes: socket to ephemeral port, name of file to send
returns: number of bytes sent
'''
def putFile(socket, file_name):

    file = open(file_name, "r")
    # The file data
    file_data = file_name + '%'   
    #prepend the file name to the file data with a delimiter of % which is the ascii code for unit separator

    # Read 65536 bytes of data    
    data_buff = file.read()
    file_data += data_buff 
        
    file_size = len(file_data)
      
    # Send the data!
    bytes_sent = 0
    while bytes_sent != file_size:
        bytes_sent += socket.send(file_data[bytes_sent:])

    file.close()
    return bytes_sent

'''
takes a socket to receive on, and the number of bytes to receive
returns the number of bytes received
the bytes received will be in the form of:
file_name + 1 byte delimiter + file_data
This function creates a file using file_name and then writes file_data into it
'''
def getFile(sock, numBytes):

    # The buffer
    recvBuff = ""

    # The temporary buffer
    tmpBuff = ""

    # Keep receiving till all is received
    while len(recvBuff) != numBytes:
        
        # Attempt to receive bytes
        tmpBuff =  sock.recv(numBytes)
        
        # The other side has closed the socket
        if not tmpBuff:
            break
        
        # Add the received bytes to the buffer
        recvBuff += tmpBuff

    # Write the data to a file
    file_size = len(recvBuff)
    i = recvBuff.find('%')
    file_name = recvBuff[0:i]
    i +=1
    file_data = recvBuff[i:]
    file = open(file_name, "w")
    file.write(file_data)
    file.close()
    return file_size


'''
  Returns a string with the local files in the system's current directory
'''
def get_local_files():
  file_list = commands.getstatusoutput('ls -l')[1]
  return file_list


