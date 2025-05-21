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
        azure_deployment="gpt-4.1",
        api_version="2025-04-01-preview",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    # llm = ChatOllama(model="qwen2.5:7b", num_ctx=32000)


    # Basic configuration for the browser
    config = BrowserConfig(
        headless=False,
        disable_security=True
    )

    # Initialize the browser with the specified configuration
    browser = Browser(config=config)

    agent = Agent(
        task="""
        Solve the puzzle captcha on
        https://codepen.io/piyushpd139/full/NWbdgwB
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

