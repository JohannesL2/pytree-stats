from __future__ import annotations
from typing import Tuple
from pathlib import Path
from collections import Counter

all_extensions = []

def collect_stats(directory: Path, ignore: set)->Tuple[int,int,list]:
    """Calculates total_folders and total_size"""
    total_size = 0
    total_folders = 1
    for path in directory.rglob("*"):
        if any(part.startswith('.') or part in ignore for part in path.parts):
            continue
        if path.is_dir():
            total_folders += 1
        elif path.is_file():
            all_extensions.append(path.suffix.lower())
            total_size += path.stat().st_size
    
    return total_size, total_folders, all_extensions

def calc_helper(root:Path, ignore:set)->Tuple[int,Counter,int,int]:
    """Helps combining crucial values in one return"""
    total_size, total_folder, all_extensions= collect_stats(root, ignore)
    total_files = len(all_extensions)
    file_counts = Counter(all_extensions)

    return total_files, file_counts, total_size, total_folder

   