import asyncio
from browser_use import Agent, Browser
from llm_config import get_agent_llm_kwargs

_active_agent = None

async def run_general(task, profile={}, browser=None) -> str:
    global _active_agent
    
    llm_kwargs = get_agent_llm_kwargs()
    if not llm_kwargs:
        return "Error: No LLM configuration found. Ensure your API Key is specified."
    
    profile_info = "\n".join([f"- {k}: {v}" for k, v in profile.items() if v])
    
    prompt = f"""
You are an autonomous web browser agent. Your task is: "{task}"

Instructions:
1. Navigate and perform the web task autonomously.
2. If the task involves Gmail compose: fill the 'To' address field first, followed by 'Subject', and then 'Body' before clicking Send.
3. If forms are encountered, fill details matching this user profile:
{profile_info}

CRITICAL RULES:
- LOGIN HANDLING: If a sign-in screen appears, check every 10 seconds and pause up to 10 minutes for manual user login. Only proceed once logged in.
- FORM FILLING: If fields are pre-filled, SKIP them entirely. Never return to previously completed fields. Use the profile details first, fallback to resume details or smart AI inferences.
- DROPDOWN HANDLING: Click to open, view options, and click corresponding match.
- SUBMIT GATE: ALWAYS pause and wait before hitting any final submission, payment, or purchase confirmation buttons.
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
        return f"General execution error: {e}"