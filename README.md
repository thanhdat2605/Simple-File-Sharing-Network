# ComputerNetwork_Assignment1
 
## General Info

Build a simple file-sharing application with application protocols defined by each group, using the TCP/IP protocol stack.

## APPLICATION DESCRIPTION

* A centralized server keeps track of which clients are connected and storing what files.

* A client informs the server as to what files are contained in its local repository but does not actually transmit file data to the server.

* When a client requires a file that does not belong to its repository, a request is sent to the server. The server identifies some other clients who store the requested file and sends their identities to the requesting client. The client will select an appropriate source node and the file is then directly fetched by the requesting client from the node that has a copy of the file without requiring any server intervention.

• Multiple clients could be downloading different files from a target client at a given point in time. This requires the client code to be multithreaded.

• The client has a simple command-shell interpreter that is used to accept two kinds of commands.

o publish lname fname: a local file (which is stored in the client's file system at lname) is added to the client's repository as a file named fname and this information is conveyed to the server.

o fetch fname: fetch some copy of the target file and add it to the local repository.

• The server has a simple command-shell interpreter

o discover hostname: discover the list of local files of the host named hostname

o ping hostname: live check the host named hostname

