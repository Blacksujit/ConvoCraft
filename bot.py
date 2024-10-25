import discord
import os
import time
import random
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg
import matplotlib.pyplot as plt
import io
import requests
from discord.ext import commands
from dotenv import load_dotenv
from forex_python.converter import CurrencyRates
from textblob import TextBlob
from wordcloud import WordCloud
import wikipedia
import qrcode
from PIL import Image
import numpy as np
from datetime import datetime, timedelta
import asyncio
from transformers import pipeline

# Load environment variables
load_dotenv()

# Directly load the Discord bot token
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_ACCESS_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not DISCORD_TOKEN:
    raise ValueError("Discord bot token is not set")

if not HUGGING_FACE_TOKEN:
    raise ValueError("Hugging Face token is not set")

if not ANTHROPIC_API_KEY:
    raise ValueError("Anthropic API key is not set")

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize the Anthropic API client for Claude
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

# Initialize the Hugging Face pipeline
qa_model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", token=HUGGING_FACE_TOKEN)

# The qa_model will be used in the following scenarios:
# 1. When a user invokes the !ask command with a question
# 2. The model will attempt to answer general knowledge questions
# 3. It will provide concise responses based on the given context
# 4. The model will not generate new information, only extract answers from the provided context
# 5. If the question is outside the model's knowledge or context, it will indicate that it cannot answer

# Function to generate a response using Claude
async def generate_response(prompt, max_tokens=100):
    # Add rate limiting
    if not hasattr(generate_response, 'last_call'):
        generate_response.last_call = 0
    
    current_time = time.time()
    if current_time - generate_response.last_call < 1:  # Limit to 1 request per second
        await asyncio.sleep(1 - (current_time - generate_response.last_call))
    
    generate_response.last_call = time.time()
    
    # Add a daily limit
    if not hasattr(generate_response, 'daily_count'):
        generate_response.daily_count = 0
        generate_response.last_reset = datetime.now().date()
    
    today = datetime.now().date()
    if today > generate_response.last_reset:
        generate_response.daily_count = 0
        generate_response.last_reset = today
    
    if generate_response.daily_count >= 1000:  # Limit to 1000 requests per day
        return "Daily limit reached. Please try again tomorrow."
    
    generate_response.daily_count += 1
    
    try:
        response = await anthropic.completions.create(
            model="claude-2",
            prompt=f"{HUMAN_PROMPT} {prompt}{AI_PROMPT}",
            max_tokens_to_sample=max_tokens
        )
        return response.completion.strip()
    except Exception as e:
        print(f"Error in generate_response: {e}")
        return "An error occurred while generating the response."

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# New visualization command
@bot.command()
async def visualize(ctx, *, prompt: str):
    """
    Creates and sends a visualization based on the user's prompt.
    Usage: !visualize <chart type> <data>
    Example: !visualize bar chart of apples:5 oranges:3 bananas:4
    """
    try:
        # Parse the prompt to extract data and chart type
        chart_type, data = parse_prompt(prompt)
        
        # Create the visualization
        plt.figure(figsize=(10, 6))
        if chart_type == 'bar':
            plt.bar(list(data.keys()), list(data.values()))
        elif chart_type == 'line':
            plt.plot(list(data.keys()), list(data.values()))
        elif chart_type == 'pie':
            plt.pie(list(data.values()), labels=list(data.keys()), autopct='%1.1f%%')
        elif chart_type == 'histogram':
            plt.hist(list(data.values()), bins=len(data), edgecolor='black')
        elif chart_type == 'scatter':
            plt.scatter(list(data.keys()), list(data.values()))
        elif chart_type == 'area':
            plt.fill_between(list(data.keys()), list(data.values()), color='blue', alpha=0.3)
        else:
            await ctx.send("Unsupported chart type. Please use 'bar', 'line', or 'pie'.")
            return

        plt.title(prompt)
        plt.tight_layout()

        # Save the plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Send the image to Discord
        await ctx.send(file=discord.File(buf, 'chart.png'))
        
        # Clear the current figure
        plt.clf()

    except Exception as e:
        await ctx.send(f"An error occurred while creating the visualization: {str(e)}")
        print(f"Error in visualize command: {e}")

def parse_prompt(prompt):
    """
    Parses the user's prompt to extract chart type and data.
    
    This function splits the prompt into words, identifies the chart type,
    and extracts key-value pairs for the data.
    
    Args:
    prompt (str): The user's input prompt.
    
    Returns:
    tuple: A tuple containing the chart type and a dictionary of data.
    """
    parts = prompt.lower().split()
    chart_type = 'bar'  # default
    data = {}

    # Determine chart type
    if 'bar' in parts:
        chart_type = 'bar'
    elif 'line' in parts:
        chart_type = 'line'
    elif 'pie' in parts:
        chart_type = 'pie'
    elif 'histogram' in parts:
        chart_type = 'histogram'
    elif 'scatter' in parts:
        chart_type = 'scatter'
    elif 'area' in parts:
        chart_type = 'area'

    # Extract data from the prompt
    # This assumes a format like "apples:5 oranges:3 bananas:4"
    for part in parts:
        if ':' in part:
            key, value = part.split(':')
            data[key] = float(value)

    return chart_type, data

# Existing commands

@bot.command()
async def joke(ctx):
    """
    Sends a random joke from a predefined list.
    Usage: !joke
    """
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "Why don't skeletons fight each other? They don't have the guts!",
        "What do you call a fake noodle? An impasta!"
    ]
    await ctx.send(random.choice(jokes))

@bot.command()
async def flip(ctx):
    """
    Simulates a coin flip.
    Usage: !flip
    """
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"The coin landed on: {result}")

@bot.command()
async def roll(ctx, dice: str):
    """
    Simulates rolling dice.
    Usage: !roll NdN (e.g., !roll 2d6 for rolling two six-sided dice)
    """
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send("Format has to be in NdN!")
        return

    results = [random.randint(1, limit) for _ in range(rolls)]
    await ctx.send(f"Rolling {dice}:\nResults: {', '.join(map(str, results))}\nSum: {sum(results)}")

# New fancy commands

@bot.command()
async def currency(ctx, amount: float, from_currency: str, to_currency: str):
    """
    Converts currency using real-time exchange rates.
    Usage: !currency <amount> <from_currency> <to_currency>
    Example: !currency 100 USD EUR
    """
    try:
        c = CurrencyRates()
        result = c.convert(from_currency.upper(), to_currency.upper(), amount)
        await ctx.send(f"{amount} {from_currency.upper()} is equal to {result:.2f} {to_currency.upper()}")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command()
async def sentiment(ctx, *, text: str):
    """
    Analyzes the sentiment of the given text.
    Usage: !sentiment <text>
    Example: !sentiment I love this Discord bot!
    """
    try:
        analysis = TextBlob(text)
        sentiment_score = analysis.sentiment.polarity
        if sentiment_score > 0:
            sentiment = "positive"
        elif sentiment_score < 0:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        await ctx.send(f"The sentiment of '{text}' is {sentiment} (score: {sentiment_score:.2f})")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command()
async def wordcloud(ctx, *, text: str):
    """
    Generates a word cloud from the given text.
    Usage: !wordcloud <text>
    Example: !wordcloud This is a sample text for generating a word cloud image
    """
    try:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        await ctx.send(file=discord.File(buf, 'wordcloud.png'))
        plt.clf()
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Additional cool features

@bot.command()
async def wiki(ctx, *, query: str):
    """
    Fetches a summary from Wikipedia for the given query.
    Usage: !wiki <query>
    Example: !wiki Python programming language
    """
    if not query:
        await ctx.send("Please provide a query. Usage: !wiki <query>")
        return
    
    try:
        summary = wikipedia.summary(query, sentences=3)
        await ctx.send(f"Wikipedia summary for '{query}':\n\n{summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        await ctx.send(f"Your query '{query}' may refer to multiple topics. Please be more specific.")
    except wikipedia.exceptions.PageError:
        await ctx.send(f"Sorry, I couldn't find a Wikipedia page for '{query}'.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command()
async def qr(ctx, *, data: str):
    """
    Generates a QR code for the given data.
    Usage: !qr <data>
    Example: !qr https://discord.com
    """
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        await ctx.send(file=discord.File(buf, 'qrcode.png'))
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command()
async def reminder(ctx, time: str, *, message: str):
    """
    Sets a reminder for the user.
    Usage: !reminder <time> <message>
    Example: !reminder 1h30m Take out the trash
    """
    try:
        duration = parse_time(time)
        if duration:
            await ctx.send(f"Okay, I'll remind you to '{message}' in {time}.")
            await asyncio.sleep(duration)
            await ctx.send(f"{ctx.author.mention} Reminder: {message}")
        else:
            await ctx.send("Invalid time format. Please use a combination of numbers and 's' (seconds), 'm' (minutes), or 'h' (hours).")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command(name="ask")
async def ask_question(ctx, *, question: str):
    """
    Answers a question using the Hugging Face model.
    Usage: !ask <question>
    Example: !ask What is the capital of France?
    """
    try:
        # Use a default context for general knowledge questions
        context = "The model can answer general knowledge questions about various topics including history, science, geography, and more."
        
        result = qa_model(question=question, context=context)
        answer = result['answer']
        
        # Check if the answer is empty, too short, or starts with "The model"
        if not answer or len(answer) < 5 or answer.lower().startswith("the model"):
            await ctx.send(f"I'm sorry, but I couldn't generate a meaningful answer to your question: '{question}'. Could you please rephrase or ask a different question?")
        else:
            await ctx.send(f"Question: {question}\nAnswer: {answer}")
    except Exception as e:
        await ctx.send(f"An error occurred while processing your question: {str(e)}")
        print(f"Error in ask command: {str(e)}")  # Log the error for debugging

    # Add a fallback response if the model fails to answer
    if not answer or len(answer) < 5 or answer.lower().startswith("the model"):
        await ctx.send("I apologize, but I'm having trouble answering your question at the moment. Please try again later or ask a different question.")

def parse_time(time_str):
    total_seconds = 0
    current = ''
    for char in time_str:
        if char.isdigit():
            current += char
        elif char in ['s', 'm', 'h']:
            if current:
                if char == 's':
                    total_seconds += int(current)
                elif char == 'm':
                    total_seconds += int(current) * 60
                elif char == 'h':
                    total_seconds += int(current) * 3600
                current = ''
    return total_seconds if total_seconds > 0 else None

# Error handling for bot connection
if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        print("Invalid Discord token. Please check your token.")
    except Exception as e:
        print(f"An error occurred while running the bot: {e}")

# Explanation of added fancy features:
# 1. Currency conversion command using real-time exchange rates.
# 2. Sentiment analysis command to determine the sentiment of given text.
# 3. Word cloud generation command to create visual representations of text data.
# 4. Wikipedia summary command to fetch quick information on various topics.
# 5. QR code generation command for easy sharing of links or text.
# 6. Reminder command to set timed reminders for users.
# 7. Question answering command using the Hugging Face model (distilbert-base-cased-distilled-squad).
# These additions provide more interactive and useful functionalities for users.

# PythonAnywhere deployment notes:
# 1. Upload this script to your PythonAnywhere account.
# 2. Install required packages using pip in a PythonAnywhere console.
# 3. Set up environment variables in the PythonAnywhere dashboard.
# 4. Create a new web app and point it to this script.
# 5. Ensure the web app is set to manual reload and always on.
# 6. Start the bot using the PythonAnywhere 'Run' button or via console.
