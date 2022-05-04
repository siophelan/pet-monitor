DROP TABLE IF EXISTS species;
DROP TABLE IF EXISTS pet;
DROP TABLE IF EXISTS caregiver;
DROP TABLE IF EXISTS activity;
DROP TABLE IF EXISTS photo;
DROP TABLE IF EXISTS video;

CREATE TABLE species (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    species_type TEXT NOT NULL
);

CREATE TABLE pet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_name TEXT NOT NULL,
    birth_year INTEGER,
    species_ID INTEGER NOT NULL,
    FOREIGN KEY (species_ID) REFERENCES species (id)
);

CREATE TABLE caregiver (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone_num NUMERIC NOT NULL,
    email_address TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_date DATETIME NOT NULL,
    activity_time DATETIME NOT NULL,
    last_activity DATETIME
);

CREATE TABLE photo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    img_date DATETIME NOT NULL,
    img_timestamp TEXT NOT NULL,
    tag TEXT
);

CREATE TABLE video (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vid_date DATETIME NOT NULL,
    vid_timestamp TEXT NOT NULL,
    tag TEXT
);

CREATE TABLE pet_caregiver ( 
    pet_id INTEGER,
    caregiver_id INTEGER,
    FOREIGN KEY(pet_id) REFERENCES pet(id),
    FOREIGN KEY(caregiver_id) REFERENCES caregiver(id)
);

CREATE TABLE pet_activity (
    pet_id INTEGER,
    activity_id INTEGER,
    FOREIGN KEY(pet_id) REFERENCES pet(id),
    FOREIGN KEY(activity_id) REFERENCES activity(id)
);

CREATE TABLE pet_photo (
    pet_id INTEGER,
    photo_id INTEGER,
    FOREIGN KEY(pet_id) REFERENCES pet(id),
    FOREIGN KEY(photo_id) REFERENCES photo(id)
);

CREATE TABLE pet_video (
    pet_id INTEGER,
    video_id INTEGER,
    FOREIGN KEY(pet_id) REFERENCES pet(id),
    FOREIGN KEY(video_id) REFERENCES video(id)
);