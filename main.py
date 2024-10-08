import discord
import os

# Get the bot token from the environment variable (or you can hardcode it for testing)
token = os.getenv("DISCORD_BOT_TOKEN")

# Ensure you have the correct token
if token is None:
    raise ValueError("Bot token not found. Please set the DISCORD_BOT_TOKEN environment variable.")

# Create a bot client class
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        # Print incoming messages to the console
        print(f'Message from {message.author}: {message.content}')
        
        # Avoid responding to the bot's own messages
        if message.author == self.user:
            return

        # Basic command response: if someone types "ping", respond with "pong"
        if message.content == 'ping':
            await message.channel.send('pong')

# Set intents to allow reading message content
intents = discord.Intents.default()
intents.message_content = True  # Enable reading message content


# Initialize the bot client with the correct intents
client = MyClient(intents=intents)

# Run the bot using the token
client.run(token)

