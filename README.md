# ComputerNetwork_Assignment1


## Table of contents
* [General info](#general-info)
* [Application description](#application-description)
* [Technologies](#technologies)

  
## General Info

Build a simple file-sharing application with application protocols defined by each group, using the TCP/IP protocol stack.

## Application description

* A centralized server keeps track of which clients are connected and storing what files.

* A client informs the server as to what files are contained in its local repository but does not actually transmit file data to the server.

* When a client requires a file that does not belong to its repository, a request is sent to the server. The server identifies some other clients who store the requested file and sends their identities to the requesting client. The client will select an appropriate source node and the file is then directly fetched by the requesting client from the node that has a copy of the file without requiring any server intervention.

* Multiple clients could be downloading different files from a target client at a given point in time. This requires the client code to be multithreaded.

* The client has a simple command-shell interpreter that is used to accept two kinds of commands.
  * __publish *lname* *fname*__: a local file (which is stored in the client's file system at lname) is added to the client's repository as a file named fname and this information is conveyed to the server.
  * __fetch *fname*__: fetch some copy of the target file and add it to the local repository.

* The server has a simple command-shell interpreter
  * __discover *hostname*__: discover the list of local files of the host named hostname
  * __ping *hostname*__: live check the host named hostname

<p align="center">
  <img src="/screenshots/figure1.png" alt="Illustration of file-sharing system activities." width=400/>
</p>

## Technologies

* Python: Version 3.11 or under
* Shareable files: text, images
