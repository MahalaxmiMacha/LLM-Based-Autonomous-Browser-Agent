import asyncio
from browser_use import Agent, Browser
from llm_config import get_agent_llm_kwargs

_active_agent = None

async def click_submit(platform, profile={}, browser=None) -> str:
    global _active_agent
    
    llm_kwargs = get_agent_llm_kwargs()
    if not llm_kwargs:
        return "Error: No LLM configuration found."
        
    prompt = f"""
You are an autonomous web browser agent. Your task is: "Explicit user authorization has been granted. Submit the current form on {platform}."

Instructions:
1. Analyze the active browser window view.
2. Locate the final submission trigger button (e.g., 'Submit', 'Apply', 'Confirm', 'Finish', 'Send').
3. Click the button ONCE.
4. Wait for the page confirmation status to load.
5. Capture and extract confirmation receipts or reference codes if available.
6. Return platform, status "Successfully Submitted", and parsed confirmations.
"""
    if browser is None:
        try:
            browser = Browser(headless=False)
        except TypeError:
            try:
                from browser_use import BrowserProfile
                profile_cfg = BrowserProfile(headless=False)
                browser = Browser(browser_profile=profile_cfg)
            except Exception:
                browser = Browser()
        
    try:
        agent = Agent(
            task=prompt,
            browser=browser,
            **llm_kwargs
        )
        _active_agent = agent
        history = await agent.run(max_steps=15)
        res = history.final_result()
        return res if res else str(history)
    except Exception as e:
        return f"Submission action failed: {e}"