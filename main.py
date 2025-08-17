import tkinter as tk
from tkinter import font
import requests
import sys

if len(sys.argv) > 1:
    UNIVERSE_ID = sys.argv[1]
else:
    UNIVERSE_ID = "8353903143"

print(f"Using Universe ID: {UNIVERSE_ID}")

API_URL = f"https://games.roproxy.com/v1/games?universeIds={UNIVERSE_ID}"
AUTO_REFRESH_INTERVAL_MS = 5000

auto_refresh_job = None

def fetch_game_data():
    try:
        response = requests.get(API_URL)
        data = response.json()
        game = data["data"][0]

        name_var.set(game["name"])
        creator_var.set(f"By {game['creator']['name']}")
        playing_var.set(f"Players Now: {game['playing']}")
        visits_var.set(f"Total Visits: {game['visits']:,}")

        status_var.set("Data refreshed successfully!")
    except Exception as e:
        status_var.set("Failed to fetch data.")
        print(e)

def auto_refresh_toggle():
    global auto_refresh_job
    if auto_refresh_var.get():
        status_var.set("Auto-refresh ON")
        schedule_auto_refresh()
    else:
        status_var.set("Auto-refresh OFF")
        if auto_refresh_job is not None:
            root.after_cancel(auto_refresh_job)
            auto_refresh_job = None

def schedule_auto_refresh():
    global auto_refresh_job
    if auto_refresh_var.get():
        fetch_game_data()
        auto_refresh_job = root.after(AUTO_REFRESH_INTERVAL_MS, schedule_auto_refresh)

def center_window(win, width=420, height=370):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

root = tk.Tk()
Title = ""
try: 
    response = requests.get(API_URL)
    data = response.json()
    game = data["data"][0]
    Title = game["name"]
except Exception as e:
    print(e)

root.title(f"RStats: {Title}")
root.configure(bg="#1e1e2f")
center_window(root)

auto_refresh_var = tk.BooleanVar(value=False)

title_font = font.Font(family="Segoe UI", size=18, weight="bold")
label_font = font.Font(family="Segoe UI", size=12)
status_font = font.Font(family="Segoe UI", size=10, slant="italic")

name_var = tk.StringVar(value="Game Loading...")
creator_var = tk.StringVar(value="")
playing_var = tk.StringVar(value="")
visits_var = tk.StringVar(value="")
status_var = tk.StringVar(value="")

frame = tk.Frame(root, bg="#2e2e44", padx=20, pady=20)
frame.pack(expand=True, fill="both", padx=20, pady=20)

tk.Label(frame, textvariable=name_var, font=title_font, fg="#ffd700", bg=frame["bg"]).pack(pady=(0,10))
tk.Label(frame, textvariable=creator_var, font=label_font, fg="#aaaaaa", bg=frame["bg"]).pack()
tk.Label(frame, textvariable=playing_var, font=label_font, fg="#ffffff", bg=frame["bg"]).pack(pady=(10,0))
tk.Label(frame, textvariable=visits_var, font=label_font, fg="#ffffff", bg=frame["bg"]).pack(pady=(0,10))

refresh_btn = tk.Button(frame, text="Refresh", command=fetch_game_data,
                        font=label_font, bg="#ffd700", fg="#1e1e2f", relief="flat",
                        activebackground="#ffea70", activeforeground="#000000",
                        padx=15, pady=7, cursor="hand2")
refresh_btn.pack()

auto_refresh_checkbox = tk.Checkbutton(frame, text="Auto Refresh Every 5s", variable=auto_refresh_var,
                                       command=auto_refresh_toggle, font=label_font,
                                       bg=frame["bg"], fg="#ffffff", selectcolor="#2e2e44",
                                       activebackground=frame["bg"], activeforeground="#ffffff",
                                       cursor="hand2",
                                       highlightthickness=1, highlightbackground="#ffd700")
auto_refresh_checkbox.pack(pady=(10,0))

status_label = tk.Label(frame, textvariable=status_var, font=status_font, fg="#ff6347", bg=frame["bg"])
status_label.pack(pady=(10,0))

fetch_game_data()

root.mainloop()
