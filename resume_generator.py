from fpdf import FPDF, XPos, YPos
import json 
import os   # Import os module for file path operations

def save_resume_data(data, filename="resume_data.json"):
    # Saves the resume data to a JSON file.
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Resume data saved successfully to '{filename}'")
    except IOError as e:
        print(f"Error saving data to '{filename}': {e}")

def load_resume_data(filename="resume_data.json"):
    # Loads resume data from a JSON file.
    if not os.path.exists(filename):
        print(f"File '{filename}' not found.")
        return None
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Resume data loaded successfully from '{filename}'")
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from '{filename}': {e}")
        return None
    except IOError as e:
        print(f"Error loading data from '{filename}': {e}")
        return None

def collect_resume_data():
    # Collects all resume data from the user via command-line input.
    data = {}

    print("\n--- Personal Information ---")
    data["name"] = input("Enter your Full Name: ")
    data["email"] = input("Enter your Email Address: ")
    data["phone"] = input("Enter your Phone Number: ")
    data["linkedin"] = input("Enter your LinkedIn Profile URL (optional, press Enter to skip): ")

    print("\n--- Summary/Objective ---")
    data["summary"] = input("Enter your Professional Summary or Objective: ")

    print("\n--- Education ---")
    education_entries = []
    while True:
        degree = input("Enter Degree (e.g., Bachelor of Science in Computer Science) (or 'done' to finish): ")
        if degree.lower() == 'done':
            break
        university = input("Enter University Name: ")
        year = input("Enter Graduation Year: ")
        education_entries.append({
            "degree": degree,
            "university": university,
            "year": year
        })
        print("Education entry added. Add another?")
    data["education"] = education_entries

    print("\n--- Experience ---")
    experience_entries = []
    while True:
        title = input("Enter Job Title (or 'done' to finish): ")
        if title.lower() == 'done':
            break
        company = input("Enter Company Name: ")
        dates = input("Enter Dates (e.g., Jan 2020 - Dec 2023): ")
        description_points = []
        print("Enter bullet points for responsibilities/achievements (type 'done' on an empty line to finish):")
        while True:
            point = input("- ")
            if point.lower() == 'done':
                break
            elif not point:
                continue
            description_points.append(point)
        experience_entries.append({
            "title": title,
            "company": company,
            "dates": dates,
            "description": description_points
        })
        print("Experience entry added. Add another?")
    data["experience"] = experience_entries

    print("\n--- Projects ---")
    project_entries = []
    while True:
        project_name = input("Enter Project Name (or 'done' to finish): ")
        if project_name.lower() == 'done':
            break
        project_link = input("Enter Project Link (optional, e.g., GitHub URL): ")
        project_dates = input("Enter Project Dates (e.g., Mar 2024 - May 2024): ")
        project_description = []
        print("Enter bullet points for project details/contributions (type 'done' on an empty line to finish):")
        while True:
            point = input("- ")
            if point.lower() == 'done':
                break
            elif not point:
                continue
            project_description.append(point)
        project_entries.append({
            "name": project_name,
            "link": project_link,
            "dates": project_dates,
            "description": project_description
        })
        print("Project entry added. Add another?")
    data["projects"] = project_entries

    print("\n--- Awards and Honors ---")
    award_entries = []
    while True:
        award_name = input("Enter Award Name (or 'done' to finish): ")
        if award_name.lower() == 'done':
            break
        awarding_body = input("Enter Awarding Body/Institution: ")
        award_date = input("Enter Date Received (e.g., Dec 2023): ")
        award_entries.append({
            "name": award_name,
            "body": awarding_body,
            "date": award_date
        })
        print("Award entry added. Add another?")
    data["awards"] = award_entries

    print("\n--- Volunteer Work ---")
    volunteer_entries = []
    while True:
        role = input("Enter Volunteer Role (or 'done' to finish): ")
        if role.lower() == 'done':
            break
        organization = input("Enter Organization Name: ")
        dates = input("Enter Dates (e.g., Sep 2022 - Aug 2023): ")
        description_points = []
        print("Enter bullet points for responsibilities/contributions (type 'done' on an empty line to finish):")
        while True:
            point = input("- ")
            if point.lower() == 'done':
                break
            elif not point:
                continue
            description_points.append(point)
        volunteer_entries.append({
            "role": role,
            "organization": organization,
            "dates": dates,
            "description": description_points
        })
        print("Volunteer work entry added. Add another?")
    data["volunteer_work"] = volunteer_entries

    print("\n--- Skills ---")
    skills_raw = input("Enter your skills, separated by commas (e.g., Python, Java, SQL): ")
    data["skills"] = [s.strip() for s in skills_raw.split(',') if s.strip()]

    return data


pdf_global_instance = None # Will be initialized in main

TEXT_COLOR = (30, 30, 30)
SECTION_HEADER_COLOR = (0, 0, 0)

def add_section_header(pdf_obj, text):
    pdf_obj.ln(5)
    pdf_obj.set_font("DejaVu", "B", size=12)
    pdf_obj.set_text_color(*SECTION_HEADER_COLOR)
    pdf_obj.cell(0, 10, text, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf_obj.line(pdf_obj.get_x(), pdf_obj.get_y(), pdf_obj.w - pdf_obj.r_margin, pdf_obj.get_y())
    pdf_obj.ln(5)
    pdf_obj.set_font("DejaVu", size=10)
    pdf_obj.set_text_color(*TEXT_COLOR)

def generate_resume_pdf(data, pdf_obj):
    pdf_obj.add_page() # Add page at the start of generation
    pdf_obj.set_auto_page_break(auto=True, margin=15)

    # Add a Unicode font (DejaVuSans.ttf needs to be in the same directory as this script)
    pdf_obj.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf_obj.add_font("DejaVu", "B", "DejaVuSans-Bold.ttf", uni=True)
    pdf_obj.set_text_color(*TEXT_COLOR) # Ensure text color is set for this PDF instance

    # Name and Contact Info
    pdf_obj.set_font("DejaVu", "B", size=20)
    pdf_obj.cell(0, 10, data["name"], align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf_obj.set_font("DejaVu", size=8)
    contact_info = f"{data['phone']} | {data['email']}"
    if data["linkedin"]:
        contact_info += f" | {data['linkedin']}"
    pdf_obj.cell(0, 5, contact_info, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf_obj.ln(10)

    # Summary
    if data["summary"]:
        add_section_header(pdf_obj, "Summary")
        pdf_obj.multi_cell(0, 5, data["summary"])

    # Education
    if data["education"]:
        add_section_header(pdf_obj, "Education") 
        for edu in data["education"]:
            pdf_obj.set_font("DejaVu", "B", size=10)
            pdf_obj.cell(0, 5, f"{edu['degree']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf_obj.set_font("DejaVu", size=10)
            pdf_obj.cell(0, 5, f"{edu['university']} - {edu['year']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf_obj.ln(2)


    # Experience
    if data["experience"]:
        add_section_header(pdf_obj, "Experience") 
        for exp in data["experience"]:
            pdf_obj.set_font("DejaVu", "B", size=10)
            pdf_obj.cell(0, 5, f"{exp['title']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf_obj.set_font("DejaVu", size=10)
            pdf_obj.cell(0, 5, f"{exp['company']} | {exp['dates']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            original_x = pdf_obj.get_x()
            indent_amount = 4
            for item in exp["description"]:
                pdf_obj.set_x(original_x + indent_amount)
                pdf_obj.multi_cell(0, 5, f"• {item}")
            pdf_obj.set_x(original_x)
            pdf_obj.ln(2)

    # Projects
    if data["projects"]:
        add_section_header(pdf_obj, "Projects") 
        for proj in data["projects"]:
            pdf_obj.set_font("DejaVu", "B", size=10)
            pdf_obj.cell(0, 5, f"{proj['name']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf_obj.set_font("DejaVu", size=10)
            if proj["link"]:
                pdf_obj.cell(0, 5, f"{proj['dates']} | {proj['link']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            else:
                pdf_obj.cell(0, 5, f"{proj['dates']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            original_x = pdf_obj.get_x()
            indent_amount = 5
            for item in proj["description"]:
                pdf_obj.set_x(original_x + indent_amount)
                pdf_obj.multi_cell(0, 5, f"• {item}")
            pdf_obj.set_x(original_x)
            pdf_obj.ln(2)

    # Awards
    if data["awards"]:
        add_section_header(pdf_obj, "Awards & Honors") 
        for award in data["awards"]:
            pdf_obj.set_font("DejaVu", "B", size=10)
            pdf_obj.cell(0, 5, f"{award['name']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf_obj.set_font("DejaVu", size=10)
            pdf_obj.cell(0, 5, f"{award['body']} - {award['date']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf_obj.ln(2)

    # Volunteer Work
    if data["volunteer_work"]:
        add_section_header(pdf_obj, "Volunteer Work") 
        for vol in data["volunteer_work"]:
            pdf_obj.set_font("DejaVu", "B", size=10)
            pdf_obj.cell(0, 5, f"{vol['role']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf_obj.set_font("DejaVu", size=10)
            pdf_obj.cell(0, 5, f"{vol['organization']} | {vol['dates']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            original_x = pdf_obj.get_x()
            indent_amount = 5
            for item in vol["description"]:
                pdf_obj.set_x(original_x + indent_amount)
                pdf_obj.multi_cell(0, 5, f"• {item}")
            pdf_obj.set_x(original_x)
            pdf_obj.ln(2)

    # Skills
    if data["skills"]:
        add_section_header(pdf_obj, "Skills") 
        skills_text = ", ".join(data["skills"])
        pdf_obj.multi_cell(0, 5, skills_text)

