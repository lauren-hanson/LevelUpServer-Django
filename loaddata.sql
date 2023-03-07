SELECT
    event.description, 
    event.date, 
    event.time,
    event.game_id,
    game.gamer_id, 
    game.title as game_name,
    user.first_name || ' ' || user.last_name as full_name
FROM levelupapi_event event
    JOIN levelupapi_game game ON event.game_id = game.id
    JOIN auth_user user ON gamer.id = user.id
    JOIN levelupapi_eventgamer eventgamer ON event.id = eventgamer.event_id 
    JOIN levelupapi_gamer gamer ON eventgamer.gamer_id = gamer.id 