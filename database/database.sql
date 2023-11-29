if not exists(select * from sys.databases where name='poker')
	create database poker
GO

--use poker --WARNING: AZURE SQL SERVED DOES NOT SUPPORT USE
GO

--DOWN
if exists(select * from INFORMATION_SCHEMA.TABLE_CONSTRAINTS
	where CONSTRAINT_NAME = 'fk_playerMove_lobby_id')
	alter table playerMove drop constraint fk_playerMove_lobby_id

drop table if exists playerMove

if exists(select * from INFORMATION_SCHEMA.TABLE_CONSTRAINTS
	where CONSTRAINT_NAME = 'fk_cardsPlayed_lobby_id')
	alter table cardsPlayed drop constraint ffk_cardsPlayed_lobby_id
drop table if exists cardsPlayed


drop table if exists lobby

drop table if exists player

GO

--UP Metadata
create table player(
	id int identity not null,
    fName varchar(50) not null,
    lName varchar(50) not null,
    uName varchar(50) not null,
    pword varchar(56) not null,
    balance decimal,
    createdAt date not null,
    gamesPlayed int,
    turnsPlayed int,
    turnsPerGame decimal,
    wins int,
    defeats int,
    plays int,
    folds int,
    winRatio decimal,
    playRatio decimal,
    foldRation decimal,
	constraint pk_player_player_id primary key(id),
    constraint u_player_player_uName unique (uName)
	)

-- create table matches(
-- 	matches_matchID int identity not null,
--     matches_player1 varchar(50) not null,
--     matches_player2 varchar(50) not null,
--     matches_player1CardRank varchar(2), not null,
--     matches_player2CardRank varchar(2) not null,
--     matches_player1CardSuite varchar(10) not null,
--     matches_player2CardSuite varchar(10) not null,
--     matches_winner varchar(50),
--     matches_winAmt decimal,
-- 	constraint pk_matches_matchID primary key (matches_matchID)
-- 	)

create table lobby(
    id int,
    status varchar(50) not null,
    hostPlayerId int,
    turn int,
    constraint pk_lobby_id primary key (id)
)

create table cardsPlayed(
    id int identity not null,
    lobby_id int,
    lobby_turn int,
    card_rank varchar(2),
    card_suite varchar(10),
    entity varchar(6),
	constraint pk_cardsPlayed_id primary key(id),
	)

alter table cardsPlayed
	add constraint fk_cardsPlayed_lobby_id foreign key(lobby_id)
	references lobby(id)

-- create table playerMatches(
--     playerMatches_matchID int not null,
--     playerMatches_playerID int not null,
--     playerMatches_opponentID int not null,
--     playerMatches_lobbyID varchar(255) not null,
--     playerMatches_cardRank varchar(2) not null,
--     playerMatches_cardSuite varchar(10) not null,
-- 	constraint pk_playerMatches_playerMatches_matchID primary key (playerMatches_matchID)
-- 	)

-- alter table playerMatches
-- 	add constraint fk_playerMatches_playerMatches_matchID foreign key(playerMatches_matchID)
-- 	references matches(matches_matchID)

create table playerMove(
    id int not null,
    lobby_id int,
    lobby_turn int,
    move_type varchar(4),
    amount decimal,
    winner varchar(6),
    move_time date,
	constraint pk_playerMove_id primary key (id)
	)

alter table playerMove
	add constraint fk_playerMove_lobby_id foreign key(lobby_id)
	references lobby(id)

GO
--UP Data

GO
--VERIFY
