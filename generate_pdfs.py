"""Generate two PDF documents for the AI Navigator project."""
from fpdf import FPDF
import datetime

now = datetime.datetime.now().strftime("%B %d, %Y")

# ============================================================
# HELPER: Custom PDF class with header/footer
# ============================================================
class DocPDF(FPDF):
    def __init__(self, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.doc_title = title

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100,100,100)
        self.cell(0, 8, self.doc_title, align="L")
        self.ln(4)
        self.set_draw_color(63, 81, 181)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150,150,150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, num, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(25,118,210)
        self.cell(0, 10, f"{num}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(25,118,210)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 100, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(50,50,50)
        self.cell(0, 8, self.safe(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30,30,30)
        self.multi_cell(0, 5.5, self.safe(text))
        self.ln(2)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30,30,30)
        self.cell(6, 5.5, "-")
        self.multi_cell(0, 5.5, self.safe(text))
        self.ln(1)

    @staticmethod
    def safe(text):
        """Replace non-latin1 chars with ASCII equivalents."""
        replacements = {
            '\u2013': '-', '\u2014': '--', '\u2018': "'", '\u2019': "'",
            '\u201c': '"', '\u201d': '"', '\u2026': '...', '\u2022': '-',
            '\u2192': '->', '\u2190': '<-', '\u00a0': ' ',
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        # Strip any remaining non-latin1 chars
        return text.encode('latin-1', errors='replace').decode('latin-1')

    def code_block(self, text):
        self.set_font("Courier", "", 9)
        self.set_fill_color(240,240,240)
        self.set_text_color(30,30,30)
        self.multi_cell(0, 5, self.safe(text), fill=True)
        self.ln(3)

    def table_header(self, cols, widths):
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(63, 81, 181)
        self.set_text_color(255,255,255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 7, col, border=1, fill=True, align="C")
        self.ln()

    def table_row(self, cells, widths):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(30,30,30)
        self.set_fill_color(250,250,250)
        for i, cell in enumerate(cells):
            self.cell(widths[i], 6.5, cell[:40], border=1, align="L")
        self.ln()


# ============================================================
# PDF 1: PROJECT SYNOPSIS
# ============================================================
def generate_synopsis():
    pdf = DocPDF("AI Navigator - Project Synopsis")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Title page
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(25,118,210)
    pdf.ln(30)
    pdf.cell(0, 15, "AI Navigator", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(100,100,100)
    pdf.cell(0, 10, "Project Synopsis", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(120,120,120)
    pdf.cell(0, 8, f"Prepared on: {now}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Developer: Nikit", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Technology: Python / Flask / SQLite / Gemini AI / Tavily API", align="C", new_x="LMARGIN", new_y="NEXT")

    # Page 2+
    pdf.add_page()

    # 1. Introduction
    pdf.section_title(1, "Introduction")
    pdf.body_text(
        "AI Navigator is a web-based AI Tool Discovery and Recommendation Engine. "
        "It helps users discover, compare, and choose the best AI tools for any task -- from writing and coding to image generation, video creation, and research. "
        "The system combines a curated local database of 65+ AI tools with real-time web search (via Tavily API) and an intelligent LLM-powered recommendation engine (via Google Gemini 2.5 Flash) "
        "to deliver highly personalized, up-to-date, and zero-empty-result responses to any user query."
    )

    # 2. Problem Statement
    pdf.section_title(2, "Problem Statement")
    pdf.body_text(
        "The AI tools landscape is exploding -- hundreds of new tools launch every month across dozens of categories. "
        "Users face decision fatigue when trying to find the right tool for their specific needs. "
        "Existing directories often contain stale data, lack intelligent recommendations, and don't help beginners understand which tools are best for them. "
        "AI Navigator solves this by providing a smart, conversational discovery engine that understands intent, corrects typos, "
        "compares tools, and always provides actionable recommendations -- even for vague or ambiguous queries."
    )

    # 3. Objectives
    pdf.section_title(3, "Objectives")
    pdf.bullet("Build a comprehensive AI tool directory with 65+ curated tools across 12 categories.")
    pdf.bullet("Implement real-time web search to discover new tools launched daily.")
    pdf.bullet("Create an LLM-powered chat assistant that provides zero-empty-result, expert AI tool recommendations.")
    pdf.bullet("Support tool comparison, exploration, filtering, and detailed reviews.")
    pdf.bullet("Provide user authentication, settings, dark/light themes, and notifications.")
    pdf.bullet("Enable automatic database updates via a background discovery scheduler (every 6 hours).")
    pdf.bullet("Deliver a responsive, modern, and visually appealing web interface.")

    # 4. Technology Stack
    pdf.section_title(4, "Technology Stack")
    widths = [45, 70, 75]
    pdf.table_header(["Layer", "Technology", "Purpose"], widths)
    rows = [
        ["Backend", "Python 3 / Flask", "Web server and routing"],
        ["Database", "SQLite", "Local data storage (zero setup)"],
        ["AI Engine", "Google Gemini 2.5 Flash", "LLM-powered recommendations"],
        ["Web Search", "Tavily API", "Real-time tool discovery"],
        ["Frontend", "HTML/CSS/JS (Jinja2)", "Responsive UI with dark mode"],
        ["Auth", "SHA-256 + Flask sessions", "User authentication"],
        ["Scheduler", "Python threading", "Background auto-discovery"],
    ]
    for r in rows:
        pdf.table_row(r, widths)
    pdf.ln(4)

    # 5. System Architecture
    pdf.section_title(5, "System Architecture (High-Level)")
    pdf.body_text(
        "The application follows a classic MVC architecture:\n\n"
        "User Browser  -->  Flask (app.py)  -->  AI Engine (ai_engine.py)\n"
        "                        |                      |\n"
        "                   Templates/           Gemini API + Tavily API\n"
        "                   Static Files                |\n"
        "                        |               discover.py (Background)\n"
        "                   SQLite DB (models.py, seed_data.py)\n\n"
        "The user interacts via a browser. Flask serves pages and API routes. "
        "The AI Engine processes chat queries using Gemini with live Tavily web context. "
        "A background scheduler periodically discovers new tools and updates the database."
    )

    # 6. Key Features
    pdf.section_title(6, "Key Features")
    pdf.bullet("AI Chat Assistant: Conversational tool recommendations powered by Gemini 2.5 Flash with zero-tolerance for empty results.")
    pdf.bullet("Real-Time Web Search: Live Tavily API integration to surface tools launched today/this week.")
    pdf.bullet("Auto-Discovery Engine: Background scheduler runs every 6 hours to find and add new AI tools.")
    pdf.bullet("65+ Seeded AI Tools: Pre-loaded across 12 categories (Writing, Image, Code, Video, Audio, etc.).")
    pdf.bullet("Tool Explorer: Filter by category, pricing, and keyword search.")
    pdf.bullet("Tool Comparison: Side-by-side comparison of any tools in the database.")
    pdf.bullet("User Reviews & Ratings: Submit and view community reviews for each tool.")
    pdf.bullet("User Auth: Registration, login, session management.")
    pdf.bullet("Dark/Light Theme: Toggleable theme with per-user persistence.")
    pdf.bullet("Notifications: In-app notification system for new features and updates.")
    pdf.bullet("Feedback Widget: Floating feedback form on every page.")
    pdf.bullet("Responsive Design: Works on desktop, tablet, and mobile.")

    # 7. Modules Overview
    pdf.section_title(7, "Module Overview")
    widths2 = [40, 150]
    pdf.table_header(["File", "Purpose"], widths2)
    mods = [
        ["app.py", "Main Flask server with all routes and APIs"],
        ["ai_engine.py", "AI recommendation engine (Gemini + Tavily)"],
        ["models.py", "SQLite database schema and connection"],
        ["helpers.py", "Template utility functions (stars, badges)"],
        ["discover.py", "Auto-discovery engine and scheduler"],
        ["seed_data.py", "Initial 65+ tools and 12 categories seeder"],
        ["templates/", "9 Jinja2 HTML templates for all pages"],
        ["static/", "CSS styles and client-side JavaScript"],
        [".env", "API keys and secrets (not committed)"],
    ]
    for m in mods:
        pdf.table_row(m, widths2)
    pdf.ln(4)

    # 8. Expected Outcomes
    pdf.section_title(8, "Expected Outcomes")
    pdf.bullet("Users can discover the perfect AI tool for any need in under 30 seconds via the AI chat.")
    pdf.bullet("The database stays current through automatic daily discovery of newly launched tools.")
    pdf.bullet("Beginners get beginner-friendly explanations; advanced users get deep comparisons.")
    pdf.bullet("The system never returns an empty or unhelpful response, regardless of query quality.")

    # 9. Future Scope
    pdf.section_title(9, "Future Scope")
    pdf.bullet("Integration with Product Hunt and GitHub APIs for richer discovery.")
    pdf.bullet("User bookmarks, tool collections, and personalized dashboards.")
    pdf.bullet("Admin panel for content moderation and analytics.")
    pdf.bullet("Deployment to cloud (AWS/Heroku/Railway) for public access.")
    pdf.bullet("Mobile-native app using React Native or Flutter.")

    # 10. Conclusion
    pdf.section_title(10, "Conclusion")
    pdf.body_text(
        "AI Navigator is a complete, production-ready web application that solves the real-world problem of AI tool overload. "
        "By combining a curated database, real-time web intelligence, and a powerful LLM-driven chat engine, "
        "it offers users an unmatched tool discovery experience. The project demonstrates full-stack Python web development, "
        "API integration, AI/LLM engineering, and modern UI/UX design principles."
    )

    out = r"c:\Users\nikit\OneDrive\Desktop\New chatbot\AI_Navigator_Synopsis.pdf"
    pdf.output(out)
    print(f"[OK] Synopsis PDF saved: {out}")


# ============================================================
# PDF 2: COMPREHENSIVE DEVELOPER DOCUMENTATION
# ============================================================
def generate_developer_docs():
    pdf = DocPDF("AI Navigator - Developer Documentation")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Title Page
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(25,118,210)
    pdf.ln(25)
    pdf.cell(0, 15, "AI Navigator", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(100,100,100)
    pdf.cell(0, 10, "Comprehensive Developer Documentation", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(120,120,120)
    pdf.cell(0, 8, f"Version 1.0  |  {now}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Technology: Python / Flask / SQLite / Gemini 2.5 Flash / Tavily API", align="C", new_x="LMARGIN", new_y="NEXT")

    # ─── TABLE OF CONTENTS ───
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(25,118,210)
    pdf.cell(0, 10, "Table of Contents", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    toc = [
        "1. Project Overview",
        "2. Getting Started (Setup Guide)",
        "3. Project Structure",
        "4. Environment Configuration (.env)",
        "5. Database Schema (models.py)",
        "6. Seeding the Database (seed_data.py)",
        "7. Flask Application (app.py) - Routes & APIs",
        "8. AI Recommendation Engine (ai_engine.py)",
        "9. Auto-Discovery Engine (discover.py)",
        "10. Helper Utilities (helpers.py)",
        "11. Frontend Architecture",
        "12. Template Pages",
        "13. Static Assets (CSS & JS)",
        "14. API Reference",
        "15. Authentication & Security",
        "16. Deployment Guide",
        "17. Troubleshooting",
        "18. Future Enhancements",
    ]
    for item in toc:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(30,30,30)
        pdf.cell(0, 6, item, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # ─── 1. PROJECT OVERVIEW ───
    pdf.add_page()
    pdf.section_title(1, "Project Overview")
    pdf.body_text(
        "AI Navigator is a full-stack Python web application that serves as an AI Tool Discovery and Recommendation Engine. "
        "It helps users find the best AI tools for any task by combining:\n\n"
        "- A curated SQLite database of 65+ AI tools across 12 categories\n"
        "- Real-time web search via the Tavily API\n"
        "- An intelligent LLM-powered chat engine using Google Gemini 2.5 Flash\n"
        "- An automatic background discovery scheduler\n\n"
        "The application provides browsing, searching, filtering, comparing, reviewing, and conversational AI-powered discovery of tools."
    )

    # ─── 2. GETTING STARTED ───
    pdf.section_title(2, "Getting Started (Setup Guide)")
    pdf.sub_title("Prerequisites")
    pdf.bullet("Python 3.10 or higher")
    pdf.bullet("pip (Python package manager)")
    pdf.bullet("A Gemini API key (from Google AI Studio)")
    pdf.bullet("A Tavily API key (from tavily.com) -- optional but recommended")

    pdf.sub_title("Installation Steps")
    pdf.code_block(
        "# 1. Clone or download the project\n"
        "cd \"New chatbot\"\n\n"
        "# 2. Install dependencies\n"
        "pip install flask requests google-genai python-dotenv fpdf2\n\n"
        "# 3. Create .env file with your API keys\n"
        "SECRET_KEY=your-secret-key\n"
        "GEMINI_API_KEY=your-gemini-key\n"
        "TAVILY_API_KEY=your-tavily-key\n\n"
        "# 4. Seed the database\n"
        "python seed_data.py\n\n"
        "# 5. Run the application\n"
        "python app.py\n\n"
        "# 6. Open in browser\n"
        "http://localhost:5000"
    )

    # ─── 3. PROJECT STRUCTURE ───
    pdf.section_title(3, "Project Structure")
    pdf.code_block(
        "New chatbot/\n"
        "|-- app.py                 # Main Flask server (routes, APIs)\n"
        "|-- ai_engine.py           # AI recommendation engine\n"
        "|-- models.py              # Database schema & connection\n"
        "|-- helpers.py             # Template helper functions\n"
        "|-- discover.py            # Auto-discovery engine\n"
        "|-- seed_data.py           # Database seeder (65+ tools)\n"
        "|-- requirements.txt       # Python dependencies\n"
        "|-- .env                   # API keys (not committed)\n"
        "|-- ai_tools.db            # SQLite database file\n"
        "|-- templates/\n"
        "|   |-- base.html          # Base template (navbar, footer)\n"
        "|   |-- index.html         # Homepage\n"
        "|   |-- explore.html       # Tool explorer with filters\n"
        "|   |-- chat.html          # AI chat interface\n"
        "|   |-- compare.html       # Tool comparison page\n"
        "|   |-- tool_detail.html   # Individual tool detail page\n"
        "|   |-- login.html         # Login page\n"
        "|   |-- register.html      # Registration page\n"
        "|   |-- settings.html      # User settings page\n"
        "|-- static/\n"
        "    |-- css/style.css      # All styles (dark/light theme)\n"
        "    |-- js/app.js          # Client-side JavaScript\n"
        "    |-- images/            # Static images"
    )

    # ─── 4. ENVIRONMENT CONFIGURATION ───
    pdf.add_page()
    pdf.section_title(4, "Environment Configuration (.env)")
    pdf.body_text(
        "The application reads configuration from a .env file in the project root. "
        "It is loaded manually in app.py and via python-dotenv in ai_engine.py."
    )
    pdf.code_block(
        "SECRET_KEY=your-flask-secret-key\n"
        "GEMINI_API_KEY=your-google-gemini-api-key\n"
        "TAVILY_API_KEY=your-tavily-api-key\n"
        "OPENAI_API_KEY=optional-openai-key"
    )
    pdf.body_text(
        "- SECRET_KEY: Used by Flask for session encryption.\n"
        "- GEMINI_API_KEY: Required for the AI chat engine (Gemini 2.5 Flash).\n"
        "- TAVILY_API_KEY: Required for real-time web search and auto-discovery.\n"
        "- OPENAI_API_KEY: Optional, reserved for future OpenAI integrations."
    )

    # ─── 5. DATABASE SCHEMA ───
    pdf.section_title(5, "Database Schema (models.py)")
    pdf.body_text(
        "The database uses SQLite with 8 tables. The schema is auto-created on first run via create_tables()."
    )

    tables = [
        ("users", "Stores user accounts with username, email, hashed password, theme and language preferences."),
        ("categories", "AI tool categories (Writing, Image, Code, etc.) with icon, description and tool count."),
        ("tools", "The core table: stores each AI tool with name, description, category, rating, pricing, URL, features, use cases, source, and flags for trending/new."),
        ("reviews", "User-submitted reviews with rating (1-5) and comment, linked to both user and tool."),
        ("search_history", "Logs every user search query and result count for analytics."),
        ("feedback", "Stores user feedback submissions with message, page, and rating."),
        ("notifications", "In-app notifications per user with read/unread state."),
        ("discovery_log", "Logs each auto-discovery run: query count, tools found, tools added."),
        ("site_stats", "Key-value store for dynamic stats (total tools, last discovery time)."),
    ]
    for name, desc in tables:
        pdf.sub_title(f"Table: {name}")
        pdf.body_text(desc)

    # ─── 6. SEEDING ───
    pdf.add_page()
    pdf.section_title(6, "Seeding the Database (seed_data.py)")
    pdf.body_text(
        "The seed_data.py script populates the database with 12 categories and 65+ hand-curated AI tools. "
        "Each tool includes: name, tagline, description, category, rating, pricing, URL, logo emoji, features, use cases, and trending/new flags."
    )
    pdf.sub_title("Categories Seeded")
    cats = ["Writing", "Image", "Code", "Video", "Audio", "Productivity", "Design", "Research", "Marketing", "Education", "Business", "Data"]
    pdf.body_text(", ".join(cats))
    pdf.sub_title("How to Run")
    pdf.code_block("python seed_data.py\n# Output: [OK] Seeded 12 categories and 65 tools!")

    # ─── 7. FLASK APP ───
    pdf.section_title(7, "Flask Application (app.py)")
    pdf.body_text(
        "app.py is the central server file. It defines all routes (page views and API endpoints), "
        "handles authentication, and starts the background discovery scheduler."
    )

    pdf.sub_title("Page Routes")
    routes_page = [
        ["GET /", "Homepage with trending, categories, featured"],
        ["GET /explore", "Tool explorer with filters (category, pricing, search)"],
        ["GET /tool/<id>", "Tool detail page with reviews and similar tools"],
        ["GET /compare", "Tool comparison page"],
        ["GET /chat", "AI chat interface"],
        ["GET /login", "Login form"],
        ["POST /login", "Login authentication"],
        ["GET /register", "Registration form"],
        ["POST /register", "Create new user account"],
        ["GET /logout", "Clear session and redirect"],
        ["GET /settings", "User settings (theme, language, history)"],
        ["POST /settings", "Update profile, theme, language, clear history"],
    ]
    w = [55, 135]
    pdf.table_header(["Route", "Description"], w)
    for r in routes_page:
        pdf.table_row(r, w)
    pdf.ln(4)

    pdf.sub_title("API Routes")
    routes_api = [
        ["POST /chat", "AI chat endpoint (returns JSON recommendations)"],
        ["GET /api/search?q=", "Search tools by name/category (autocomplete)"],
        ["GET /api/notifications", "Get user notifications"],
        ["POST /api/notifications/read", "Mark all notifications as read"],
        ["GET /api/stats", "Get live site stats (total tools, categories)"],
        ["POST /api/discover", "Manually trigger tool discovery"],
        ["POST /feedback", "Submit user feedback"],
        ["POST /tool/<id>/review", "Submit a tool review"],
    ]
    pdf.table_header(["Route", "Description"], w)
    for r in routes_api:
        pdf.table_row(r, w)
    pdf.ln(4)

    # ─── 8. AI ENGINE ───
    pdf.add_page()
    pdf.section_title(8, "AI Recommendation Engine (ai_engine.py)")
    pdf.body_text(
        "This is the brain of the application. It processes user chat queries through a 4-step pipeline:"
    )
    pdf.bullet("Step 1: perform_deep_web_search() -- Searches the live web via Tavily API for real-time AI tool data.")
    pdf.bullet("Step 2: get_local_db_context() -- Queries the local SQLite database for matching tools.")
    pdf.bullet("Step 3: analyze_with_llm() -- Sends both contexts + user query to Gemini 2.5 Flash with a detailed system prompt.")
    pdf.bullet("Step 4: format_ui_cards() -- Converts the LLM's JSON response into UI-ready card data.")
    pdf.ln(2)

    pdf.sub_title("System Prompt (EXPERT_SYSTEM_PROMPT)")
    pdf.body_text(
        "The system prompt is a 7-section instruction set that governs the LLM's behavior:\n\n"
        "1. FORBIDDEN RESPONSES: Never return empty results, never say 'I don't understand'.\n"
        "2. UNIVERSAL INTENT DECODER: Spell correction, comparison detection, task-specific matching.\n"
        "3. RESPONSE TEMPLATE: Structured markdown summary with pro tips.\n"
        "4. FALLBACK RULES: If query is uninterpretable, still return top 5 tools.\n"
        "5. MULTI-LANGUAGE RULE: Detect and respond in the user's language.\n"
        "6. REAL-TIME SEARCH TRIGGER: Auto-trigger web search for trending/new queries.\n"
        "7. OUTPUT SCHEMA: Strict JSON format with name, tier_label, category, power_level, pricing, URL, etc."
    )

    pdf.sub_title("Key Functions")
    funcs = [
        ["get_recommendations(query)", "Main entry point. Orchestrates the 4-step pipeline."],
        ["perform_deep_web_search(q)", "Tavily API call with optimized query."],
        ["get_local_db_context(q)", "LIKE-based SQLite search for matching tools."],
        ["analyze_with_llm(q, local, web)", "Gemini API call with system prompt + context."],
        ["format_ui_cards(llm_tools)", "Converts LLM JSON to frontend card objects."],
        ["search_tools(query)", "Simple DB search for autocomplete API."],
        ["compare_tools(tool_ids)", "Returns full tool data for comparison."],
        ["get_trending()", "Returns all trending-flagged tools."],
        ["get_new_tools()", "Returns all new-flagged tools."],
        ["log_search(uid, q, count)", "Logs a search query to search_history."],
    ]
    w2 = [65, 125]
    pdf.table_header(["Function", "Description"], w2)
    for f in funcs:
        pdf.table_row(f, w2)
    pdf.ln(4)

    # ─── 9. DISCOVERY ENGINE ───
    pdf.section_title(9, "Auto-Discovery Engine (discover.py)")
    pdf.body_text(
        "The auto-discovery engine runs in a background thread and periodically searches the web for new AI tools. "
        "It uses 24 pre-defined search queries across all categories and adds newly found tools to the database."
    )
    pdf.sub_title("How It Works")
    pdf.bullet("1. Selects a subset of discovery queries (rotates based on time).")
    pdf.bullet("2. Searches Tavily API for each query (max 8 results each).")
    pdf.bullet("3. Parses each result to extract tool name, URL, description, pricing, and category.")
    pdf.bullet("4. Skips duplicates and generic results (e.g., 'Best AI tools list').")
    pdf.bullet("5. Inserts new tools into the database with source='tavily_discovery' and is_new=1.")
    pdf.bullet("6. Updates category counts and site stats.")
    pdf.bullet("7. Logs the discovery run in discovery_log table.")
    pdf.ln(2)

    pdf.sub_title("Scheduling")
    pdf.body_text(
        "The scheduler starts automatically when app.py runs. Default interval: every 6 hours (4 times/day). "
        "Each run processes 6 search queries. A full manual scan (24 queries) can be triggered via:\n"
        "  python discover.py          # CLI full scan\n"
        "  POST /api/discover           # API trigger"
    )

    # ─── 10. HELPERS ───
    pdf.add_page()
    pdf.section_title(10, "Helper Utilities (helpers.py)")
    pdf.body_text("Small utility functions registered as Jinja2 template globals:")
    pdf.bullet("stars_html(rating) -- Generates star rating string (full/half/empty stars).")
    pdf.bullet("time_ago(dt_str) -- Converts timestamp to 'Today', '3 days ago', '2 months ago'.")
    pdf.bullet("pricing_badge(pricing) -- Returns CSS class name for Free/Freemium/Paid badges.")

    # ─── 11. FRONTEND ARCHITECTURE ───
    pdf.section_title(11, "Frontend Architecture")
    pdf.body_text(
        "The frontend uses Jinja2 templates served by Flask. All pages extend base.html which provides:\n\n"
        "- Responsive navbar with search autocomplete, theme toggle, notifications, and auth links\n"
        "- Flash message display queue\n"
        "- Footer with navigation and category links\n"
        "- Floating feedback widget\n"
        "- Dark/light theme support via CSS custom properties and data-theme attribute\n\n"
        "Client-side JavaScript (static/js/app.js) handles:\n"
        "- Chat message sending/receiving and response rendering\n"
        "- Search autocomplete with debouncing\n"
        "- Theme toggling and persistence in localStorage\n"
        "- Notifications panel loading\n"
        "- Mobile menu toggle\n"
        "- Carousel scrolling\n"
        "- Feedback submission"
    )

    # ─── 12. TEMPLATE PAGES ───
    pdf.section_title(12, "Template Pages")
    templates_info = [
        ["base.html", "Master template with navbar, footer, feedback widget, flash messages, and JS/CSS includes."],
        ["index.html", "Homepage: hero section with search, trending tools carousel, category grid, top-rated tools, new arrivals, and CTA to chat."],
        ["explore.html", "Tool explorer: filter by category and pricing, keyword search, grid display of all tools."],
        ["chat.html", "AI chat interface: message input, typing indicator, and dynamic response rendering."],
        ["compare.html", "Tool comparison: select multiple tools and see side-by-side feature grids."],
        ["tool_detail.html", "Individual tool page: description, features, use cases, reviews, and similar tool suggestions."],
        ["login.html", "Login form with username and password."],
        ["register.html", "Registration form with username, email, and password."],
        ["settings.html", "User settings: profile, theme, language, search history, and danger zone actions."],
    ]
    w3 = [40, 150]
    pdf.table_header(["Template", "Description"], w3)
    for t in templates_info:
        pdf.table_row(t, w3)
    pdf.ln(4)

    # ─── 13. STATIC ASSETS ───
    pdf.section_title(13, "Static Assets (CSS & JS)")
    pdf.sub_title("CSS (static/css/style.css)")
    pdf.body_text(
        "- Full dark and light theme using CSS custom properties (--bg-primary, --text-primary, etc.)\n"
        "- Responsive layout with media queries\n"
        "- Component styles: tool cards, chat bubbles, carousels, badges, modals\n"
        "- Glassmorphism effects and smooth hover animations"
    )
    pdf.sub_title("JavaScript (static/js/app.js)")
    pdf.body_text(
        "- Theme toggle with localStorage persistence\n"
        "- sendChat() -- Sends message to POST /chat, shows typing indicator, renders response\n"
        "- renderSearchResult() -- Builds tool cards with ratings, descriptions, quick steps, and visit links\n"
        "- renderHowTo() -- Builds step-by-step guide cards for how-to queries\n"
        "- onSearch() -- Debounced search autocomplete for navbar\n"
        "- Notification panel loading and badge display\n"
        "- Mobile menu toggle and carousel scrolling"
    )

    # ─── 14. API REFERENCE ───
    pdf.add_page()
    pdf.section_title(14, "API Reference")

    pdf.sub_title("POST /chat")
    pdf.body_text("Request: { \"message\": \"suggest coding tools\" }\nResponse: { type, tools[], query, summary }")
    pdf.body_text("Each tool object in the response contains: name, category, pricing, url, description, tagline, rating, quick_steps[].")

    pdf.sub_title("GET /api/search?q=<query>")
    pdf.body_text("Returns: Array of { id, name, category, rating, logo } -- max 10 results. Used for autocomplete.")

    pdf.sub_title("GET /api/stats")
    pdf.body_text("Returns: { total_tools, total_categories, last_update }")

    pdf.sub_title("POST /api/discover")
    pdf.body_text("Triggers manual tool discovery. Returns: { success: true, tools_added: N }")

    pdf.sub_title("GET /api/notifications")
    pdf.body_text("Returns: Array of notification objects for the current logged-in user.")

    pdf.sub_title("POST /feedback")
    pdf.body_text("Request: { message, rating, page }\nReturns: { success: true, message: 'Thank you...' }")

    # ─── 15. AUTH & SECURITY ───
    pdf.section_title(15, "Authentication & Security")
    pdf.bullet("Passwords are hashed using SHA-256 before storage (hash_pw function in app.py).")
    pdf.bullet("Sessions are managed via Flask's built-in session with a SECRET_KEY.")
    pdf.bullet("No sensitive data (API keys) is hardcoded -- loaded from .env file.")
    pdf.bullet("Foreign keys are enabled on the SQLite connection (PRAGMA foreign_keys = ON).")
    pdf.bullet("All user-submitted content is escaped in templates via Jinja2 auto-escaping.")
    pdf.bullet("Note for production: Upgrade to bcrypt/argon2 for password hashing and use HTTPS.")

    # ─── 16. DEPLOYMENT GUIDE ───
    pdf.section_title(16, "Deployment Guide")
    pdf.sub_title("Local Development")
    pdf.code_block("python app.py\n# Runs at http://localhost:5000 with debug mode ON")
    pdf.sub_title("Production Deployment (Recommendation)")
    pdf.body_text(
        "1. Set debug=False in app.py\n"
        "2. Use gunicorn or waitress as WSGI server\n"
        "3. Deploy to Railway, Render, Heroku, or AWS\n"
        "4. Set environment variables via platform dashboard\n"
        "5. Consider migrating to PostgreSQL for production"
    )
    pdf.code_block("# Example with gunicorn (Linux)\npip install gunicorn\ngunicorn app:app --bind 0.0.0.0:8000 --workers 4")

    # ─── 17. TROUBLESHOOTING ───
    pdf.add_page()
    pdf.section_title(17, "Troubleshooting")
    pdf.sub_title("Common Issues")
    pdf.bullet("ImportError 'search_tools': This function must exist in ai_engine.py. If missing, add it (see Section 8).")
    pdf.bullet("Empty chat responses: Check that GEMINI_API_KEY is valid. Check server console for 'LLM Error' messages.")
    pdf.bullet("No web search results: Verify TAVILY_API_KEY is set and valid.")
    pdf.bullet("Database locked: Ensure only one instance of the app is running.")
    pdf.bullet("UnicodeEncodeError on Windows: The server handles emoji via UTF-8. Use a modern terminal (Windows Terminal).")
    pdf.bullet("Port 5000 in use: Kill existing process or change port in app.py (app.run(port=5001)).")

    # ─── 18. FUTURE ENHANCEMENTS ───
    pdf.section_title(18, "Future Enhancements")
    pdf.bullet("Admin dashboard for managing tools, reviewing feedback, and viewing analytics.")
    pdf.bullet("User tool bookmarks and personal collections.")
    pdf.bullet("Email notification system for new tool discoveries.")
    pdf.bullet("Integration with Product Hunt, GitHub Trending, and Hacker News APIs.")
    pdf.bullet("Rate limiting and caching for API endpoints.")
    pdf.bullet("Advanced search with embeddings-based semantic matching.")
    pdf.bullet("Multi-language frontend (i18n support).")
    pdf.bullet("Progressive Web App (PWA) support for mobile.")

    out = r"c:\Users\nikit\OneDrive\Desktop\New chatbot\AI_Navigator_Developer_Docs.pdf"
    pdf.output(out)
    print(f"[OK] Developer Docs PDF saved: {out}")


# ============================================================
# MAIN: Generate both PDFs
# ============================================================
if __name__ == "__main__":
    generate_synopsis()
    generate_developer_docs()
    print("\n[DONE] Both PDFs generated successfully!")
