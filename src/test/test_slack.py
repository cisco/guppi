import unittest
import plugins
import user_interfaces.SlackInterface as slack

class TestSlack(unittest.TestCase):
    def setUp(self):
        self.channel_name = 'testing'
        self.message = 'sent from unit test again'
        self.unique_message = 'this message was never sent by anyone'
        self.users = slack.user_info()
    
    def test_get_latest(self):
        # test get_latest function by checking the last 10 messages for a message that's never been sent
        # if the message isn't found, the test passses
        messages = slack.get_latest_messages(self.channel_name, self.users, 10)
        success = True
        for message in messages:
            if message['text'] == self.unique_message:
                success = False
        self.assertTrue(success)

    def test_post_get_latest(self):
        # test post_message by making a post and then get_latest by checking if the post is there
        # if the message is found, the test passes
        slack.post_message(self.channel_name, self.message)
        messages = slack.get_latest_messages(self.channel_name, self.users, 3)
        success = False
        for message in messages:
            if message['text'] == self.message:
                success = True
        self.assertTrue(success)