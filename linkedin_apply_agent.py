import asyncio
import os
from browser_use import Agent, Browser
from llm_config import get_agent_llm_kwargs

_active_agent = None

async def apply_linkedin(job_url, profile={}, browser=None) -> str:
    global _active_agent
    
    llm_kwargs = get_agent_llm_kwargs()
    if not llm_kwargs:
        return "Error: No LLM configuration found."
        
    resume_path = profile.get("resume_path", "")
    available_files = [resume_path] if (resume_path and os.path.exists(resume_path)) else []
    profile_info = "\n".join([f"- {k}: {v}" for k, v in profile.items() if v])
    
    prompt = f"""
You are an autonomous web browser agent. Your task is: "Apply to the LinkedIn job: {job_url}"

Instructions:
1. Open the target job URL: {job_url}
2. Pause and wait up to 10 minutes for manual login if required.
3. Click the 'Easy Apply' button. Stop and report if not present.
4. Complete the multi-step form panels:
   - Input fields: skip if already filled.
   - Upload resume from available files.
   - Dropdown selections:
     * Right to work / Work Authorization? -> Yes
     * Sponsorship? -> No
     * Veteran status? -> No
     * Disability? -> No
     * Race / Ethnicity? -> I prefer not to answer
     * Relocate? -> Yes
     * Notice Period? -> Immediate
5. STOP at the final 'Submit' button. Do NOT click submit.
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
        return f"LinkedIn application error: {e}"