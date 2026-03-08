"""AI Navigator -- Main Flask Server with auto-discovery."""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import os, hashlib
from models import get_db, create_tables
from ai_engine import search_tools, get_recommendations, compare_tools, get_trending, get_new_tools, log_search, ai_compare_tools
from helpers import stars_html, time_ago, pricing_badge
from discover import start_scheduler, get_site_stats, discover_tools

# Load .env manually (no extra dependency)
if os.path.exists('.env'):
    for line in open('.env'):
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            os.environ[k.strip()] = v.strip()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'ai-nav-secret-2026')

# Template helpers
app.jinja_env.globals.update(stars=stars_html, time_ago=time_ago, pricing_badge=pricing_badge)

# ─── Auth helpers ───
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def current_user():
    if 'user_id' not in session:
        return None
    db = get_db()
    u = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    db.close()
    return dict(u) if u else None

@app.context_processor
def inject_user():
    return {'user': current_user()}

# ─── Pages ───
@app.route('/')
def home():
    db = get_db()
    trending = db.execute('SELECT * FROM tools WHERE is_trending = 1 ORDER BY rating DESC').fetchall()
    categories = db.execute('SELECT * FROM categories WHERE tool_count > 0 ORDER BY name').fetchall()
    featured = db.execute('SELECT * FROM tools ORDER BY rating DESC LIMIT 8').fetchall()
    new_tools = db.execute('SELECT * FROM tools WHERE is_new = 1 ORDER BY created_at DESC LIMIT 8').fetchall()
    total_tools = db.execute('SELECT COUNT(*) FROM tools').fetchone()[0]
    total_cats = db.execute('SELECT COUNT(*) FROM categories WHERE tool_count > 0').fetchone()[0]
    # Get last discovery time
    last_update = db.execute("SELECT value FROM site_stats WHERE key='last_discovery'").fetchone()
    db.close()
    stats = {
        'total_tools': total_tools,
        'total_categories': total_cats,
        'last_update': last_update['value'] if last_update else 'Not yet'
    }
    return render_template('index.html', trending=trending, categories=categories,
                           featured=featured, new_tools=new_tools, stats=stats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        u = db.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                        (request.form['username'], hash_pw(request.form['password']))).fetchone()
        db.close()
        if u:
            session['user_id'] = u['id']
            flash('Welcome back!', 'success')
            return redirect('/')
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_db()
        try:
            db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                        (request.form['username'], request.form['email'], hash_pw(request.form['password'])))
            db.commit()
            u = db.execute('SELECT id FROM users WHERE username = ?', (request.form['username'],)).fetchone()
            session['user_id'] = u['id']
            total = db.execute('SELECT COUNT(*) FROM tools').fetchone()[0]
            db.execute('INSERT INTO notifications (user_id, title, message) VALUES (?, ?, ?)',
                        (u['id'], 'Welcome to AI Navigator!', f'Explore {total}+ AI tools. Our database updates automatically with new tools every day!'))
            db.execute('INSERT INTO notifications (user_id, title, message) VALUES (?, ?, ?)',
                        (u['id'], 'Try AI Chat', 'Ask our AI assistant anything! Try: "how to use ChatGPT" or "best tools for video editing"'))
            db.commit()
            db.close()
            flash('Account created!', 'success')
            return redirect('/')
        except:
            db.close()
            flash('Username or email already exists', 'error')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/explore')
def explore():
    db = get_db()
    cat = request.args.get('category', '')
    pricing = request.args.get('pricing', '')
    q = request.args.get('q', '')
    query = 'SELECT * FROM tools WHERE 1=1'
    params = []
    if cat:
        query += ' AND category = ?'
        params.append(cat)
    if pricing:
        query += ' AND pricing = ?'
        params.append(pricing)
    if q:
        query += ' AND (name LIKE ? OR description LIKE ? OR features LIKE ? OR category LIKE ?)'
        params.extend([f'%{q}%'] * 4)
    query += ' ORDER BY rating DESC'
    tools = db.execute(query, params).fetchall()
    categories = db.execute('SELECT * FROM categories WHERE tool_count > 0 ORDER BY name').fetchall()
    db.close()
    if q and 'user_id' in session:
        log_search(session['user_id'], q, len(tools))
    return render_template('explore.html', tools=tools, categories=categories,
                           selected_cat=cat, selected_pricing=pricing, search_q=q)

@app.route('/tool/<int:tool_id>')
def tool_detail(tool_id):
    db = get_db()
    tool = db.execute('SELECT * FROM tools WHERE id = ?', (tool_id,)).fetchone()
    if not tool:
        db.close()
        return redirect('/explore')
    reviews = db.execute('''SELECT r.*, u.username FROM reviews r 
                            LEFT JOIN users u ON r.user_id = u.id 
                            WHERE r.tool_id = ? ORDER BY r.created_at DESC''', (tool_id,)).fetchall()
    similar = db.execute('SELECT * FROM tools WHERE category = ? AND id != ? LIMIT 4',
                          (tool['category'], tool_id)).fetchall()
    db.close()
    return render_template('tool_detail.html', tool=tool, reviews=reviews, similar=similar)

@app.route('/tool/<int:tool_id>/review', methods=['POST'])
def add_review(tool_id):
    if 'user_id' not in session:
        flash('Please login to write a review', 'error')
        return redirect('/login')
    db = get_db()
    db.execute('INSERT INTO reviews (user_id, tool_id, rating, comment) VALUES (?, ?, ?, ?)',
               (session['user_id'], tool_id, int(request.form.get('rating', 5)), request.form.get('comment', '')))
    avg = db.execute('SELECT AVG(rating) FROM reviews WHERE tool_id = ?', (tool_id,)).fetchone()[0]
    if avg:
        db.execute('UPDATE tools SET rating = ? WHERE id = ?', (round(avg, 1), tool_id))
    db.commit()
    db.close()
    flash('Review submitted!', 'success')
    return redirect(f'/tool/{tool_id}')

@app.route('/compare')
def compare():
    db = get_db()
    ids = request.args.getlist('ids')
    tools = []
    if ids:
        for i in ids:
            t = db.execute('SELECT * FROM tools WHERE id = ?', (i,)).fetchone()
            if t:
                tools.append(dict(t))
    all_tools = db.execute('SELECT id, name, category FROM tools ORDER BY name').fetchall()
    db.close()
    return render_template('compare.html', tools=tools, all_tools=all_tools)

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat_api():
    data = request.get_json() or {}
    query = data.get('message', request.form.get('message', ''))
    if not query:
        return jsonify({'error': 'Please type a message'}), 400
    result = get_recommendations(query)
    if 'user_id' in session:
        log_search(session['user_id'], query, len(result.get('tools', [])))
    return jsonify(result)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' not in session:
        return redirect('/login')
    db = get_db()
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'update_profile':
            db.execute('UPDATE users SET email = ?, notify_email = ? WHERE id = ?',
                        (request.form.get('email', ''), request.form.get('notify_email', ''), session['user_id']))
            flash('Settings saved!', 'success')
        elif action == 'update_theme':
            db.execute('UPDATE users SET theme = ? WHERE id = ?',
                        (request.form.get('theme', 'dark'), session['user_id']))
            flash('Theme updated!', 'success')
        elif action == 'update_language':
            db.execute('UPDATE users SET language = ? WHERE id = ?',
                        (request.form.get('language', 'en'), session['user_id']))
            flash('Language updated!', 'success')
        elif action == 'clear_history':
            db.execute('DELETE FROM search_history WHERE user_id = ?', (session['user_id'],))
            flash('Search history cleared!', 'success')
        db.commit()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    history = db.execute('SELECT * FROM search_history WHERE user_id = ? ORDER BY created_at DESC LIMIT 20',
                          (session['user_id'],)).fetchall()
    db.close()
    return render_template('settings.html', profile=user, history=history)

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json() or request.form
    db = get_db()
    db.execute('INSERT INTO feedback (user_id, message, page, rating) VALUES (?, ?, ?, ?)',
               (session.get('user_id'), data.get('message', ''), data.get('page', ''), int(data.get('rating', 5))))
    db.commit()
    db.close()
    return jsonify({'success': True, 'message': 'Thank you for your feedback!'})

@app.route('/api/search')
def api_search():
    q = request.args.get('q', '')
    tools = search_tools(q) if q else []
    return jsonify(tools[:10])

@app.route('/api/notifications')
def api_notifications():
    if 'user_id' not in session:
        return jsonify([])
    db = get_db()
    notes = db.execute('SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT 10',
                        (session['user_id'],)).fetchall()
    db.close()
    return jsonify([dict(n) for n in notes])

@app.route('/api/notifications/read', methods=['POST'])
def mark_read():
    if 'user_id' in session:
        db = get_db()
        db.execute('UPDATE notifications SET is_read = 1 WHERE user_id = ?', (session['user_id'],))
        db.commit()
        db.close()
    return jsonify({'success': True})

@app.route('/api/stats')
def api_stats():
    """Return live site stats (used by homepage for dynamic counts)."""
    db = get_db()
    total_tools = db.execute('SELECT COUNT(*) FROM tools').fetchone()[0]
    total_cats = db.execute('SELECT COUNT(*) FROM categories WHERE tool_count > 0').fetchone()[0]
    last_update = db.execute("SELECT value FROM site_stats WHERE key='last_discovery'").fetchone()
    db.close()
    return jsonify({
        'total_tools': total_tools,
        'total_categories': total_cats,
        'last_update': last_update['value'] if last_update else 'Not yet'
    })

@app.route('/api/discover', methods=['POST'])
def api_discover():
    """Manually trigger discovery (admin use)."""
    added = discover_tools(max_queries=6)
    return jsonify({'success': True, 'tools_added': added})

@app.route('/api/compare', methods=['POST'])
def api_compare():
    """AI-powered tool comparison. Accepts tool names (even tools not in DB)."""
    data = request.get_json() or {}
    tool_names = data.get('tools', [])
    if len(tool_names) < 2:
        return jsonify({'error': 'Please provide at least 2 tool names'}), 400
    result = ai_compare_tools(tool_names[:3])  # Max 3 tools
    return jsonify(result)

if __name__ == '__main__':
    create_tables()
    # Start auto-discovery scheduler (every 6 hours)
    start_scheduler(interval_hours=6)
    print("[OK] AI Navigator running at http://localhost:5000")
    app.run(debug=True, port=5000, use_reloader=False)
