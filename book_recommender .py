"""Rule-Based Book Recommendation System (AI Mini Project)
Concepts: Knowledge Base, IF-THEN Rules, Forward Chaining, Backward Chaining (Unit IV)
Run: python book_recommender.py  -> opens the website automatically.
No extra installation needed (uses only Python's standard library)."""

import webbrowser
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# ---------- KNOWLEDGE BASE 1: Facts (books) : title, author, genre, level, tone ----------
BOOKS = [
    ("Harry Potter and the Philosopher's Stone", "J.K. Rowling", "Fantasy", "Easy", "Thrilling"),
    ("The Hobbit", "J.R.R. Tolkien", "Fantasy", "Easy", "Thrilling"),
    ("The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", "Hard", "Deep"),
    ("A Game of Thrones", "George R.R. Martin", "Fantasy", "Hard", "Thrilling"),
    ("The Name of the Wind", "Patrick Rothfuss", "Fantasy", "Medium", "Deep"),
    ("Percy Jackson: The Lightning Thief", "Rick Riordan", "Fantasy", "Easy", "Light"),
    ("The Chronicles of Narnia", "C.S. Lewis", "Fantasy", "Easy", "Light"),
    ("Mistborn", "Brandon Sanderson", "Fantasy", "Medium", "Thrilling"),

    ("Dune", "Frank Herbert", "Sci-Fi", "Hard", "Deep"),
    ("Ender's Game", "Orson Scott Card", "Sci-Fi", "Medium", "Thrilling"),
    ("The Martian", "Andy Weir", "Sci-Fi", "Easy", "Light"),
    ("1984", "George Orwell", "Sci-Fi", "Medium", "Deep"),
    ("Brave New World", "Aldous Huxley", "Sci-Fi", "Medium", "Deep"),
    ("Foundation", "Isaac Asimov", "Sci-Fi", "Medium", "Deep"),
    ("I, Robot", "Isaac Asimov", "Sci-Fi", "Easy", "Thrilling"),
    ("Neuromancer", "William Gibson", "Sci-Fi", "Hard", "Thrilling"),

    ("A Study in Scarlet", "Arthur Conan Doyle", "Mystery", "Easy", "Thrilling"),
    ("And Then There Were None", "Agatha Christie", "Mystery", "Easy", "Thrilling"),
    ("The Girl with the Dragon Tattoo", "Stieg Larsson", "Mystery", "Medium", "Thrilling"),
    ("Gone Girl", "Gillian Flynn", "Mystery", "Medium", "Thrilling"),
    ("The Da Vinci Code", "Dan Brown", "Mystery", "Easy", "Thrilling"),
    ("Murder on the Orient Express", "Agatha Christie", "Mystery", "Easy", "Light"),
    ("The Silent Patient", "Alex Michaelides", "Mystery", "Medium", "Deep"),
    ("The Name of the Rose", "Umberto Eco", "Mystery", "Hard", "Deep"),

    ("Atomic Habits", "James Clear", "Self-Help", "Easy", "Inspiring"),
    ("The 7 Habits of Highly Effective People", "Stephen Covey", "Self-Help", "Medium", "Inspiring"),
    ("Deep Work", "Cal Newport", "Self-Help", "Medium", "Deep"),
    ("Think and Grow Rich", "Napoleon Hill", "Self-Help", "Easy", "Inspiring"),
    ("The Power of Now", "Eckhart Tolle", "Self-Help", "Medium", "Deep"),
    ("Rich Dad Poor Dad", "Robert Kiyosaki", "Self-Help", "Easy", "Inspiring"),
    ("The Subtle Art of Not Giving a F*ck", "Mark Manson", "Self-Help", "Easy", "Light"),
    ("Thinking, Fast and Slow", "Daniel Kahneman", "Self-Help", "Hard", "Deep"),

    ("Artificial Intelligence: A Modern Approach", "Russell & Norvig", "Technology", "Hard", "Deep"),
    ("Clean Code", "Robert C. Martin", "Technology", "Medium", "Deep"),
    ("The Pragmatic Programmer", "Hunt & Thomas", "Technology", "Medium", "Inspiring"),
    ("Python Crash Course", "Eric Matthes", "Technology", "Easy", "Light"),
    ("Life 3.0", "Max Tegmark", "Technology", "Medium", "Deep"),
    ("Superintelligence", "Nick Bostrom", "Technology", "Hard", "Deep"),
    ("Hands-On Machine Learning", "Aurelien Geron", "Technology", "Hard", "Deep"),
    ("Automate the Boring Stuff with Python", "Al Sweigart", "Technology", "Easy", "Light"),

    ("Sapiens", "Yuval Noah Harari", "History", "Easy", "Deep"),
    ("Guns, Germs, and Steel", "Jared Diamond", "History", "Hard", "Deep"),
    ("The Discovery of India", "Jawaharlal Nehru", "History", "Hard", "Deep"),
    ("India After Gandhi", "Ramachandra Guha", "History", "Hard", "Deep"),
    ("The Diary of a Young Girl", "Anne Frank", "History", "Easy", "Inspiring"),
    ("Homo Deus", "Yuval Noah Harari", "History", "Medium", "Deep"),
    ("A Brief History of Time", "Stephen Hawking", "History", "Medium", "Deep"),
    ("Wings of Fire", "A.P.J. Abdul Kalam", "History", "Easy", "Inspiring"),

    ("Pride and Prejudice", "Jane Austen", "Fiction", "Medium", "Light"),
    ("The Fault in Our Stars", "John Green", "Fiction", "Easy", "Light"),
    ("Me Before You", "Jojo Moyes", "Fiction", "Easy", "Light"),
    ("Normal People", "Sally Rooney", "Fiction", "Medium", "Deep"),
    ("The Notebook", "Nicholas Sparks", "Fiction", "Easy", "Light"),
    ("Jane Eyre", "Charlotte Bronte", "Fiction", "Hard", "Deep"),
    ("Outlander", "Diana Gabaldon", "Fiction", "Medium", "Thrilling"),
    ("The Kite Runner", "Khaled Hosseini", "Fiction", "Medium", "Inspiring"),
]

# ---------- KNOWLEDGE BASE 2: IF-THEN Rules (IF fact THEN new fact) ----------
RULES = [
    ("level=Beginner", "lvl=Easy"),
    ("level=Intermediate", "lvl=Easy"),
    ("level=Intermediate", "lvl=Medium"),
    ("level=Advanced", "lvl=Medium"),
    ("level=Advanced", "lvl=Hard"),
    ("mood=Relaxed", "tone=Light"),
    ("mood=Excited", "tone=Thrilling"),
    ("mood=Thoughtful", "tone=Deep"),
    ("mood=Motivated", "tone=Inspiring"),
]

GENRES = sorted({b[2] for b in BOOKS})
LEVELS = ["Beginner", "Intermediate", "Advanced"]
MOODS = ["Relaxed", "Excited", "Thoughtful", "Motivated"]


# ---------- INFERENCE ENGINE: Forward Chaining ----------
def recommend(genre, level, mood):
    facts = {f"level={level}", f"mood={mood}"}          # known facts from user
    fired = []
    changed = True
    while changed:                                        # keep applying rules
        changed = False
        for i, (cond, concl) in enumerate(RULES, 1):
            if cond in facts and concl not in facts:
                facts.add(concl)
                fired.append(f"R{i}: IF {cond} THEN {concl}")
                changed = True
    lvls = {f[4:] for f in facts if f.startswith("lvl=")}
    tones = {f[5:] for f in facts if f.startswith("tone=")}
    # Final rule: IF genre matches AND level allowed AND tone matches THEN recommend
    result = [b for b in BOOKS if b[2] == genre and b[3] in lvls and b[4] in tones]
    note = ""
    if not result:                                        # fallback rule
        result = [b for b in BOOKS if b[2] == genre and b[3] in lvls]
        note = "No exact match, so the mood rule was relaxed."
    return result, fired, note


# ---------- INFERENCE ENGINE: Backward Chaining (goal-driven) ----------
def prove(goal, facts, trace, d=0):
    """Try to prove 'goal': is it a known fact? else find a rule that concludes it."""
    if goal in facts:
        trace.append((d, f"{goal} is a known fact  [YES]"))
        return True
    for cond, concl in RULES:
        if concl == goal:
            trace.append((d, f"Goal {goal}: try rule IF {cond} THEN {goal}"))
            if prove(cond, facts, trace, d + 1):
                trace.append((d, f"{goal} proved  [YES]"))
                return True
    trace.append((d, f"{goal} cannot be proved  [NO]"))
    return False


def backward(title, genre, level, mood):
    """Goal: recommend(book). Sub-goals: genre, level and tone must all be proved."""
    book = next(b for b in BOOKS if b[0] == title)
    facts = {f"genre={genre}", f"level={level}", f"mood={mood}"}   # only user facts
    trace = [(0, f"MAIN GOAL: recommend('{title}')")]
    subgoals = [f"genre={book[2]}", f"lvl={book[3]}", f"tone={book[4]}"]
    ok = True
    for g in subgoals:
        ok = prove(g, facts, trace, 1) and ok
    trace.append((0, "RESULT: book is " + ("RECOMMENDED" if ok else "NOT recommended")))
    return ok, trace


# ---------- WEB PAGE ----------
def options(items, chosen):
    return "".join(f"<option {'selected' if i == chosen else ''}>{i}</option>" for i in items)


def book_opts(chosen):
    return "<option value=''>-- none --</option>" + "".join(
        f"<option {'selected' if b[0] == chosen else ''}>{escape(b[0])}</option>" for b in BOOKS)


def page(genre="", level="", mood="", book=""):
    out = ""
    if genre and level and mood:
        books, fired, note = recommend(genre, level, mood)
        rules = "".join(f"<li>{escape(r)}</li>" for r in fired)
        cards = "".join(
            f"<div class='card'><b>{escape(t)}</b><br>by {escape(a)}"
            f"<br><small>{g} | {l} | {tn}</small></div>" for t, a, g, l, tn in books)
        out = (f"<h2>Recommended Books ({len(books)})</h2><p><i>{note}</i></p>{cards}"
               f"<h3>Rules Fired (Forward Chaining)</h3><ul>{rules}</ul>")
    if book and genre and level and mood:
        ok, trace = backward(book, genre, level, mood)
        steps = "".join(f"<div style='margin-left:{d * 22}px'>{escape(t)}</div>" for d, t in trace)
        out += (f"<h3>Backward Chaining: Why / Why not this book?</h3>"
                f"<div class='card' style='border-color:{'green' if ok else 'red'}'>{steps}</div>")
    return f"""<!DOCTYPE html><html><head><meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>Book Recommender</title><style>
body{{font-family:Arial;background:#f0f4f8;margin:0;padding:20px}}
.box{{max-width:760px;margin:auto;background:#fff;padding:25px;border-radius:12px}}
h1{{color:#2c3e50}} select,button{{padding:8px;margin:5px;font-size:15px}}
button{{background:#2c7be5;color:#fff;border:0;border-radius:6px}}
.card{{background:#eef5ff;margin:8px 0;padding:10px;border-left:5px solid #2c7be5;border-radius:6px}}
</style></head><body><div class='box'>
<h1>Rule-Based Book Recommendation System</h1>
<p>{len(BOOKS)} books in knowledge base | {len(RULES)} IF-THEN rules</p>
<form>Genre: <select name='genre'>{options(GENRES, genre)}</select>
Level: <select name='level'>{options(LEVELS, level)}</select>
Mood: <select name='mood'>{options(MOODS, mood)}</select>
<br>Verify a book: <select name='book'>{book_opts(book)}</select>
<button>Recommend / Verify</button></form>{out}</div></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        get = lambda k: q.get(k, [""])[0]
        body = page(get("genre"), get("level"), get("mood"), get("book")).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print("Open http://localhost:8000  (Press Ctrl+C to stop)")
    webbrowser.open("http://localhost:8000")
    HTTPServer(("localhost", 8000), Handler).serve_forever()
