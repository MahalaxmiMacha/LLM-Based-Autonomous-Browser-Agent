import os

def extract_pdf_text(pdf_path: str) -> str:
    if not pdf_path or not os.path.exists(pdf_path):
        return ""
    
    # Try pdfplumber
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text.strip()
    except Exception as e:
        print(f"pdfplumber extraction warning: {e}. Attempting pypdf fallback...")
        
    # Fallback to pypdf
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"pypdf extraction warning: {e}")
        return ""

def build_full_profile(profile: dict) -> dict:
    resume_path = profile.get("resume_path", "")
    resume_text = ""
    if resume_path:
        resume_text = extract_pdf_text(resume_path)
        
    full_name = profile.get("name", "")
    parts = full_name.split()
    first_name = parts[0] if parts else ""
    last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

    full_profile = {
        "name": full_name,
        "first_name": first_name,
        "last_name": last_name,
        "email": profile.get("email", ""),
        "phone": profile.get("phone", ""),
        "phone_country_code": profile.get("phone_country_code") or "+91",
        "city": profile.get("city") or "Mumbai",
        "country": profile.get("country") or "India",
        "state": profile.get("state") or "Maharashtra",
        "zip_code": profile.get("zip_code") or "400001",
        "degree": profile.get("degree") or "B.Tech Computer Science",
        "college": profile.get("college") or "IIT Bombay",
        "graduation_year": profile.get("graduation_year") or "2026",
        "gpa": profile.get("gpa") or "8.5/10",
        "skills": profile.get("skills") or "Python, SQL, Streamlit, LangChain, Machine Learning",
        "linkedin": profile.get("linkedin") or "",
        "github": profile.get("github") or "",
        "years_of_experience": profile.get("years_of_experience") or "0",
        "experience_level": profile.get("experience_level") or "Fresher",
        "notice_period": profile.get("notice_period") or "Immediate",
        "expected_salary": profile.get("expected_salary") or "Negotiable",
        "gender": profile.get("gender") or "Male",
        "disability": profile.get("disability") or "No",
        "veteran_status": profile.get("veteran_status") or "No",
        "work_authorization": profile.get("work_authorization") or "Yes",
        "require_sponsorship": profile.get("require_sponsorship") or "No",
        "citizenship": profile.get("citizenship") or "Indian",
        "willing_to_relocate": profile.get("willing_to_relocate") or "Yes",
        "available_from": profile.get("available_from") or "Immediate",
        "cover_letter": profile.get("cover_letter") or (
            f"Dear Hiring Manager,\n\nI am writing to express my strong interest in the opportunity. "
            f"With skills in {profile.get('skills', 'software development')} and my background, "
            f"I am eager to contribute effectively to your team.\n\nSincerely,\n{full_name}"
        ),
        "resume_path": resume_path,
        "resume_text": resume_text or profile.get("resume_text", "")
    }
    
    return full_profile