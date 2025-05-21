from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    # Initialize the model
    llm = AzureChatOpenAI(
        azure_deployment="gpt-4.1-mini",
        api_version="2025-04-01-preview",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    #llm = ChatOllama(model="gemma3:12b", num_ctx=32000)

    # Basic configuration for the browser
    config = BrowserConfig(
        headless=False,
        disable_security=True
    )

    # Initialize the browser with the specified configuration
    browser = Browser(config=config)

    agent = Agent(
        task="""
        Research the latest developments regarding Romanian presidential
        elections from at least 3 different reputable news sources.
        For each source:
        1. Navigate to their search function and find articles about the topic from the past week
        2. Extract the headline, publication date, and author
        3. Summarize the key points in 2-3 sentences

        After gathering information, synthesize the findings into a comprehensive summary that notes any differences in reporting or perspective between the sources.
        """,
        llm=llm,
        browser=browser,
        use_vision=True,
        generate_gif=True
    )

    try:
        result = await agent.run()
        # display(result.action_results())
        print('--------------------------')
        for action in result.action_results():
            if action.is_done:
                print(action.extracted_content)
        print('--------------------------')
        # Close the browser after completion
        await browser.close()
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

