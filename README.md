# Distributed-file-synchronization
The Distributed File Synchronization System (DFS) is a network application designed to allow users to synchronize files across multiple devices in real-time. This system will enable users to access their files from any connected device, ensuring that the most up-to-date version of each file is always available.
The DFS will consist of a central server and multiple client applications. The central server will be responsible for managing user accounts, storing file metadata, and coordinating synchronization between clients. Client applications will run on various devices (desktops, laptops, mobile devices) and handle local file operations, detect changes, and communicate with the server to maintain synchronization.

to run the client(linux):
  python3 client.py <action> <path/filename>

to run the server:
  python3 server.py

make sure to replace your port numbers and IP with the server's port number and IP.
