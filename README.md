# Folder_Sync_Goncalo_Nascimento

This project offers a utility for periodically synchronizing files between a source folder and a replica folder. The synchronization is one-way, meaning that the contents of the replica folder will match those of the source folder.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Future Improvements](#future-improvements)

## Installation

To clone this project, please execute the following commands:

```bash
git clone https://github.com/Gigolino2001/Folder_Sync_Goncalo_Nascimento.git
cd Folder_Sync_Goncalo_Nascimento
```

Before running this project you should install:

- [Python](https://www.python.org/)

### Note

This program was built and tested on Windows 10.

## Usage

To use the folder synchronization, run the script from the command line with the required parameters:

```bash
python app.py <source_folder_path> <replica_folder_path> <interval_in_seconds> <log_file_path>
```

If the specified paths do not exist, the program will automatically create them.

### Example

This example will synchronize files from `/path/to/source_folder` to `/path/to/replica_folder` every 10 seconds, logging output to `/path/to/log_file.log`.

```bash
python app.py /path/to/source_folder /path/to/replica_folder 10 /path/to/log_file.log
```

## Future Improvements

1. Create Unit Tests
2. Create Performance Tests
