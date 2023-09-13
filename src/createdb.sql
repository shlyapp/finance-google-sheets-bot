CREATE TABLE file (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    folder INTEGER,
    name TEXT,
    FOREIGN KEY(folder) REFERENCES folder(id)
);

CREATE TABLE folder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    parent INTEGER,
    FOREIGN KEY(parent) REFERENCES folder(id)
);


