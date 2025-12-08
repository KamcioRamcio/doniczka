-- schemat bazy

CREATE TABLE IF NOT EXISTS env_sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_pnt DATE NOT NULL,
    temperature FLOAT NOT NULL,
    pressure FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    light FLOAT NOT NULL,
    uv INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS moist_sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_pnt DATE NOT NULL,
    moisture FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS water_pump (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    water_time DATE NOT NULL
);
