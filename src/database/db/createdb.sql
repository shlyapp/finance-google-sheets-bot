CREATE TABLE item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  category_id INTEGER,
  FOREIGN KEY(category_id) REFERENCES category(id)
);

CREATE TABLE category (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  parent_category_id INTEGER,
  FOREIGN KEY(parent_category_id) REFERENCES category(id)
);

INSERT INTO category(id, name, parent_category_id) VALUES
(0, "Расход", -1),
(1, "Доход", -1),
(2, "Сотрудники", 0),
(3, "Материалы", 0),
(4, "Продажа", 1);

INSERT INTO item(id, name, category_id) VALUES
(0, "Прочее", 0),
(1, "Прочее", 1),
(2, "Юрист", 2),
(3, "Адвокат", 2),
(4, "Дерево", 3),
(5, "Бетон", 3),
(6, "Ламинат", 4),
(7, "Паркет", 4);

