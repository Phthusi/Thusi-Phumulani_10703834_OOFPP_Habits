from rich.table import Table
from rich.console import Console

console = Console()

table = Table(title="Habits")

table.add_column("Id")
table.add_column("Name")
table.add_column("start_datetime")
table.add_column("duration")
table.add_column("status")
table.add_column("progress")

table.add_row("1","Alice enfdeudnuuednunerff", "2023-01-01 10:00:00", "30m", "completed","100%")
table.add_row("2","Bob", "2023-01-02 11:00:00", "45m", "in_progress","50%")
table.add_row("3","Sam", "2027-01-05 14:00:00", "1hr20m", "upcoming","-")

console.print(table)

# html = """
# <html>
#   <body>
#     <h1>Hello from Python</h1>
#   </body>
# </html>
# """

# with open("index.html", "w") as f:
#     f.write(html)

# import webbrowser
# webbrowser.open("index.html")