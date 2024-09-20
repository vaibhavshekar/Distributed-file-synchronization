import socket
import sys
import os

def upload_file(file_socket, filepath):
    # Handle file upload (TCP Connection)
    filename = os.path.basename(filepath)
    try:
        file_socket.send(f"UPLOAD {filename}".encode())
        with open(filepath, "rb") as f:
            data = f.read(1024)
            while data:
                file_socket.send(data)
                data = f.read(1024)
        print(f"File {filename} uploaded.")
    except Exception as e:
        print(f"Failed to upload file: {e}")

def request_view(file_socket, filename):
    # Handle file view request (TCP Connection)
    try:
        file_socket.send(f"VIEW_REQUEST {filename}".encode())
        file_content = ""
        while True:
            data = file_socket.recv(1024)
            if b"END_OF_FILE" in data:
                file_content += data.decode().replace("END_OF_FILE", "")
                break
            file_content += data.decode()

        print(f"Viewing {filename}:")
        print(file_content)
    except Exception as e:
        print(f"Failed to view file: {e}")

def request_edit(file_socket, filename):
    # Handle file edit request (TCP Connection)
    try:
        file_socket.send(f"EDIT_REQUEST {filename}".encode())
        response = file_socket.recv(1024).decode()
        if response.startswith("EDIT_DENIED"):
            print(response)
            return

        file_content = ""
        while True:
            data = file_socket.recv(1024)
            if b"END_OF_FILE" in data:
                file_content += data.decode().replace("END_OF_FILE", "")
                break
            file_content += data.decode()

        print(f"Editing {filename}:")
        print(file_content)

        edited_content = file_content
        while True:
            line = input()
            if line.strip() == "~exit":
                break
            edited_content += line + "\n"

        file_socket.send(edited_content.encode() + b"~exit")
        print("Edit complete.")
    except Exception as e:
        print(f"Failed to edit file: {e}")

def download_file(file_socket, filename):
    # Handle file download (TCP Connection)
    try:
        file_socket.send(f"DOWNLOAD_REQUEST {filename}".encode())
        with open(f"downloaded_{filename}", "wb") as f:
            while True:
                data = file_socket.recv(1024)
                if b"END_OF_FILE" in data:
                    break
                f.write(data)
        print(f"File downloaded as downloaded_{filename}")
    except Exception as e:
        print(f"Failed to download file: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 client.py <upload/download/view/edit> <file_path>")
        sys.exit(1)

    action = sys.argv[1]
    filepath = sys.argv[2]
    
    file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        file_socket.connect(('192.168.135.132', 9000))
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        sys.exit(1)

    if action == "upload":
        upload_file(file_socket, filepath)
    elif action == "download":
        download_file(file_socket, filepath)
    elif action == "view":
        request_view(file_socket, filepath)
    elif action == "edit":
        request_edit(file_socket, filepath)
    else:
        print("Unknown action. Use 'upload', 'download', 'view', or 'edit'.")

    # Close connection after operation (TCP Connection)
    file_socket.close()

if __name__ == "__main__":
    main()
