from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, reply_keyboard
from database import db
from menu.item import Item

from typing import List, NamedTuple, Optional


class Category(NamedTuple):
    id: Optional[int]
    name: str
    parent_category_id: int


class CategoryMenu:
    def __init__(self):
        self._items = self._load_items()
        self._categories = self._load_categories()
        self._remove_button = KeyboardButton("Удалить")
        self._add_button = KeyboardButton("Добавить кнопку")

    def _load_items(self) -> List[Item]:
        items_db = db.fetchall(
                "item", "id name category_id".split()
                )
        items = []
        for item in items_db:
            items.append(Item(
                id = int(item["id"]),
                name = str(item["name"]),
                category_id = int(item["category_id"])
                ))
        return items

    def _load_categories(self) -> List[Category]:
        categories_db = db.fetchall(
                "category", "id name parent_category_id".split()
                )
        categories = []
        for category in categories_db:
            categories.append(Category(
                id = int(category["id"]),
                name = str(category["name"]),
                parent_category_id=str(category["parent_category_id"])
                ))
        return categories

    def _get_category_elements(self, category_id: int):
        elements = []
        for category in self._categories:
            if int(category.parent_category_id) == int(category_id):
                elements.append(category)
        for item in self._items:
            if int(item.category_id) == int(category_id):
                elements.append(item)
        return elements

    def add_item_to_category(self, item: Item, category_id: int):
        for element in self._items:
            if element.name == item.name:
                return 

        db.insert("item", {
            "name": item.name,
            "category_id": category_id
            })
        self._items = self._load_items()

    def remove_item(self, item_id: int):
        db.delete("item", item_id)
        self._items = self._load_items()

    def add_category(self, category: Category):
        for element in self._categories:
            if element.name == category.name:
                return

        db.insert("category", {
            "name": category.name,
            "parent_category_id": category.parent_category_id
            })
        self._items = self._load_categories()

    def remove_category(self, category_id: int):
        for item in self._items:
            if int(item.category_id) == category_id:
                self.remove_item(item.id)
        db.delete("category", category_id)

    def get_category_id_by_name(self, category_name: str) -> int:
        for category in self._categories:
            if category.name == category_name:
                return category.id
        return -1

    def get_category_by_id(self, id: int) -> Category:
        for category in self._categories:
            if int(category.id) == id: 
                return category
        return None

    def get_category_menu(self, category_id: int):
        elements = self._get_category_elements(category_id)
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for element in elements:
            reply_keyboard.add(KeyboardButton(element.name), self._remove_button)
        reply_keyboard.add(self._add_button)
        return reply_keyboard

    def get_type_menu(self):
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for element in self._categories:
            if int(element.parent_category_id) == -1:
                reply_keyboard.add(KeyboardButton(element.name))
        return reply_keyboard
    
    

