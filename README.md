# Secure Shredder (Python/Linux)

A security utility designed for **permanent file destruction** on Linux systems. Standard deletion (`rm`) only unlinks files, leaving data recoverable. This tool ensures data is overwritten multiple times before removal.

## 🛡️ Security Logic
* **DOD-Standard Overwriting:** Uses the `shred` utility to overwrite data bits, making recovery via forensic tools like `testdisk` or `photorec` significantly harder.
* **Recursive Processing:** Capable of handling entire directories for bulk data sanitization.
* **Risk Awareness:** Documentation includes warnings regarding SSD wear leveling and journaled file systems (EXT4), showing an understanding of hardware-level security.

## 🚀 Usage
```bash
# Shred a single file
python3 shredder.py secret_file.txt

# Shred a directory recursively
python3 shredder.py -u /path/to/directory/
