from interactions import (
    slash_command,
    slash_option,
    OptionType,
    Extension,
    SlashContext,
    File,
    ChannelType,
    Embed,
    Color,
    GuildText,
)
from typing import Union
from io import BytesIO
from dependencies.settings import get_setting
import aiohttp


class Search(Extension):
    @slash_command(
        name='search',
        description='Upload a file',
    )
    @slash_option(
        name='name',
        description='The name or id of the file to be searched',
        opt_type=OptionType.STRING,
        required=True,
        min_length=1,
        argument_name='provided_name'
    )
    async def show_list_of_files(self, ctx: SlashContext, channels: list):
        description = ""
        for channel in channels:
        message = await ctx.respond(
            embed=Embed(
                title="📁 **Files found**",
                description=
            )
        )

    async def search(self, ctx: SlashContext, provided_name: str):
        author_id = str(ctx.author.id)

        provided_id = None
        if provided_name.isdigit():
            print(f"An id was provided: {provided_id}")
            provided_id = provided_name

        host_guild = await self.bot.fetch_guild(get_setting('server_id'))
        channels = await host_guild.fetch_channels()

        if not provided_id is None:
            for channel in channels:
                if channel.type == ChannelType.GUILD_TEXT:
                    id = channel.name.split('-')[0]
                    print(f"Current id: {id}")
                    if id == provided_id:
                        print("Channel found")
                        message = await channel.fetch_message(channel.last_message_id)
                        lines = message.content.splitlines()
                        args = {}
                        for line in lines:
                            key, value = line.split(': ')
                            args[key] = value

                        if author_id == args['owner'] or author_id in args['members'] or args['members'] == 'all':
                            attachment = message.attachments[0]

                            async with aiohttp.ClientSession() as session:
                                async with session.get(attachment.url) as response:
                                    data = await response.read()
                            await ctx.respond(
                                content=
                                    f"### 📁 **__Here is your file__**\n"
                                    f"**__Name__**: `{attachment.filename}`",
                                files=File(BytesIO(data), attachment.filename),
                                ephemeral=False
                            )
                        else:
                            await ctx.respond(
                                embed=Embed(
                                    title="❌ Access denied",
                                    description="You don't have permission to access this file"
                                )
                            )
                        return
        else:
            matching_channels = {
                "name_extension": [],
                "name": [],
                "partially": [],
            }
            for channel in channels:
                if channel.type == ChannelType.GUILD_TEXT:
                    name = channel.name.split('-')[1]
                    extension = channel.name.split('-')[2]
                    file_name = f"{name}.{extension}"

                    if provided_name == file_name:
                        matching_channels["name_extension"].append(channel)
                    elif provided_name == name:
                        matching_channels["name"].append(channel)
                    elif provided_name in name:
                        matching_channels["partially"].append(channel)

                if matching_channels.get("name_extension") != []:
                    pass

        await ctx.respond(
            embed=Embed(
                title="❌ File not found",
                color=Color.from_rgb(210, 0, 0)
            ),
            ephemeral=True
        )