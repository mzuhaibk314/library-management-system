from flask import Flask, request, redirect, url_for, flash, render_template_string
from pathlib import Path
from datetime import date, timedelta
import json

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

DATA_DIR = Path(__file__).parent
BOOKS_FILE = DATA_DIR / "books.txt"
ISSUED_FILE = DATA_DIR / "issued.txt"

DEFAULT_BOOKS = {
    # 🏛️ Literary Classics (Pre-20th Century)
    "L101": {"title": "Pride and Prejudice by Jane Austen", "shelf": "A-1", "total_stock": 5, "available_stock": 2},
    "L102": {"title": "Jane Eyre by Charlotte Brontë", "shelf": "A-2", "total_stock": 4, "available_stock": 1},
    "L103": {"title": "Wuthering Heights by Emily Brontë", "shelf": "A-3", "total_stock": 3, "available_stock": 1},
    "L104": {"title": "Frankenstein by Mary Shelley", "shelf": "A-4", "total_stock": 4, "available_stock": 2},
    "L105": {"title": "Dracula by Bram Stoker", "shelf": "A-5", "total_stock": 3, "available_stock": 1},
    "L106": {"title": "Great Expectations by Charles Dickens", "shelf": "A-6", "total_stock": 5, "available_stock": 3},
    "L107": {"title": "A Tale of Two Cities by Charles Dickens", "shelf": "A-7", "total_stock": 4, "available_stock": 2},
    "L108": {"title": "David Copperfield by Charles Dickens", "shelf": "A-8", "total_stock": 3, "available_stock": 1},
    "L109": {"title": "Oliver Twist by Charles Dickens", "shelf": "A-9", "total_stock": 5, "available_stock": 3},
    "L110": {"title": "Middlemarch by George Eliot", "shelf": "A-10", "total_stock": 3, "available_stock": 1},
    "L111": {"title": "Emma by Jane Austen", "shelf": "A-11", "total_stock": 4, "available_stock": 2},
    "L112": {"title": "Sense and Sensibility by Jane Austen", "shelf": "A-12", "total_stock": 4, "available_stock": 2},
    "L113": {"title": "Moby-Dick by Herman Melville", "shelf": "A-13", "total_stock": 3, "available_stock": 1},
    "L114": {"title": "The Scarlet Letter by Nathaniel Hawthorne", "shelf": "A-14", "total_stock": 4, "available_stock": 2},
    "L115": {"title": "The Picture of Dorian Gray by Oscar Wilde", "shelf": "A-15", "total_stock": 5, "available_stock": 3},
    "L116": {"title": "The Count of Monte Cristo by Alexandre Dumas", "shelf": "A-16", "total_stock": 3, "available_stock": 1},
    "L117": {"title": "The Three Musketeers by Alexandre Dumas", "shelf": "A-17", "total_stock": 4, "available_stock": 2},
    "L118": {"title": "Les Misérables by Victor Hugo", "shelf": "A-18", "total_stock": 3, "available_stock": 1},
    "L119": {"title": "The Hunchback of Notre-Dame by Victor Hugo", "shelf": "A-19", "total_stock": 3, "available_stock": 1},
    "L120": {"title": "Anna Karenina by Leo Tolstoy", "shelf": "A-20", "total_stock": 4, "available_stock": 2},
    "L121": {"title": "War and Peace by Leo Tolstoy", "shelf": "A-21", "total_stock": 2, "available_stock": 0},
    "L122": {"title": "Crime and Punishment by Fyodor Dostoevsky", "shelf": "A-22", "total_stock": 4, "available_stock": 2},
    "L123": {"title": "The Brothers Karamazov by Fyodor Dostoevsky", "shelf": "A-23", "total_stock": 3, "available_stock": 1},
    "L124": {"title": "Madame Bovary by Gustave Flaubert", "shelf": "A-24", "total_stock": 3, "available_stock": 1},
    "L125": {"title": "Don Quixote by Miguel de Cervantes", "shelf": "A-25", "total_stock": 3, "available_stock": 1},
    "L126": {"title": "The Adventures of Huckleberry Finn by Mark Twain", "shelf": "A-26", "total_stock": 5, "available_stock": 3},
    "L127": {"title": "The Adventures of Tom Sawyer by Mark Twain", "shelf": "A-27", "total_stock": 5, "available_stock": 3},
    "L128": {"title": "The Odyssey by Homer", "shelf": "A-28", "total_stock": 4, "available_stock": 2},
    "L129": {"title": "The Iliad by Homer", "shelf": "A-29", "total_stock": 4, "available_stock": 2},
    "L130": {"title": "The Divine Comedy by Dante Alighieri", "shelf": "A-30", "total_stock": 3, "available_stock": 1},
    "L131": {"title": "The Canterbury Tales by Geoffrey Chaucer", "shelf": "A-31", "total_stock": 3, "available_stock": 1},
    "L132": {"title": "Little Women by Louisa May Alcott", "shelf": "A-32", "total_stock": 5, "available_stock": 3},
    "L133": {"title": "The Strange Case of Dr. Jekyll and Mr. Hyde by Robert Louis Stevenson", "shelf": "A-33", "total_stock": 4, "available_stock": 2},
    "L134": {"title": "Treasure Island by Robert Louis Stevenson", "shelf": "A-34", "total_stock": 5, "available_stock": 3},
    "L135": {"title": "Alice's Adventures in Wonderland by Lewis Carroll", "shelf": "A-35", "total_stock": 6, "available_stock": 4},

    # 🏢 20th-Century Modern Classics
    "M101": {"title": "The Great Gatsby by F. Scott Fitzgerald", "shelf": "B-1", "total_stock": 5, "available_stock": 3},
    "M102": {"title": "To Kill a Mockingbird by Harper Lee", "shelf": "B-2", "total_stock": 6, "available_stock": 4},
    "M103": {"title": "1984 by George Orwell", "shelf": "B-3", "total_stock": 6, "available_stock": 4},
    "M104": {"title": "Animal Farm by George Orwell", "shelf": "B-4", "total_stock": 5, "available_stock": 3},
    "M105": {"title": "Brave New World by Aldous Huxley", "shelf": "B-5", "total_stock": 4, "available_stock": 2},
    "M106": {"title": "Fahrenheit 451 by Ray Bradbury", "shelf": "B-6", "total_stock": 4, "available_stock": 2},
    "M107": {"title": "The Catcher in the Rye by J.D. Salinger", "shelf": "B-7", "total_stock": 5, "available_stock": 3},
    "M108": {"title": "Lord of the Flies by William Golding", "shelf": "B-8", "total_stock": 4, "available_stock": 2},
    "M109": {"title": "Of Mice and Men by John Steinbeck", "shelf": "B-9", "total_stock": 5, "available_stock": 3},
    "M110": {"title": "The Grapes of Wrath by John Steinbeck", "shelf": "B-10", "total_stock": 3, "available_stock": 1},
    "M111": {"title": "East of Eden by John Steinbeck", "shelf": "B-11", "total_stock": 3, "available_stock": 3},
    "M112": {"title": "Beloved by Toni Morrison", "shelf": "B-12", "total_stock": 4, "available_stock": 4},
    "M113": {"title": "The Bluest Eye by Toni Morrison", "shelf": "B-13", "total_stock": 4, "available_stock": 4},
    "M114": {"title": "Song of Solomon by Toni Morrison", "shelf": "B-14", "total_stock": 3, "available_stock": 3},
    "M115": {"title": "One Hundred Years of Solitude by Gabriel García Márquez", "shelf": "B-15", "total_stock": 4, "available_stock": 4},
    "M116": {"title": "Love in the Time of Cholera by Gabriel García Márquez", "shelf": "B-16", "total_stock": 3, "available_stock": 3},
    "M117": {"title": "Ulysses by James Joyce", "shelf": "B-17", "total_stock": 2, "available_stock": 2},
    "M118": {"title": "A Portrait of the Artist as a Young Man by James Joyce", "shelf": "B-18", "total_stock": 3, "available_stock": 3},
    "M119": {"title": "To the Lighthouse by Virginia Woolf", "shelf": "B-19", "total_stock": 3, "available_stock": 3},
    "M120": {"title": "Mrs. Dalloway by Virginia Woolf", "shelf": "B-20", "total_stock": 4, "available_stock": 4},
    "M121": {"title": "Orlando by Virginia Woolf", "shelf": "B-21", "total_stock": 3, "available_stock": 3},
    "M122": {"title": "The Metamorphosis by Franz Kafka", "shelf": "B-22", "total_stock": 5, "available_stock": 5},
    "M123": {"title": "The Trial by Franz Kafka", "shelf": "B-23", "total_stock": 3, "available_stock": 3},
    "M124": {"title": "Invisible Man by Ralph Ellison", "shelf": "B-24", "total_stock": 3, "available_stock": 3},
    "M125": {"title": "Their Eyes Were Watching God by Zora Neale Hurston", "shelf": "B-25", "total_stock": 4, "available_stock": 4},
    "M126": {"title": "The Color Purple by Alice Walker", "shelf": "B-26", "total_stock": 4, "available_stock": 4},
    "M127": {"title": "The Handmaid's Tale by Margaret Atwood", "shelf": "B-27", "total_stock": 5, "available_stock": 5},
    "M128": {"title": "Catch-22 by Joseph Heller", "shelf": "B-28", "total_stock": 4, "available_stock": 4},
    "M129": {"title": "The Sun Also Rises by Ernest Hemingway", "shelf": "B-29", "total_stock": 4, "available_stock": 4},
    "M130": {"title": "The Old Man and the Sea by Ernest Hemingway", "shelf": "B-30", "total_stock": 5, "available_stock": 5},
    "M131": {"title": "For Whom the Bell Tolls by Ernest Hemingway", "shelf": "B-31", "total_stock": 3, "available_stock": 3},
    "M132": {"title": "Lolita by Vladimir Nabokov", "shelf": "B-32", "total_stock": 3, "available_stock": 3},
    "M133": {"title": "Things Fall Apart by Chinua Achebe", "shelf": "B-33", "total_stock": 4, "available_stock": 4},
    "M134": {"title": "Midnight's Children by Salman Rushdie", "shelf": "B-34", "total_stock": 3, "available_stock": 3},
    "M135": {"title": "The Stranger by Albert Camus", "shelf": "B-35", "total_stock": 4, "available_stock": 4},
    "M136": {"title": "The Plague by Albert Camus", "shelf": "B-36", "total_stock": 3, "available_stock": 3},
    "M137": {"title": "The Bell Jar by Sylvia Plath", "shelf": "B-37", "total_stock": 4, "available_stock": 4},
    "M138": {"title": "Native Son by Richard Wright", "shelf": "B-38", "total_stock": 3, "available_stock": 3},
    "M139": {"title": "All Quiet on the Western Front by Erich Maria Remarque", "shelf": "B-39", "total_stock": 4, "available_stock": 4},
    "M140": {"title": "Slaughterhouse-Five by Kurt Vonnegut", "shelf": "B-40", "total_stock": 4, "available_stock": 4},

    # 🧝‍♂️ Epic Fantasy, Sci-Fi & Popular Classics
    "F101": {"title": "The Hobbit by J.R.R. Tolkien", "shelf": "C-1", "total_stock": 6, "available_stock": 6},
    "F102": {"title": "The Fellowship of the Ring by J.R.R. Tolkien", "shelf": "C-2", "total_stock": 5, "available_stock": 5},
    "F103": {"title": "The Two Towers by J.R.R. Tolkien", "shelf": "C-3", "total_stock": 5, "available_stock": 5},
    "F104": {"title": "The Return of the King by J.R.R. Tolkien", "shelf": "C-4", "total_stock": 5, "available_stock": 5},
    "F105": {"title": "Harry Potter and the Sorcerer's Stone by J.K. Rowling", "shelf": "C-5", "total_stock": 8, "available_stock": 8},
    "F106": {"title": "The Chronicles of Narnia by C.S. Lewis", "shelf": "C-6", "total_stock": 5, "available_stock": 5},
    "F107": {"title": "Dune by Frank Herbert", "shelf": "C-7", "total_stock": 5, "available_stock": 5},
    "F108": {"title": "Foundation by Isaac Asimov", "shelf": "C-8", "total_stock": 4, "available_stock": 4},
    "F109": {"title": "Neuromancer by William Gibson", "shelf": "C-9", "total_stock": 3, "available_stock": 3},
    "F110": {"title": "The Hitchhiker's Guide to the Galaxy by Douglas Adams", "shelf": "C-10", "total_stock": 5, "available_stock": 5},

    # 🕵️ Mystery, Thriller & Contemporary Classics
    "C101": {"title": "And Then There Were None by Agatha Christie", "shelf": "D-1", "total_stock": 5, "available_stock": 5},
    "C102": {"title": "Murder on the Orient Express by Agatha Christie", "shelf": "D-2", "total_stock": 5, "available_stock": 5},
    "C103": {"title": "The Hound of the Baskervilles by Arthur Conan Doyle", "shelf": "D-3", "total_stock": 4, "available_stock": 4},
    "C104": {"title": "The Secret History by Donna Tartt", "shelf": "D-4", "total_stock": 3, "available_stock": 3},
    "C105": {"title": "The Goldfinch by Donna Tartt", "shelf": "D-5", "total_stock": 3, "available_stock": 3},
    "C106": {"title": "Never Let Me Go by Kazuo Ishiguro", "shelf": "D-6", "total_stock": 4, "available_stock": 4},
    "C107": {"title": "The Remains of the Day by Kazuo Ishiguro", "shelf": "D-7", "total_stock": 3, "available_stock": 3},
    "C108": {"title": "Atonement by Ian McEwan", "shelf": "D-8", "total_stock": 4, "available_stock": 4},
    "C109": {"title": "Life of Pi by Yann Martel", "shelf": "D-9", "total_stock": 5, "available_stock": 5},
    "C110": {"title": "The Book Thief by Markus Zusak", "shelf": "D-10", "total_stock": 5, "available_stock": 5},
    "C111": {"title": "The Shadow of the Wind by Carlos Ruiz Zafón", "shelf": "D-11", "total_stock": 3, "available_stock": 3},
    "C112": {"title": "The Kite Runner by Khaled Hosseini", "shelf": "D-12", "total_stock": 6, "available_stock": 6},
    "C113": {"title": "A Thousand Splendid Suns by Khaled Hosseini", "shelf": "D-13", "total_stock": 5, "available_stock": 5},
    "C114": {"title": "Normal People by Sally Rooney", "shelf": "D-14", "total_stock": 4, "available_stock": 4},
    "C115": {"title": "Americanah by Chimamanda Ngozi Adichie", "shelf": "D-15", "total_stock": 4, "available_stock": 4}
}


def get_default_issued():
    """Generates exactly 37 initially issued records with mixed due dates (Overdue, Due Today, Tomorrow, within 1 week)."""
    today = date.today()
    book_ids = list(DEFAULT_BOOKS.keys())
    records = []
    
    # Offsets distribution for 37 books: e.g., -4, -3, -2, -1 (Overdue), 0 (Due Today), 1 (Tomorrow), 2 to 6 (Upcoming within 1 week)
    for i in range(37):
        book_id = book_ids[i % len(book_ids)]
        student_id = f"STD{201 + i}"
        
        # Calculate offset from today (-4 days to +5 days)
        offset = (i % 10) - 4 
        due = today + timedelta(days=offset)
        issue = due - timedelta(days=6) # Issued 6 days before due date
        if issue > today:
            issue = today - timedelta(days=1)
            
        records.append({
            "student_id": student_id,
            "book_id": book_id,
            "issue_date": issue.isoformat(),
            "due_date": due.isoformat()
        })
    return records


def load_data(path, default):
    """Read JSON data from a .txt file, or create it if missing."""
    if not path.exists():
        initial_data = default() if callable(default) else default.copy()
        save_data(path, initial_data)
        return initial_data

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, (list, dict)) else (default() if callable(default) else default.copy())
    except (json.JSONDecodeError, OSError):
        initial_data = default() if callable(default) else default.copy()
        return initial_data


def save_data(path, data):
    """Save data permanently in a plain text file."""
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_books():
    return load_data(BOOKS_FILE, DEFAULT_BOOKS)


def get_issued():
    return load_data(ISSUED_FILE, get_default_issued)


def save_all(books, issued):
    save_data(BOOKS_FILE, books)
    save_data(ISSUED_FILE, issued)


def calculate_return_days(due_date):
    """Return days remaining, zero if due today, or a negative overdue count."""
    return (date.fromisoformat(due_date) - date.today()).days


def find_book(books, query):
    query = query.strip().lower()
    if not query:
        return []
    return [
        (book_id, details)
        for book_id, details in books.items()
        if query == book_id.lower() or query in details["title"].lower()
    ]


BASE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ page_title }} | BookNest Library</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--navy:#171b4b;--indigo:#4546c8;--purple:#7776ee;--bg:#f5f6fc;--ink:#202342;--muted:#8589a5;--line:#e9eaf3;--white:#fff;--green:#16845d;--red:#d34b5c}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:'DM Sans',sans-serif}
.layout{display:flex;min-height:100vh}.sidebar{width:245px;background:var(--navy);color:#fff;padding:27px 18px;display:flex;flex-direction:column;flex-shrink:0}
.brand{font:800 23px Manrope,sans-serif;letter-spacing:-1px;padding:5px 12px 35px}.brand span{color:#a6a5ff}
.nav-label{font-size:10px;letter-spacing:1.7px;color:#898bb7;padding:0 13px 12px;font-weight:700}
.nav a{display:block;text-decoration:none;color:#b9bbd7;padding:13px 14px;border-radius:11px;margin:4px 0;font-size:14px;font-weight:600}
.nav a:hover,.nav a.active{background:#30336f;color:#fff}.nav a .ico{display:inline-block;width:26px}
.side-bottom{margin-top:auto;padding:17px 12px;color:#aeb0d0;font-size:12px;line-height:1.7;border-top:1px solid #34366c}
.main{flex:1;min-width:0;padding:30px 4.2% 50px;max-width:1500px;margin:0 auto;width:100%}
.topbar{display:flex;align-items:center;justify-content:space-between;margin-bottom:30px;gap:15px}
.eyebrow{color:var(--muted);font-size:12px;font-weight:700;letter-spacing:1.3px;text-transform:uppercase}
h1{font:800 27px Manrope,sans-serif;margin:7px 0 0;letter-spacing:-.8px}
.profile{display:flex;align-items:center;gap:10px;background:white;padding:8px 14px;border:1px solid var(--line);border-radius:14px;font-size:13px;font-weight:700}
.avatar{width:34px;height:34px;border-radius:11px;background:#e8e8ff;color:var(--indigo);display:grid;place-items:center;font-weight:800}
.welcome{background:linear-gradient(110deg,#30338c,#6464df);color:white;border-radius:20px;padding:27px 30px;margin-bottom:23px;position:relative;overflow:hidden}
.welcome:after{content:"";position:absolute;width:220px;height:220px;border:35px solid #ffffff12;border-radius:50%;right:7%;top:-105px}
.welcome h2{font:800 22px Manrope;margin:0 0 8px}.welcome p{margin:0;color:#e0e0ff;font-size:14px;max-width:550px;line-height:1.6}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:24px}
.stat,.panel{background:white;border:1px solid var(--line);border-radius:17px;padding:20px}
.stat-top{display:flex;justify-content:space-between;align-items:center;color:var(--muted);font-size:12px;font-weight:700}
.stat-icon{width:35px;height:35px;display:grid;place-items:center;border-radius:11px;background:#eeeeff;color:var(--indigo);font-size:17px}
.stat-number{font:800 27px Manrope;margin-top:12px}.stat-note{font-size:11px;color:var(--muted);margin-top:3px}
.content-grid{display:grid;grid-template-columns:1.3fr .9fr;gap:18px;margin-bottom:20px}
.panel{padding:22px}.panel-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:18px}
.panel h3{font:800 16px Manrope;margin:0}.sub{color:var(--muted);font-size:12px;margin-top:5px}
.search-form{display:flex;gap:9px;margin-bottom:17px}
input,select{font:14px 'DM Sans';padding:12px 13px;border:1px solid #e3e4ef;border-radius:10px;outline:none;background:#fff;color:var(--ink);width:100%;min-width:0}
input:focus,select:focus{border-color:var(--purple);box-shadow:0 0 0 3px #7776ee18}
.btn{display:inline-block;border:0;border-radius:10px;padding:12px 17px;background:var(--indigo);color:white;font:700 13px 'DM Sans';text-decoration:none;cursor:pointer;white-space:nowrap}
.btn:hover{background:#3536a9}.btn-light{background:#eeeeff;color:var(--indigo)}.btn-light:hover{background:#e1e1ff}
.btn-red{background:#fff0f1;color:var(--red)}.btn-green{background:#e9f8f1;color:var(--green)}
table{width:100%;border-collapse:collapse;font-size:13px}th{text-align:left;color:var(--muted);font-size:10px;letter-spacing:1px;text-transform:uppercase;padding:11px 9px;border-bottom:1px solid var(--line)}
td{padding:13px 9px;border-bottom:1px solid #f0f0f6}tr:last-child td{border-bottom:0}
.book-title{font-weight:700}.book-id{font-size:11px;color:var(--muted);margin-top:4px}
.pill{display:inline-block;padding:5px 9px;border-radius:30px;background:#eaf7f1;color:var(--green);font-size:10px;font-weight:700}
.pill.low{background:#fff4e5;color:#ad6a0b}.pill.overdue{background:#fff0f1;color:var(--red)}
.muted{color:var(--muted)}.empty{text-align:center;padding:25px;color:var(--muted);font-size:13px}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:13px}.field label{display:block;font-size:12px;font-weight:700;margin:0 0 7px}.field.full{grid-column:1/-1}
.flash{padding:12px 15px;border-radius:11px;background:#eaf7f1;color:#176d50;margin-bottom:15px;font-size:13px;font-weight:600}
.flash.error{background:#fff0f1;color:#bd3d4e}
.actions{display:flex;gap:7px;flex-wrap:wrap}.section-gap{margin-top:19px}
.footer{text-align:center;color:#a1a3b8;font-size:11px;padding:25px}
@media(max-width:1000px){.stats{grid-template-columns:repeat(2,1fr)}.content-grid{grid-template-columns:1fr}}
@media(max-width:650px){.layout{display:block}.sidebar{width:100%;padding:15px}.brand{padding:5px 8px 13px}.nav{display:flex;overflow:auto}.nav-label,.side-bottom{display:none}.nav a{white-space:nowrap;padding:10px}.main{padding:22px 15px}.topbar{align-items:flex-start}.profile{display:none}.stats{gap:9px}.stat{padding:14px}.stat-number{font-size:23px}.welcome{padding:22px}.panel{padding:15px}.form-grid{grid-template-columns:1fr}.field.full{grid-column:auto}table{font-size:11px}td,th{padding:10px 5px}}
</style>
</head>
<body>
<div class="layout">
<aside class="sidebar">
  <div class="brand">Book<span>Nest.</span></div>
  <div class="nav-label">MAIN MENU</div>
  <nav class="nav">
    <a href="{{ url_for('dashboard') }}" class="{{ 'active' if active=='dashboard' else '' }}"><span class="ico">▦</span> Dashboard</a>
    <a href="{{ url_for('catalog') }}" class="{{ 'active' if active=='catalog' else '' }}"><span class="ico">▤</span> Book catalogue</a>
    <a href="{{ url_for('issue') }}" class="{{ 'active' if active=='issue' else '' }}"><span class="ico">↗</span> Issue a book</a>
    <a href="{{ url_for('returns') }}" class="{{ 'active' if active=='returns' else '' }}"><span class="ico">↙</span> Return a book</a>
  </nav>
  <div class="side-bottom">LIBRARY MANAGEMENT SYSTEM<br>Academic Year 2026–2027<br>Python • Flask • Text Files</div>
</aside>
<main class="main">
  <header class="topbar">
    <div><div class="eyebrow">School Library / {{ page_title }}</div><h1>{{ page_title }}</h1></div>
    <div class="profile"><div class="avatar">Z</div><div>Library Staff<br><span class="muted" style="font-size:10px;font-weight:400">Administrator</span></div></div>
  </header>
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}<div class="flash {{ 'error' if category=='error' else '' }}">{{ message }}</div>{% endfor %}
  {% endwith %}
  {{ content|safe }}
  <div class="footer">BookNest Library Manager · Built with Python</div>
</main>
</div>
</body></html>
"""


def page(title, active, content, **context):
    return render_template_string(
        BASE, page_title=title, active=active, content=content, **context
    )


@app.route("/")
def dashboard():
    books = get_books()
    issued = get_issued()
    total_titles = len(books)
    total_copies = sum(book["total_stock"] for book in books.values())
    available = sum(book["available_stock"] for book in books.values())
    overdue = sum(
        1 for record in issued
        if calculate_return_days(record["due_date"]) < 0
    )
    recent = issued[-5:][::-1]

    content = r"""
    <section class="welcome">
      <h2>Your library, organised.</h2>
      <p>Manage your books, keep track of student issues, and stay updated on return dates from one simple dashboard.</p>
    </section>
    <section class="stats">
      <div class="stat"><div class="stat-top">BOOK TITLES <span class="stat-icon">▤</span></div><div class="stat-number">{{ total_titles }}</div><div class="stat-note">Different titles in catalogue</div></div>
      <div class="stat"><div class="stat-top">TOTAL COPIES <span class="stat-icon">▣</span></div><div class="stat-number">{{ total_copies }}</div><div class="stat-note">Copies registered in library</div></div>
      <div class="stat"><div class="stat-top">AVAILABLE <span class="stat-icon">✓</span></div><div class="stat-number">{{ available }}</div><div class="stat-note">Copies ready to issue</div></div>
      <div class="stat"><div class="stat-top">OVERDUE <span class="stat-icon">!</span></div><div class="stat-number">{{ overdue }}</div><div class="stat-note">Books past their due date</div></div>
    </section>
    <section class="content-grid">
      <div class="panel">
        <div class="panel-head"><div><h3>Find a book</h3><div class="sub">Search by title or unique Book ID</div></div></div>
        <form class="search-form" action="{{ url_for('catalog') }}" method="get"><input name="q" placeholder="Try 1984, Dune or L101"><button class="btn">Search</button></form>
        <div class="sub">Use the catalogue to view shelf location and available stock.</div>
      </div>
      <div class="panel">
        <div class="panel-head"><div><h3>Quick actions</h3><div class="sub">Common library tasks</div></div></div>
        <div class="actions"><a class="btn" href="{{ url_for('issue') }}">＋ Issue a book</a><a class="btn btn-light" href="{{ url_for('returns') }}">↙ Return a book</a></div>
      </div>
    </section>
    <section class="panel">
      <div class="panel-head"><div><h3>Recent issue records</h3><div class="sub">Latest books issued to students (37 initial records loaded)</div></div><a class="btn btn-light" href="{{ url_for('returns') }}">View all</a></div>
      {% if recent %}
      <table><thead><tr><th>Student</th><th>Book ID</th><th>Issue date</th><th>Due date</th><th>Status</th></tr></thead><tbody>
      {% for r in recent %}<tr><td class="book-title">{{ r.student_id }}</td><td>{{ r.book_id }}</td><td>{{ r.issue_date }}</td><td>{{ r.due_date }}</td><td>{% set days=(r.due_date|todays_days) %}{% if days<0 %}<span class="pill overdue">Overdue</span>{% elif days==0 %}<span class="pill low">Due today</span>{% else %}<span class="pill">On time</span>{% endif %}</td></tr>{% endfor %}
      </tbody></table>
      {% else %}<div class="empty">No books have been issued yet.</div>{% endif %}
    </section>
    """
    return page("Dashboard", "dashboard", content, total_titles=total_titles,
                total_copies=total_copies, available=available, overdue=overdue,
                recent=recent)


@app.template_filter("todays_days")
def todays_days(due_date):
    return calculate_return_days(due_date)


@app.route("/catalog")
def catalog():
    books = get_books()
    query = request.args.get("q", "").strip()
    matches = find_book(books, query) if query else list(books.items())
    content = r"""
    <section class="panel">
      <div class="panel-head"><div><h3>Library catalogue</h3><div class="sub">Search, view, and add books to your collection.</div></div></div>
      <form class="search-form" method="get"><input name="q" value="{{ query }}" placeholder="Search by title or Book ID"><button class="btn">Search</button><a class="btn btn-light" href="{{ url_for('catalog') }}">Clear</a></form>
      <table><thead><tr><th>Book details</th><th>Shelf</th><th>Availability</th><th>Status</th></tr></thead><tbody>
      {% for book_id,b in matches %}
      <tr><td><div class="book-title">{{ b.title }}</div><div class="book-id">{{ book_id }}</div></td><td>{{ b.shelf }}</td><td>{{ b.available_stock }} / {{ b.total_stock }}</td><td>{% if b.available_stock>0 %}<span class="pill">In stock</span>{% else %}<span class="pill overdue">Unavailable</span>{% endif %}</td></tr>
      {% else %}<tr><td colspan="4" class="empty">No matching book record found.</td></tr>{% endfor %}
      </tbody></table>
    </section>
    <section class="panel section-gap">
      <div class="panel-head"><div><h3>Add a new book</h3><div class="sub">Register a title and its shelf location.</div></div></div>
      <form method="post" action="{{ url_for('add_book') }}" class="form-grid">
        <div class="field"><label>Book ID</label><input name="book_id" placeholder="e.g. B105" required></div>
        <div class="field"><label>Book title</label><input name="title" placeholder="Enter book title" required></div>
        <div class="field"><label>Shelf location</label><input name="shelf" placeholder="e.g. A-2" required></div>
        <div class="field"><label>Total copies</label><input name="stock" type="number" min="1" placeholder="e.g. 5" required></div>
        <div class="field full"><button class="btn">＋ Add book to catalogue</button></div>
      </form>
    </section>
    """
    return page("Book Catalogue", "catalog", content, query=query, matches=matches)


@app.route("/add-book", methods=["POST"])
def add_book():
    books = get_books()
    book_id = request.form.get("book_id", "").strip().upper()
    title = request.form.get("title", "").strip()
    shelf = request.form.get("shelf", "").strip()
    try:
        stock = int(request.form.get("stock", ""))
        if not all([book_id, title, shelf]) or stock <= 0:
            raise ValueError
    except ValueError:
        flash("Enter a valid Book ID, title, shelf, and positive stock number.", "error")
        return redirect(url_for("catalog"))
    if book_id in books:
        flash("That Book ID already exists. Choose a unique ID.", "error")
        return redirect(url_for("catalog"))
    books[book_id] = {"title": title, "shelf": shelf,
                      "total_stock": stock, "available_stock": stock}
    save_data(BOOKS_FILE, books)
    flash(f"{title} was added to the catalogue.")
    return redirect(url_for("catalog"))


@app.route("/issue", methods=["GET", "POST"])
def issue():
    books = get_books()
    issued = get_issued()
    today_date = date.today()
    max_due_date = today_date + timedelta(days=7)

    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip().upper()
        book_id = request.form.get("book_id", "").strip().upper()
        due_date = request.form.get("due_date", "").strip()
        if not student_id or not book_id or not due_date:
            flash("Please complete every field.", "error")
        elif book_id not in books:
            flash("Book ID not found in the catalogue.", "error")
        elif books[book_id]["available_stock"] <= 0:
            flash("No copies of this book are currently available.", "error")
        else:
            try:
                due = date.fromisoformat(due_date)
                if due < today_date or due > max_due_date:
                    raise ValueError
                books[book_id]["available_stock"] -= 1
                issued.append({
                    "student_id": student_id,
                    "book_id": book_id,
                    "issue_date": today_date.isoformat(),
                    "due_date": due.isoformat()
                })
                save_all(books, issued)
                flash(f"Book {book_id} successfully issued to {student_id}.")
                return redirect(url_for("returns"))
            except ValueError:
                flash("Due date must be between today and within 1 week (max 7 days).", "error")

    content = r"""
    <section class="panel">
      <div class="panel-head"><div><h3>Issue a book</h3><div class="sub">Assign an available copy to a student (Maximum borrowing time: 1 week).</div></div></div>
      <form method="post" class="form-grid">
        <div class="field full"><label>Student ID</label><input name="student_id" placeholder="e.g. STD101" required></div>
        <div class="field full"><label>Book ID</label><select name="book_id" required><option value="">Select a book</option>{% for bid,b in books.items() if b.available_stock>0 %}<option value="{{ bid }}">{{ bid }} · {{ b.title }} ({{ b.available_stock }} available)</option>{% endfor %}</select></div>
        <div class="field full"><label>Due date (Max 1 week / 7 days)</label><input type="date" name="due_date" min="{{ today }}" max="{{ max_date }}" required></div>
        <div class="field full"><button class="btn">Confirm issue</button></div>
      </form>
    </section>
    """
    return page("Issue a Book", "issue", content, books=books, today=today_date.isoformat(), max_date=max_due_date.isoformat())


@app.route("/returns", methods=["GET", "POST"])
def returns():
    books = get_books()
    issued = get_issued()
    if request.method == "POST":
        try:
            index = int(request.form.get("record_index", ""))
            if index < 0 or index >= len(issued):
                raise ValueError
            record = issued.pop(index)
            if record["book_id"] in books:
                books[record["book_id"]]["available_stock"] += 1
            save_all(books, issued)
            flash(f"Book {record['book_id']} returned by {record['student_id']}. Stock updated.")
            return redirect(url_for("returns"))
        except (ValueError, KeyError):
            flash("That issue record could not be found.", "error")

    records = []
    for index, record in enumerate(issued):
        days = calculate_return_days(record["due_date"])
        records.append({**record, "index": index, "days": days})
    records.reverse()
    content = r"""
    <section class="panel">
      <div class="panel-head"><div><h3>Issued book records</h3><div class="sub">Track due dates and process returned books.</div></div></div>
      {% if records %}
      <table><thead><tr><th>Student / Book</th><th>Issue date</th><th>Due date</th><th>Return status</th><th>Action</th></tr></thead><tbody>
      {% for r in records %}<tr>
        <td><div class="book-title">{{ r.student_id }}</div><div class="book-id">{{ r.book_id }}</div></td>
        <td>{{ r.issue_date }}</td><td>{{ r.due_date }}</td>
        <td>{% if r.days<0 %}<span class="pill overdue">Overdue by {{ -r.days }} day(s)</span>{% elif r.days==0 %}<span class="pill low">Due today</span>{% else %}<span class="pill">{{ r.days }} day(s) left</span>{% endif %}</td>
        <td><form method="post"><input type="hidden" name="record_index" value="{{ r.index }}"><button class="btn btn-green">Mark returned</button></form></td>
      </tr>{% endfor %}
      </tbody></table>
      {% else %}<div class="empty">There are currently no issued books.</div>{% endif %}
    </section>
    """
    return page("Returns & Due Dates", "returns", content, records=records)


if __name__ == "__main__":
    # Create the text files on the first run.
    if not BOOKS_FILE.exists():
        save_data(BOOKS_FILE, DEFAULT_BOOKS)
    if not ISSUED_FILE.exists():
        save_data(ISSUED_FILE, get_default_issued())
    app.run(debug=True)