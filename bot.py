from dotenv import load_dotenv
import os

load_dotenv()

import discord
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from tavily import TavilyClient

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def surfInterNet(query:str):
    """Use this tool ONLY when the question requires real-time or latest info."""

    result = tavily_client.search(query=query , max_results=2)

    return "\n".join([r["content"] for r in result["results"]])



model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature = 0,
    max_retries = 1
)

agent = create_agent(model=model, tools=[surfInterNet])


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    content = message.content

    try:
        response = await agent.ainvoke({"messages":[HumanMessage(content)]})

        agent_message = response["messages"][-1].content

    except Exception : 
        agent_message = "API limit reached, Try again later"


    def split_message(text, limit=2000):

        return [text[i:i+limit] for i in range(0, len(text), limit)]


    for chunk in split_message(agent_message):
        await message.channel.send(chunk)







client.run(token=os.getenv("DISCORD_API_KEY"))