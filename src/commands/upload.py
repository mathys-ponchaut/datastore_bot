from interactions import (
    SlashContext,
    Extension,
    slash_command, slash_option,
    OptionType,
    Attachment,
    File,
    Embed
)
import aiohttp
from io import BytesIO # Allow to convert Bytes to readable data for Discord

from dependencies.settings import *

class Upload(Extension):
    @slash_command(
        name='upload',
        description='Upload a file',
    )
    @slash_option(
        name='file',
        description='The file to upload',
        opt_type=OptionType.ATTACHMENT,
        required=True,
    )
    @slash_option(
        name='name',
        description='The name of the file to upload',
        opt_type=OptionType.STRING,
        required=False,
        min_length=1,
    )
    async def upload(self, ctx: SlashContext, file: Attachment):
        author = ctx.author
        name, extension = os.path.splitext(file.filename)

        if '-' in name:
            name = name.replace('-', '')
            await ctx.respond(
                content=
                    f"⚠️ File's name cannot contain a '-'\n"
                    f"> File was renamed as: '{name}",
                ephemeral=True,
            )

        host_guild = await self.bot.fetch_guild(get_setting('server_id'))
        channel = await host_guild.create_text_channel(
            name=f'{ctx.id}-{name}-{extension}',
            reason=f"Created by {author.global_name} ({author.id}) and uploaded: {file.filename}",
        )

        data = any
        """Download file (temp)"""
        async with aiohttp.ClientSession() as session:
            async with session.get(file.url) as response:
                data = await response.read()

        await ctx.respond(
            embed=Embed(
                title="📁 File was uploaded sucessfully",
                description=
                    f"🔗 Channel: {channel.mention}\n"
                    f"🆔 **__Id__**:\n```{ctx.id}```\n"
                    f"📁 **__File name__**:\n```{file.filename}```",
                )
        )
        await channel.send(
            content=
                f"owner: {author.id}\n"
                f"members: -1",
            file=File(BytesIO(data), file.filename))