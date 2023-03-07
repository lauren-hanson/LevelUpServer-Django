"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View
from levelupreports.views.helpers import dict_fetch_all


class UserEventList(View):

    def get(self, request):
        # establish a connection to the database
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
            SELECT
                event.description, 
                event.date, 
                event.time,
                event.game_id,
                game.gamer_id, 
                game.title,
                user.first_name || ' ' || user.last_name as full_name
            FROM levelupapi_event event
                JOIN levelupapi_game game ON event.game_id = game.id
                JOIN auth_user user ON gamer.id = user.id
                JOIN levelupapi_eventgamer eventgamer ON event.id = eventgamer.event_id 
                JOIN levelupapi_gamer gamer ON eventgamer.gamer_id = gamer.id 
            """)

            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each gamer.
            # This will be the structure of the games_by_user list:
            #
            # [
            # {
            #     "gamer_id": 1,
            #     "full_name": "Molly Ringwald",
            #     "events": [
            #     {
            #         "id": 5,
            #         "date": "2020-12-23",
            #         "time": "19:00",
            #         "game_name": "Fortress America"
            #     }
            #     ]
            # }
            # ]

            events_by_user = []

            for row in dataset:
                # TODO: Create a dictionary called game that includes
                # the name, description, number_of_players, maker,
                # game_type_id, and skill_level from the row dictionary
                event = {
                    'description': row['description'],
                    'date': row['date'],
                    'time': row['time'], 
                    'game': row['game_id']
                }

                # See if the gamer has been added to the games_by_user list already
                user_dict = None
                for user_event in events_by_user:
                    if user_event['gamer_id'] == row['gamer_id']:
                        user_dict = user_event

                if user_dict:
                    # If the user_dict is already in the games_by_user list, append the game to the games list
                    user_dict['events'].append(event)
                else:
                    # If the user is not on the games_by_user list, create and add the user to the list
                    events_by_user.append({
                        "gamer_id": row['gamer_id'],
                        "full_name": row['full_name'],
                        "events": [event]
                    })

        # The template string must match the file name of the html template
        template = 'users/list_with_events.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "userevent_list": events_by_user
        }

        return render(request, template, context)
