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

@bot.slash_command(name = "new", description = "Create something new")
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
        announcements = await bot.fetch_channel(1035075167669469214)
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
        announcements = await bot.fetch_channel(1035075167669469214)
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
        announcements = await bot.fetch_channel(1035075167669469214)
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

        self.description = discord.ui.TextInput(
            label = "Content of the message",
            style = discord.TextInputStyle.paragraph,
            placeholder = "This is the message that will be sentt",
            required = True
        )
        self.add_item(self.description)
    
    async def callback(self, interaction: discord.Interaction) -> None:
        message_embed = discord.Embed(title = "New message!", description = self.description.value, colour = discord.Colour.blue())
        await self.channel.send(embed = message_embed)
        await interaction.send("Message sent!", ephemeral = True)

@new.subcommand(name = "message", description = "Send a new message")
async def message(interaction: discord.Interaction, channel: discord.abc.GuildChannel = discord.SlashOption(name = "channel", description = "The channel you would like to send the message in", channel_types = [discord.ChannelType.text], required = True)):
    modal = Message(channel)
    await interaction.response.send_modal(modal)

@bot.slash_command(name = "award", description = "Award points to a house")
async def award(interaction: discord.Interaction, house: str = discord.SlashOption(name = "house", description = "The house to which the points have to be awarded", choices = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"], required = True), points: int = discord.SlashOption(name = "points", description = "The number of points to be awarded", required = True)):
    if house == "Gryffindor":
        channel = await bot.fetch_channel(1035088045067743283)
    elif house == "Hufflepuff":
        channel = await bot.fetch_channel(1035088097341358160)
    elif house == "Ravenclaw":
        channel = await bot.fetch_channel(1035088147685576714)
    else:
        channel = await bot.fetch_channel(1035088203037810729)
    old_points = int(channel.name.split(":")[1][1:])
    new_points = old_points + points
    await channel.edit(name = f"{house}: {new_points}")
    await interaction.send("Points awarded")

bot.run(token)