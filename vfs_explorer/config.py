""" Stores multiple global variables that need to be accessible through
    multiple classes (elements, child windows...) of VFS Explorer. """
import os


class Global:
    app = None
    translator = None
    settings = None
    softRestart = None
    path_to_languages = os.path.join(os.getcwd(), "vfs_explorer",
                            "languages")
