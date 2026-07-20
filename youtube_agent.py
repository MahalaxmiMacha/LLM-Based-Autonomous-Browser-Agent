import asyncio
from browser_use import Agent, Browser
from llm_config import get_agent_llm_kwargs

_active_agent = None

async def run_youtube(task, browser=None) -> str:
    global _active_agent
    
    llm_kwargs = get_agent_llm_kwargs()
    if not llm_kwargs:
        return "Error: No LLM configuration found."
        
    prompt = f"""
You are an autonomous web browser agent. Your task is: "{task}"

Instructions:
1. Open youtube.com. Wait for login if needed.
2. Search for the requested video/song.
3. Click ONLY individual video thumbnails. Do NOT click playlists, compilations, or mixes.
4. If a video shows "unavailable", "Playback error", or is blocked, go back to search results and try the next candidate. Try up to 5 times.
5. Verify playback has initialized and is unpaused. Click play if paused.
6. Provide a result summary featuring: Video Title, Channel Name, and any skipped candidates.
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
        return f"YouTube execution error: {e}"