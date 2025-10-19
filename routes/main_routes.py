from datetime import datetime
from math import ceil
from collections import defaultdict
from flask import session, request, redirect, render_template
from app import app
import items

@app.route("/theme")
def theme():
    current = session.get("theme")
    new = "light" if current == "dark" else "dark"
    session["theme"] = new
    return redirect(request.referrer or "/")

@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    per_page = 20

    all_items = items.get_items()
    total_count = len(all_items)
    total_pages = ceil(total_count / per_page)

    start = (page - 1) * per_page
    end = start + per_page
    paged_items = all_items[start:end]

    grouped = defaultdict(list)
    for item in paged_items:
        formatted_date = datetime.strptime(item["date"], "%Y-%m-%d").strftime("%d.%m.%Y")
        grouped[formatted_date].append(item)

    sorted_grouped = dict(sorted(
        grouped.items(),
        key=lambda kv: datetime.strptime(kv[0], "%d.%m.%Y"),
        reverse=True
    ))

    return render_template(
        "index.html",
        grouped=sorted_grouped,
        page=page,
        total_pages=total_pages
    )

@app.route("/info")
def info():
    return render_template("info.html")

@app.template_filter("datetimeformat")
def datetimeformat(value):
    value = datetime.strptime(value, "%Y-%m-%d")
    return value.strftime("%d.%m.%Y")
