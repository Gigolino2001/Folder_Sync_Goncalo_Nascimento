import sys
import os
import time
import logging
import hashlib
import shutil


def setup_logger(log_file):
    logging.basicConfig(level=logging.INFO,
                        format="{asctime} - {levelname} - {message}",
                        style="{",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        handlers=[
                            logging.FileHandler(log_file),
                            logging.StreamHandler()
                        ])

def create_folders(source_folder, replica_folder):
    if not os.path.exists(source_folder):
        os.makedirs(source_folder, exist_ok=True)
        logging.info(f"Source folder '{source_folder}' created.")

    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder, exist_ok=True)
        logging.info(f"Replica folder '{replica_folder}' created.")

def is_file_modified (source_file, replica_file):    
    source_file_stat = os.stat(source_file)
    replica_file_stat = os.stat(replica_file)

    if source_file_stat.st_size != replica_file_stat.st_size:
        return True
    
    if source_file_stat.st_mtime != replica_file_stat.st_mtime:
        return True
    
    return hashlib.md5(open(source_file, 'rb').read()).hexdigest() != hashlib.md5(open(replica_file, 'rb').read()).hexdigest()

def sync_folders(source_folder, replica_folder):
    for root, _, files in os.walk(source_folder):
        for file in files:
            print(root)
            source_file = os.path.join(root, file)
            relative_replica_path = os.path.relpath(source_file, source_folder)
            replica_file = os.path.join(replica_folder, relative_replica_path)
            if os.path.isfile(replica_file):
                if is_file_modified():
                    logging.info(f"File '{source_file}' has been modified. Updating '{replica_file}'...")
                    shutil.copy2(source_file, replica_file)
                    logging.info(f"Updated '{replica_file}' with '{source_file}'")
                else:
                    logging.info(f"No changes detected in '{source_file}'")
            else:
                logging.info(f"New file detected: '{source_file}'")
                os.makedirs(os.path.dirname(replica_file), exist_ok=True)
                shutil.copy2(source_file, replica_file)
                logging.info(f"Copied '{source_file}' to '{replica_file}'")

    for root, _, files in os.walk(replica_folder):
        for file in files:
            replica_file = os.path.join(root, file)
            relative_source_path = os.path.relpath(replica_file, replica_folder)
            source_file = os.path.join(source_folder, relative_source_path)
            if not os.path.exists(source_file):
                os.remove(replica_file)
                logging.info(f"Removed '{replica_file}'")


def main(source_folder, replica_folder, interval, log_file_path):

    setup_logger(log_file_path)
    create_folders(source_folder, replica_folder)

    logging.info("Starting the synchronization process...")
    while True:
        try:
            sync_folders(source_folder, replica_folder)
            logging.info("Synchronization completed successfully.")
        except Exception as e:
            logging.error(f"An error occurred during synchronization: {e}")

        logging.info(f"Waiting for {interval} seconds before the next synchronization...")
        time.sleep(interval)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python app.py <source_folder_path> <replica_folder_path> <interval_in_seconds> <log_file_path>")
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    interval = int(sys.argv[3])
    log_file_path = sys.argv[4]

    main(source_folder, replica_folder, interval, log_file_path)