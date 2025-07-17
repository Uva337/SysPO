#!/bin/bash
# clean_binaries.sh - Remove binary files from packaging directories.
# This helps avoid binary file issues in text-based environments.

# Exit if any unexpected error occurs
set -euo pipefail

# Directories to search for binaries
TARGET_DIRS=("packaging/windows" "packaging/linux/debian/DEBIAN")

# Extensions considered as binary artifacts
EXTS=("ico" "png" "exe" "AppImage" "so" "dll" "bin")

# Track if any deletion fails
fail=0

for dir in "${TARGET_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "Directory $dir does not exist, skipping." >&2
        continue
    fi

    for ext in "${EXTS[@]}"; do
        # Search recursively for matching files
        while IFS= read -r -d '' file; do
            echo "Removing $file"
            if ! rm -f "$file"; then
                echo "Failed to remove $file" >&2
                fail=1
            fi
        done < <(find "$dir" -type f -name "*.$ext" -print0)
    done

done

exit $fail
