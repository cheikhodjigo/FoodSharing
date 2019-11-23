
CREATE TABLE IF NOT EXISTS Categories (
    categorie_id INTEGER PRIMARY KEY,
    categorie_title varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Offers (
    offer_id INTEGER PRIMARY KEY,
    offer_categorie_id INTEGER,
    offer_user_id INTEGER,
    offer_title varchar(255) NOT NULL,
    offer_description varchar(255) NOT NULL,
    offer_price varchar(255) NOT NULL,
    FOREIGN KEY(offer_categorie_id) REFERENCES Categories(categorie_id),
    FOREIGN KEY(offer_user_id) REFERENCES regularsUsers(user_id)
);