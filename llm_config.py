import os
import streamlit as st

def get_agent_llm_kwargs():
    """
    Returns kwargs representing the LLM instance.
    Directly utilizes official langchain integrations to ensure the model parameter 
    is respected without fallback overrides.
    """
    # Force pull from session state to ensure environment persistency
    provider = st.session_state.get("api_provider", "OpenAI")
    key_val = st.session_state.get("api_key_val", "").strip()
    
    if key_val:
        if provider == "OpenAI":
            os.environ["OPENAI_API_KEY"] = key_val
            os.environ["GEMINI_API_KEY"] = ""
            os.environ["GOOGLE_API_KEY"] = ""
        elif provider == "Gemini / Google":
            os.environ["GEMINI_API_KEY"] = key_val
            os.environ["GOOGLE_API_KEY"] = key_val
            os.environ["OPENAI_API_KEY"] = ""
            
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    gemini_key = (os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")).strip()
    
    if openai_key:
        try:
            from browser_use import ChatOpenAI
        except ImportError:
            try:
                from browser_use.llm import ChatOpenAI
            except ImportError:
                from langchain_openai import ChatOpenAI
                
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_key)
        if not hasattr(llm, 'provider'):
            object.__setattr__(llm, 'provider', 'openai')
        return {"llm": llm}
        
    elif gemini_key:
        # Directly use the official integration model to prevent any internal defaults from overriding the model ID
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Instantiate directly with gemini-2.0-flash and the active API Key
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=gemini_key)
        
        # Inject provider standard attribute to pass browser-use validation checks
        if not hasattr(llm, 'provider'):
            object.__setattr__(llm, 'provider', 'google')
            
        return {"llm": llm}
        
    else:
        return {}