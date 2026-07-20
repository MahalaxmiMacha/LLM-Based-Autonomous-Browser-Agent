import asyncio
import os
from browser_use import Agent, Browser
from llm_config import get_agent_llm_kwargs

_active_agent = None

async def send_whatsapp(task, profile={}, browser=None) -> str:
    global _active_agent
    
    llm_kwargs = get_agent_llm_kwargs()
    if not llm_kwargs:
        return "Error: No LLM configuration found."
    
    resume_path = profile.get("resume_path", "")
    available_files = [resume_path] if (resume_path and os.path.exists(resume_path)) else []
        
    prompt = f"""
You are an autonomous web browser agent. Your task is: "{task}"

Instructions:
1. Open web.whatsapp.com.
2. QR Code scan is required: pause and monitor every 10 seconds for the user to authenticate manually. Proceed when the chat panel is fully loaded.
3. Locate the intended target recipient or group.
4. Understand task parameters: text, media, document transfer, or chat logging.
5. If sending files, choose paperclip/plus symbol -> Document, and select the permitted uploaded document.
6. Trigger the send command.
7. Provide an action report summarizing: recipient name, communication medium, status.
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
        return f"WhatsApp execution error: {e}"