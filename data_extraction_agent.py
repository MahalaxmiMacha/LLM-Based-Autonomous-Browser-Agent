import asyncio
from browser_use import Agent, Browser
from llm_config import get_agent_llm_kwargs

_active_agent = None

async def extract_data(task, browser=None) -> str:
    global _active_agent
    
    llm_kwargs = get_agent_llm_kwargs()
    if not llm_kwargs:
        return "Error: No LLM configuration found."
        
    prompt = f"""
You are an autonomous web browser agent. Your task is: "{task}"

Instructions:
1. Navigate to target resource pages (e.g., GeeksforGeeks, W3Schools, Wikipedia, MDN, StackOverflow).
2. Gather detailed content: Main text structures, headings, diagrams, tables, list arrays, code blocks.
3. Compile and construct a clean Markdown overview comprising:
   - Source: [Exact page url]
   - Overview: Broad context overview
   - Key Concepts: Bullet highlights
   - Code Examples: Plain code segments (if applicable)
   - Takeaways: Quick recap summaries
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
        return f"Extraction error: {e}"