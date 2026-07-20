import asyncio
import os
import re
from browser_use import Agent, Browser
from llm_config import get_agent_llm_kwargs

_active_agent = None

async def apply_company(task, profile={}, browser=None) -> str:
    global _active_agent
    
    llm_kwargs = get_agent_llm_kwargs()
    if not llm_kwargs:
        return "Error: No LLM configuration found."
        
    resume_path = profile.get("resume_path", "")
    available_files = [resume_path] if (resume_path and os.path.exists(resume_path)) else []
    profile_info = "\n".join([f"- {k}: {v}" for k, v in profile.items() if v])
    
    url_match = re.search(r"https?://[^\s]+", task)
    url_instruction = f"Open: {url_match.group(0)}" if url_match else "Search company careers site and locate target opening."

    prompt = f"""
You are an autonomous web browser agent. Your task is: "{task}"

Instructions:
1. {url_instruction}
2. Open target position and click Apply.
3. Pause for manual login if required.
4. Populated inputs using this profile data:
{profile_info}

CRITICAL RULES:
- Check for existing filled inputs and skip them.
- Dropdown standard defaults: Sponsorship -> No, Work Auth -> Yes, Relocate -> Yes, Notice -> Immediate.
- STOP before clicking the final 'Submit' button.
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
            available_file_paths=available_files,
            **llm_kwargs
        )
        _active_agent = agent
        history = await agent.run(max_steps=500)
        res = history.final_result()
        return res if res else str(history)
    except Exception as e:
        return f"Company application error: {e}"