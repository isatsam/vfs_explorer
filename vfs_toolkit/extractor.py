from PySide6.QtWidgets import QFileDialog, QMessageBox, QCheckBox
from PySide6.QtCore import QFileInfo
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
    def extractSelected(cls, extract_files, ui_obj):
        try:
            target_dir_info = QFileInfo(cls.spawnTargetPathPrompt(ui_obj) + '/')
            target_path = target_dir_info.absolutePath()
        except NotADirectoryError as e:
            print(e)
            return

        extract_objects = []
        for file_entry in extract_files:
            candidates = ui_obj.archive.root.search(file_entry.text(0)).values()
            for candidate in candidates:
                if cls.get_embed_file_vfs_path(candidate, file_entry, ui_obj):
                    extract_objects.append(candidate)

        multiple_files = len(extract_objects) > 1
        user_response = None
        apply_all_selected = False
        successfully_extracted_filenames = []
        for obj in extract_objects:
            target_filepath = os.path.join(target_path, obj.name)
            if os.path.isfile(target_filepath):
                if not apply_all_selected:
                    display_path = os.path.basename(target_path)
                    user_response, apply_all_selected = cls.overwriteFilePrompt(obj.name, display_path, multiple_files)

                match user_response:
                    case 16384:     # Yes, overwrite
                        pass
                    case 4194304:   # User cancelled, escape the loop
                        break
                    case _:         # No, don't overwrite this file (go back to the loop)
                        continue

            obj.extract(out_path=target_path)
            successfully_extracted_filenames.append(obj.name)
            print(f'Extracted {obj.name} to {target_path}')

        return successfully_extracted_filenames, target_path

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
        print(response)
        if apply_to_all:
            apply_all_select = apply_to_all.isChecked()
        else:
            apply_all_select = False

        return response, apply_all_select
