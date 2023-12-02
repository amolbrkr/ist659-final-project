select  balance,
        createdat,
        gamesplayed,
        turnsplayed,
        wins,
        defeats,
        plays,
        folds
from players
where player id = @player_id
