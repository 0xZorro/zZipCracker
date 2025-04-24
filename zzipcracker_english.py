
# ============================================
# zZipCracker – Brute-Force ZIP Cracking Tool
# ============================================
# Author: Jose Luis Ocana (GitHub: 0xZorro)
# Created:   2025-04-21
# Description: A lightweight Python tool to demonstrate brute-force attacks on
#              password-protected ZIP files. Developed for learning and 
#              awareness purposes. Supports automatic workload splitting 
#              across parallel processes.
#
#
# License: MIT License (see LICENSE file for details)
# Version: 1.0
# Repository: https://github.com/0xZorro/zZipCracker
# ============================================

from argparse import ArgumentParser
from subprocess import Popen, PIPE, STDOUT,  TimeoutExpired
from tqdm import tqdm
import itertools
import string
import os

# ---------- Prepare character list ----------
all_chars = string.ascii_letters + string.digits + string.punctuation
filtered_chars = []

for c in all_chars:
    if c != '"':    # Remove the character " as it causes issues when passing to the command line
        filtered_chars.append(c)

characters = ''.join(filtered_chars)
  
# ---------- Function to test a password ----------
def unzip(archiv, pwd):
    #print(f"Teste Passwort: {pwd}")  # <--- nur zur Kontrolle
    sCmd = f"7z x \"{archiv}\" -p\"{pwd}\" -y"    
    try:
        prozess = Popen(sCmd, stdout=PIPE, stderr=STDOUT)
        stdout, _ = prozess.communicate(timeout=1)  
        return prozess.returncode == 0 # Verify the return value – 0 indicates that the unzip operation was successful
    except TimeoutExpired:
        #print(f"[TIMEOUT] bei Passwort: {pwd}")
        prozess.kill()
        return False
    
# ---------- This function executes the individual process. ----------#
def crack_zip(archiv, min_len=1, max_len=10, segment_index =None):
    # The character list is split into 4 processes here
    # Note: Extending to more processes requires adjustments throughout the entire workflow
    num_processes = 4     
    character_length = len(characters)
    range_size = character_length // num_processes
    segments  = []
    start = 0
    for i in range(num_processes):
        # The last segment takes the remaining characters
        if i == num_processes - 1:
            ende = character_length
        else:
            ende = start + range_size

        segment  = characters[start:ende]
        segments .append(segment)
        start = ende

   # Define the character section for this process to work on
    start_character = segments [segment_index ]

    for n in tqdm(range(min_len, max_len + 1), total=max_len - min_len + 1, desc="password length", position=0, leave=True):
        rest_len = n - 1
        # For each start character in this range, test all possible combinations
        for first_letter in start_character:
            total_kombis = len(characters) ** rest_len
            for kombi in tqdm(itertools.product(characters, repeat=rest_len),total=total_kombis,desc=f"{first_letter}xxxx",leave=False):
                password = first_letter + ''.join(kombi)
                print(f"\password: {password}", end="", flush=True)
                if unzip(archiv, password):
                    print(f"\nPassword cracked: {password}")
                    return password              
    print("Password not found!")


def main():
    parser = ArgumentParser(description = "ZIP cracker using brute-force attack")
    parser.add_argument("archiv", help="path to zip file")
    parser.add_argument("min", type=int, help="Minimum password length")
    parser.add_argument("max", type=int, help="Maximum password length")
    parser.add_argument("segment_index ", nargs="?", type=int, help="Character range index (for CMD processes)")  #Dieses Argument ist optional
    args = parser.parse_args() 
    # Normally, the segment_index argument is not set.
    # It is only used to manually test a specific character range.


    # Only executed if segment_index is set – useful for manually testing a specific range
    # Usually, it's left as None, and the program automatically starts four processes
    if args.segment_index  is not None:
        crack_zip(args.archiv, args.min, args.max, segment_index =args.segment_index )
        return

   # Default case: Automatically start 4 CMD windows (one process per character range)
    try:
        number_of_segments = 4
        for segment_index  in range(number_of_segments):
            cmd = f'start cmd /k python "{__file__}" "{args.archiv}" {args.min} {args.max} "{segment_index }"'
            os.system(cmd)

    except KeyboardInterrupt:
        print("\n Operation manually aborted (Ctrl + C).")


if __name__ == "__main__":
    main()
