if not exists(select * from sys.databases where name='poker')
	create database poker
GO

--use poker --WARNING: AZURE SQL SERVED DOES NOT SUPPORT USE
GO

--DOWN
if exists(select * from INFORMATION_SCHEMA.TABLE_CONSTRAINTS
	where CONSTRAINT_NAME = 'fk_playersMove_lobby_id')
	alter table playerMoves drop constraint fk_playerMove_lobby_id

drop table if exists playerMoves

if exists(select * from INFORMATION_SCHEMA.TABLE_CONSTRAINTS
	where CONSTRAINT_NAME = 'fk_cardsPlayed_lobby_id')
	alter table cardsPlayed drop constraint fk_cardsPlayed_lobby_id
drop table if exists cardsPlayed

if exists(select * from INFORMATION_SCHEMA.TABLE_CONSTRAINTS
	where CONSTRAINT_NAME = 'fk_lobbies_player_id')
	alter table lobbies drop constraint fk_lobbies_player_id

drop table if exists lobbies

drop table if exists players

GO

--UP Metadata
CREATE TABLE players (
    id INT PRIMARY KEY IDENTITY,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    username VARCHAR(50) UNIQUE,
    passwordhash VARCHAR(100),
    balance FLOAT DEFAULT 100,
    createdat DATETIME DEFAULT GETDATE(),

    gamesplayed INT DEFAULT 0,
    turnsplayed INT DEFAULT 0,
    wins INT DEFAULT 0,
    defeats INT DEFAULT 0,
    plays INT DEFAULT 0,
    folds INT DEFAULT 0,

);



CREATE TABLE lobbies (
    id INT PRIMARY KEY IDENTITY,
    status VARCHAR(50) DEFAULT 'WAITING' NOT NULL,
    hostplayerId INT NOT NULL,
    turn INT DEFAULT 0 NOT NULL
)
alter table lobbies
	add constraint fk_lobbies_player_id foreign key(hostplayerId)
	references players(id)

CREATE TABLE CardsPlayed (
    id INT PRIMARY KEY IDENTITY,
    lobby_id INT NOT NULL,
    lobby_turn INT NOT NULL,
    card_rank VARCHAR(2) NOT NULL,
    card_suite VARCHAR(10) NOT NULL,
    entity VARCHAR(6) NOT NULL,
	)
alter table cardsPlayed
	add constraint fk_cardsPlayed_lobby_id foreign key(lobby_id)
	references lobbies(id)


CREATE TABLE playerMoves (
    id INT PRIMARY KEY IDENTITY,
    lobby_id INT NOT NULL ,
    lobby_turn INT NOT NULL DEFAULT 1,
    move_type VARCHAR(4) NOT NULL,
    amount FLOAT NOT NULL,
    winner VARCHAR(6) NOT NULL DEFAULT 'none',
    move_time DATETIME DEFAULT GETDATE()
)

alter table playerMoves
	add constraint fk_playerMove_lobby_id foreign key(lobby_id)
	references lobbies(id)

GO
--UP sample Data
INSERT INTO players (firstname, lastname, username, passwordhash)
VALUES ('John', 'Doe', 'johndoe', 'hash1234');

INSERT INTO players (firstname, lastname, username, passwordhash)
VALUES ('Alice', 'Smith', 'alicesmith', 'hash5678');

INSERT INTO players (firstname, lastname, username, passwordhash)
VALUES ('Bob', 'Johnson', 'bobjohnson', 'hash91011');

GO
--VERIFY
select * from players


select * from lobbies

select * from CardsPlayed

select * from playerMoves

