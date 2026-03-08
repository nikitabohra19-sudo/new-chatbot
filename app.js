/* AI Navigator — Client-Side JavaScript */

// ─── Theme Toggle ───
function initTheme() {
    const saved = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
    const btn = document.getElementById('themeBtn');
    if (btn) btn.textContent = saved === 'dark' ? '☀️' : '🌙';
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    const btn = document.getElementById('themeBtn');
    if (btn) btn.textContent = next === 'dark' ? '☀️' : '🌙';
    fetch('/settings', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `action=update_theme&theme=${next}`
    }).catch(() => {});
}

// ─── Mobile Menu ───
function toggleMenu() {
    document.getElementById('navLinks')?.classList.toggle('show');
}

// ─── Carousel Scroll ───
function scrollCarousel(id, dir) {
    const el = document.getElementById(id);
    if (el) el.scrollBy({ left: dir * 320, behavior: 'smooth' });
}

// ─── Chat ───
async function sendChat() {
    const input = document.getElementById('chatInput');
    const msg = input?.value.trim();
    if (!msg) return;
    const box = document.getElementById('chatMessages');
    
    // User message
    box.innerHTML += `<div class="chat-msg user"><div class="msg-content">${escapeHtml(msg)}</div></div>`;
    input.value = '';
    box.scrollTop = box.scrollHeight;
    
    // Typing indicator
    const typing = document.createElement('div');
    typing.className = 'typing-indicator';
    typing.innerHTML = '<span></span><span></span><span></span>';
    box.appendChild(typing);
    box.scrollTop = box.scrollHeight;
    
    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: msg})
        });
        const data = await res.json();
        typing.remove();
        
        if (data.type === 'how_to') {
            box.innerHTML += renderHowTo(data);
        } else {
            box.innerHTML += renderSearchResult(data);
        }
    } catch(e) {
        typing.remove();
        box.innerHTML += `<div class="chat-msg bot"><div class="msg-content">Sorry, something went wrong. Please try again!</div></div>`;
    }
    box.scrollTop = box.scrollHeight;
}

function renderHowTo(data) {
    const g = data.guide;
    let html = `<div class="chat-msg bot"><div class="msg-content">`;
    html += `<div class="bot-intro">${escapeHtml(data.summary)}</div>`;
    
    // Tool info card
    if (g.tool) {
        html += `<div class="chat-tool-highlight">
            <span class="tool-emoji">${g.tool.logo || '🤖'}</span>
            <div class="tool-info">
                <div class="chat-tool-name">${escapeHtml(g.tool.name)}</div>
                <div class="chat-tool-meta">⭐ ${g.tool.rating} &middot; ${g.tool.pricing}</div>
            </div>
            <a href="${g.tool.url}" target="_blank" class="chat-visit-btn">Visit ↗</a>
        </div>`;
    }
    
    // Steps
    html += `<div class="how-to-steps">`;
    for (const s of g.steps) {
        html += `<div class="how-to-step">
            <div class="step-number">${s.step}</div>
            <div class="step-content">
                <div class="step-title">${escapeHtml(s.title)}</div>
                <div class="step-desc">${escapeHtml(s.desc)}</div>
            </div>
        </div>`;
    }
    html += `</div>`;
    
    // Tips
    if (g.tips && g.tips.length) {
        html += `<div class="how-to-tips"><strong>💡 Pro Tips:</strong><ul>`;
        for (const t of g.tips) html += `<li>${escapeHtml(t)}</li>`;
        html += `</ul></div>`;
    }
    
    // AI Insight
    if (g.ai_insight) {
        html += `<div class="ai-insight"><strong>🔍 Research Insight:</strong><p>${escapeHtml(g.ai_insight)}</p></div>`;
    }
    
    html += `</div></div>`;
    return html;
}

function renderSearchResult(data) {
    let html = `<div class="chat-msg bot"><div class="msg-content">`;
    html += `<div class="bot-intro">${escapeHtml(data.summary || 'Here are my recommendations:')}</div>`;
    
    // Tool cards with usage steps
    if (data.tools && data.tools.length) {
        for (const t of data.tools.slice(0, 5)) {
            html += `<div class="chat-tool-block">`;
            // Tool header
            html += `<div class="chat-tool-highlight">
                <span class="tool-emoji">${t.logo || '🤖'}</span>
                <div class="tool-info">
                    <div class="chat-tool-name">${escapeHtml(t.name)}</div>
                    <div class="chat-tool-meta">⭐ ${t.rating} &middot; ${t.pricing}</div>
                </div>
                <a href="/tool/${t.id}" class="chat-visit-btn">Details</a>
            </div>`;
            // Description
            html += `<div class="chat-tool-desc">${escapeHtml((t.description || '').substring(0, 150))}</div>`;
            // Quick steps
            if (t.quick_steps && t.quick_steps.length) {
                html += `<div class="chat-quick-steps"><strong>🚀 Quick Start:</strong><ol>`;
                for (const s of t.quick_steps) {
                    html += `<li>${escapeHtml(s)}</li>`;
                }
                html += `</ol></div>`;
            }
            // Visit button
            html += `<div class="chat-tool-actions">
                <a href="${t.url}" target="_blank" class="chat-visit-btn primary">Visit ${escapeHtml(t.name)} ↗</a>
            </div>`;
            html += `</div>`;
        }
    } else {
        html += `<div class="bot-empty">No tools found for this query. Try different keywords like "image generation" or "writing assistant".</div>`;
    }
    
    html += `</div></div>`;
    return html;
}

// ─── Search Autocomplete ───
let searchTimer;
function onSearch(input) {
    clearTimeout(searchTimer);
    const q = input.value.trim();
    const dropdown = document.getElementById('searchDropdown');
    if (!dropdown) return;
    if (q.length < 2) { dropdown.classList.remove('show'); return; }
    searchTimer = setTimeout(async () => {
        const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
        const tools = await res.json();
        if (!tools.length) { dropdown.classList.remove('show'); return; }
        dropdown.innerHTML = tools.slice(0, 5).map(t => 
            `<a href="/tool/${t.id}" class="search-item">
                <span>${t.logo || '🤖'}</span>
                <div>
                    <div style="font-weight:600;font-size:0.88rem">${escapeHtml(t.name)}</div>
                    <div style="font-size:0.75rem;color:var(--text-muted)">${t.category} · ⭐${t.rating}</div>
                </div>
            </a>`
        ).join('');
        dropdown.classList.add('show');
    }, 300);
}

// ─── Star Select (Reviews) ───
function setStars(n) {
    const btns = document.querySelectorAll('.star-select button');
    const input = document.getElementById('ratingInput');
    btns.forEach((b, i) => b.classList.toggle('active', i < n));
    if (input) input.value = n;
}

// ─── Feedback ───
function toggleFeedback() {
    document.getElementById('feedbackModal')?.classList.toggle('show');
}

async function submitFeedback() {
    const msg = document.getElementById('feedbackMsg')?.value;
    const rating = document.getElementById('feedbackRating')?.value || 5;
    if (!msg) return;
    const res = await fetch('/feedback', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: msg, rating: parseInt(rating), page: window.location.pathname})
    });
    const data = await res.json();
    alert(data.message || 'Thanks!');
    document.getElementById('feedbackMsg').value = '';
    toggleFeedback();
}

// ─── Notifications ───
async function toggleNotifications() {
    const panel = document.getElementById('notifPanel');
    if (!panel) return;
    panel.classList.toggle('show');
    if (panel.classList.contains('show')) {
        const res = await fetch('/api/notifications');
        const notes = await res.json();
        if (notes.length === 0) {
            panel.innerHTML = '<div class="notif-empty">No notifications yet</div>';
        } else {
            panel.innerHTML = notes.map(n => `
                <div class="notif-item ${n.is_read ? '' : 'unread'}">
                    <div class="notif-title">${escapeHtml(n.title)}</div>
                    <div class="notif-msg">${escapeHtml(n.message)}</div>
                    <div class="notif-time">${n.created_at || ''}</div>
                </div>
            `).join('');
            fetch('/api/notifications/read', { method: 'POST' }).catch(() => {});
            const badge = document.getElementById('notifBadge');
            if (badge) badge.style.display = 'none';
        }
    }
}

async function loadNotifCount() {
    try {
        const res = await fetch('/api/notifications');
        const notes = await res.json();
        const badge = document.getElementById('notifBadge');
        const unread = notes.filter(n => !n.is_read).length;
        if (badge) {
            badge.textContent = unread;
            badge.style.display = unread > 0 ? 'flex' : 'none';
        }
    } catch(e) {}
}

// ─── Flash auto-dismiss ───
function autoCloseFlash() {
    document.querySelectorAll('.flash').forEach(f => {
        setTimeout(() => f.style.opacity = '0', 3000);
        setTimeout(() => f.remove(), 3500);
    });
}

// ─── Helpers ───
function escapeHtml(str) {
    const d = document.createElement('div');
    d.textContent = str || '';
    return d.innerHTML;
}

// ─── Init ───
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    autoCloseFlash();
    loadNotifCount();
    
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.nav-search')) document.getElementById('searchDropdown')?.classList.remove('show');
        if (!e.target.closest('.notif-wrap')) document.getElementById('notifPanel')?.classList.remove('show');
    });
    
    const chatInput = document.getElementById('chatInput');
    if (chatInput) chatInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendChat(); });
    
    const heroSearch = document.getElementById('heroSearch');
    if (heroSearch) heroSearch.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') window.location.href = `/explore?q=${encodeURIComponent(heroSearch.value)}`;
    });
});
