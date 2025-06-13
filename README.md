# Zecret Explorer

A simple command-line Zcash blockchain explorer written in Python.  
It allows you to fetch detailed information about any Zcash block by entering its block height or block hash.
---

## Features

- Retrieve block data by height or hash
- Display block summary including:
- Block hash, height, confirmations, size, difficulty, previous/next blocks, and timestamp
- Display transaction details within the block
- Show transaction outputs with addresses and amounts (in ZEC)
- Clean, colored terminal output powered by the [`rich`](https://github.com/Textualize/rich) library for better readability

---

## Requirements

- Python 3.7+
- [`requests`](https://pypi.org/project/requests/)
- [`rich`](https://pypi.org/project/rich/)


## Install
- `git clone https://github.com/roguehashrate/zecret-explorer.git`
- `cd` into the directory
- Run `python3 main.py`
- It should be running now, just follow the instructions :)

(This is still very much a work in progress but it does technically work.)
