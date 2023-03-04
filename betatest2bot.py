import discord
import asyncio
import colorama
import discord
import requests

webhook_url = ""
TOKEN = 'MTA4MTY1OTQzOTU3NDE3NTc4NA.GKN54f.cyaNt_TVH_n-9RbFXGdmf3I_GgpKFPfco9U8GE'

# Define your key here
key = "betabeta2121"


# This function sends a message to the webhook with the specified status and result
def send_webhook(next_roll, safe_prediction):
    data = {
        "content":
        f"The prediction {next_roll}! The next safe prediction is {safe_prediction}. This prediction may be wrong, go with the safe one."
    }
    requests.post(webhook_url, json=data)


# Initialize colorama
colorama.init()

# Discord bot token

# Client instance
intents = discord.Intents().default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith("!predict"):
        # Check if the message starts with '!predict'
        key_input = await message.channel.send("Please enter the key:")

        def check_key(m):
            return m.author == message.author and m.channel == message.channel

        key_attempt = await client.wait_for("message", check=check_key)
        if key_attempt.content != key:
            await message.channel.send("Incorrect key. Please try again.")
            return
        seed = key_attempt.content
        seed_input = await message.channel.send("Please enter the seed:")
        seed_attempt = await client.wait_for("message", check=check_key)
        seed = seed_attempt.content
        if len(seed) < 9:
            await message.channel.send(
                "Invalid seed. Seed must be at least 9 characters.")
        else:
            rolls = []
            for i in range(5):
                roll_input = await message.channel.send(f"Enter roll {i + 1}: ")
                roll_attempt = await client.wait_for("message", check=check_key)
                if not roll_attempt.content.replace('.', '').isdigit():
                    await message.channel.send(
                        "Invalid roll. Please enter a number between 0 and 100.")
                    return
                roll = float(roll_attempt.content)
                rolls.append(roll)

            roll_sum = sum(rolls)

            next_roll = roll_sum / 5
            safe_prediction = ""
            if next_roll > 50:
                safe_prediction = "roll over 30"
            else:
                safe_prediction = "roll under 60"

            prediction_embed = discord.Embed(
                title=f"predictor made by aarav#6969 get ready to make 💸 ",
                description=f"The safe roll is predicted to be: {safe_prediction}",
                color=discord.Color.green())

            await message.channel.send(embed=prediction_embed)

            # Send a ping to the webhook with the result and status
            send_webhook(next_roll, safe_prediction)

            # Ask if the user won and for how much profit
            win_input = await message.channel.send("Did you win? (Yes or No)")
            win_attempt = await client.wait_for("message", check=check_key)
            win = win_attempt.content.lower() == "yes"
            if win:
                profit_input = await message.channel.send("How much profit did you make?")
                profit_attempt = await client.wait_for("message", check=check_key)
                profit = float(profit_attempt.content)
            else:
                profit = 0.0

            # Send a thank you message
            await message.channel.send("Thank you for participating in the survey!")

            # Send the data to the webhook
            data = {
                "content": f"User {message.author} made a profit of {profit} from the prediction."
            }
            requests.post(webhook_url, json=data)
          # Start the client
client.run(TOKEN)