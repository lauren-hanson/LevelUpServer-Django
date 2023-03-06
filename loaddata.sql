
SELECT
    game.title, 
    game.description, 
    game.min_player, 
    game.max_player, 
    game.game_type_id, 
    game.gamer_id,
    user.first_name || ' ' || user.last_name as full_name
FROM levelupapi_game as game
JOIN levelupapi_gamer as gamer ON game.gamer_id = levelupapi_game.id
JOIN auth_user as user ON gamer.user_id = user.id