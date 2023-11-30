IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'updateStats')
    DROP PROCEDURE updateStats;
GO

CREATE PROCEDURE updateStats 
    @player_id INT
AS
BEGIN
    -- Start a transaction
    BEGIN TRANSACTION;

    BEGIN TRY
        -- Declare variables to hold intermediate results
        DECLARE @gamesPlayed INT, @turnsPlayed INT, @wins INT, @defeats INT, @plays INT, @folds INT

        -- Calculate games played
        SELECT @gamesPlayed = COUNT(id)
        FROM Lobbies 
        WHERE hostPlayerId = @player_id;

        -- Calculate turns played
        SELECT @turnsPlayed = SUM(turn) 
        FROM Lobbies
        WHERE hostPlayerId = @player_id;

        -- Calculate wins
        SELECT @wins = COUNT(pm.id) 
        FROM PlayerMoves as pm
        JOIN Lobbies as l ON pm.lobby_id = l.id
        JOIN Players as p ON l.hostPlayerId = p.id
        WHERE p.id = @player_id AND pm.winner = 'Player';
     
        -- Calculate defeats
        SELECT @defeats = COUNT(pm.id) 
        FROM PlayerMoves as pm
        JOIN Lobbies as l ON pm.lobby_id = l.id
        JOIN Players as p ON l.hostPlayerId = p.id
        WHERE p.id = @player_id AND pm.winner = 'Dealer';

        -- Calculate plays
        SELECT @plays = COUNT(pm.id) 
        FROM PlayerMoves as pm
        JOIN Lobbies as l ON pm.lobby_id = l.id
        JOIN Players as p ON l.hostPlayerId = p.id
        WHERE p.id = @player_id AND move_type = 'play';

        -- Calculate folds
        SELECT @folds = COUNT(pm.id) 
        FROM PlayerMoves as pm
        JOIN Lobbies as l ON pm.lobby_id = l.id
        JOIN Players as p ON l.hostPlayerId = p.id
        WHERE p.id = @player_id AND move_type = 'fold';

        -- Update player stats
        UPDATE Players
        SET 
            gamesplayed = @gamesPlayed,
            turnsplayed = @turnsPlayed,
            wins = @wins,
            defeats =  @defeats,
            plays = @plays,
            folds = @folds
        WHERE id = @player_id;

        -- Commit the transaction
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        -- Rollback the transaction in case of an error
        ROLLBACK TRANSACTION;
        -- You can log the error here
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR (@ErrorMessage, 16, 1);
    END CATCH
END;
GO

GO

EXEC updateStats @player_id = 2;


go

select * from players

 