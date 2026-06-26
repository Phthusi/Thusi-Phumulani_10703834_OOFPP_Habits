from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Frame, TextArea

'''
#use this for selecting delete and update options
items = [
    "Apple",
    "Banana",
    "Orange",
    "Mango",
    "Pineapple"
]

current = 0

text = TextArea(
    text="",
    focusable=False,
    scrollbar=True
)

def refresh():
    lines = []

    for i, item in enumerate(items):
        prefix = "➜ " if i == current else "  "
        lines.append(f"{prefix}{item}")

    text.text = "\n".join(lines)

refresh()

kb = KeyBindings()

@kb.add("down")
def _(event):
    global current
    if current < len(items) - 1:
        current += 1
        refresh()

@kb.add("up")
def _(event):
    global current
    if current > 0:
        current -= 1
        refresh()

@kb.add("enter")
def _(event):
    print(f"\nSelected: {items[current]}")
    event.app.exit()

@kb.add("q")
def _(event):
    event.app.exit()

app = Application(
    layout=Layout(Frame(text, title="Fruit Selector")),
    key_bindings=kb,
    full_screen=True
)

app.run()'''


'''
#view habits
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Frame, TextArea

pages = [
    """
Dashboard

Habits Completed: 12
Habits Missed: 3
Current Streak: 8
""",
    """
Analytics

Completion Rate: 80%
Best Day: Monday
Worst Day: Friday
""",
    """
Upcoming Tasks

- Gym
- Read 20 pages
- Bike 30 mins
""",
]

current_page = 0

content = TextArea(
    text="",
    focusable=False
)

def refresh():
    content.text = (
        f"Page {current_page + 1}/{len(pages)}\n\n"
        + pages[current_page]
    )

refresh()

kb = KeyBindings()

@kb.add("right")
def _(event):
    global current_page
    if current_page < len(pages) - 1:
        current_page += 1
        refresh()

@kb.add("left")
def _(event):
    global current_page
    if current_page > 0:
        current_page -= 1
        refresh()

@kb.add("q")
def _(event):
    event.app.exit()

app = Application(
    layout=Layout(Frame(content, title="Habit Tracker")),
    key_bindings=kb,
    full_screen=True
)

app.run()

'''

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Frame, TextArea

pages = {
    "Dashboard": [
        "Today's Progress",
        "Current Streak",
        "Completion Rate"
    ],
    "Habits": [
        "Gym",
        "Read",
        "Bike",
        "Meditate"
    ],
    "Analytics": [
        "Weekly Stats",
        "Monthly Stats",
        "Yearly Stats"
    ]
}

page_names = list(pages.keys())

current_page = 0
current_option = 0

content = TextArea(focusable=False)

def refresh():
    page = page_names[current_page]
    options = pages[page]

    lines = []

    tabs = " | ".join(
        f"[{p}]" if i == current_page else p
        for i, p in enumerate(page_names)
    )

    lines.append(tabs)
    lines.append("")
    lines.append(f"Page: {page}")
    lines.append("")

    for i, option in enumerate(options):
        prefix = "➜" if i == current_option else " "
        lines.append(f"{prefix} {option}")

    content.text = "\n".join(lines)

refresh()

kb = KeyBindings()

@kb.add("right")
def _(event):
    global current_page, current_option

    if current_page < len(page_names) - 1:
        current_page += 1
        current_option = 0
        refresh()

@kb.add("left")
def _(event):
    global current_page, current_option

    if current_page > 0:
        current_page -= 1
        current_option = 0
        refresh()

@kb.add("down")
def _(event):
    global current_option

    options = pages[page_names[current_page]]

    if current_option < len(options) - 1:
        current_option += 1
        refresh()

@kb.add("up")
def _(event):
    global current_option

    if current_option > 0:
        current_option -= 1
        refresh()

@kb.add("enter")
def _(event):
    page = page_names[current_page]
    option = pages[page][current_option]

    print(f"\nSelected: {page} -> {option}")

@kb.add("q")
def _(event):
    event.app.exit()

app = Application(
    layout=Layout(Frame(content, title="Habit Tracker")),
    key_bindings=kb,
    full_screen=True
)

app.run()