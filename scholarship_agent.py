import asyncio
from browser_use import Agent, Browser
from llm_config import get_agent_llm_kwargs

_active_agent = None

async def main(task="Find engineering scholarships in India", profile={}, browser=None) -> str:
    global _active_agent
    
    llm_kwargs = get_agent_llm_kwargs()
    if not llm_kwargs:
        return "Error: No LLM configuration found."
        
    prompt = f"""
You are an autonomous web browser agent. Your task is: "{task}"

Instructions:
1. Search and open the National Scholarship Portal or similar verified official portals.
2. Locate key application forms for engineering candidates.
3. Extract and organize:
   - Scholarship Program Name
   - Detailed Eligibility Requirements
   - Supporting Documents Required
   - Application Process Paths
   - Cutoff Dates and Deadlines
4. Provide a structured summary output.
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
        history = await agent.run(max_steps=500)
        res = history.final_result()
        return res if res else str(history)
    except Exception as e:
        return f"Scholarship search error: {e}"