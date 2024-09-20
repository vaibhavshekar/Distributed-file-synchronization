import socket
import threading
import os

# Dictionary to manage file locks
file_locks = {}
file_locks_lock = threading.Lock()

def handle_client(client_socket, address):
    # TCP Connection handling for individual client requests
    print(f"Connection from {address}")
    while True:
        try:
            request = client_socket.recv(1024).decode()
            if not request:
                break

            if request.startswith("UPLOAD"):
                _, filename = request.split(maxsplit=1)
                receive_upload(client_socket, filename)

            elif request.startswith("DOWNLOAD_REQUEST"):
                _, filename = request.split(maxsplit=1)
                send_file(client_socket, filename)

            elif request.startswith("VIEW_REQUEST"):
                _, filename = request.split(maxsplit=1)
                send_file_for_view(client_socket, filename)

            elif request.startswith("EDIT_REQUEST"):
                _, filename = request.split(maxsplit=1)
                handle_edit_request(client_socket, filename)

            # Close connection after each operation
            break

        except Exception as e:
            print(f"Error handling client: {e}")
            break
    client_socket.close()
    print(f"Connection with {address} closed.")

def receive_upload(client_socket, filename):
    # Handle file upload (TCP Connection)
    filepath = os.path.join("files", filename)
    with open(filepath, "wb") as f:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            f.write(data)
    print(f"File {filename} uploaded.")

def send_file(client_socket, filename):
    # Handle file download (TCP Connection)
    filepath = os.path.join("files", filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.send(data)
        client_socket.send(b"END_OF_FILE")
    else:
        client_socket.send(b"FILE_NOT_FOUND")
    print(f"File {filename} sent for download.")

def send_file_for_view(client_socket, filename):
    # Handle file view request (TCP Connection)
    filepath = os.path.join("files", filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.send(data)
        client_socket.send(b"END_OF_FILE")
    else:
        client_socket.send(b"FILE_NOT_FOUND")
    print(f"File {filename} sent for viewing.")

def handle_edit_request(client_socket, filename):
    # Handle file edit request (TCP Connection)
    with file_locks_lock:
        if filename in file_locks:
            client_socket.send(b"EDIT_DENIED: Another client is currently editing this file.")
            return
        file_locks[filename] = client_socket

    filepath = os.path.join("files", filename)

    try:
        # Send existing file content
        with open(filepath, "r") as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.send(data.encode())
        client_socket.send(b"END_OF_FILE")

        # Receive edited content from client
        edited_content = ""
        while True:
            data = client_socket.recv(1024)
            if b"~exit" in data:
                edited_content += data.decode().replace("~exit", "")
                break
            edited_content += data.decode()

        # Save updated file
        with open(filepath, "w") as f:
            f.write(edited_content)
        print(f"File {filename} successfully edited.")
        client_socket.send(b"EDIT_COMPLETE")
    except Exception as e:
        print(f"Error during editing file {filename}: {e}")
    finally:
        with file_locks_lock:
            if filename in file_locks and file_locks[filename] == client_socket:
                del file_locks[filename]  # Release the lock
        print(f"Edit lock released for {filename}")

def start_server():
    # Start server and accept client connections (TCP Connection)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9000))
    server_socket.listen(5)
    print("Server is listening on port 9000...")

    while True:
        client_socket, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
