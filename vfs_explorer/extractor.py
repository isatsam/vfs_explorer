from PySide6.QtWidgets import QFileDialog, QMessageBox, QCheckBox
from PySide6.QtCore import QFileInfo
from .vfs_tree import VfsTreeItemFile, VfsTreeItemDirectory
import os.path


class Extractor:
    @classmethod
    def get_embed_file_vfs_path(cls, embed_file, file_tree_item, ui_obj):
        if not embed_file.parent.parent and file_tree_item.parent() == ui_obj.treeItems[0]:
            """ Check for files in top-level directories/trees """
            return True

        next_tree_parent = file_tree_item.parent()
        next_embed_parent = embed_file.parent
        while next_tree_parent and next_embed_parent:
            if next_tree_parent.text(0) != next_embed_parent.name:
                return False
            else:
                next_tree_parent = next_tree_parent.parent()
                next_embed_parent = next_embed_parent.parent

        return True

    @classmethod
    def extractSelectedFiles(cls, ui_obj, dry_run=False):
        return cls.extractFiles(files=ui_obj.tree.selectedItems(), ui_obj=ui_obj, dry_run=dry_run)

    @classmethod
    def extractFiles(cls, files: list, ui_obj, dry_run=False):
        try:
            target_dir_info = QFileInfo(cls.spawnTargetPathPrompt(ui_obj) + '/')
            starter_target_path = target_dir_info.absolutePath()
        except NotADirectoryError as e:
            print(e)
            return None, None

        print(f"Dry run: {dry_run}")

        def traverse_directory(directory, list_of_files=[]):
            for i in range(directory.childCount()):
                if type(directory) is VfsTreeItemFile:
                    list_of_files.append(directory.child(i).embeddedFile)
                else:
                    list_of_files = traverse_directory(directory.child(i), list_of_files)
            return list_of_files

        extract_files = []
        for item in files:
            if type(item) is VfsTreeItemDirectory:
                extract_files += item.getEmbeddedFiles()
            else:
                extract_files.append(item.embeddedFile)

        """ Hacky way to figure out if we need to create any subdirectories on the drive. """
        # TODO: Currently we're creating subdirectories relatively to the root of the VFS. If we don't start
        #   extracting at the root but in a deeper level subdirectory, we should be creating subdirectories
        #   relative to that. Might be easier if we implement EmbeddedFile to know its full path first?
        map_of_directories = {'': []}
        for file in extract_files:
            if file.parent.parent is None:
                map_of_directories[''].append(file)
            else:
                parent = file.parent
                new_path = []
                while parent.parent is not None:
                    new_path.append(parent.name)
                    new_path_dict_key = "/".join(new_path)
                    parent = parent.parent
                if new_path_dict_key not in map_of_directories.keys():
                    map_of_directories[new_path_dict_key] = []
                map_of_directories[new_path_dict_key].append(file)

        multiple_files = len(extract_files) > 1
        user_response = None
        apply_all_selected = False
        successfully_extracted_filenames = []
        for path in map_of_directories:
            """ Try to create a subdirectory for files not from the root of the tree, if that is needed """
            target_dir = os.path.join(starter_target_path, path)
            if not os.path.exists(target_dir):
                if not dry_run:
                    os.mkdir(target_dir)
                print(f"Created directory {target_dir}")

            for obj in map_of_directories[path]:
                """ Check if file already exists """
                target_filepath = os.path.join(target_dir, obj.name)
                if os.path.isfile(target_filepath):
                    if not apply_all_selected:
                        display_path = os.path.basename(starter_target_path)
                        user_response, apply_all_selected = cls.overwriteFilePrompt(obj.name, display_path,
                                                                                    multiple_files)

                    match user_response:
                        case 16384:  # Yes, overwrite
                            pass
                        case 4194304:  # User cancelled, escape the loop
                            break
                        case _:  # No, don't overwrite this file (go back to the loop)
                            continue

                if not dry_run:
                    obj.extract(out_path=target_dir)

                if obj.name in successfully_extracted_filenames:
                    print(f"There was a double: {obj.name}")
                successfully_extracted_filenames.append(obj.name)

        print(f"Extracted {len(successfully_extracted_filenames)} file(s) to {starter_target_path}")
        return successfully_extracted_filenames, starter_target_path

    @classmethod
    def spawnTargetPathPrompt(cls, ui_obj):
        openDialog = QFileDialog(ui_obj)
        openDialog.setAcceptMode(QFileDialog.AcceptSave)
        openDialog.setViewMode(QFileDialog.Detail)
        openDialog.setOption(QFileDialog.DontUseNativeDialog)
        openDialog.setNameFilter('Extract to...')

        selected = openDialog.getExistingDirectory()
        if not os.path.exists(selected):
            raise NotADirectoryError('Path not selected or it doesn\'t exist')
        else:
            return selected

    @classmethod
    def overwriteFilePrompt(cls, filename, target_dir_name, are_multiple_files):
        prompt = QMessageBox()
        prompt.setText(f'File {filename} already exists in folder {target_dir_name}. Overwrite it?')

        yes_button = prompt.addButton(QMessageBox.StandardButton.Yes)
        yes_button.setText('Overwrite')
        no_button = prompt.addButton(QMessageBox.StandardButton.No)
        no_button.setText('Skip overwriting')
        prompt.setDefaultButton(no_button)
        prompt.addButton(QMessageBox.StandardButton.Cancel)

        if are_multiple_files:
            apply_to_all = QCheckBox()
            apply_to_all.setText('Apply to all')
            prompt.setCheckBox(apply_to_all)
        else:
            apply_to_all = None

        response = prompt.exec()
        print(f"User choice: {response}")
        if apply_to_all:
            apply_all_select = apply_to_all.isChecked()
        else:
            apply_all_select = False

        return response, apply_all_select
