import sys
import unittest
import unittest.mock
from unittest.mock import AsyncMock, patch

from discord.ext.commands import Context

sys.path.append("../bot/cogs")
from lhcloudy import one_frame_execute


class ChannelTestClass:
    def send():
        pass


class AuthorTestClass:
    bot = None


class MessageTestClass:
    channel = None
    content = None
    author = None


class CogsLhCloudyTests(unittest.IsolatedAsyncioTestCase):

    botPrefix = "!"

    @patch.object(Context, "send")
    async def test_shouldReturnOneFrame_when1FrameCommandCalled(self, mocked_context):
        """
        The test_shouldReturnOneFrame_when1FrameCommandCalled function specifically tests the one_frame_execute function.

        :param self: Used to access the class variables and methods.
        :param mocked_context: Used to mock the context of the command.
        :return: the following:.
        :doc-author: Trelent
        """
        print("Running test_shouldReturnOneFrame_when1FrameCommandCalled")

        await one_frame_execute(mocked_context)

        self.assertTrue(mocked_context.send.called)

        self.assertEqual(
            "https://www.twitch.tv/lhcloudy27/clip/AbstruseKindRuffFutureMan-dLWae-FGvNag2jtK",
            mocked_context.send.call_args_list[0][0][0],
        )
