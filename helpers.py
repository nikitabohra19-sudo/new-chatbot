"""Helper utilities for AI Navigator."""

def stars_html(rating):
    """Generate star rating HTML."""
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half
    return '★' * full + ('½' if half else '') + '☆' * empty

def time_ago(dt_str):
    """Simple time ago string."""
    from datetime import datetime
    try:
        dt = datetime.strptime(str(dt_str), '%Y-%m-%d %H:%M:%S')
        diff = (datetime.now() - dt).days
        if diff == 0: return 'Today'
        if diff == 1: return 'Yesterday'
        if diff < 30: return f'{diff} days ago'
        return f'{diff // 30} months ago'
    except:
        return 'Recently'

def pricing_badge(pricing):
    """Return CSS class for pricing type."""
    p = str(pricing).lower()
    if 'free' in p: return 'badge-free'
    if 'freemium' in p: return 'badge-freemium'
    return 'badge-paid'
