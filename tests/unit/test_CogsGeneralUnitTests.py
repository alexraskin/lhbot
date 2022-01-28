from asyncio import Future
from asyncio.windows_events import NULL
from cgi import test
from lib2to3.pgen2.token import EQUAL
import unittest
from unittest import mock
import unittest.mock

from unittest.mock import AsyncMock, MagicMock, Mock, PropertyMock, create_autospec, patch

import discord
from discord.ext.commands import Context
from discord.message import Message

import sys
sys.path.append("../../cogs")

from general import info_execute, get_year_string, ping_execute, on_message_execute

class CogsGeneralTests(unittest.IsolatedAsyncioTestCase):
    
    botPrefix = "!"

    @patch.object(Context, 'send')
    async def test_shouldReturnInfo_whenInfoCommandCalled(self, mocked_context):
        """
        This test tests the Info command from the General Cog

        :mock Context: Discord context mocked send command
        :param mocked_content: mocked content to pass into general as ctx param
        """
        print("Running test_shouldReturnInfo_whenInfoCommandCalled")
        await info_execute(mocked_context)

        mocked_context.send.assert_called_once()

        self.assertEqual("Bot Information", mocked_context.send.call_args_list[0][1]['embed'].author.name)
        self.assertEqual("reinfrog#1738", mocked_context.send.call_args_list[0][1]['embed'].fields[0].value)
        self.assertEqual("Owner:", mocked_context.send.call_args_list[0][1]['embed'].fields[0].name)

        self.assertEqual(self.botPrefix, mocked_context.send.call_args_list[0][1]['embed'].fields[1].value)
        self.assertEqual("Prefix:", mocked_context.send.call_args_list[0][1]['embed'].fields[1].name)

        self.assertEqual("Python Version:", mocked_context.send.call_args_list[0][1]['embed'].fields[2].name)

        self.assertEqual("https://github.com/alexraskin/lhbot", mocked_context.send.call_args_list[0][1]['embed'].fields[3].value)
        self.assertEqual("URL:", mocked_context.send.call_args_list[0][1]['embed'].fields[3].name)
    
    def test_shouldReturnStringWithDate_whenGetYearStringCalled(self):
        """
        This test tests the get year string function

        expected start with: For your information, the year is 
        expected end with:  over!

        """
        print("Running test_shouldReturnStringWithDate_whenGetYearStringCalled")
        self.assertTrue(get_year_string().startswith("For your information, the year is "))
        self.assertTrue(get_year_string().endswith(" over!"))

    @patch.object(Context, 'send')
    async def test_shouldReturnPing_whenPingCommandCalled(self, mocked_context):
        """
        This test tests the Ping command from the General Cog

        :mock Context: Discord context mocked message.author
        :param mocked_content: mocked content to pass into general as ctx param
        """
        print("Running test_shouldReturnPing_whenPingCommandCalled")
 
        await ping_execute(mocked_context, 100)
  
        self.assertTrue(mocked_context.send.called)
        print(mocked_context.send.call_args_list[0][1]['embed'].footer.text)
        self.assertTrue(mocked_context.send.call_args_list[0][1]['embed'].footer.text.startswith("Requested by <AsyncMock name='send.message.author' "))
        
        self.assertEqual("🏓 Pong!", mocked_context.send.call_args_list[0][1]['embed'].title)
        self.assertEqual("The bot latency is 100ms.", mocked_context.send.call_args_list[0][1]['embed'].description)
        self.assertEqual(0x42F56C, mocked_context.send.call_args_list[0][1]['embed'].color.value)

    async def test_shouldCallMessage_whenOnMessageCommandCalled(self):
        """
        This test tests the Ping command from the General Cog

        :mock Context: Discord context mocked message.author
        :param mocked_content: mocked content to pass into general as ctx param
        """
        pass
        """ print("Running test_shouldCallMessage_whenOnMessageCommandCalled")
        mocked_message = AsyncMock()
        mocked_message.content = Mock(return_value='hi')
        mocked_message.channel.send = Mock(return_value=True)
        mocked_message.author.bot = Mock(return_value=False)
        print(mocked_message.content())
        await on_message_execute(mocked_message)

        print(mocked_message.channel.send.called) """

