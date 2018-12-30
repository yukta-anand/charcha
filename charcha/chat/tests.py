from django.test import TestCase
from charcha.discussions.models import User
from charcha.team.models import Team, TeamMember, ADMIN, MEMBER

from .models import Channel, Message

class DiscussionTests(TestCase):
    def setUp(self):
        self._create_team()

    def _create_team(self):
        team = Team(name="test team")
        team.save()
        self.team = team

        ramesh = User.objects.create_user(
            username="ramesh", password="top_secret")
        amit = User.objects.create_user(
            username="amit", password="top_secret")
        swetha = User.objects.create_user(
            username="swetha", password="top_secret")

        self.ramesh = TeamMember(team=team, user=ramesh, role=ADMIN)
        self.ramesh.save()
        self.amit = TeamMember(team=team, user=amit, role=MEMBER)
        self.amit.save()
        self.swetha = TeamMember(team=team, user=swetha, role=MEMBER)
        self.swetha.save()

    def test_private_message(self):
        ramesh, amit, swetha = self.ramesh, self.amit, self.swetha

        self.assertTrue(not ramesh.get_messages_since(0))
        self.assertTrue(not amit.get_messages_since(0))

        self.ramesh.send_direct_message(self.amit, "Hi Amit!")
        self.ramesh.send_direct_message(self.amit, "How are you today?")

        self.assertEquals(len(ramesh.get_messages_since(0)), 2)
        self.assertEquals(len(amit.get_messages_since(0)), 2)
        self.assertEquals(len(swetha.get_messages_since(0)), 0)

        self.amit.send_direct_message(self.ramesh, "I am doing good. How about you?")

        self.assertEquals(len(ramesh.get_messages_since(0)), 3)
        self.assertEquals(len(ramesh.get_messages_since(2)), 1)
        self.assertEquals(len(amit.get_messages_since(2)), 1)
        self.assertEquals(len(swetha.get_messages_since(0)), 0)
