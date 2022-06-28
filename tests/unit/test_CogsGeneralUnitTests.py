import sys
import unittest
import unittest.mock
from unittest.mock import AsyncMock, patch

from discord.ext.commands import Context

from bot.cogs.general import (get_year_string, info_execute,
                              on_message_execute, ping_execute,
                              shatter_execute)


class ChannelTestClass:
    def send():
        pass


class AuthorTestClass:
    bot = None


class MessageTestClass:
    channel = None
    content = None
    author = None


class CogsGeneralTests(unittest.IsolatedAsyncioTestCase):

    botPrefix = "!"

    @patch.object(Context, "send")
    async def test_shouldReturnInfo_whenInfoCommandCalled(self, mocked_context):
        """
        This test tests the Info command from the General Cog

        :mock Context: Discord context mocked send command
        :param mocked_content: mocked content to pass into general as ctx param
        """
        print("Running test_shouldReturnInfo_whenInfoCommandCalled")
        # arrange
        # act
        await info_execute(mocked_context)

        # assert
        mocked_context.send.assert_called_once()

        self.assertEqual(
            "Bot Information",
            mocked_context.send.call_args_list[0][1]["embed"].author.name,
        )
        self.assertEqual(
            "reinfrog#1738",
            mocked_context.send.call_args_list[0][1]["embed"].fields[0].value,
        )
        self.assertEqual(
            "Owner:", mocked_context.send.call_args_list[0][1]["embed"].fields[0].name
        )

        self.assertEqual(
            self.botPrefix,
            mocked_context.send.call_args_list[0][1]["embed"].fields[1].value,
        )
        self.assertEqual(
            "Prefix:", mocked_context.send.call_args_list[0][1]["embed"].fields[1].name
        )

        self.assertEqual(
            "Python Version:",
            mocked_context.send.call_args_list[0][1]["embed"].fields[2].name,
        )

        self.assertEqual(
            "https://github.com/alexraskin/lhbot",
            mocked_context.send.call_args_list[0][1]["embed"].fields[3].value,
        )
        self.assertEqual(
            "URL:", mocked_context.send.call_args_list[0][1]["embed"].fields[3].name
        )

    def test_shouldReturnStringWithDate_whenGetYearStringCalled(self):
        """
        This test tests the get year string function

        expected start with: For your information, the year is
        expected end with:  over!

        """
        print("Running test_shouldReturnStringWithDate_whenGetYearStringCalled")
        # arrange
        # act
        # assert
        self.assertTrue(
            get_year_string().startswith("For your information, the year is ")
        )
        self.assertTrue(get_year_string().endswith(" over!"))

    @patch.object(Context, "send")
    async def test_shouldReturnPing_whenPingCommandCalled(self, mocked_context):
        """
        This test tests the Ping command from the General Cog

        :mock Context: Discord context mocked message.author
        :param mocked_content: mocked content to pass into general as ctx param
        """
        print("Running test_shouldReturnPing_whenPingCommandCalled")
        # arrange
        # act
        await ping_execute(mocked_context, 100)
        # assert
        self.assertTrue(mocked_context.send.called)
        self.assertTrue(
            mocked_context.send.call_args_list[0][1]["embed"].footer.text.startswith(
                "Requested by <AsyncMock name='send.message.author' "
            )
        )

        self.assertEqual(
            "🏓 Pong!", mocked_context.send.call_args_list[0][1]["embed"].title
        )
        self.assertEqual(
            "The bot latency is 100ms.",
            mocked_context.send.call_args_list[0][1]["embed"].description,
        )
        self.assertEqual(
            0x42F56C, mocked_context.send.call_args_list[0][1]["embed"].color.value
        )

    @patch.object(ChannelTestClass, "send")
    async def test_shouldCallMessage_whenOnMessageCommandCalled(self, mocked_channel):
        """
        This test tests the Ping command from the General Cog

        :mock Context: Discord context mocked message.author
        :param mocked_content: mocked content to pass into general as ctx param
        """
        print("Running test_shouldCallMessage_whenOnMessageCommandCalled")
        # arrange
        mocked_channel = AsyncMock(mocked_channel)
        mocked_channel.send = AsyncMock(return_value=True)
        message = MessageTestClass()

        author = AuthorTestClass()
        author.bot = False

        message.author = author
        message.channel = mocked_channel
        # act
        message.content = "hi lhbot"
        await on_message_execute(message)
        # assert
        self.assertTrue(mocked_channel.send.called)
        self.assertEqual("hello", mocked_channel.send.call_args_list[0][0][0])

        mocked_channel.reset_mock()

        message.content = "you wanna fight, lhbot?"
        await on_message_execute(message)

        self.assertTrue(mocked_channel.send.called)
        self.assertEqual(
            "bring it on pal (╯°□°）╯︵ ┻━┻", mocked_channel.send.call_args_list[0][0][0]
        )

        mocked_channel.reset_mock()

        message.content = "lhbot meow"
        await on_message_execute(message)

        self.assertTrue(mocked_channel.send.called)
        self.assertEqual("ฅ^•ﻌ•^ฅ", mocked_channel.send.call_args_list[0][0][0])

        mocked_channel.reset_mock()

        message.content = "lh what's the answer to life, the universe and everything"
        await on_message_execute(message)

        self.assertTrue(mocked_channel.send.called)
        self.assertEqual("42", mocked_channel.send.call_args_list[0][0][0])

    @patch.object(Context, "send")
    async def test_shouldReturnShatter_whenShatterCommandCalled(self, mocked_context):
        """
        This test tests the Ping command from the General Cog

        :mock Context: Discord context mocked message.author
        :param mocked_content: mocked content to pass into general as ctx param
        """
        print("Running test_shouldReturnShatter_whenShatterCommandCalled")
        # arrange
        # act
        await shatter_execute(mocked_context, "reinfrog")
        # assert
        self.assertTrue(mocked_context.send.called)
        self.assertTrue(
            mocked_context.send.call_args_list[0][1]["embed"].footer.text.startswith(
                "Requested by <AsyncMock name='send.message.author' "
            )
        )

        self.assertEqual(
            "Shatter!", mocked_context.send.call_args_list[0][1]["embed"].title
        )
        self.assertIsNotNone(
            mocked_context.send.call_args_list[0][1]["embed"].description
        )
        if len(mocked_context.send.call_args_list[0][1]["embed"].description) == len(
            "Your shatter hit reinfrog."
        ):
            self.assertEqual(
                "Your shatter hit reinfrog.",
                mocked_context.send.call_args_list[0][1]["embed"].description,
            )
        else:
            self.assertEqual(
                "Your shatter was blocked by reinfrog.",
                mocked_context.send.call_args_list[0][1]["embed"].description,
            )

        self.assertEqual(
            0x42F56C, mocked_context.send.call_args_list[0][1]["embed"].color.value
        )

        await shatter_execute(mocked_context, "")
        # assert
        self.assertTrue(mocked_context.send.called)
        self.assertEqual(
            "You shattered no one, so it missed. Your team is now flaming you, and the enemy mercy typed MTD.",
            mocked_context.send.call_args_list[1][0][0],
        )
