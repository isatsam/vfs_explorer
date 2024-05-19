#!/bin/bash
# Script for building Linux binaries on Linux.
#
# Additionally, this script uses py7zip to automatically package the produced
# folder into a .tar.gz archive. You can usually get py7zip from your
# distro's repositories. If you don't need that functionality,
# comment out the last two lines of the script.
source ".venv/bin/activate"

program_name="VFS_Explorer_linux_amd64"

if [ -d "dist/$program_name" ]; then
    rm -rf "dist/$program_name";
fi
if [ -d "dist/$program_name.zip" ]; then
    rm -rf "dist/$program_name.zip";
fi

pyinstaller \
vfs_explorer.py \
--name "$program_name" \
--contents-directory "programresources" \
--noconsole \
--add-data=COPYING:License


cd dist/
tar czf $program_name.tar.gz $program_name/*
