from rich.table import Table
from rich.console import Console
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Frame, TextArea
from io import StringIO


class View:

    def __init__(self):

        self.pages = {
            "p1": [
                (1, "jogging", "2026-06-01 14:00:00", "00:15:00", "MISSED"),
                (2, "reading", "2026-06-02 14:00:00", "00:20:00", "DONE"),
                (3, "coding", "2026-06-03 14:00:00", "01:00:00", "MISSED"),
            ],

            "p2": [
                (4, "studying", "2026-06-10 14:10:00", "02:00:00", "UPCOMING"),
                (5, "gym", "2026-06-11 14:10:00", "00:45:00", "UPCOMING"),
            ],

            "p3": [
                (6, "meditation", "2026-06-25 14:10:00", "00:15:00", "UPCOMING"),
                (7, "walking", "2026-06-26 14:10:00", "00:30:00", "UPCOMING"),
            ]
        }


        self.page_names = list(self.pages.keys())

        self.current_page = 0
        self.current_option = 0


        self.buffer = StringIO()

        self.console = Console(
            record=True,
            file=self.buffer
        )


        self.content = TextArea(
            focusable=False
        )



    def render_table(self):

        # clear buffer
        self.buffer.seek(0)
        self.buffer.truncate(0)


        table = Table(
            title="Habits"
        )


        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Start")
        table.add_column("Duration")
        table.add_column("Status")


        habits = self.pages[
            self.page_names[self.current_page]
        ]


        for index, habit in enumerate(habits):

            style = (
                "reverse"
                if index == self.current_option
                else ""
            )


            table.add_row(
                str(habit[0]),
                habit[1],
                habit[2],
                habit[3],
                habit[4],
                style=style
            )


        self.console.print(table)


        return self.buffer.getvalue()



    def refresh(self):

        tabs = " | ".join(
            f"[{page}]"
            if i == self.current_page
            else page
            for i, page in enumerate(self.page_names)
        )


        page = self.page_names[
            self.current_page
        ]


        self.content.text = (
            tabs
            + "\n\n"
            + f"Page: {page}\n\n"
            + self.render_table()
            + "\n\n"
            + "↑ ↓ Move   ← → Pages   Enter Select   Q Quit"
        )





def run():

    view = View()

    view.refresh()


    kb = KeyBindings()



    @kb.add("down", eager=True)
    def _(event):

        habits = view.pages[
            view.page_names[view.current_page]
        ]


        if view.current_option < len(habits)-1:
            view.current_option += 1


        view.refresh()

        event.app.invalidate()



    @kb.add("up", eager=True)
    def _(event):

        if view.current_option > 0:
            view.current_option -= 1


        view.refresh()

        event.app.invalidate()



    @kb.add("right", eager=True)
    def _(event):

        if view.current_page < len(view.page_names)-1:

            view.current_page += 1
            view.current_option = 0


        view.refresh()

        event.app.invalidate()



    @kb.add("left", eager=True)
    def _(event):

        if view.current_page > 0:

            view.current_page -= 1
            view.current_option = 0


        view.refresh()

        event.app.invalidate()



    @kb.add("enter", eager=True)
    def _(event):

        page = view.page_names[
            view.current_page
        ]


        selected = view.pages[page][
            view.current_option
        ]


        print("\nSelected:")
        print(selected)

        event.app.exit()



    @kb.add("q", eager=True)
    def _(event):

        event.app.exit()



    app = Application(
        layout=Layout(
            Frame(
                view.content,
                title="Habit Tracker"
            )
        ),
        key_bindings=kb,
        full_screen=True
    )


    app.run()



if __name__ == "__main__":
    run()