from typing import List, NamedTuple, Optional
from file import File
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, reply_keyboard

import db


class Folder(NamedTuple):
    id: Optional[int]
    name: str
    parent: int
    

class Filesystem:
    def __init__(self):
        self._folders = self._load_folders()
        self._files = self._load_files()
        self._add_button = KeyboardButton("Добавить элемент")
        self._delete_button = KeyboardButton("Удалить")


    def _load_folders(self) -> List[Folder]:
        folders_load = db.fetchall(
            "folder", "id name parent".split()
        )
        folders = []
        for folder in folders_load:
            folders.append(Folder(
                id = int(folder["id"]),
                name = folder["name"],
                parent = folder["parent"]
            ))
        return folders

    def _load_files(self) -> List[File]:
        files_load = db.fetchall(
            "file", "id name folder".split()
        )
        files = []
        for file in files_load:
            files.append(File(
                id = int(file["id"]),
                name = file["name"],
                folder = file["folder"]
                ))
        return files

    def add_folder(self, folder: Folder):
        db.insert("folder", {
            "name": folder.name,
            "parent": folder.parent
        })
    
    def add_file(self, folder_id: int, file: File):
        db.insert("file", {
            "name": file.name,
            "folder": folder_id
        })

    def get_folders(self):
        return self._folders

    def get_files(self, folder_id: int):
        files = []
        for file in self._files:
            if file.id == folder_id:
                files.append(file)

        return files

    def _get_folder_items(self, folder_id: int):
        items = []
        for folder in self._folders:
            if folder.parent == folder_id:
                items.append(folder)

        for file in self._files:
            if file.folder == folder_id:
                items.append(file)

        return items

    def get_id_by_name(self, name: str):
        for folder in self._folders:
            if folder.name == name:
                return folder.id
            for file in self.get_files(folder.id):
                if file.name == name:
                    return file.id
    
    def get_folder(self, name):
        for folder in self._folders:
            if folder.name == name:
                return folder

    def get_folder_by_id(self, id):
        for folder in self._folders:
            if folder.id == id:
                return folder
        return None

    def get_markup_keyboard(self, folder_id: int):
        items = self._get_folder_items(folder_id)
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for item in items:
            reply_keyboard.add(KeyboardButton(item.name), self._delete_button)
        reply_keyboard.add(self._add_button)
        return reply_keyboard




