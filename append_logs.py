import time
import os

def create_and_append_logs(file_path, num_entries):
    with open(file_path, 'w') as f:
        f.write('')  # Create an empty file or clear existing content

    for i in range(1, num_entries + 1):
        with open(file_path, 'a') as f:
            f.write(f'Hello World {i}\n')
        time.sleep(1)

if __name__ == "__main__":
    log_file_path = os.path.join(os.path.dirname(__file__), 'log_file.log')
    
    num_entries = 200  # Number of entries to append
    create_and_append_logs(log_file_path, num_entries)
