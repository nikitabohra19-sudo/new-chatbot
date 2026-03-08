"""Auto-Discovery Engine — Finds new AI tools using Tavily API and keeps data fresh.

Runs in background to:
1. Discover NEW AI tools across all categories
2. Update existing tool info (ratings, pricing changes)
3. Track what's trending in the AI market
4. Log all discovery activity for analytics
"""
import requests, os, re, json, threading, time
from datetime import datetime
from models import get_db, create_tables

def get_tavily_key():
    return os.getenv('TAVILY_API_KEY', '')

# Category emoji mapping
CAT_ICONS = {
    'Writing': '✍️', 'Image': '🎨', 'Code': '💻', 'Video': '🎬',
    'Audio': '🎵', 'Productivity': '⚡', 'Design': '🎯', 'Research': '🔬',
    'Marketing': '📢', 'Education': '📚', 'Business': '💼', 'Data': '📊',
    'Healthcare': '🏥', 'Finance': '💰', 'Legal': '⚖️', 'HR': '👥',
    'Customer Support': '🎧', 'Social Media': '📱', 'E-commerce': '🛒',
    'Automation': '🤖', 'Translation': '🌍', 'Security': '🔒',
    '3D': '🧊', 'Gaming': '🎮', 'Other': '🔧'
}

# Logo emoji based on first letter or category
TOOL_LOGOS = ['🤖','🧠','⚡','🔮','💎','🎯','🌟','🔥','💡','🎨',
              '🖱️','📊','🧪','🎬','🎵','✨','🌀','🦁','🔍','📝']

# ─── Tavily Search ───
def tavily_search(query, max_results=10):
    """Search via Tavily API."""
    if not get_tavily_key():
        return {}
    try:
        r = requests.post('https://api.tavily.com/search', json={
            'api_key': get_tavily_key(),
            'query': query,
            'search_depth': 'advanced',
            'max_results': max_results,
            'include_answer': True
        }, timeout=20)
        if r.ok:
            return r.json()
    except Exception as e:
        print(f"[DISCOVER] Tavily error: {e}")
    return {}

# ─── Parse Tool Info from Tavily Result ───
def parse_tool_from_result(result, category):
    """Extract tool info from a Tavily search result."""
    title = result.get('title', '')
    url = result.get('url', '')
    content = result.get('content', '')
    
    # Try to extract tool name from title
    # Common patterns: "ToolName - Description", "ToolName: Description", "ToolName | Site"
    name = title.split(' - ')[0].split(' | ')[0].split(': ')[0].strip()
    name = re.sub(r'\s*(Review|Pricing|Features|Guide|Tutorial|vs|Alternative).*', '', name, flags=re.IGNORECASE).strip()
    
    # Skip if name is too long (likely not a tool name) or too short
    if len(name) > 40 or len(name) < 2:
        return None
    
    # Skip generic titles
    skip_words = ['best', 'top', 'list', 'free', 'how to', 'what is', 'guide', 
                  'review', 'comparison', 'alternative', 'reddit', 'quora',
                  'youtube', 'tiktok', 'twitter', 'facebook', 'linkedin',
                  'wikipedia', 'forbes', 'techcrunch']
    if any(w in name.lower() for w in skip_words):
        return None
    
    # Extract description (first 200 chars of content)
    desc = content[:250].strip() if content else f'{name} is an AI tool for {category.lower()} tasks.'
    
    # Guess pricing from content
    pricing = 'Freemium'
    content_lower = (content or '').lower()
    if 'free' in content_lower and 'paid' not in content_lower:
        pricing = 'Free'
    elif 'paid' in content_lower or 'subscription' in content_lower or 'premium' in content_lower:
        pricing = 'Paid'
    elif 'freemium' in content_lower or 'free plan' in content_lower or 'free tier' in content_lower:
        pricing = 'Freemium'
    
    # Pick a logo emoji
    logo = TOOL_LOGOS[hash(name) % len(TOOL_LOGOS)]
    
    return {
        'name': name,
        'tagline': f'AI tool for {category.lower()}',
        'description': desc,
        'category': category,
        'rating': 4.0,
        'pricing': pricing,
        'url': url,
        'logo': logo,
        'features': '',
        'use_cases': '',
        'is_trending': 0,
        'is_new': 1,
        'source': 'tavily_discovery'
    }

# ─── Discovery Queries ───
DISCOVERY_QUERIES = [
    ("new AI writing tools 2026", "Writing"),
    ("new AI image generation tools 2026", "Image"),
    ("new AI coding tools developer 2026", "Code"),
    ("new AI video generation tools 2026", "Video"),
    ("new AI voice music tools 2026", "Audio"),
    ("new AI productivity tools 2026", "Productivity"),
    ("new AI design tools 2026", "Design"),
    ("new AI research tools 2026", "Research"),
    ("new AI marketing tools 2026", "Marketing"),
    ("new AI education tools 2026", "Education"),
    ("new AI business tools 2026", "Business"),
    ("new AI data analysis tools 2026", "Data"),
    ("trending AI tools this week", "Writing"),
    ("best new AI tools launched recently", "Productivity"),
    ("AI tools for automation 2026", "Productivity"),
    ("AI tools for customer support 2026", "Business"),
    ("AI tools for social media 2026", "Marketing"),
    ("AI tools for healthcare 2026", "Research"),
    ("AI tools for e-commerce 2026", "Business"),
    ("AI chatbot tools 2026", "Writing"),
    ("AI presentation tools 2026", "Productivity"),
    ("AI translation tools 2026", "Writing"),
    ("AI 3D generation tools 2026", "Design"),
    ("AI game development tools 2026", "Code"),
]

# ─── Core Discovery Function ───
def discover_tools(max_queries=5):
    """Run discovery: search Tavily for new AI tools and add them to DB.
    
    Args:
        max_queries: How many search queries to run (saves API credits).
                     Use 5 for hourly checks, 24 for daily full scan.
    """
    if not get_tavily_key():
        print("[DISCOVER] No Tavily API key found. Skipping discovery.")
        return 0
    
    db = get_db()
    total_added = 0
    total_found = 0
    
    # Get existing tool names (lowercase) to avoid duplicates
    existing = set()
    for row in db.execute('SELECT LOWER(name) as n FROM tools').fetchall():
        existing.add(row['n'])
    
    # Pick queries to run (rotate through them)
    now = datetime.now()
    start_idx = (now.hour + now.day) % len(DISCOVERY_QUERIES)
    queries = DISCOVERY_QUERIES[start_idx:start_idx + max_queries]
    if len(queries) < max_queries:
        queries += DISCOVERY_QUERIES[:max_queries - len(queries)]
    
    for query, category in queries:
        print(f"[DISCOVER] Searching: {query}")
        data = tavily_search(query, max_results=8)
        results = data.get('results', []) if isinstance(data, dict) else []
        total_found += len(results)
        
        for result in results:
            tool = parse_tool_from_result(result, category)
            if not tool:
                continue
            
            # Skip if already exists
            if tool['name'].lower() in existing:
                continue
            
            # Add to database
            try:
                db.execute('''INSERT INTO tools 
                    (name, tagline, description, category, rating, pricing, url, logo, 
                     features, use_cases, is_trending, is_new, source, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)''',
                    (tool['name'], tool['tagline'], tool['description'], tool['category'],
                     tool['rating'], tool['pricing'], tool['url'], tool['logo'],
                     tool['features'], tool['use_cases'], tool['is_trending'], tool['is_new'],
                     tool['source']))
                existing.add(tool['name'].lower())
                total_added += 1
                print(f"[DISCOVER] + Added: {tool['name']} ({category})")
            except Exception as e:
                pass  # Likely duplicate
        
        # Small delay between queries to be nice to the API
        time.sleep(1)
    
    # Ensure categories exist for new tools
    for cat_name, icon in CAT_ICONS.items():
        try:
            db.execute('INSERT OR IGNORE INTO categories (name, icon, description) VALUES (?, ?, ?)',
                       (cat_name, icon, f'AI tools for {cat_name.lower()}'))
        except:
            pass
    
    # Update category counts
    for row in db.execute('SELECT DISTINCT category FROM tools').fetchall():
        cat = row['category']
        count = db.execute('SELECT COUNT(*) FROM tools WHERE category = ?', (cat,)).fetchone()[0]
        db.execute('UPDATE categories SET tool_count = ? WHERE name = ?', (count, cat))
    
    # Update site stats
    tool_count = db.execute('SELECT COUNT(*) FROM tools').fetchone()[0]
    cat_count = db.execute('SELECT COUNT(*) FROM categories WHERE tool_count > 0').fetchone()[0]
    db.execute('INSERT OR REPLACE INTO site_stats (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)',
               ('total_tools', str(tool_count)))
    db.execute('INSERT OR REPLACE INTO site_stats (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)',
               ('total_categories', str(cat_count)))
    db.execute('INSERT OR REPLACE INTO site_stats (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)',
               ('last_discovery', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    # Log discovery run
    db.execute('INSERT INTO discovery_log (query, tools_found, tools_added, status) VALUES (?, ?, ?, ?)',
               (f'{len(queries)} queries', total_found, total_added, 'ok'))
    
    db.commit()
    db.close()
    
    print(f"[DISCOVER] Done! Found {total_found} results, added {total_added} new tools. Total in DB: {tool_count}")
    return total_added

# ─── Update Trending ───
def update_trending():
    """Use Tavily to find what's currently trending in AI tools."""
    if not get_tavily_key():
        return
    
    data = tavily_search("most popular AI tools trending right now 2026", max_results=10)
    answer = data.get('answer', '') if isinstance(data, dict) else ''
    
    if not answer:
        return
    
    db = get_db()
    # Reset all trending
    db.execute('UPDATE tools SET is_trending = 0')
    
    # Find mentioned tools in the trending answer
    tools = db.execute('SELECT id, name FROM tools').fetchall()
    for tool in tools:
        if tool['name'].lower() in answer.lower():
            db.execute('UPDATE tools SET is_trending = 1 WHERE id = ?', (tool['id'],))
    
    db.commit()
    db.close()
    print("[DISCOVER] Trending tools updated")

# ─── Get Dynamic Stats ───
def get_site_stats():
    """Get dynamic site stats from database."""
    db = get_db()
    stats = {}
    for row in db.execute('SELECT key, value, updated_at FROM site_stats').fetchall():
        stats[row['key']] = {'value': row['value'], 'updated': row['updated_at']}
    
    # Fallback: count directly
    if 'total_tools' not in stats:
        count = db.execute('SELECT COUNT(*) FROM tools').fetchone()[0]
        stats['total_tools'] = {'value': str(count), 'updated': 'now'}
    if 'total_categories' not in stats:
        count = db.execute('SELECT COUNT(*) FROM categories WHERE tool_count > 0').fetchone()[0]
        stats['total_categories'] = {'value': str(count), 'updated': 'now'}
    
    db.close()
    return stats

# ─── Background Scheduler ───
_scheduler_running = False

def start_scheduler(interval_hours=6):
    """Start background discovery scheduler. Runs every `interval_hours` hours.
    Default: every 6 hours (4 times a day).
    """
    global _scheduler_running
    if _scheduler_running:
        return
    _scheduler_running = True
    
    def run_loop():
        while _scheduler_running:
            try:
                print(f"[SCHEDULER] Running auto-discovery at {datetime.now()}")
                discover_tools(max_queries=6)  # 6 queries per run
                update_trending()
            except Exception as e:
                print(f"[SCHEDULER] Error: {e}")
            # Sleep for interval
            time.sleep(interval_hours * 3600)
    
    thread = threading.Thread(target=run_loop, daemon=True)
    thread.start()
    print(f"[SCHEDULER] Auto-discovery started (every {interval_hours} hours)")

def stop_scheduler():
    global _scheduler_running
    _scheduler_running = False

# ─── CLI: Run discovery manually ───
if __name__ == '__main__':
    import sys
    # Load .env
    if os.path.exists('.env'):
        for line in open('.env'):
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()
    # TAVILY_KEY loaded via os.environ
    
    create_tables()
    queries = int(sys.argv[1]) if len(sys.argv) > 1 else 24  # Full scan by default
    print(f"[DISCOVER] Starting full discovery ({queries} queries)...")
    added = discover_tools(max_queries=queries)
    update_trending()
    print(f"[DISCOVER] Complete! {added} new tools added.")
