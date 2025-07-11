import customtkinter as ctk
import tkinter as tk # We might still need some basic tkinter constants/exceptions
from tkinter import filedialog, messagebox # For file dialogs and pop-up messages
import os


from resume_generator import collect_resume_data, generate_resume_pdf, save_resume_data, load_resume_data, FPDF # Import FPDF as well

class ResumeBuilderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Python Resume Builder")
        self.geometry("800x700") # Set initial window size
        self.resizable(True, True) # Allow resizing

        # Configure grid layout for the main window (1 column, 2 rows for example)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Row for scrollable frame

        # --- Top Control Frame ---
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_columnconfigure(1, weight=1)
        self.control_frame.grid_columnconfigure(2, weight=1)

        self.load_button = ctk.CTkButton(self.control_frame, text="Load Resume", command=self.load_resume_gui)
        self.load_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.save_button = ctk.CTkButton(self.control_frame, text="Save Resume", command=self.save_resume_gui)
        self.save_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.generate_pdf_button = ctk.CTkButton(self.control_frame, text="Generate PDF", command=self.generate_pdf_gui)
        self.generate_pdf_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # --- Scrollable Frame for Resume Sections ---
        # This will hold all our input fields
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Resume Details")
        self.scrollable_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1) # Allow content to expand horizontally

        # --- Data Storage ---
        self.resume_data = {} # This will hold the current resume data (similar to the dict in CLI)
        self.current_json_filename = None # To track which file we loaded/saved from

        # --- Build the UI for sections (placeholders for now) ---
        self._create_personal_info_section()
        self._create_summary_section()
        self._create_education_section() # Will need dynamic handling
        self._create_experience_section() # Will need dynamic handling
        self._create_projects_section()   # Will need dynamic handling
        self._create_awards_section()     # Will need dynamic handling
        self._create_volunteer_section()  # Will need dynamic handling
        self._create_skills_section()

    def _create_personal_info_section(self):
        # We'll create a new frame for each section to keep them organized
        personal_info_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        personal_info_frame.pack(fill="x", padx=10, pady=5)
        personal_info_frame.grid_columnconfigure(1, weight=1) # Allow entry field to expand

        ctk.CTkLabel(personal_info_frame, text="Personal Information", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,5))

        ctk.CTkLabel(personal_info_frame, text="Full Name:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.name_entry = ctk.CTkEntry(personal_info_frame)
        self.name_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(personal_info_frame, text="Email:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.email_entry = ctk.CTkEntry(personal_info_frame)
        self.email_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(personal_info_frame, text="Phone:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.phone_entry = ctk.CTkEntry(personal_info_frame)
        self.phone_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

        ctk.CTkLabel(personal_info_frame, text="LinkedIn:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.linkedin_entry = ctk.CTkEntry(personal_info_frame)
        self.linkedin_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=2)


    def _create_summary_section(self):
        summary_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        summary_frame.pack(fill="x", padx=10, pady=5)
        summary_frame.grid_columnconfigure(0, weight=1) # Allow text area to expand

        ctk.CTkLabel(summary_frame, text="Summary/Objective", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", pady=(0,5))
        self.summary_textbox = ctk.CTkTextbox(summary_frame, height=100, wrap="word") # wrap="word" for soft wrapping
        self.summary_textbox.grid(row=1, column=0, sticky="ew", padx=5, pady=2)


    def _create_education_section(self):
        # Education and other list-based sections will be more complex.
        # We'll use a frame to hold existing entries and an "Add New" button.
        self.education_frames = [] # To keep track of individual education entry frames

        self.education_section_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.education_section_frame.pack(fill="x", padx=10, pady=5)
        self.education_section_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.education_section_frame, text="Education", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", pady=(0,5))

        # Frame to hold dynamic education entries
        self.education_entries_container = ctk.CTkFrame(self.education_section_frame, fg_color="transparent")
        self.education_entries_container.grid(row=1, column=0, sticky="ew")
        self.education_entries_container.grid_columnconfigure(0, weight=1)


        self.add_education_button = ctk.CTkButton(self.education_section_frame, text="Add New Education", command=self._add_education_entry_gui)
        self.add_education_button.grid(row=2, column=0, sticky="w", pady=5)

    def _add_education_entry_gui(self, initial_values=None):
        # Creates a new set of input fields for one education entry
        # initial_values will be a dict if loading, or None if adding new
        entry_frame = ctk.CTkFrame(self.education_entries_container, border_width=1, corner_radius=8)
        entry_frame.pack(fill="x", padx=5, pady=5)
        entry_frame.grid_columnconfigure(1, weight=1)

        row_num = 0
        ctk.CTkLabel(entry_frame, text="Degree:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        degree_entry = ctk.CTkEntry(entry_frame)
        degree_entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        ctk.CTkLabel(entry_frame, text="University:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        university_entry = ctk.CTkEntry(entry_frame)
        university_entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        ctk.CTkLabel(entry_frame, text="Year:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        year_entry = ctk.CTkEntry(entry_frame)
        year_entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        if initial_values: # Populate if initial data is provided (e.g., from loading)
            degree_entry.insert(0, initial_values.get("degree", ""))
            university_entry.insert(0, initial_values.get("university", ""))
            year_entry.insert(0, initial_values.get("year", ""))

        # Button to remove this specific entry
        remove_button = ctk.CTkButton(entry_frame, text="Remove", command=lambda: self._remove_education_entry_gui(entry_frame))
        remove_button.grid(row=row_num, column=0, columnspan=2, pady=5, sticky="e")

        self.education_frames.append({
            "frame": entry_frame,
            "degree": degree_entry,
            "university": university_entry,
            "year": year_entry
        })

    def _remove_education_entry_gui(self, entry_frame_to_remove):
        entry_frame_to_remove.destroy() # Remove the frame from the UI
        # Also remove it from our internal tracking list
        self.education_frames = [
            item for item in self.education_frames if item["frame"] != entry_frame_to_remove
        ]

    # --- Placeholder methods for other sections (will be similar to education) ---
    def _create_experience_section(self):
        # Similar structure to education, but with textbox for description
        self.experience_frames = []
        self.experience_section_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.experience_section_frame.pack(fill="x", padx=10, pady=5)
        self.experience_section_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.experience_section_frame, text="Experience", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", pady=(0,5))
        self.experience_entries_container = ctk.CTkFrame(self.experience_section_frame, fg_color="transparent")
        self.experience_entries_container.grid(row=1, column=0, sticky="ew")
        self.experience_entries_container.grid_columnconfigure(0, weight=1)
        self.add_experience_button = ctk.CTkButton(self.experience_section_frame, text="Add New Experience", command=self._add_experience_entry_gui)
        self.add_experience_button.grid(row=2, column=0, sticky="w", pady=5)

    def _add_experience_entry_gui(self, initial_values=None):
        entry_frame = ctk.CTkFrame(self.experience_entries_container, border_width=1, corner_radius=8)
        entry_frame.pack(fill="x", padx=5, pady=5)
        entry_frame.grid_columnconfigure(1, weight=1)

        row_num = 0
        ctk.CTkLabel(entry_frame, text="Title:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        title_entry = ctk.CTkEntry(entry_frame)
        title_entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        ctk.CTkLabel(entry_frame, text="Company:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        company_entry = ctk.CTkEntry(entry_frame)
        company_entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        ctk.CTkLabel(entry_frame, text="Dates:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        dates_entry = ctk.CTkEntry(entry_frame)
        dates_entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        ctk.CTkLabel(entry_frame, text="Description:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        description_textbox = ctk.CTkTextbox(entry_frame, height=70, wrap="word")
        description_textbox.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        if initial_values:
            title_entry.insert(0, initial_values.get("title", ""))
            company_entry.insert(0, initial_values.get("company", ""))
            dates_entry.insert(0, initial_values.get("dates", ""))
            if initial_values.get("description"):
                # Join list of points with newline for textbox
                description_textbox.insert("0.0", "\n".join(initial_values["description"]))

        remove_button = ctk.CTkButton(entry_frame, text="Remove", command=lambda: self._remove_experience_entry_gui(entry_frame))
        remove_button.grid(row=row_num, column=0, columnspan=2, pady=5, sticky="e")

        self.experience_frames.append({
            "frame": entry_frame,
            "title": title_entry,
            "company": company_entry,
            "dates": dates_entry,
            "description": description_textbox
        })


    def _remove_experience_entry_gui(self, entry_frame_to_remove):
        entry_frame_to_remove.destroy()
        self.experience_frames = [
            item for item in self.experience_frames if item["frame"] != entry_frame_to_remove
        ]

    def _create_projects_section(self):
        self.projects_frames = []
        self.projects_section_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.projects_section_frame.pack(fill="x", padx=10, pady=5)
        self.projects_section_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.projects_section_frame, text="Projects", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", pady=(0,5))
        self.projects_entries_container = ctk.CTkFrame(self.projects_section_frame, fg_color="transparent")
        self.projects_entries_container.grid(row=1, column=0, sticky="ew")
        self.projects_entries_container.grid_columnconfigure(0, weight=1)
        self.add_projects_button = ctk.CTkButton(self.projects_section_frame, text="Add New Project", command=self._add_project_entry_gui)
        self.add_projects_button.grid(row=2, column=0, sticky="w", pady=5)

    def _add_project_entry_gui(self, initial_values=None):
        entry_frame = ctk.CTkFrame(self.projects_entries_container, border_width=1, corner_radius=8)
        entry_frame.pack(fill="x", padx=5, pady=5)
        entry_frame.grid_columnconfigure(1, weight=1)
        
        # Project Name, Link, Dates, Description (similar to experience)
        row_num = 0
        ctk.CTkLabel(entry_frame, text="Name:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        name_entry = ctk.CTkEntry(entry_frame)
        name_entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        ctk.CTkLabel(entry_frame, text="Link:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        link_entry = ctk.CTkEntry(entry_frame)
        link_entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        ctk.CTkLabel(entry_frame, text="Dates:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        dates_entry = ctk.CTkEntry(entry_frame)
        dates_entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        ctk.CTkLabel(entry_frame, text="Description:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        description_textbox = ctk.CTkTextbox(entry_frame, height=70, wrap="word")
        description_textbox.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        if initial_values:
            name_entry.insert(0, initial_values.get("name", ""))
            link_entry.insert(0, initial_values.get("link", ""))
            dates_entry.insert(0, initial_values.get("dates", ""))
            if initial_values.get("description"):
                description_textbox.insert("0.0", "\n".join(initial_values["description"]))

        remove_button = ctk.CTkButton(entry_frame, text="Remove", command=lambda: self._remove_project_entry_gui(entry_frame))
        remove_button.grid(row=row_num, column=0, columnspan=2, pady=5, sticky="e")

        self.projects_frames.append({
            "frame": entry_frame,
            "name": name_entry,
            "link": link_entry,
            "dates": dates_entry,
            "description": description_textbox
        })
    def _remove_project_entry_gui(self, entry_frame_to_remove):
        entry_frame_to_remove.destroy()
        self.projects_frames = [
            item for item in self.projects_frames if item["frame"] != entry_frame_to_remove
        ]

    def _create_awards_section(self):
        self.awards_frames = []
        self.awards_section_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.awards_section_frame.pack(fill="x", padx=10, pady=5)
        self.awards_section_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.awards_section_frame, text="Awards & Honors", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", pady=(0,5))
        self.awards_entries_container = ctk.CTkFrame(self.awards_section_frame, fg_color="transparent")
        self.awards_entries_container.grid(row=1, column=0, sticky="ew")
        self.awards_entries_container.grid_columnconfigure(0, weight=1)
        self.add_awards_button = ctk.CTkButton(self.awards_section_frame, text="Add New Award", command=self._add_award_entry_gui)
        self.add_awards_button.grid(row=2, column=0, sticky="w", pady=5)

    def _add_award_entry_gui(self, initial_values=None):
        entry_frame = ctk.CTkFrame(self.awards_entries_container, border_width=1, corner_radius=8)
        entry_frame.pack(fill="x", padx=5, pady=5)
        entry_frame.grid_columnconfigure(1, weight=1)
        
        # Award Name, Body, Date (similar to education)
        row_num = 0
        ctk.CTkLabel(entry_frame, text="Award Name:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        name_entry = ctk.CTkEntry(entry_frame)
        name_entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        ctk.CTkLabel(entry_frame, text="Awarding Body:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        body_entry = ctk.CTkEntry(entry_frame)
        body_entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        ctk.CTkLabel(entry_frame, text="Date Received:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        date_entry = ctk.CTkEntry(entry_frame)
        date_entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        if initial_values:
            name_entry.insert(0, initial_values.get("name", ""))
            body_entry.insert(0, initial_values.get("body", ""))
            date_entry.insert(0, initial_values.get("date", ""))

        remove_button = ctk.CTkButton(entry_frame, text="Remove", command=lambda: self._remove_award_entry_gui(entry_frame))
        remove_button.grid(row=row_num, column=0, columnspan=2, pady=5, sticky="e")

        self.awards_frames.append({
            "frame": entry_frame,
            "name": name_entry,
            "body": body_entry,
            "date": date_entry
        })
    def _remove_award_entry_gui(self, entry_frame_to_remove):
        entry_frame_to_remove.destroy()
        self.awards_frames = [
            item for item in self.awards_frames if item["frame"] != entry_frame_to_remove
        ]

    def _create_volunteer_section(self):
        self.volunteer_frames = []
        self.volunteer_section_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.volunteer_section_frame.pack(fill="x", padx=10, pady=5)
        self.volunteer_section_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.volunteer_section_frame, text="Volunteer Work", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", pady=(0,5))
        self.volunteer_entries_container = ctk.CTkFrame(self.volunteer_section_frame, fg_color="transparent")
        self.volunteer_entries_container.grid(row=1, column=0, sticky="ew")
        self.volunteer_entries_container.grid_columnconfigure(0, weight=1)
        self.add_volunteer_button = ctk.CTkButton(self.volunteer_section_frame, text="Add New Volunteer Work", command=self._add_volunteer_entry_gui)
        self.add_volunteer_button.grid(row=2, column=0, sticky="w", pady=5)

    def _add_volunteer_entry_gui(self, initial_values=None):
        entry_frame = ctk.CTkFrame(self.volunteer_entries_container, border_width=1, corner_radius=8)
        entry_frame.pack(fill="x", padx=5, pady=5)
        entry_frame.grid_columnconfigure(1, weight=1)
        
        # Role, Organization, Dates, Description (similar to experience)
        row_num = 0
        ctk.CTkLabel(entry_frame, text="Role:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        role_entry = ctk.CTkEntry(entry_frame)
        role_entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        ctk.CTkLabel(entry_frame, text="Organization:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        org_entry = ctk.CTkEntry(entry_frame)
        org_entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        ctk.CTkLabel(entry_frame, text="Dates:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        dates_entry = ctk.CTkEntry(entry_frame)
        dates_entry.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        ctk.CTkLabel(entry_frame, text="Description:").grid(row=row_num, column=0, sticky="w", padx=5, pady=2)
        description_textbox = ctk.CTkTextbox(entry_frame, height=70, wrap="word")
        description_textbox.grid(row=row_num, column=1, sticky="ew", padx=5, pady=2)
        row_num += 1

        if initial_values:
            role_entry.insert(0, initial_values.get("role", ""))
            org_entry.insert(0, initial_values.get("organization", ""))
            dates_entry.insert(0, initial_values.get("dates", ""))
            if initial_values.get("description"):
                description_textbox.insert("0.0", "\n".join(initial_values["description"]))

        remove_button = ctk.CTkButton(entry_frame, text="Remove", command=lambda: self._remove_volunteer_entry_gui(entry_frame))
        remove_button.grid(row=row_num, column=0, columnspan=2, pady=5, sticky="e")

        self.volunteer_frames.append({
            "frame": entry_frame,
            "role": role_entry,
            "organization": org_entry,
            "dates": dates_entry,
            "description": description_textbox
        })
    def _remove_volunteer_entry_gui(self, entry_frame_to_remove):
        entry_frame_to_remove.destroy()
        self.volunteer_frames = [
            item for item in self.volunteer_frames if item["frame"] != entry_frame_to_remove
        ]

    def _create_skills_section(self):
        skills_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        skills_frame.pack(fill="x", padx=10, pady=5)
        skills_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(skills_frame, text="Skills (Comma Separated)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", pady=(0,5))
        self.skills_entry = ctk.CTkEntry(skills_frame)
        self.skills_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=2)

    # --- Methods to get data from GUI and set data to GUI ---

    def _get_data_from_gui(self):
        """Collects all data from the GUI widgets into a dictionary."""
        data = {}

        # Personal Info
        data["name"] = self.name_entry.get()
        data["email"] = self.email_entry.get()
        data["phone"] = self.phone_entry.get()
        data["linkedin"] = self.linkedin_entry.get()

        # Summary
        data["summary"] = self.summary_textbox.get("0.0", "end").strip() # Get all text from textbox

        # Education
        education_entries = []
        for edu_item in self.education_frames:
            education_entries.append({
                "degree": edu_item["degree"].get(),
                "university": edu_item["university"].get(),
                "year": edu_item["year"].get()
            })
        data["education"] = education_entries

        # Experience
        experience_entries = []
        for exp_item in self.experience_frames:
            description_text = exp_item["description"].get("0.0", "end").strip()
            description_points = [p.strip() for p in description_text.split('\n') if p.strip()]
            experience_entries.append({
                "title": exp_item["title"].get(),
                "company": exp_item["company"].get(),
                "dates": exp_item["dates"].get(),
                "description": description_points
            })
        data["experience"] = experience_entries

        # Projects
        projects_entries = []
        for proj_item in self.projects_frames:
            description_text = proj_item["description"].get("0.0", "end").strip()
            description_points = [p.strip() for p in description_text.split('\n') if p.strip()]
            projects_entries.append({
                "name": proj_item["name"].get(),
                "link": proj_item["link"].get(),
                "dates": proj_item["dates"].get(),
                "description": description_points
            })
        data["projects"] = projects_entries

        # Awards
        awards_entries = []
        for award_item in self.awards_frames:
            awards_entries.append({
                "name": award_item["name"].get(),
                "body": award_item["body"].get(),
                "date": award_item["date"].get()
            })
        data["awards"] = awards_entries

        # Volunteer Work
        volunteer_entries = []
        for vol_item in self.volunteer_frames:
            description_text = vol_item["description"].get("0.0", "end").strip()
            description_points = [p.strip() for p in description_text.split('\n') if p.strip()]
            volunteer_entries.append({
                "role": vol_item["role"].get(),
                "organization": vol_item["organization"].get(),
                "dates": vol_item["dates"].get(),
                "description": description_points
            })
        data["volunteer_work"] = volunteer_entries

        # Skills
        skills_text = self.skills_entry.get().strip()
        data["skills"] = [s.strip() for s in skills_text.split(',') if s.strip()]

        return data

    def _set_data_to_gui(self, data):
        """Populates GUI widgets with data from a dictionary (e.g., loaded data)."""
        # Clear existing multi-entry sections before populating
        self._clear_all_multi_entries()

        self.name_entry.delete(0, ctk.END)
        self.name_entry.insert(0, data.get("name", ""))

        self.email_entry.delete(0, ctk.END)
        self.email_entry.insert(0, data.get("email", ""))

        self.phone_entry.delete(0, ctk.END)
        self.phone_entry.insert(0, data.get("phone", ""))

        self.linkedin_entry.delete(0, ctk.END)
        self.linkedin_entry.insert(0, data.get("linkedin", ""))

        self.summary_textbox.delete("0.0", "end")
        self.summary_textbox.insert("0.0", data.get("summary", ""))

        # Populate multi-entry sections by adding entries
        for edu in data.get("education", []):
            self._add_education_entry_gui(edu)
        for exp in data.get("experience", []):
            self._add_experience_entry_gui(exp)
        for proj in data.get("projects", []):
            self._add_project_entry_gui(proj)
        for award in data.get("awards", []):
            self._add_award_entry_gui(award)
        for vol in data.get("volunteer_work", []):
            self._add_volunteer_entry_gui(vol)

        self.skills_entry.delete(0, ctk.END)
        self.skills_entry.insert(0, ", ".join(data.get("skills", [])))

        self.resume_data = data # Update internal data storage
        messagebox.showinfo("Load Success", "Resume data loaded into the form.")

    def _clear_all_multi_entries(self):
        # Helper to remove all dynamically added frames (Education, Experience, etc.)
        for item in list(self.education_frames): # Use list() to avoid issues when modifying list during iteration
            item["frame"].destroy()
        self.education_frames = []

        for item in list(self.experience_frames):
            item["frame"].destroy()
        self.experience_frames = []
        
        for item in list(self.projects_frames):
            item["frame"].destroy()
        self.projects_frames = []

        for item in list(self.awards_frames):
            item["frame"].destroy()
        self.awards_frames = []

        for item in list(self.volunteer_frames):
            item["frame"].destroy()
        self.volunteer_frames = []


    # --- Button Command Methods ---

    def load_resume_gui(self):
        file_path = filedialog.askopenfilename(
            title="Select Resume JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            loaded_data = load_resume_data(file_path)
            if loaded_data:
                self._set_data_to_gui(loaded_data)
                self.current_json_filename = file_path # Remember the loaded file
            else:
                messagebox.showerror("Load Error", "Failed to load resume data.")

    def save_resume_gui(self):
        current_data = self._get_data_from_gui()
        if not current_data.get("name"): # Simple validation
            messagebox.showwarning("Save Warning", "Please enter at least your name before saving.")
            return

        initial_file = self.current_json_filename if self.current_json_filename else "resume_data.json"
        file_path = filedialog.asksaveasfilename(
            initialfile=os.path.basename(initial_file), # Suggest previous filename
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            save_resume_data(current_data, file_path)
            self.current_json_filename = file_path # Update the current filename
            messagebox.showinfo("Save Success", f"Resume data saved to {os.path.basename(file_path)}")
        else:
            messagebox.showinfo("Save Cancelled", "Resume data not saved.")

    def generate_pdf_gui(self):
        current_data = self._get_data_from_gui()
        if not current_data.get("name"):
            messagebox.showwarning("PDF Generation Warning", "Please enter at least your name before generating PDF.")
            return

        file_path = filedialog.asksaveasfilename(
            initialfile=f"{current_data.get('name', 'resume').replace(' ', '_')}_Resume.pdf",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            # Create a new FPDF instance for each PDF generation
            pdf_instance = FPDF(unit="mm", format="A4")
            try:
                generate_resume_pdf(current_data, pdf_instance) # Pass the FPDF instance
                pdf_instance.output(file_path)
                messagebox.showinfo("PDF Success", f"Resume PDF generated successfully to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("PDF Error", f"Failed to generate PDF: {e}")
        else:
            messagebox.showinfo("PDF Cancelled", "PDF generation cancelled.")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("green")  # Themes: "blue" (default), "green", "dark-blue"

    app = ResumeBuilderApp()
    app.mainloop()