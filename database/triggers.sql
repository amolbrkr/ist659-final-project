-- Drop the trigger if it already exists
IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'trg_UpdatePlayerStats')
    DROP TRIGGER trg_UpdatePlayerStats;
GO

-- Create the trigger
CREATE TRIGGER trg_UpdatePlayerStats
ON PlayerMoves
AFTER  UPDATE
AS
BEGIN
    -- Start a transaction
    BEGIN TRANSACTION;

    BEGIN TRY
        -- Declare a variable to hold the player_id
        DECLARE @player_id INT;

        IF EXISTS ( SELECT hostplayerId 
                    FROM lobbies as l
                    join inserted as i on i.lobby_id=l.id
                    )
        BEGIN
            SELECT @player_id = hostplayerID 
            FROM lobbies as l
            join inserted as i on i.lobby_id=l.id;
            -- Execute the updateStats stored procedure
            EXEC updateStats @player_id = @player_id;
        END

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
