
CREATE TABLE IF NOT EXISTS Roles (
    role_id INTEGER PRIMARY KEY,
    title varchar(255) NOT NULL
);

INSERT into Roles(title) VALUES('Administrateur');
INSERT into Roles(title) VALUES('Utilisateur');

CREATE Table IF NOT EXISTS Users_Role (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    role_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES regularsUsers(user_id),
    FOREIGN KEY(role_id) REFERENCES Roles(role_id)
);