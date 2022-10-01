CREATE TABLE clans (
    clan_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(32) NOT NULL,
    tag VARCHAR(8) NOT NULL,
    description TEXT,
    owner INT NOT NULL,
    join_method VARCHAR(64) NOT NULL,
    status VARCHAR(64) NOT NULL,
    updated_at DATETIME NOT NULL DEFAULT NOW(),
    created_at DATETIME NOT NULL DEFAULT NOW()
);