# Development Plan & Status

This document outlines the development plan for the RocketRecap project, moving from a simple prototype to a full-fledged community platform. It also serves as a guide for setting up and running the development environment.

## Current Status (Phase 0: Complete)

The initial refactoring and foundation-building phase is complete. The original `fasthtml` prototype has been successfully migrated to a robust Django project structure.

**Key Accomplishments:**

*   **Framework:** The application is now built on the Django web framework.
*   **Database:** The system uses Django's ORM with a SQLite backend for development. It is configured and ready to be switched to PostgreSQL for production.
*   **Core Logic:** The core functionality—accepting a YouTube URL, downloading the transcript, and generating a summary via the Google Gemini API—is fully operational.
*   **Project Structure:** The code is organized into a `community_project` for project-level settings and a `summarizer` app for all the core application logic. This structure is scalable and follows Django best practices.
*   **Data Persistence:** Generated videos, transcripts, and summaries are now saved to the database, preventing redundant processing of the same URL.
*   **Code Separation:** Business logic (API calls, transcript processing) is cleanly separated into a `services.py` file, away from the web-handling logic in `views.py`. Utility functions and forms are also in their own dedicated modules.

The project is now on a solid foundation, ready for the implementation of community features in Phase 1.

---

## How to Run the Project (Phase 0)

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd rocketrecap2
    ```

2.  **Install Dependencies:**
    This project uses `uv` for package management.
    ```bash
    uv sync
    ```

3.  **Set Up Environment Variables:**
    The application requires an API key for the Google Gemini service. Create a `.env` file in the project root (`rocketrecap2/`).
    ```
    # .env
    GEMINI_API_KEY="your_google_gemini_api_key_here"
    ```
    *Note: Django can be configured to automatically load this file, but for now, you may need to export it manually before running the server if you don't have `python-dotenv` configured.*
    ```bash
    export GEMINI_API_KEY="your_google_gemini_api_key_here"
    ```

4.  **Apply Database Migrations:**
    This will create the SQLite database file and set up the necessary tables based on `summarizer/models.py`.
    ```bash
    uv run python manage.py migrate
    ```

5.  **Run the Development Server:**
    ```bash
    uv run python manage.py runserver
    ```    The application will be available at `http://127.0.0.1:8000`.

6.  **Run Tests (Optional):**
    To ensure all utility functions are working correctly:
    ```bash
    uv run python manage.py test summarizer
    ```

---

## The Project Plan: A Phased Approach

### **Phase 0: Foundation and Refactoring (Completed)**

The goal of this phase was to move the existing prototype code onto a solid, scalable foundation.

1.  **Set Up Django Project:** A Django project (`community_project`) and a core app (`summarizer`) were created. The app was structured as a sibling to the project directory to ensure proper module resolution.
2.  **Defined Database Models:** The following models were created in `summarizer/models.py` to structure the data:
    *   `Video`: Stores information about the YouTube video.
    *   `Transcript`: Stores the raw transcript text, linked to a `Video`.
    *   `Summary`: Stores the generated summary, the model used, and a foreign key relationship to the `Video`.
3.  **Migrated Existing Logic:**
    *   Gemini API call logic was moved into `summarizer/services.py`.
    *   Transcript parsing and URL validation were moved into `summarizer/utils.py`.
    *   The frontend was recreated using a Django Form (`summarizer/forms.py`) and a Django Template (`summarizer/templates/`).
    *   The view (`summarizer/views.py`) was created to handle form submissions, call the service layer, and render the results.

**Outcome:** The project now has the same core functionality as the prototype but runs on a robust and scalable Django backend, ready for new features.

---

### **Phase 1: The Core Community (Users & Content)**

The next goal is to add user accounts and link content to individual users.

1.  **Implement User Authentication:**
    *   Leverage Django's built-in `auth` system for user registration, login, logout, and password management.
    *   **Recommendation:** Use the `django-allauth` package to easily add social logins (e.g., "Login with Google"), which is a standard and secure choice.

2.  **Create User Profiles:**
    *   Extend the built-in `User` model with a `Profile` model (using a one-to-one link). This can store user-specific information like a bio, points, or preferences.

3.  **Link Summaries to Users:**
    *   Add a `ForeignKey` from the `Summary` model to the `User` model.
    *   Update views to require a user to be logged in to create a summary.
    *   Create a dashboard page where a user can view their submission history.

**Outcome:** The site will transform from a simple tool into a platform where users have identities and own their contributions.

---

### **Phase 2: Fostering Engagement (Discussions & Gamification)**

With users and content, the focus shifts to interaction.

1.  **Implement a Commenting/Discussion System:**
    *   **Initial Approach:** Create a `Comment` model in Django with foreign keys to the `Summary` and `User` models. This allows for threaded discussions directly on a summary page.
    *   **Future Possibility:** For a richer experience, integrate a dedicated forum software like **Discourse** via Single Sign-On (SSO).

2.  **Introduce Basic Gamification:**
    *   **Points System:** Add a `points` field to the User Profile model.
    *   **Logic:** Award points for actions: creating a summary, commenting, or receiving an upvote.
    *   **Likes/Upvotes:** Create a `Like` model to allow users to upvote helpful summaries.
    *   **Leaderboard:** Create a simple page that ranks users by their total points to foster friendly competition.

**Outcome:** The platform becomes an interactive community where users are incentivized to contribute high-quality content and engage in discussions.

---

### **Phase 3: Implementing Unique Features**

With a strong community foundation, we can build the advanced features that set this platform apart.

1.  **Bridge the Language Gap:**
    *   Add a `language` field to the `Summary` model.
    *   Update the `services.py` and UI to allow users to request summaries in different languages, passing instructions to the Gemini API.

2.  **Integrate UMAP Visualizations:**
    *   **Backend:** Create a REST API endpoint (using **Django Rest Framework**). Implement a background task queue (using **Celery** and **Redis**) to generate vector embeddings for summaries and periodically re-calculate UMAP coordinates.
    *   **Frontend:** Use a JavaScript library like D3.js or Plotly.js to fetch the coordinate data from the API and render an interactive visualization map of related videos.

3.  **AI-Powered Q&A:**
    *   Add a form on the summary page to "Ask a question about this video."
    *   The backend will construct a new, detailed prompt for the Gemini API, including the user's question, the full transcript, and the generated summary. The AI's response will be displayed on the page.


StreamingHttpResponse
