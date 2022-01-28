from asyncio.windows_events import NULL
from lib2to3.pgen2.token import EQUAL
import unittest
import unittest.mock

from unittest.mock import patch

import discord
from discord.ext.commands import Context

import sys
sys.path.append("../../cogs")

from general import info_Execute

class CogsGeneralTests(unittest.IsolatedAsyncioTestCase):
    
    botPrefix = "!"

    """
    This test tests the Info command from the General Cog

    :mock Context: Discord context mocked send command
    :param mocked_content: mocked content to pass into general as ctx param
    """
    @patch.object(Context, 'send')
    async def test_shouldReturnInfo_whenInfoCommandCalled(self, mocked_context):
        print("Running test_shouldReturnInfo_whenInfoCommandCalled")
        await info_Execute(mocked_context)

        mocked_context.send.assert_called_once()

        self.assertEqual("Bot Information", mocked_context.send.call_args_list[0][1]['embed'].author.name)
        self.assertEqual("reinfrog#1738", mocked_context.send.call_args_list[0][1]['embed'].fields[0].value)
        self.assertEqual("Owner:", mocked_context.send.call_args_list[0][1]['embed'].fields[0].name)

        self.assertEqual(self.botPrefix, mocked_context.send.call_args_list[0][1]['embed'].fields[1].value)
        self.assertEqual("Prefix:", mocked_context.send.call_args_list[0][1]['embed'].fields[1].name)

        self.assertEqual("Python Version:", mocked_context.send.call_args_list[0][1]['embed'].fields[2].name)

        self.assertEqual("https://github.com/alexraskin/lhbot", mocked_context.send.call_args_list[0][1]['embed'].fields[3].value)
        self.assertEqual("URL:", mocked_context.send.call_args_list[0][1]['embed'].fields[3].name)



