# Hash Manager
- This is just a simple program i create for managing hashes, if you find any bugs or ideas how to make this better, i will love to hear it (Maybe not so much the bugs tho XD).

## Installation
- Apt packages to install: 
```bash
sudo apt-get install python3-pil.imagetk python3-tk
```
- Pip3 packages to install:
```bash
pip3 install -r requirements.txt
```

## Usage
- You can copy the data from the items with a right click

- I didn't manage to optimze the size of the items automaticly, so you must edit them manually in the file.

- I also wrote a program that converts the json data to the database format expected by the main program. Usage example:
```bash
./json2sldb.py -i data.json -o out.db
```
- The json file can look for example like this:
```json
[
    {"username": "david", "hash": "25f9e794323b453885f5181f1b624d0b", "password": "123456789", "state": 1},
    {"username": "john", "hash": "f93fc10472a31bb3061aa0b45e228c5a", "state": 0}
]
```
- `"state": 1` for cracked password and `"state": 0` for not cracked password
