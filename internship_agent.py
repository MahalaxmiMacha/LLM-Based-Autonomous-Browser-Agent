import asyncio
import os
from browser_use import Agent, Browser
from llm_config import get_agent_llm_kwargs

_active_agent = None

async def main(role, profile={}, browser=None) -> str:
    global _active_agent
    
    llm_kwargs = get_agent_llm_kwargs()
    if not llm_kwargs:
        return "Error: No LLM configuration found."
        
    resume_path = profile.get("resume_path", "")
    available_files = [resume_path] if (resume_path and os.path.exists(resume_path)) else []
    profile_info = "\n".join([f"- {k}: {v}" for k, v in profile.items() if v])
    
    prompt = f"""
You are an autonomous web browser agent. Your task is: "Find and apply for a {role} internship in India on Internshala."

Instructions:
1. Open internshala.com.
2. Query the platform for the specified internship: "{role}".
3. Select the most relevant listing and click Apply.
4. Pause for manual login if required.
5. Populate inputs using this profile data:
{profile_info}

CRITICAL RULES:
- SKIP fields that are already filled. Do not overwrite existing answers.
- Fill forward only, never restart.
- STOP directly before submitting. Do NOT click the final submit button.
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
        return f"Internship application error: {e}"