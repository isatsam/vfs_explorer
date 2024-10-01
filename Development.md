# Setting up the environment
VFS Explorer requires `git` and Python 3.12 installed and available in PATH.

1. Clone the repository (`git clone https://github.com/isatsam/vfs_explorer.git`)
2. Move into the new directory: `cd vfs_explorer`
3. Create and activate a virtual environment: `python -m venv venv`, then source it:
   - for Unix-based systems `source ./venv/bin/activate`
   - for Windows on PowerShell: `venv\Scripts\Activate.ps1`
   - for Windows with cmd.exe: `venv\Scripts\activate.bat`
5. Install the required packages: `pip install -r requirements.txt`
6. Run: `python vfs_explorer.py`. Or, optionally, specify a path to a VFS archive right-away: `python vfs_explorer.py /path/to/Archive.vfs`

# Building
VFS Explorer is built using [PyInstaller](https://pyinstaller.org/en/stable/) and the [build.spec](./vfs_explorer/build/build.spec) file.

To generate a binary file for your system, use: `pyinstaller ./build/build.spec`

For developers on Linux trying to generate a Windows binary, Wine can be used for this purpose, and [this tutorial](https://www.makeworld.space/2021/10/linux-wine-pyinstaller.html) by makeworld.space has proven working for VFS Explorer. In short:
1. Download latest Python release for Windows from python.org
2. Run the installer through `wine`. Check the "install in PATH" box. You can additionally change Python directory to something more convenient
3. Use your wine's new Python installation to install requirements through pip, then to run pyinstaller with the provided .spec file (the commands are the same, you just need to specify `wine C:\\path\\to\\python` in the beginning)

We additionally should try to keep (build_macos.spec)[./vfs_explorer/build/build_macos.spec] up-to-date, even though we don't currently use it or provide MacOS builds; this lack of support comes from Apple's draconian fees for the independent developer account, which is mandatory for certifying applications and making them easy to run on any MacOS system. If this is something you believe you can assist the project with, please open an issue.

# Localization
VFS Explorer has support for shipping multiple languages, and, if there's a correct translation available, it should be able to automatically set the language based off
the user's settings. It is also possible to manually set a language via "Preferences" > "Language", which will take priority over automatic detection. For making VFS Explorer available in your language, see [Translating](#Translating)

## Translating
We rely on Qt's [internalization system](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/translations.html) in VFS Explorer. In particular:
  - All strings visible in the GUI must be wrapped in `tr()` or `self.tr()`.
  - QT Linguist tool is used for creating the `.qm` language files.

QT Linguist requires a `.ts` file containing all strings in the app to create a `.qm` file for a language. To (re)generate a `.ts` file, run:
```sh
pyside6-lupdate vfs_explorer/* -ts languages/ts/LanguageName.ts
```
After that, launch QT Linguist with `pyside6-linguist` and open the generated .ts file there. Once you finish providing the translated equivalents of
the strings in the .ts file, click on "File" > "Release as..." and place the new .qm file in languages/ directory.

If your system language corresponds to the language you just added to the app, your development copy of VFS Explorer should now pick it up automatically. If it doesn't,
please run: `python languages/detect.py` and rename your `.ts` and `.qm` files to the output of that command.

Check that the new language is also present in the list in "Preferences" > "Languages", then manually test the app to ensure everything looks and reads right.

Please submit your translation as a separate PR from any code changes you might add.

# Github workflows
We use Actions to generate dev builds of VFS Explorer.
TODO: We also want to use them for automatic testing!


# To-do list
- [X] Provide pre-built binaries (Windows and Linux)
    - ~~[ ] MacOS binaries~~
- [ ] "Extract as" button, converting files to more common formats (for ex. a .tga named .tex -> .png)
- [ ] File information layout
  - [ ] Identify file types with magic
  - [ ] Wrap around libmagic to identify Pathologic-specific file formats? (LSH, main.dat and such)
- [ ] Preview layout
  - [ ] Preview text files
  - [ ] Preview images
