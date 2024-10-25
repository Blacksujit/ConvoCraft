# Super Cool ConvoCraft 🤖✨

![bot](https://github.com/user-attachments/assets/8e4b3af0-df7e-46ae-93c6-53853b16ec20)


## Overview:

ConvoCraft is an all-in-one, feature-packed Discord bot designed to boost engagement, facilitate information sharing, and add a fun, interactive layer to any Discord server. Whether you're looking to analyze sentiments, generate dynamic visuals, set reminders, or simply add some humor, ConvoCraft brings a seamless blend of utility and entertainment to your Discord community.

## 🤔 Why I Created This:

With the growing need for vibrant, community-focused spaces online, ConvoCraft was created to enrich Discord server experiences with accessible, intelligent, and interactive tools. Inspired by my interest in AI, data science, and automation, I aimed to create a bot that goes beyond simple commands, instead fostering a deeper level of engagement, information retrieval, and usability for all users. ConvoCraft combines functionality with entertainment, offering an integrated set of commands that reflect the value of AI in everyday digital interactions.

## 🔍 Research & Inspiration:

To develop ConvoCraft, I researched various topics, from data visualization techniques and sentiment analysis to asynchronous programming models. The ideology behind ConvoCraft is rooted in enhancing community engagement with intelligent automation and visually-driven tools.

**Some key research and resources that influenced this project include:**

1.) Sentiment Analysis in Natural Language Processing: "TextBlob: Simplified Text Processing" [[link to paper](https://textblob.readthedocs.io/en/dev/)]

2.) Currency conversion and financial APIs: "Automating Financial Operations with Forex-python" [[link to forex-python documentation](https://forex-python.readthedocs.io/en/latest/)]

3.) Visual representation techniques: "Data Visualization with Matplotlib" [[link to paper](https://www.dundas.com/support/learning/documentation/data-visualizations/)]

4.) Asynchronous Programming: "Concurrency with Asyncio in Python" [[link to Python docs](https://docs.python.org/3/library/asyncio.html)]

## Technical Details:

### ⚙️ Dependencies:

***ConvoCraft utilizes various Python libraries and APIs for different functionalities, including:***

1.) bot.py: Interfaces with the Discord API.

2.) python-dotenv: Manages environment variables for secure token handling.

3.) matplotlib: Generates data visualizations.

4.) forex-python: Handles real-time currency conversion.

5.) textblob: Performs sentiment analysis.

6.) wordcloud: Creates word clouds from text.

7.) wikipedia: Fetches summarized information from Wikipedia.

8.) qrcode: Generates QR codes for URLs and text.

9.) Pillow (PIL): Assists in image processing.

10.) numpy: Facilitates numerical computations.

11.) asyncio: Enables non-blocking asynchronous programming for smooth multitasking.


## Key Features & Ideology:

***ConvoCraft is designed to balance utility with engagement. Here’s a closer look at each feature and the thinking behind its inclusion:***

### Visualization Command (!visualize) 📊:

***Purpose: Provides community members with a quick, interactive way to visualize data within Discord.
Implementation: Uses matplotlib to generate bar graphs, line plots, and other chart types, sending the images directly to the chat.
Ideology: Visuals play a crucial role in data interpretation, and this feature brings an educational, analytical tool to the server.***

### Currency Conversion (!currency) 💱:

***Purpose: Offers real-time exchange rates to users, essential for global communities.***
***Implementation: Utilizes forex-python to fetch current rates and perform conversions.***
***Ideology: With servers often hosting international members, this tool eases quick currency conversions for collaborative projects or discussions.***

### Chatbot (!ask) 🤖: (An Anthropic Chatbot)

***Purpose: Provides a chatbot interface for users to interact with, powered by Anthropic's API.***
***Implementation: Utilizes the Anthropic API to generate responses to user queries.***
***Ideology: This feature enhances conversational interactions within the server, offering a dynamic and responsive chatbot experience.***


### Sentiment Analysis (!sentiment) 📈:

***Purpose: Analyzes the sentiment behind messages, offering insights into community mood and discussions.
Implementation: Uses TextBlob for text sentiment analysis, providing users with a positivity or negativity score.
Ideology: This feature can be valuable for moderators and administrators to monitor overall sentiment, helping to create a positive, inclusive community environment.***

### Word Cloud Generation (!wordcloud) ☁️:

***Purpose: Visualizes word frequency in text data, which can represent discussion trends or popular topics in the server.
Implementation: Creates a word cloud from input text using wordcloud and Pillow.
Ideology: A unique way to display frequently discussed topics in a channel, adding a fun and engaging visual element to the server.***

### Wikipedia Summary (!wiki) 🌐:

***Purpose: Quickly fetches information on various topics, helping users learn and share knowledge in seconds.
Implementation: The wikipedia library retrieves short summaries based on input queries.
Ideology: This feature provides accessible information to users, enhancing conversations with factual insights.***

### QR Code Generation (!qr) 📱:

***Purpose: Simplifies information sharing, allowing users to convert URLs and text into QR codes.
Implementation: Uses the qrcode library to create scannable QR codes, perfect for mobile sharing.
Ideology: This addition allows quick content sharing among mobile users, fostering easier access to shared resources.***

### Reminder System (!reminder) ⏰:

***Purpose: Enables users to set reminders within the chat, ideal for coordinating tasks or tracking events.
Implementation: Leverages asyncio for efficient scheduling, notifying users when their reminder is due.
Ideology: A practical feature for teams and communities that need task management or timed reminders.***

### Fun Commands 🎉:

***Purpose: Adds a light-hearted touch to the server with commands like !joke, !flip, and !roll.
Ideology: Community building relies on fun and engagement, and these commands break the ice or add humor to daily interactions.***

### Implementation Details:


#### Asynchronous Programming with asyncio

***Why: To ensure smooth, non-blocking responses for multiple commands.
How: The bot employs asyncio to manage concurrent tasks, enhancing performance and ensuring the bot remains responsive even with multiple commands running.***

#### Image Processing:

***Purpose: Features like word clouds and QR code generation require robust image manipulation.
Tools: Pillow (PIL) and qrcode handle image generation and processing for these commands.***

#### Data Visualization

***Purpose: Matplotlib creates visual feedback for users, turning data into digestible charts.
Benefit: These visuals are useful for educational or analytical discussions within the server.
Natural Language Processing
Purpose: TextBlob processes message sentiment, offering a glance into emotional context.
Benefit: Adds a new dimension to server interactions, potentially assisting in moderating community dynamics.***


## 🛠️ Bot Initialization:

***The bot initializes with Discord’s Intents system, allowing it to access server interactions with the ! command prefix and message content intent enabled.***



## Getting Started:

******Run the below commands to start the bot:******

***create an `.env` file at the root of the project directory  and add your bot token and hugging face access token:***

```
DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN

``` 

```
HUGGING_FACE_ACCESS_TOKEN=YOUR_HUGGING_FACE_ACCESS_TOKEN

``` 

```
ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY

``` 

***Run the bot:***

```
python bot.py

```

 
 
## Conclusion:

ConvoCraft represents a thoughtful blend of interactivity, information, and entertainment—transforming Discord into a smart, user-centered community hub. By combining utility with fun, this bot exemplifies how technology can enhance user engagement and simplify tasks. Whether you're looking to analyze text sentiment, visualize data, or just have a laugh, ConvoCraft has it covered.

Enjoy Super Cool ConvoCraft! Feel free to explore, contribute, and make it your own. 🎉
