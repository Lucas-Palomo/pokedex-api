CREATE TABLE IF NOT EXISTS pokemon
(
    id          UUID UNIQUE PRIMARY KEY,
    external_id INT UNIQUE CHECK ( external_id > 0),
    name        VARCHAR,
    weight      INT,
    height      INT,
    types       VARCHAR[],
    hp          INT,
    speed       INT,
    attack      INT,
    defense     INT,
    images      VARCHAR[]
);