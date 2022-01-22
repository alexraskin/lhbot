import itertools

from discord import Embed
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand, HelpCommand


class myHelpCommand(HelpCommand):
    def __init__(self, **options):
        """
        The __init__ function is used to initialize the class. It's called when an instance of a class is created, with the arguments that were passed to the class.

        :param self: Used to refer to the object itself.
        :param **options: Used to pass a dictionary of keyword arguments into the function.
        :return: the superclass of the class, which is the object class.
        :doc-author: Trelent
        """
        super().__init__(**options)
        self.paginator = None
        self.spacer = "\u1160"

    async def send_pages(self, header=False, footer=False):
        """
        The send_pages function specifically accomplishes two things:
            1. It sends the pages to the user.
            2. It adds a footer to each page, which contains information about how many pages there are and what commands can be used to get more information.

        :param self: Used to access the attributes and methods of the class in which it is used.
        :param header=False: Used to tell the send_pages function to not.
        :param footer=False: Used to remove the footer from the embed.
        :return: an Embed object.
        :doc-author: Trelent
        """
        destination = self.get_destination()
        embed = Embed(
            color=0x2ECC71
        )
        if header:
            embed.set_author(
                name=self.context.bot.description
            )
        for category, entries in self.paginator:
            embed.add_field(
                name=category,
                value=entries,
                inline=False
            )
        if footer:
            embed.set_footer(
                text='Use !help <command/category> for more information.'
            )
        await destination.send(embed=embed)

    async def send_bot_help(self, mapping):
        """
        The send_bot_help function specifically accomplishes two things:
            1. It creates a paginator with the help command's output.
            2. It adds an entry to the paginator for each cog, formatted as "Category Name:". This is done by grouping commands by their cog and then iterating over them.

        :param self: Used to access the bot's help command.
        :param mapping: Used to determine which commands to show.
        :return: a list of tuples.
        :doc-author: Trelent
        """
        ctx = self.context
        bot = ctx.bot

        def get_category(command):
            """
            The get_category function specifically returns the cog that a command belongs to.
            This is useful for commands that belong to more than one cog.

            :param command: Used to access the command that was called.
            :return: the cog of the command.
            :doc-author: Trelent
            """
            cog = command.cog
            return cog.qualified_name + ':' if cog is not None else 'Help:'

        filtered = await self.filter_commands(
            bot.commands,
            sort=True,
            key=get_category
        )
        to_iterate = itertools.groupby(filtered, key=get_category)
        for cog_name, command_grouper in to_iterate:
            cmds = sorted(command_grouper, key=lambda c: c.name)
            category = f'► {cog_name}'
            if len(cmds) == 1:
                entries = f'{self.spacer}{cmds[0].name} → {cmds[0].short_doc}'
            else:
                entries = ''
                while len(cmds) > 0:
                    entries += self.spacer
                    entries += ' | '.join([cmd.name for cmd in cmds[0:8]])
                    cmds = cmds[8:]
                    entries += '\n' if cmds else ''
            self.paginator.append((category, entries))
        await self.send_pages(header=True, footer=True)

    async def send_cog_help(self, cog):
        """
        The send_cog_help function is used to send the help command for a specific cog.
        It takes in the cog as an argument and then sends a paginated embed with all of the commands that are part of that cog.

        :param self: Used to access the bot object.
        :param cog: Used to access the cog object.
        :return: a Paginator.
        :doc-author: Trelent
        """
        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        if not filtered:
            await self.context.send(
                'No public commands in this cog. Try again with lhbot helpall.'
            )
            return
        category = f'▼ {cog.qualified_name}'
        entries = '\n'.join(
            self.spacer +
            f'**{command.name}** → {command.short_doc or command.description}'
            for command in filtered
        )
        self.paginator.append((category, entries))
        await self.send_pages(footer=True)

    async def send_group_help(self, group):
        """
        The send_group_help function is used to send the help command for a specific group.
        It takes in the group as an argument and then sends a message containing all of the commands that are part of that group.

        :param self: Used to access the bot's attributes, such as its database.
        :param group: Used to get the name of the group, and it's description.
        :return: a string.
        :doc-author: Trelent
        """
        filtered = await self.filter_commands(group.commands, sort=True)
        if not filtered:
            await self.context.send(
                'No public commands in group. Try again with !help helpall.'
            )
            return
        category = f'**{group.name}** - {group.description or group.short_doc}'
        entries = '\n'.join(
            self.spacer + f'**{command.name}** → {command.short_doc}'
            for command in filtered
        )
        self.paginator.append((category, entries))
        await self.send_pages(footer=True)

    async def send_command_help(self, command):
        """
        The send_command_help function specifically accomplishes two things:
        1. It adds the command signature to the paginator, along with its help text (if it exists).
        2. It also checks if there are any subcommands that need to be displayed and calls send_command_help recursively on each of them.

        :param self: Used to access the bot's attributes and methods.
        :param command: Used to get the name of the command.
        :return: the signature and helptext of the command.
        :doc-author: Trelent
        """
        signature = self.get_command_signature(command)
        helptext = command.help or command.description or 'No help Text'
        self.paginator.append(
            (signature, helptext)
        )
        await self.send_pages()

    async def prepare_help_command(self, ctx, command=None):
        """
        The prepare_help_command function is used to prepare the help command for use.
        It's a bit complicated, but it allows us to take commands that have been passed in as arguments and also
        to format them correctly.

        :param self: Used to store the context of the command.
        :param ctx: Used to get the current context of where the command was called.
        :param command=None: Used to check if the user wants to see general help or help for a specific command.
        :return: a list of strings that will be used as the help command description.
        :doc-author: Trelent
        """
        self.paginator = []
        await super().prepare_help_command(ctx, command)


class Help(commands.Cog):
    def __init__(self, client):
        """
        The __init__ function is the constructor for a class. It is called whenever an object of that class is instantiated.
        The __init__ function can take arguments (as shown), but its first parameter must be 'self'. The self-parameter refers to the object being created, and it's used to access variables that belong to the object.

        :param self: Used to refer to the bot itself.
        :param client: Used to access the client's functionality.
        :return: a client object from the discord.
        :doc-author: Trelent
        """
        self.client = client
        self.client.help_command = myHelpCommand(
            command_attrs={
                'aliases': ['halp'],
                'help': 'Shows help about the bot, a command, or a category'
            }
        )

    async def cog_check(self, ctx):
        """
        The cog_check function is used to check if the user has permission to use a specific command.
        This function will be called automatically before every command in this cog.
        The bot checks if the user has admin rights, and returns True or False accordingly.

        :param self: Used to access the cog instance.
        :param ctx: Used to check if the user has permission to use a command.
        :return: a function that takes the ctx object as an argument.
        :doc-author: Trelent
        """
        return self.client.user_is_admin(ctx.author)

    def cog_unload(self):
        """
        The cog_unload function specifically unregisters the help command so that it can be re-registered by the cog reloader.

        :param self: Used to access the attributes and methods of the cog.
        :return: a boolean value.
        :doc-author: Trelent
        """
        self.client.get_command('help').hidden = False
        self.client.help_command = DefaultHelpCommand()

    @commands.command(
        aliases=['halpall'],
        hidden=True
    )
    async def helpall(self, ctx, *, text=None):
        """
        The helpall function specifically prints the help command including all hidden commands.
        It is used to print a list of all commands, even those that are not normally visible.

        :param self: Used to access the attributes and methods of your cog, as well as any other parts of the bot.
        :param ctx: Used to access the bot's attributes and functions.
        :param *: Used to allow for any number of arguments to be passed in.
        :param text=None: Used to pass a command name to the help function.
        :return: all of the commands, including hidden ones.
        :doc-author: Trelent
        """
        """Print bot help including all hidden commands"""
        self.client.help_command = myHelpCommand(show_hidden=True)
        if text:
            await ctx.send_help(text)
        else:
            await ctx.send_help()
        self.client.help_command = myHelpCommand()


def setup(client):
    """
    The setup function is used to register the commands that will be used in the bot.
    This function is run when you load a cog, and it allows you to use commands in your cogs.

    :param client: Used to access the API.
    :return: an instance of the class.
    :doc-author: Trelent
    """
    client.add_cog(Help(client))
