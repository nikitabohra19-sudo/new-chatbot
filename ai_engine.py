"""AI recommendation engine + Gemini 2.5 Flash + Tavily web search.

Provides a cutting-edge "Real-Time AI Tool Discovery Engine".
1. Searches the live web FIRST (Product Hunt, Reddit, trending news)
2. Uses Gemini 2.5 to analyze intent, compare tools, and apply Freshness Tiers.
3. Generates beautifully formatted markdown per tool and dynamic UI cards.
"""
import requests, os, json, re, datetime
from models import get_db
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

TAVILY_KEY = os.getenv('TAVILY_API_KEY', '')
GEMINI_KEY = os.getenv('GEMINI_API_KEY', '')

if GEMINI_KEY:
    client = genai.Client(api_key=GEMINI_KEY)
else:
    client = None

# The expert persona prompt from the user
EXPERT_SYSTEM_PROMPT = """You are an elite AI Tool Discovery Assistant. You have ZERO tolerance for returning empty results. Every single user message — no matter how vague, misspelled, incomplete, or unusual — MUST receive a rich, helpful tool recommendation response.

═══════════════════════════════════════════════════════════
SECTION 1: FORBIDDEN RESPONSES (NEVER SAY THESE)
═══════════════════════════════════════════════════════════

❌ NEVER say: "I couldn't find exact matches"
❌ NEVER say: "No tools found for this query"
❌ NEVER say: "Try different keywords"
❌ NEVER say: "I don't understand your query"
❌ NEVER say: "Please rephrase your question"
❌ NEVER return an empty result for ANY input

If you are about to say any of the above — STOP. 
Re-analyze the query and find the intent. Then answer.

═══════════════════════════════════════════════════════════
SECTION 2: UNIVERSAL INTENT DECODER
═══════════════════════════════════════════════════════════

Before responding, run this internal decode process on EVERY user message:

STEP 1 — SPELL CORRECTION
Fix all typos automatically:
- "chatgpt" → ChatGPT
- "poweful" → powerful  
- "han" / "than" → than
- "lauched" → launched
- "writting" → writing
- "reserch" → research
Never penalize the user for typos. Silently correct and proceed.

STEP 2 — INTENT PATTERN MATCHING
Match the query to one or more of these universal intent patterns:

COMPARISON INTENTS:
- "better than X" / "more powerful than X" / "stronger than X"
  → Find tools that outperform X in speed, features, accuracy, or cost

- "alternative to X" / "instead of X" / "replace X"
  → Find direct competitors and substitutes for X

- "updated version of X" / "upgraded X" / "newer than X" / "latest X"
  → Find the most recent, evolved, or next-gen version of X or similar tools

- "cheaper than X" / "free version of X" / "open source X"
  → Find budget or open-source alternatives

SPECIFICITY INTENTS:
- "tool for [specific job]" / "best for [task]" / "specialized in [field]"
  → Find niche, purpose-built tools for that exact task

- "X but for [industry/role]"
  → Find vertical-specific tools (e.g., "ChatGPT but for lawyers")

- "X with [feature]" / "X that can [capability]"
  → Find tools matching that feature requirement

- "most powerful [category]" / "strongest [category]" / "top [category]"
  → Rank and list the best tools in that category

DISCOVERY INTENTS:
- "new AI tools" / "latest tools" / "tools launched recently"
  → Search for tools from last 7–90 days

- "trending tools" / "viral AI" / "everyone is using"
  → Find currently hyped/popular tools

- "hidden gem" / "underrated tool" / "not many know about"
  → Surface lesser-known but highly effective tools

- "all in one tool" / "multipurpose AI" / "Swiss army knife"
  → Find broad, multi-feature platforms

TASK-SPECIFIC INTENTS (auto-detect these topics):
- Writing → Jasper, Copy.ai, Claude, Notion AI, Sudowrite
- Coding → Cursor, GitHub Copilot, Codeium, Tabnine, Replit AI
- Image → Midjourney, DALL-E 3, Stable Diffusion, Ideogram, Flux
- Video → Runway, Pika, Sora, Kling, HeyGen, Synthesia
- Audio/Voice → ElevenLabs, Murf, Suno, Udio
- Research → Perplexity, Elicit, Consensus, Scholarcy
- Automation → Make, Zapier, n8n, Bardeen
- SEO → Surfer SEO, Frase, MarketMuse
- Data/Analytics → Julius AI, Obviously AI, Akkio
- Presentation → Gamma, Beautiful.ai, Tome
- Customer Support → Intercom AI, Tidio, Chatbase
- HR/Recruiting → Paradox, HireVue, Fetcher
- Legal → Harvey AI, CoCounsel, Lexis+ AI
- Finance → Domo, Planful, Cube
- Sales → Clay, Apollo AI, Gong

STEP 3 — CONFIDENCE SCORING
Even if only 1 word is understood, extract maximum meaning:
- Single word "coding" → Full coding tool breakdown
- "like chatgpt" → ChatGPT alternatives list
- "image" → Image generation tool recommendations
- "free" → Free AI tools across all categories
- Emoji only 🎨 → Art/image tools
- Question in any language → Detect language, respond in same language

═══════════════════════════════════════════════════════════
SECTION 3: RESPONSE TEMPLATE (Use for EVERY answer)
═══════════════════════════════════════════════════════════

Always structure your `summary_markdown` like this (NOTE: Do NOT include the individual tool breakdowns here, as those will be rendered automatically via the JSON `tools_to_show` array over our UI cards):

---
🎯 **I understand you're looking for**: [restate their intent in clear English]
[If Fallback Rule used: "I want to make sure I give you the best answer! Here are powerful AI tools across popular categories while I understand your need better:"]

💡 **Pro tip**: [One actionable insight based on their specific query]

🔍 **Want me to go deeper?** I can compare any of these tools, find free alternatives, or search for tools launched this week. [Or ask a clarifying question if Fallback Rule was used]
---

═══════════════════════════════════════════════════════════
SECTION 4: FALLBACK RULES (Last Resort — Never Fail)
═══════════════════════════════════════════════════════════

If the query is completely uninterpretable after all steps above:

RULE 1: Make your BEST GUESS at intent and answer that guess
RULE 2: Show top 5 tools across the most common categories
RULE 3: Ask ONE clarifying question at the end
RULE 4: STILL never return empty — always give value first, clarify second

═══════════════════════════════════════════════════════════
SECTION 5: MULTI-LANGUAGE RULE
═══════════════════════════════════════════════════════════

- Detect the user's language automatically
- Respond FULLY in that same language in the `summary_markdown`
- Tool names stay in English, explanations translate
- Never ask the user to switch to English

═══════════════════════════════════════════════════════════
SECTION 6: REAL-TIME SEARCH TRIGGER
═══════════════════════════════════════════════════════════

Automatically trigger a live web search when user says:
- "latest" / "newest" / "just launched" / "this week" / "today"
- "updated version" / "v2" / "new release"
- Any tool name you're not 100% certain about
- "everyone is talking about" / "trending" / "viral"

Search sources: Product Hunt → Reddit → Twitter/X → Futurepedia → theresanaiforthat.com → Hacker News → GitHub Trending

ABSOLUTE FINAL RULE: 
A user will ALWAYS get a helpful, specific, actionable answer. 
No exceptions. No empty responses. No redirects. Ever.

═══════════════════════════════════════════════════════════
SECTION 7: OUTPUT SCHEMA & SYSTEM INTEGRATION (CRITICAL)
═══════════════════════════════════════════════════════════

Your response must ONLY be a valid JSON object matching the exact schema below. Do NOT wrap it in Markdown brackets like `json` blocks.
   
The `summary_markdown` string should be a highly conversational, expert response answering the user directly. Follow the instructions from SECTION 3.
   
Schema:
{
    "intent": "search|compare|how_to|alternatives",
    "summary_markdown": "A conversational summary formatted as markdown...",
    "tools_to_show": [
        {
            "name": "Tool Name",
            "tier_label": "🔴 JUST LAUNCHED | 🟠 VERY NEW | 🟡 RECENT | 🟢 ESTABLISHED | ⚪ MATURE",
            "what_it_does": "1 sentence description",
            "relevance": "Why it's relevant to this specific query",
            "community_verdict": "Real users are saying... / community sentiment",
            "comparison": "Honest comparison vs [tool user mentioned] (if applicable) / specific advantage",
            "satisfaction_signal": "Early review buzz, upvotes, or GitHub stars",
            "best_for": "Specific use cases",
            "category": "Writing | Image Gen | Coding | etc.",
            "power_level": "Beginner | Intermediate | Advanced",
            "url": "https://...",
            "pricing": "Free | Freemium | Paid",
            "source": "Local DB | Web"
        }
    ]
}
"""

# ─── Real-Time Web Search ───
def perform_deep_web_search(query):
    """Hits Tavily for real-time data from ProductHunt, Reddit, HackerNews."""
    if not TAVILY_KEY:
        return ""
    
    # We construct a highly specific query to force Tavily to find new tools
    current_month = datetime.datetime.now().strftime("%B %Y")
    smart_queries = [
        f"new AI tools launched {current_month} {query}",
        f"best alternative to {query} 2026",
        f"Product Hunt trending AI tools {query}",
        f"site:reddit.com/r/artificial OR site:producthunt.com {query} AI"
    ]
    
    # Just use one broad optimized query to save time/API calls
    optimized_query = f"{query} new AI tools {current_month} OR Product Hunt OR Reddit reviews"
    
    try:
        r = requests.post('https://api.tavily.com/search', json={
            'api_key': TAVILY_KEY,
            'query': optimized_query,
            'search_depth': 'advanced',
            'max_results': 5,
            'include_answer': True
        }, timeout=12)
        if r.ok:
            data = r.json()
            context = "Live Web Search Results:\n"
            if data.get('answer'):
                context += f"AI Summary: {data['answer']}\n"
            for res in data.get('results', []):
                snippet = res.get('content', '').replace('\n', ' ')
                context += f"- [{res.get('title')}]({res.get('url')}): {snippet[:300]}...\n"
            return context
    except Exception as e:
        print("Tavily Error:", e)
        pass
    
    return "No live web results available."

# ─── Local DB Tools List ───
def get_local_db_context(query):
    db = get_db()
    # Pull tools that might remotely match the query to give LLM options
    q = f"%{query}%"
    words = [w for w in query.split() if len(w) > 3]
    
    local_tools = []
    # Broad search
    local = db.execute('SELECT name, category, pricing, tagline, url FROM tools WHERE name LIKE ? OR category LIKE ? LIMIT 10', (q, q)).fetchall()
    for row in local:
        local_tools.append(dict(row))
        
    if not local_tools and words:
        for w in words:
            k = f"%{w}%"
            rows = db.execute('SELECT name, category, pricing, tagline, url FROM tools WHERE name LIKE ? OR category LIKE ? OR features LIKE ? LIMIT 5', (k, k, k)).fetchall()
            for r in rows:
                if not any(t['name'] == r['name'] for t in local_tools):
                    local_tools.append(dict(r))
                    
    db.close()
    
    if not local_tools:
        return "No strictly matching local tools found in database."
        
    context = "Local Database Tools:\n"
    for t in local_tools:
        context += f"- {t['name']} ({t['category']}) - {t['pricing']}: {t['tagline']} | URL: {t['url']}\n"
    return context

# ─── Analyze Intent & Generate Output with Gemini ───
def analyze_with_llm(user_query, local_context, web_context):
    """Use Gemini 2.5 Flash to parse intent, process live data, and generate the expert summary + tool cards."""
    if not client:
        return None
        
    try:
        full_prompt = f"{EXPERT_SYSTEM_PROMPT}\n\n{local_context}\n\n{web_context}\n\nUser Query: {user_query}\n\nReturn ONLY the requested JSON object."
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3, # low temp for JSON stability
            ),
        )
        content = response.text
        content = content.replace('```json', '').replace('```', '').strip()
        return json.loads(content)
    except Exception as e:
        print("LLM Error:", e)
        print("Raw response may have failed parsing.")
        return None

# ─── Format Final Cards for UI ───
def format_ui_cards(llm_tools):
    """Takes the rich tool objects generated by the LLM and formats them perfectly for the existing frontend UI schema."""
    ui_tools = []
    for t in llm_tools:
        # Convert LLM schema to UI schema
        ui_tool = {
            'name': t.get('name', 'Unknown Tool'),
            'category': t.get('category') or ('Web Discovery' if t.get('source', '') == 'Web' else 'Local Database'),
            'pricing': t.get('pricing', 'Freemium'),
            'url': t.get('url', '#'),
            'description': t.get('what_it_does', ''),
            'tagline': t.get('relevance', ''),
            'rating': 5.0 if 'LAUNCHED' in t.get('tier_label', '') else 4.8, # Simulated high rating for new tools
            'logo_url': None # Frontend falls back to ✨
        }
        
        # Build the exact "Quick Start" steps asked for by the user prompt
        # using the rich Markdown breakdown the LLM provides
        quick_steps = []
        if t.get('tier_label'): quick_steps.append(f"**Freshness:** {t['tier_label']}")
        if t.get('power_level'): quick_steps.append(f"**Level:** {t['power_level']}")
        if t.get('relevance'): quick_steps.append(f"**Why it's relevant:** {t['relevance']}")
        if t.get('best_for'): quick_steps.append(f"**Best for:** {t['best_for']}")
        if t.get('comparison') and t.get('comparison') != "N/A": quick_steps.append(f"**Comparison:** {t['comparison']}")
        if t.get('community_verdict'): quick_steps.append(f"**Community verdict:** {t['community_verdict']}")
        if t.get('satisfaction_signal'): quick_steps.append(f"**Traction:** {t['satisfaction_signal']}")
        
        ui_tool['quick_steps'] = quick_steps
        ui_tools.append(ui_tool)
        
    return ui_tools

# ─── Main Interface ───
def get_recommendations(user_query):
    """The main entry point for the chat API."""
    # 1. Gather live web data FIRST
    web_context = perform_deep_web_search(user_query)
    
    # 2. Gather local DB data
    local_context = get_local_db_context(user_query)
    
    # 3. Call Gemini Expert Analyst
    llm_result = analyze_with_llm(user_query, local_context, web_context) if client else None
    
    # ── Fallback if API fails (or no key) ──
    if not llm_result:
        # Simple local fallback
        db = get_db()
        q = f"%{user_query}%"
        local = db.execute('SELECT * FROM tools WHERE name LIKE ? OR category LIKE ? LIMIT 4', (q, q)).fetchall()
        db.close()
        
        tools = [dict(t) for t in local]
        for t in tools:
            t['quick_steps'] = ["Explore the dashboard and experiment!"]
            
        return {
            'type': 'search',
            'tools': tools,
            'query': user_query,
            'summary': f"Here are the best tools I found in my local database for: {user_query}. (Live web search failed)."
        }

    # 4. Process LLM Result into UI format
    intent = llm_result.get('intent', 'search')
    summary = llm_result.get('summary_markdown', '')
    llm_tools = llm_result.get('tools_to_show', [])
    
    ui_tools = format_ui_cards(llm_tools)

    return {
        'type': intent,
        'tools': ui_tools[:6], # Max 6 cards
        'query': user_query,
        'summary': summary
    }

# ─── Other Functions ───
def compare_tools(tool_ids):
    db = get_db()
    tools = []
    for tid in tool_ids:
        t = db.execute('SELECT * FROM tools WHERE id = ?', (tid,)).fetchone()
        if t: tools.append(dict(t))
    db.close()
    return tools

def get_trending():
    db = get_db()
    tools = db.execute('SELECT * FROM tools WHERE is_trending = 1 ORDER BY rating DESC').fetchall()
    db.close()
    return [dict(t) for t in tools]

def get_new_tools():
    db = get_db()
    tools = db.execute('SELECT * FROM tools WHERE is_new = 1 ORDER BY created_at DESC').fetchall()
    db.close()
    return [dict(t) for t in tools]

def log_search(user_id, query, count):
    db = get_db()
    db.execute('INSERT INTO search_history (user_id, query, results_count) VALUES (?, ?, ?)', (user_id, query, count))
    db.commit()
    db.close()

def search_tools(query):
    db = get_db()
    q = f"%{query}%"
    rows = db.execute('SELECT id, name, category, rating, logo FROM tools WHERE name LIKE ? OR category LIKE ?', (q, q)).fetchall()
    db.close()
    return [dict(r) for r in rows]

# ─── AI-Powered Tool Comparison ───
COMPARE_SYSTEM_PROMPT = """You are an elite AI Tool Comparison Engine with REAL-TIME web search capabilities.

Given a list of AI tool names, you must produce a detailed, honest, expert comparison.

## RULES
1. Search the provided web context for the latest info on each tool.
2. If a tool is not in the local database, use web search data to fill in its details.
3. NEVER say you can't compare a tool. Always provide your best analysis.
4. Be honest about pros AND cons of each tool.
5. Respond in the same language the user uses.

## OUTPUT (JSON only, no markdown wrappers)
{
    "summary": "A detailed markdown summary comparing all tools. Include a verdict/recommendation at the end. Use bold, bullet points, and clear sections for readability.",
    "tools": [
        {
            "name": "Tool Name",
            "tier_label": "JUST LAUNCHED | VERY NEW | RECENT | ESTABLISHED | MATURE",
            "what_it_does": "1 sentence description",
            "category": "Writing | Image Gen | Coding | etc.",
            "pricing": "Free | Freemium | Paid",
            "power_level": "Beginner | Intermediate | Advanced",
            "best_for": "Specific use cases",
            "community_verdict": "What real users say",
            "comparison": "Key strengths vs the other tools in this comparison",
            "satisfaction_signal": "Review buzz, stars, upvotes",
            "url": "https://..."
        }
    ]
}
"""

def ai_compare_tools(tool_names):
    """Compare any tools by name using Gemini + Tavily, even if not in DB."""
    # 1. Web search for each tool
    web_contexts = []
    for name in tool_names:
        ctx = perform_deep_web_search(f"{name} AI tool review pricing features 2026")
        if ctx:
            web_contexts.append(f"Web data for {name}:\n{ctx}")

    # 2. Local DB data for each tool
    db = get_db()
    local_contexts = []
    for name in tool_names:
        row = db.execute('SELECT name, category, pricing, description, features, use_cases, rating, url FROM tools WHERE LOWER(name) = LOWER(?)', (name,)).fetchone()
        if row:
            r = dict(row)
            local_contexts.append(f"DB data for {r['name']}: Category={r['category']}, Pricing={r['pricing']}, Rating={r['rating']}, URL={r['url']}, Desc={r['description']}, Features={r['features']}, UseCases={r['use_cases']}")
    db.close()

    # 3. Ask Gemini to compare
    if not client:
        return {'summary': 'AI comparison unavailable (no API key).', 'tools': []}

    combined_context = "\n\n".join(local_contexts + web_contexts)
    tools_str = ", ".join(tool_names)

    try:
        full_prompt = f"{COMPARE_SYSTEM_PROMPT}\n\n{combined_context}\n\nCompare these tools: {tools_str}\n\nReturn ONLY the JSON object."

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        content = response.text.replace('```json', '').replace('```', '').strip()
        result = json.loads(content)
        return result
    except Exception as e:
        print("Compare LLM Error:", e)
        return {'summary': f'Comparison of {tools_str} is temporarily unavailable. Please try again.', 'tools': []}
