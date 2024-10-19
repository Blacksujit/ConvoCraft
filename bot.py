import discord
import os
import time
import aiohttp
import discord
from discord.ext import commands
from transformers import GPT2LMHeadModel, GPT2Tokenizer


# MISTRAL_API_KEY = ''
DISCORD_TOKEN = 'your_bot_token_to_discord'

# Rate limiting variables
last_request_time = 0
request_interval = 1  # Minimum interval between requests in seconds


# @bot.event
# async def on_ready():
#     print(f'Logged in as {bot.user}')

# @bot.command()
# async def chat(ctx, *, prompt: str):
#     # Encode the input prompt
#     inputs = tokenizer.encode(prompt, return_tensors='pt')
#     # Generate a response
#     outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     # Send the response back to Discord
#     await ctx.send(response)

# # Run the bot
# bot.run('YOUR_DISCORD_BOT_TOKEN')


# class MyClient(discord.Client):

#     async def on_ready(self):
#         print('Logged on as', self.user)

#     async def on_message(self, message):
#         global last_request_time
#         current_time = time.time()  # Define current_time here
        
#         print(f'Message from {message.author}: {message.content}')
#         if message.author == self.user:
#             return

#         if message.content == 'hey':
#             await message.channel.send('hello')

#         # Respond to "!mistral"
#         if message.content.startswith('!mistral'):
#             prompt = message.content[len('!mistral '):]  # Get the message after the command

#             # Rate limiting
#             if current_time - last_request_time < request_interval:
#                 await message.channel.send("Please wait before sending another request.")
#                 return
            
#             # Update the last request time
#             last_request_time = current_time

#             # Get response from Mistral
#             response = await self.get_response_from_mistral(prompt)

#             if response:
#                 await message.channel.send(response)

#     async def get_response_from_mistral(self, prompt):
#         url = "https://api.mistral.ai/v1/chat/completions"
#         headers = {
#             'Authorization': f'Bearer {MISTRAL_API_KEY}',
#             'Content-Type': 'application/json'
#         }
#         data = {
#             'prompt': prompt,
#             'max_tokens': 50
#         }

#         async with aiohttp.ClientSession() as session:
#             async with session.post(url, headers=headers, json=data) as response:
#                 if response.status == 200:
#                     stream = await response.content.read()  # Ensure the entire content is read
#                     # Process the response as needed
#                     return stream.decode('utf-8').strip()  # Return decoded response text
#                 else:
#                     return f"Error: {response.status} - {await response.text()}"

# # Set intents to allow reading message content
# intents = discord.Intents.default()
# intents.message_content = True

# # Initialize the client with the correct intents
# client = MyClient(intents=intents)

# # Run the client with the correct token
# client.run(DISCORD_TOKEN)


import discord
import os
import time
import aiohttp
from discord.ext import commands
from transformers import GPT2LMHeadModel, GPT2Tokenizer

DISCORD_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

# Load the Hugging Face GPT model and tokenizer
model_name = "gpt2"  # You can use any other GPT model from Hugging Face
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Rate limiting variables
last_request_time = 0
request_interval = 1  # Minimum interval between requests in seconds

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def chat(ctx, *, prompt: str):
    global last_request_time
    current_time = time.time()  # Define current_time here

    # Rate limiting
    if current_time - last_request_time < request_interval:
        await ctx.send("Please wait before sending another request.")
        return
    
    # Update the last request time
    last_request_time = current_time

    # Encode the input prompt
    inputs = tokenizer.encode(prompt, return_tensors='pt')

    # Generate a response
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Send the response back to Discord
    await ctx.send(response)

# Run the bot
bot.run(DISCORD_TOKEN)
