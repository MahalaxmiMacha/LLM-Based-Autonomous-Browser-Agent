from browser_use import Agent
import asyncio

async def main():

    agent = Agent(
        task="Open google.com and search for engineering scholarships"
    )

    await agent.run()

asyncio.run(main())