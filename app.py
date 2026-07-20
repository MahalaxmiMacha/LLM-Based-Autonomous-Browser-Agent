import streamlit as st
import asyncio
import os
import re
import sys
import base64

# Platform event loop policy config
if sys.platform == 'win32':
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except Exception:
        pass

# Page Configuration
st.set_page_config(page_title="LLM-Based Autonomous Browser Agent", page_icon="⚡", layout="wide")

# Theme setup fallback
bg_img_css = ""
if os.path.exists("background.png"):
    try:
        with open("background.png", "rb") as f:
            bin_str = base64.b64encode(f.read()).decode()
        bg_img_css = f"background-image: url('data:image/png;base64,{bin_str}');"
    except Exception:
        pass

# UI Custom Style Inject
st.markdown(f"""
<style>
.stAppViewContainer {{
    background-color: #0f1117;
    {bg_img_css}
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}

/* Styled Panel Cards */
.card-container {{
    background-color: #161b27;
    border: 1px solid #2d3748;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    color: #f1f5f9;
}}
.custom-badge {{
    background-color: #2563eb;
    color: white;
    padding: 0.3rem 0.6rem;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 600;
}}
div.stButton > button {{
    background-color: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
}}
div.stButton > button:hover {{
    background-color: #3b82f6 !important;
}}
</style>
""", unsafe_allow_html=True)

# Session State Initializations
states = {
    "logged_in": False,
    "user_email": "",
    "profile": {},
    "history": [],
    "selected_task": "",
    "submit_pending": False,
    "submit_context": {},
    "language": "English",
    "voice_enabled": False,
    "browser_instance": None
}
for key, value in states.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Initialize browser state once for persistency across sequential agents
if st.session_state.browser_instance is None and st.session_state.logged_in:
    from browser_use import Browser

    # Safe dynamic initialization to adapt to any browser-use version parameters
    try:
        st.session_state.browser_instance = Browser(headless=False)
    except TypeError:
        try:
            from browser_use import BrowserProfile
            profile = BrowserProfile(headless=False)
            st.session_state.browser_instance = Browser(browser_profile=profile)
        except Exception:
            st.session_state.browser_instance = Browser()

# Async safe wrapper to run coroutines in Streamlit context
def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    if loop.is_running():
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(lambda: asyncio.run(coro))
            return future.result()
    else:
        return loop.run_until_complete(coro)

# Agent Routing & Mapping Execution Flow
async def execute_task(task_text, profile):
    import translator
    import general_agent
    import youtube_agent
    import whatsapp_agent
    import scholarship_agent
    import internship_agent
    import linkedin_apply_agent
    import company_careers_agent
    import data_extraction_agent

    # 1. Translation layer
    translated_text = translator.translate_to_english(task_text)
    translated_lower = translated_text.lower()
    
    # Check for browser instance availability
    br = st.session_state.browser_instance

    # 2. Match URLs first
    url_match = re.search(r"https?://[^\s]+", task_text)
    agent_type = ""
    result = ""

    if url_match:
        url = url_match.group(0)
        if "linkedin.com" in url:
            agent_type = "LinkedIn Easy Apply Agent"
            result = await linkedin_apply_agent.apply_linkedin(url, profile, browser=br)
        else:
            agent_type = "Company Career Portal Agent"
            result = await company_careers_agent.apply_company(task_text, profile, browser=br)
    else:
        # 3. Match Specific Keywords
        if any(k in translated_lower for k in ["whatsapp", "send message", "send file"]):
            agent_type = "WhatsApp Web Agent"
            result = await whatsapp_agent.send_whatsapp(translated_text, profile, browser=br)
        elif "scholarship" in translated_lower:
            agent_type = "Scholarship Search Agent"
            result = await scholarship_agent.main(translated_text, profile, browser=br)
        elif "internship" in translated_lower:
            agent_type = "Internship Application Agent"
            result = await internship_agent.main(translated_text, profile, browser=br)
        elif any(k in translated_lower for k in ["youtube", "video", "play", "watch", "song", "music"]) and not any(k in translated_lower for k in ["extract", "scrape"]):
            agent_type = "YouTube Video Agent"
            result = await youtube_agent.run_youtube(translated_text, browser=br)
        elif any(k in translated_lower for k in ["careers", "apply at", "apply for", "jobs at"]):
            agent_type = "Company Career Portal Agent"
            result = await company_careers_agent.apply_company(translated_text, profile, browser=br)
        elif any(k in translated_lower for k in ["extract", "scrape", "summarize", "analyze", "get data", "geeksforgeeks", "w3schools", "wikipedia"]):
            agent_type = "Data Extraction Agent"
            result = await data_extraction_agent.extract_data(translated_text, browser=br)
        else:
            agent_type = "General Web Agent"
            result = await general_agent.run_general(translated_text, profile, browser=br)
            
    return agent_type, result

# AUTH PANEL UI
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>⚡ LLM-Based Autonomous Browser Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Form filling, automation, and tasks executed programmatically</p>", unsafe_allow_html=True)
    
    auth_left, auth_center, auth_right = st.columns([1, 2, 1])
    with auth_center:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        tab_login, tab_register = st.tabs(["Sign In", "Create Account"])
        
        with tab_login:
            st.subheader("Login")
            email_in = st.text_input("Email", key="li_email").strip()
            pass_in = st.text_input("Password", type="password", key="li_pass")
            if st.button("Log In", use_container_width=True):
                if email_in and pass_in:
                    import auth
                    import profile_builder
                    success, msg, prof = auth.login(email_in, pass_in)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_email = email_in
                        st.session_state.profile = profile_builder.build_full_profile(prof)
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please fill out all credentials.")
                    
        with tab_register:
            st.subheader("Register")
            name_rg = st.text_input("Name", key="rg_name").strip()
            email_rg = st.text_input("Email Address", key="rg_email").strip()
            phone_rg = st.text_input("Phone Number", key="rg_phone").strip()
            pass_rg = st.text_input("Password", type="password", key="rg_pass")
            deg_rg = st.text_input("Degree", key="rg_degree").strip()
            coll_rg = st.text_input("College", key="rg_college").strip()
            grad_rg = st.text_input("Graduation Year", key="rg_grad").strip()
            city_rg = st.text_input("City", key="rg_city").strip()
            skills_rg = st.text_area("Skills (Comma Separated)", key="rg_skills").strip()
            linked_rg = st.text_input("LinkedIn URL", key="rg_linkedin").strip()
            pdf_rg = st.file_uploader("Upload Resume PDF", type=["pdf"])
            
            if st.button("Create Account", use_container_width=True):
                if name_rg and email_rg and pass_rg:
                    res_path = ""
                    if pdf_rg:
                        res_path = f"resume_{email_rg.replace('@', '_').replace('.', '_')}.pdf"
                        with open(res_path, "wb") as file_writer:
                            file_writer.write(pdf_rg.getbuffer())
                    
                    profile_payload = {
                        "name": name_rg,
                        "email": email_rg,
                        "phone": phone_rg,
                        "degree": deg_rg,
                        "college": coll_rg,
                        "graduation_year": grad_rg,
                        "city": city_rg,
                        "skills": skills_rg,
                        "linkedin": linked_rg,
                        "resume_path": res_path
                    }
                    import auth
                    success, msg = auth.create_account(email_rg, pass_rg, profile_payload)
                    if success:
                        st.success(msg + " Try logging in.")
                    else:
                        st.error(msg)
                else:
                    st.error("Fields Name, Email, and Password must be completed.")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # MAIN AGENT INTERFACE
    from voice_output import GTTS_LANG_CODES
    
    # Sidebar Setup
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.profile.get('name', 'Operator')}")
        st.markdown(f"📧 `{st.session_state.user_email}`")
        st.markdown("---")
        
        with st.expander("📝 My Profile Details", expanded=False):
            st.write(f"**Phone:** {st.session_state.profile.get('phone', 'N/A')}")
            st.write(f"**Degree:** {st.session_state.profile.get('degree', 'N/A')}")
            st.write(f"**College:** {st.session_state.profile.get('college', 'N/A')}")
            st.write(f"**Grad Year:** {st.session_state.profile.get('graduation_year', 'N/A')}")
            st.write(f"**City:** {st.session_state.profile.get('city', 'N/A')}")
            
            resume_loc = st.session_state.profile.get("resume_path", "")
            if resume_loc and os.path.exists(resume_loc):
                st.success("📄 Resume active")
            else:
                st.warning("⚠️ No resume found")
                new_pdf = st.file_uploader("Upload Resume PDF", type=["pdf"], key="side_resume_up")
                if new_pdf:
                    res_path = f"resume_{st.session_state.user_email.replace('@', '_').replace('.', '_')}.pdf"
                    with open(res_path, "wb") as f_write:
                        f_write.write(new_pdf.getbuffer())
                    st.session_state.profile["resume_path"] = res_path
                    import profile_builder, auth
                    st.session_state.profile = profile_builder.build_full_profile(st.session_state.profile)
                    auth.update_profile(st.session_state.user_email, st.session_state.profile)
                    st.success("Resume saved successfully.")
                    st.rerun()

        # Quick inline Profile Modification
        edit_profile = st.checkbox("⚙️ Edit Profile Details")
        if edit_profile:
            with st.form("quick_edit_profile"):
                edt_name = st.text_input("Name", value=st.session_state.profile.get("name", ""))
                edt_phone = st.text_input("Phone", value=st.session_state.profile.get("phone", ""))
                edt_degree = st.text_input("Degree", value=st.session_state.profile.get("degree", ""))
                edt_college = st.text_input("College", value=st.session_state.profile.get("college", ""))
                edt_grad = st.text_input("Grad Year", value=st.session_state.profile.get("graduation_year", ""))
                edt_city = st.text_input("City", value=st.session_state.profile.get("city", ""))
                edt_skills = st.text_area("Skills", value=st.session_state.profile.get("skills", ""))
                
                if st.form_submit_button("Save changes"):
                    import profile_builder, auth
                    updated_data = {
                        **st.session_state.profile,
                        "name": edt_name,
                        "phone": edt_phone,
                        "degree": edt_degree,
                        "college": edt_college,
                        "graduation_year": edt_grad,
                        "city": edt_city,
                        "skills": edt_skills
                    }
                    full_p = profile_builder.build_full_profile(updated_data)
                    success, msg = auth.update_profile(st.session_state.user_email, full_p)
                    if success:
                        st.session_state.profile = full_p
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                        
        st.markdown("---")
        
        # --- Updated State-Persistent API Configurations Block ---
        st.markdown("#### 🔑 Provider Keys")
        provider = st.radio("Provider Selection", ["browser-use Cloud", "OpenAI", "Gemini / Google"], index=1)
        st.session_state["api_provider"] = provider
        
        # Pull standard key based on active radio selection
        if provider == "OpenAI":
            default_key = os.getenv("OPENAI_API_KEY", "")
        elif provider == "Gemini / Google":
            default_key = os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")
        else:
            default_key = ""

        api_key_val = st.text_input("Enter API Key", type="password", value=default_key)
        st.session_state["api_key_val"] = api_key_val.strip()
        
        if api_key_val.strip():
            if provider == "OpenAI":
                os.environ["OPENAI_API_KEY"] = api_key_val.strip()
                os.environ["GEMINI_API_KEY"] = ""  # Clear Gemini
                os.environ["GOOGLE_API_KEY"] = ""
            elif provider == "Gemini / Google":
                os.environ["GEMINI_API_KEY"] = api_key_val.strip()
                os.environ["GOOGLE_API_KEY"] = api_key_val.strip()
                os.environ["OPENAI_API_KEY"] = ""  # Clear OpenAI
                
            st.markdown('<span class="custom-badge">Connected</span>', unsafe_allow_html=True)
        else:
            # Clear standard environment keys if box is blank
            if provider == "OpenAI":
                os.environ["OPENAI_API_KEY"] = ""
            elif provider == "Gemini / Google":
                os.environ["GEMINI_API_KEY"] = ""
                os.environ["GOOGLE_API_KEY"] = ""
            st.markdown('<span class="custom-badge" style="background-color: #ef4444;">Disconnected</span>', unsafe_allow_html=True)
        
        # Task History
        st.markdown("#### 🕒 Recent Tasks")
        if st.session_state.history:
            unique_tasks = []
            for item in reversed(st.session_state.history):
                if item["task"] not in unique_tasks:
                    unique_tasks.append(item["task"])
                if len(unique_tasks) >= 5:
                    break
            for t in unique_tasks:
                if st.button(f"🔄 {t[:30]}...", key=f"rec_task_{t}"):
                    st.session_state.selected_task = t
                    st.rerun()
        else:
            st.info("No past activities.")
            
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.session_state.profile = {}
            st.session_state.history = []
            st.session_state.submit_pending = False
            if st.session_state.browser_instance:
                # Browser cleanup
                try:
                    asyncio.run(st.session_state.browser_instance.close())
                except Exception:
                    pass
                st.session_state.browser_instance = None
            st.rerun()

    # CORE USER PANEL VIEW
    st.markdown("<h2>⚡ LLM-Based Autonomous Browser Agent</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8;'>Perform complex operations, browser scraping, or job applications autonomously.</p>", unsafe_allow_html=True)

    # SUBMIT AUTHORIZATION OVERLAY
    if st.session_state.submit_pending:
        st.markdown('<div class="card-container" style="border: 2px solid #2563eb;">', unsafe_allow_html=True)
        st.subheader("⚠️ Application Ready for Submission")
        platform_info = st.session_state.submit_context.get("platform", "Form Portal")
        st.write(f"The browser-agent successfully populated the fields on **{platform_info}**.")
        st.warning("Would you like the agent to proceed and perform the final submit click?")
        
        col_auth_yes, col_auth_no = st.columns(2)
        with col_auth_yes:
            if st.button("🚀 Authorize and Submit"):
                import submit_agent
                with st.spinner("Submitting application..."):
                    res_sub = run_async(submit_agent.click_submit(platform_info, st.session_state.profile, browser=st.session_state.browser_instance))
                st.success(res_sub)
                st.session_state.history.append({
                    "task": "Final Submit Trigger",
                    "agent": "Submit Agent",
                    "result": res_sub
                })
                if st.session_state.voice_enabled:
                    from voice_output import speak
                    speak("Submission completed successfully.", st.session_state.language)
                st.session_state.submit_pending = False
                st.session_state.submit_context = {}
                st.rerun()
        with col_auth_no:
            if st.button("❌ Cancel / Complete Manually"):
                st.info("Submission cancelled. The portal remains loaded inside the window for manual reviews.")
                st.session_state.submit_pending = False
                st.session_state.submit_context = {}
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # USER INLINE CONTROLS
    col_input_box, col_go_btn, col_voice_btn = st.columns([5, 1, 1])
    
    with col_input_box:
        task_query = st.text_input(
            "Enter tasks:",
            value=st.session_state.selected_task,
            placeholder="e.g., Apply for SWE internship at Stripe or search scholarships on NSP"
        )
        
    def trigger_agent_execution(command):
        if not command.strip():
            st.error("Query cannot be blank.")
            return
            
        with st.spinner(f"Agent executing your task: '{command}'..."):
            try:
                agent, outcome = run_async(execute_task(command, st.session_state.profile))
                
                # Render outcome card
                st.markdown("### 📋 Agent Outcome Log")
                st.markdown(f"""
                <div class="card-container">
                    <h4>🤖 {agent}</h4>
                    <p>{outcome}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Append to persistent trace
                st.session_state.history.append({
                    "task": command,
                    "agent": agent,
                    "result": outcome
                })
                
                # Activate submission gate flags
                if any(x in agent for x in ["LinkedIn", "Career", "Internship"]):
                    st.session_state.submit_pending = True
                    st.session_state.submit_context = {
                        "platform": agent,
                        "task": command
                    }
                
                # Perform voice vocalizations
                if st.session_state.voice_enabled:
                    from voice_output import speak
                    speak(f"Completed. {outcome}", st.session_state.language)
                    
                st.rerun()
            except Exception as e:
                st.error(f"Task runtime failure: {e}")

    with col_go_btn:
        if st.button("Run Task", use_container_width=True):
            trigger_agent_execution(task_query)
            
    with col_voice_btn:
        if st.button("🎤 Speak", use_container_width=True):
            from voice_input import listen
            with st.spinner("Listening..."):
                heard_command = listen(st.session_state.language)
            if "Error:" in heard_command:
                st.error(heard_command)
            else:
                st.success(f"Recognized: {heard_command}")
                st.session_state.selected_task = heard_command
                trigger_agent_execution(heard_command)

    # Execution History Panel
    if st.session_state.history:
        st.markdown("### 📝 Detailed Runtime Activity")
        for entry in reversed(st.session_state.history):
            with st.expander(f"Task: {entry['task'][:50]}... | {entry.get('agent', 'System')}", expanded=False):
                st.markdown(entry["result"])