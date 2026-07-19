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