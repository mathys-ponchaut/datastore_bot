from interactions import (
    SlashContext,
    Embed,
    Color,
    ComponentContext,
    ComponentCommand,
    Button,
    ButtonStyle,
)

async def display_files(self, ctx: SlashContext, reason: str, channels: list):
    description = ""

    for channel in channels:
        name, extension = channel.name.split("-")[1:]
        file_name = f"{name}.{extension}"

        description = f"{description}📄 - {file_name}\n"

    await ctx.respond(
        embed=Embed(
            title=f"📁 - {reason}",
            description=description
        ),
        components=[
            Button(
                custom_id="previous",
                label="Previous",
                style=ButtonStyle.BLUE,
                emoji="⬆️",
                disabled=True,
            ),
            Button(
                custom_id="next",
                label="Next",
                style=ButtonStyle.BLUE,
                emoji="⬇️",
                disabled=False
            ),
            Button(
                custom_id="next_page",
                label="Next page",
                style=ButtonStyle.GRAY,
                emoji="➡️",
                disabled=False
            )
        ]
    )