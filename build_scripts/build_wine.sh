#!/bin/bash
# Script for building Windows binaries (.EXE) on Linux using Wine.
# For this to work, you need to:
#   1. Install Python for Windows via your Wine prefix of choice,
#   2. Change path_to_wineprefix to point to the prefix
#   3. Change python_dir to point to your Python directory in the prefix
#      (use Windows-style path like C:/Python312,
#      not the full path like /home/user/wine/...etc)
#
# This script was adapted from instructions by makeworld:
# https://www.makeworld.space/2021/10/linux-wine-pyinstaller.html
#
# Additionally, this script uses py7zip to automatically package the produced
# folder into a .zip archive. You can usually get py7zip from your distro's
# distro's repositories. If you don't need that functionality,
# comment out the last two lines of the script.
python_dir="C:/Python312"
path_to_wineprefix = "`pwd`/wineprefix"

program_name="VFS_Explorer_windows_amd64"

if [ -d "dist/$program_name" ]; then
    rm -rf "dist/$program_name";
fi
if [ -d "dist/$program_name.zip" ]; then
    rm -rf "dist/$program_name.zip";
fi

WINEPREFIX="$path_to_wineprefix" wine $python_dir/Scripts/pyinstaller.exe \
vfs_explorer.py
--name "$program_name" \
--contents-directory "programresources" \
--noconsole \
--icon icon.ico

cd .dist/
7za a $program_name.zip $program_name
