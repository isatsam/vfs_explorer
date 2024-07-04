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
path_to_wineprefix="`pwd`/wineprefix"

program_name="VFS_Explorer_windows_amd64"

WINEPREFIX="$path_to_wineprefix" wine $python_dir/Scripts/pip.exe install -U -r "`pwd`/requirements.txt"

if [ -d "dist/$program_name" ]; then
    rm -rf "dist/$program_name";
fi
if [ -d "dist/$program_name.zip" ]; then
    rm -rf "dist/$program_name.zip";
fi

echo "# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
# filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
# Set not needed items to zero 0.
filevers=(0, 1, 0, 0),
prodvers=(0, 1, 0, 0),
# Contains a bitmask that specifies the valid bits 'flags'r
mask=0x3f,
# Contains a bitmask that specifies the Boolean attributes of the file.
flags=0x0,
# The operating system for which this file was designed.
# 0x4 - NT and there is no need to change it.
OS=0x4,
# The general type of file.
# 0x1 - the file is an application.
fileType=0x1,
# The function of the file.
# 0x0 - the function is not defined for this fileType
subtype=0x0,
# Creation date and time stamp.
date=(0, 0)
),
  kids=[
StringFileInfo(
  [
  StringTable(
    u'040904B0',
    [StringStruct(u'CompanyName', u'hypnotiger'),
    StringStruct(u'FileDescription', u'Tool for VFS archives in IPL games'),
    StringStruct(u'FileVersion', u'1.0.0'),
    StringStruct(u'InternalName', u'VFS Explorer'),
    StringStruct(u'LegalCopyright', u'Licensed under GNU GPLv3'),
    StringStruct(u'OriginalFilename', u'VFS Explorer.exe'),
    StringStruct(u'ProductName', u'VFS Explorer'),
    StringStruct(u'ProductVersion', u'1.0.0')])
  ]),
  ]
)" > version_file.txt

WINEPREFIX="$path_to_wineprefix" wine $python_dir/Scripts/pyinstaller.exe \
vfs_explorer.py \
--name "$program_name" \
--contents-directory "programresources" \
--noconsole \
--icon build_scripts/icon.ico \
--version-file version_file.txt \
--add-data=COPYING:License \
--clean

cd dist/
7za a $program_name.zip $program_name
