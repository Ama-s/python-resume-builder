# Python Resume Builder 🚀

![Python Logo](https://img.shields.io/badge/Python-3.9+-blue.svg?style=flat&logo=python&logoColor=white)
![CustomTkinter Badge](https://img.shields.io/badge/GUI-CustomTkinter-green.svg?style=flat&logo=python&logoColor=white)
![PDF Generation Badge](https://img.shields.io/badge/PDF-FPDF-red.svg?style=flat&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48c3ZnIHZlcnNpb249IjEuMSIgaWQ9IkxheWVyXzEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMuorg/1999/xlinkIiB4PSIwIiB5PSIwIiB2aWV3Qm94PSIwIDAgMTggMTgiIHN0eWxlPSJlbmFibGUtYmFja2dyb3VuZDpjb25ldyAzMzk5MzIzNDk3OTQzNjM2MzYzNjM2MzYzNjM2MzYzNiAzMDQ1NjkzNTMxMzIzNDkzNDkzMDQ1OTQyMTIzMjEyMzQ1NzM0ODc5MjM0ODcwMzQyMzIzNDc4OTIzNDg3OTA1Njk0MjM0ODc2NzI3MzQ4NzQyMzczNDg3MTEzNDg3NzM0ODc2NjY3MzQ4NzYzNjYzNDg3OTAzNDg3OTQ1OTc0NjMzOTkzMzk5MzIzNDk3OTQzNjM2MzYzNjM2MzYzNjM2MzYzNjMwNDU2OTM1MzEzMjM0OTM0OTMwNDU5NDIxMjMyMTIzNDU3MzQ4NzkyMzQ4NzAzNDIzMjM0Nzg5MjM0ODc5MDU2OTQyMzQ4NzY3MjczNDg3NDIzNzM0ODcxMTM0ODc3MzQ4NzY2Njc=;width:10px;height:10px;"&logoColor=white)

A user-friendly desktop application for quickly creating and managing professional resumes. Say goodbye to manual formatting headaches and generate sleek PDF resumes with ease!


### Table of Contents

1.  [About The Project](#about-the-project)
2.  [Features](#features)
3.  [How To Use](#how-to-use)
    * [For Developers (Run from Source)](#for-developers-run-from-source)
4.  [Project Structure](#project-structure)
5.  [Technical Overview](#technical-overview)
    * [Backend (Data Handling & PDF Generation)](#backend-data-handling--pdf-generation)
    * [Frontend (Graphical User Interface)](#frontend-graphical-user-interface)
6.  [Contributing](#contributing)


### 1. About The Project

This project aims to simplify the resume creation process for job seekers. Built with Python, it features a robust backend for data management and PDF generation, coupled with a modern, intuitive graphical user interface (GUI) built using CustomTkinter. Users can easily input their personal details, education, experience, skills, and more, then save their data and generate a professional PDF resume with a single click.

**Key Motivations:**
* Streamline resume updates and creation.
* Ensure consistent, clean formatting.
* Provide an easy-to-use interface for non-technical users.



### 2. Features

* **Comprehensive Data Input:** Collects all essential resume sections (Personal Info, Summary, Education, Experience, Projects, Awards, Volunteer Work, Skills, Hobbies).
* **Dynamic Sections:** Easily add and remove multiple entries for Education, Experience, Projects, Awards, and Volunteer Work.
* **Data Persistence:** Save your resume data to a JSON file for future edits and quick loading.
* **Professional PDF Generation:** Creates a cleanly formatted, ready-to-print PDF resume using the FPDF library.
* **Modern GUI:** Intuitive and aesthetically pleasing user interface powered by CustomTkinter.
* **CLI Option (for developers/testing):** Original command-line interface still available for direct interaction (primarily for debugging or headless use).



### 3. How To Use

#### For Developers (Run from Source)

If you want to run the application from its source code, explore its internals, or contribute, follow these steps:

1.  **Prerequisites:**
    * [Python 3.9+](https://www.python.org/downloads/) (Make sure to check "Add Python to PATH" during installation)
    * [Git](https://git-scm.com/downloads)

2.  **Clone the Repository:**
    ```bash
    git clone [https://https://github.com/Ama-s/python-resume-builder.git](https://https://github.com/Ama-s/python-resume-builder.git)
    cd python-resume-builder
    ```

3.  **Set Up Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    ```
    * **Activate on Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **Activate on macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies:**
    Once the virtual environment is active, install all required libraries:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the GUI Application:**
    ```bash
    python resume_gui.py
    ```

6.  **Run the CLI Application (Optional - for direct backend interaction/debugging):**
    ```bash
    python resume_generator.py
    ```



### 4. Project Structure

.
├── venv/
├── resume_generator.py
├── resume_gui.py
├── DejaVuSans.ttf                 
├── DejaVuSans-Bold.ttf         # all DejaVu fonts actually
├── requirements.txt
├── README.md
├── .gitignore
├── *.json
└── *.pdf

### 5. Technical Overview

This project is structured with a clear separation of concerns, making it modular and maintainable.

#### Backend (Data Handling & PDF Generation)
* **File:** `resume_generator.py`
* **Libraries:** `json` for data persistence, `fpdf` for PDF creation.
* **Core Logic:**
    * Handles the structured collection of resume information.
    * Manages saving (serialization) and loading (deserialization) of resume data to/from JSON files.
    * Controls the precise layout, fonts, and content rendering for the PDF output. It acts as the "printing press," taking raw data and turning it into a professional document.

#### Frontend (Graphical User Interface)
* **File:** `resume_gui.py`
* **Library:** `CustomTkinter`
* **Core Logic:**
    * Provides the interactive visual interface for users to input, edit, and view resume details.
    * Dynamically generates input fields for sections like Education and Experience, allowing users to add/remove entries as needed.
    * Acts as the bridge, collecting data from user inputs and passing it to the `resume_generator.py` for processing (saving, loading, PDF generation).
    * Handles user feedback (e.g., success/error messages).



### 6. Contributing

Contributions are welcome! If you have ideas for features, bug fixes, or improvements, feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

