import subprocess
import time
import os

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def test_performance(action, file_path, server_ip):
    start_time = time.time()
    
    # Determine the correct command based on the action
    if action == 'upload':
        command = f"python3 client.py {action} {file_path}"  # Full file path for upload
    else:
        filename = os.path.basename(file_path)  # Just the filename for other actions
        command = f"python3 client.py {action} {filename}"
    
    # Run the client application for the specified action
    run_command(command)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time

def main():
    server_ip = '10.12.235.163'  # Replace with your server IP
    file_path = '/home/vaibhav-client/Documents/Networks/project/sample2.txt'
    actions = ['upload', 'download', 'view', 'edit']
    
    # Create a file to use for testing
    with open(file_path, 'wb') as f:
        f.write(b'hi \n ~exit')  # 1 MB random content

    results = []
    
    for action in actions:
        print(f"Testing {action}...")
        time_taken = test_performance(action, file_path, server_ip)
        results.append((action, time_taken))
    
    # Print results
    for action, duration in results:
        print(f"Action: {action}, Time Taken: {duration:.2f} seconds")

if __name__ == "__main__":
    main()
