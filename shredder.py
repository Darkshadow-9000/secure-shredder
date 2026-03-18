import os
import subprocess
import sys
import shutil

def show_help():
    """Logic: Print a clear menu explaining how to use the tool."""
    print("""
=========================================
      SECURE SHREDDER TOOL (v1.0)
=========================================
Usage: 
    python3 shredder.py [options] <path>

Arguments:
    <path>      The file or folder you want to shred.

Options:
    -u          Deletes the file/folder after shredding (Unlink).
    -h, --help  Show this help menu.

Examples:
    python3 shredder.py my_folder/       <- Overwrites content only.
    python3 shredder.py -u my_folder/    <- Overwrites and DELETES.
=========================================
    """)

def secure_cleanup(path, use_u_flag=False):
    if not os.path.exists(path):
        print(f"[-] Error: {path} not found.")
        return

    # LOGIC: Removed '-v' to keep the terminal quiet
    shred_command = ["shred", "-n", "3", "-z"]
    
    if use_u_flag:
        shred_command.append("-u")

    if os.path.isfile(path):
        print(f"[*] Securely wiping file...")
        result = subprocess.run(shred_command + [path])
        if result.returncode != 0:
            print(f"[-] Error: Failed to shred {path}")
            return
        print("[+] Done.")
        return

    if os.path.isdir(path):
        print(f"[*] Processing directory: {path}")
        file_count = 0
        
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                # Run shred with error checking
                result = subprocess.run(shred_command + [file_path], capture_output=True)
                if result.returncode != 0:
                    print(f"[-] Warning: Failed to shred {file_path}")
                    if use_u_flag:
                        # Force delete if shred fails
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            print(f"[-] Error removing {file_path}: {e}")
                else:
                    file_count += 1

            if use_u_flag:
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    try:
                        os.rmdir(dir_path)
                    except OSError as e:
                        print(f"[-] Warning: Could not remove {dir_path}: {e}")

        if use_u_flag:
            try:
                os.rmdir(path)
                print(f"[+] Cleaned {file_count} files and removed directory successfully.")
            except OSError as e:
                print(f"[-] Error: Could not remove root directory {path}: {e}")
                print(f"[+] Cleaned {file_count} files, but directory still contains items.")
        else:
            print(f"[+] Successfully overrode {file_count} files.")

# --- EXECUTION LOGIC ---
if __name__ == "__main__":
    # 1. Logic Check: No arguments
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    # 2. Logic Check: Help requested
    if sys.argv[1] in ["-h", "--help"]:
        show_help()
        sys.exit(0)

    # 3. Logic: Handle "Flag First" vs "Path First"
    if sys.argv[1] == "-u":
        # Conventional: -u comes before the path
        if len(sys.argv) < 3:
            print("[-] Error: Please provide a path after the -u flag.")
            sys.exit(1)
        target_path = sys.argv[2]
        wants_to_delete = True
    else:
        # Default: First argument is the path, no deletion
        target_path = sys.argv[1]
        wants_to_delete = False

    secure_cleanup(target_path, wants_to_delete)