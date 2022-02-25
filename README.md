# Project 2: Distributed File System
## Innopolis University, Fall 2020
**Team**:

[Natalia Matrosova](https://github.com/MatrosovaTalia) - responsible for client and hosting

[Alisa Martyanova](https://github.com/AlisaMartyanova) - responsible for data and naming servers

## Project Description

The Distributed File System (DFS) is a file system with data stored on a server. The data is accessed and processed as if it was stored on the local client machine. The DFS makes it convenient to share information and files among users on a network.Files will be hosted remotely on one or more storage servers. Separately, a single naming server will index the files, indicating which one is stored where. When a client wishes to access a file, it first contacts the naming server to obtain information about the storage server hosting it. After that, it communicates directly with the storage server to complete the operation.

## How to use the file system

run the following command in console: 
```dif
docker run -e N_SERVER_HOST=3.16.46.152 -e N_SERVER_PORT=5550 -it  matrosovatalia/client:v3
```
It will automatically connect to docker swarm with servers and launch the client. You will see the following:

![alt text](https://github.com/AlisaMartyanova/DistributedSystems/blob/master/term.png)

### You can type the following commands in client: 
```dif
init_size -          Get free memory size
create_f <file> -    Create empty file
edit_f <file> -      Append text to <file>
cat_f <file> -       Print <file> content to stdout
read_f <file> -      Download file <file> from server
send_f <file> -      Upload file <file> to server
rm_f <file> -        Delete locally file <file>
rm_f_server <file> - Delete file <file> from server
cp <file> -          Create a copy of <file>
info <file> -        Get info from server about file <file>
mv <src> <dest> -    Move file <src> to <dest>
cd .. -              Go to upper dir
cd <dir> -           Open <dir>
mkdir <dir> -        Create directory <dir> 
mkdir_server <dir> - Create directory <dir> on server
rmdir <dir> -        Delete directory <dir>
rmdir_server <dir> - Delete directory <dir> on server
ls -                 List files in the local directory
ls_server -          List files in the current directory on server
send_all -           Submit all changes to server
quit -               Exit from program
help -               Show available commands
```

**Links to dockerhub:**
[storage server](https://hub.docker.com/repository/docker/matrosovatalia/storage-server), [name server](https://hub.docker.com/repository/docker/matrosovatalia/nameserver), [client](https://hub.docker.com/repository/docker/matrosovatalia/client)

## Architectural Diagram

![alt text](https://github.com/AlisaMartyanova/DistributedSystems/blob/master/architecture_diagram.png)

## Description of communication protocols
As main communication protocol we used the **Hypertext Transfer Protocol (HTTP)** - an application-level TCP/IP based protocol. 

**Client**

The HTTP client sends a request to the server in the form of a request method, URI, and protocol version, followed by a MIME-like message containing request modifiers, client information, and possible body content over a TCP/IP connection.

**Server**

The HTTP server responds with a status line, including the message's protocol version and a success or error code, followed by a MIME-like message containing server information, entity meta information, and possible entity-body content.
