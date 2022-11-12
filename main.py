import nextcord as discord
from nextcord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents = intents)

token = os.getenv("DISCORD_TOKEN")
guild_id = 852578295967121438

@bot.event
async def on_ready():
    print("Expelliarmus!")
    my_user = await bot.fetch_user(706855396828250153)
    await my_user.send("Expelliarmus!")

@bot.slash_command(name = "new", description = "Create something new", default_member_permissions = discord.Permissions(administrator = True))
async def new():
    pass

class Potternews(discord.ui.Modal):
    def __init__(self):
        super().__init__("New PotterNews edition!", timeout = None)

        self.description = discord.ui.TextInput(
            label = "Content of the message",
            style = discord.TextInputStyle.paragraph,
            placeholder = "This is the message that will be sent along with the latest edition",
            required = True
        )
        self.add_item(self.description)
    
    async def callback(self, interaction: discord.Interaction) -> None:
        announcements = await bot.fetch_channel(1035093863477555230)
        potternews_embed = discord.Embed(title = "New PotterNews edition!", description = self.description.value, colour = discord.Colour.blue())
        await announcements.send(embed = potternews_embed)
        await interaction.send("Edition sent!", ephemeral = True)

@new.subcommand(name = "potternews", description = "Send a new edition of PotterNews")
async def potternews(interaction: discord.Interaction):
    modal = Potternews()
    await interaction.response.send_modal(modal)


class Pottertube(discord.ui.Modal):
    def __init__(self):
        super().__init__("New PotterTube video!", timeout = None)

        self.description = discord.ui.TextInput(
            label = "Content of the message",
            style = discord.TextInputStyle.paragraph,
            placeholder = "This is the message that will be sent along with the latest video",
            required = True
        )
        self.add_item(self.description)
    
    async def callback(self, interaction: discord.Interaction) -> None:
        announcements = await bot.fetch_channel(1035093863477555230)
        pottertube_embed = discord.Embed(title = "New PotterTube video!", description = self.description.value, colour = discord.Colour.blue())
        await announcements.send(embed = pottertube_embed)
        await interaction.send("Video sent!", ephemeral = True)

@new.subcommand(name = "pottertube", description = "Send a new video from PotterTube")
async def pottertube(interaction: discord.Interaction):
    modal = Pottertube()
    await interaction.response.send_modal(modal)


class Event(discord.ui.Modal):
    def __init__(self):
        super().__init__("New event!", timeout = None)

        self.description = discord.ui.TextInput(
            label = "Content of the message",
            style = discord.TextInputStyle.paragraph,
            placeholder = "This is the message that will be sent along with the latest event",
            required = True
        )
        self.add_item(self.description)
    
    async def callback(self, interaction: discord.Interaction) -> None:
        announcements = await bot.fetch_channel(1035093863477555230)
        event_embed = discord.Embed(title = "New event!", description = self.description.value, colour = discord.Colour.blue())
        await announcements.send(embed = event_embed)
        await interaction.send("Event sent!", ephemeral = True)

@new.subcommand(name = "event", description = "Send a new event")
async def event(interaction: discord.Interaction):
    modal = Event()
    await interaction.response.send_modal(modal)


class Message(discord.ui.Modal):
    def __init__(self, channel: discord.TextChannel):
        self.channel = channel

        super().__init__("New message!", timeout = None)

        self.name = discord.ui.TextInput(
            label = "Title of the message",
            style = discord.TextInputStyle.short,
            placeholder = "This is the title of the message that will be sent",
            required = False
        )
        self.add_item(self.name)

        self.description = discord.ui.TextInput(
            label = "Content of the message",
            style = discord.TextInputStyle.paragraph,
            placeholder = "This is the message that will be sent",
            required = True
        )
        self.add_item(self.description)
    
    async def callback(self, interaction: discord.Interaction) -> None:
        title = self.name.value
        if not self.name.value:
            title = "New message!"
        message_embed = discord.Embed(title = title, description = self.description.value, colour = discord.Colour.blue())
        await self.channel.send(embed = message_embed)
        await interaction.send("Message sent!", ephemeral = True)

@new.subcommand(name = "message", description = "Send a new message")
async def message(interaction: discord.Interaction, channel: discord.abc.GuildChannel = discord.SlashOption(name = "channel", description = "The channel you would like to send the message in", channel_types = [discord.ChannelType.text], required = True)):
    modal = Message(channel)
    await interaction.response.send_modal(modal)

class Award(discord.ui.Modal):
    def __init__(self, channel: discord.TextChannel, house: str, points: int):
        self.channel = channel
        self.house = house
        self.points = points

        super().__init__("Awarding points!", timeout = None)

        self.description = discord.ui.TextInput(
            label = "Content of the message",
            style = discord.TextInputStyle.paragraph,
            placeholder = "This is the message that will be sent",
            required = False
        )
        self.add_item(self.description)
    
    async def callback(self, interaction: discord.Interaction):
        old_points = int(self.channel.name.split(":")[1][1:])
        new_points = old_points + self.points
        await self.channel.edit(name = f"{self.house}: {new_points}")
        if self.description.value:
            points_logs = await bot.fetch_channel(1035454847660609536)
            await points_logs.send(f'''{self.description.value}

<#1035088045067743283>
<#1035088097341358160>
<#1035088147685576714>
<#1035088203037810729>
''')
        await interaction.send("Points awarded!", ephemeral = True)
        

@bot.slash_command(name = "award", description = "Award points to a house", default_member_permissions = discord.Permissions(administrator = True))
async def award(interaction: discord.Interaction, house: str = discord.SlashOption(name = "house", description = "The house to which the points have to be awarded", choices = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"], required = True), points: int = discord.SlashOption(name = "points", description = "The number of points to be awarded", required = True)):
    if house == "Gryffindor":
        channel = await bot.fetch_channel(1035088045067743283)
    elif house == "Hufflepuff":
        channel = await bot.fetch_channel(1035088097341358160)
    elif house == "Ravenclaw":
        channel = await bot.fetch_channel(1035088147685576714)
    elif house == "Slytherin":
        channel = await bot.fetch_channel(1035088203037810729)
    modal = Award(channel, house, points)
    await interaction.response.send_modal(modal)

bot.run(token)