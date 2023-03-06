import json
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import Gamer, Event


class EventTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games']

    # creates resources before a test is run
    def setUp(self):
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_event(self):
        """
        Ensure we can get an existing event.
        """
        # Seed the database with an event
        event = Event()
        event.game_id = 2
        event.description = "WOOOO"
        event.date = "2026-07-07"
        event.time = "08:00:00"
        event.save()

        # Initiate request and store response
        response = self.client.get(f"/events/{event.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["description"], "WOOOO")
        self.assertEqual(json_response["date"], "2026-07-07")
        self.assertEqual(json_response["time"], "08:00:00")
