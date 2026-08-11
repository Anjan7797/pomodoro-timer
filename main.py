import tkinter


# ---------------------------- CONSTANTS -------------------------------

START_COLOR = "#4CAF50"
RESET_COLOR = "#78909C"
PAUSE_COLOR = "#D9A05B"
CHECKMARK_COLOR = "#8ECA3C"
LABEL_COLOR = "#659287"
WINDOW_COLOR = "#FFFAF3"

FONT = "Sitka Heading Semibold"
TIMER_FONT = "Digital-7 Mono"

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20


# ---------------------------- TIMER STATE -------------------------------

reps = 0
timer = None
remaining_time = 0
is_paused = False


# ---------------------------- PAUSE TIMER -------------------------------

def pause():
    """Pause the currently running timer and preserve its remaining time."""
    global timer, is_paused

    if timer is not None:
        window.after_cancel(timer)
        timer = None
        is_paused = True


# ---------------------------- TIMER RESET -------------------------------

def reset():
    """Stop the timer and reset the application to its initial state."""
    global reps, timer, is_paused, remaining_time

    if timer is not None:
        window.after_cancel(timer)
        timer = None

    canvas.itemconfig(timer_text, text="00:00")
    text_label.config(text="Timer")
    checkmark_label.config(text="")

    reps = 0
    remaining_time = 0
    is_paused = False


# ---------------------------- TIMER MECHANISM -------------------------------

def start_timer():
    """Start a new Pomodoro session or resume a paused timer."""
    global reps, is_paused

    # Prevent multiple countdowns from running at the same time.
    if timer is not None:
        return

    # Resume the paused session instead of starting a new one.
    if is_paused:
        is_paused = False
        countdown(remaining_time)
        return

    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        countdown(long_break_sec)
        text_label.config(text="Long Break")

    elif reps % 2 == 0:
        countdown(short_break_sec)
        text_label.config(text="Short Break")

    else:
        countdown(work_sec)
        text_label.config(text="Work")


# ---------------------------- COUNTDOWN MECHANISM -------------------------------

def countdown(count):
    """Update the timer display and schedule the next countdown step."""
    global reps, remaining_time, timer

    minutes = count // 60
    seconds = count % 60

    remaining_time = count

    canvas.itemconfig(
        timer_text,
        text=f"{minutes:02d}:{seconds:02d}"
    )

    if count > 0:
        timer = window.after(1000, countdown, count - 1)

    else:
        # No countdown is active, so Start can begin the next session.
        timer = None

        # A checkmark represents a completed work session.
        if reps % 2 != 0:
            checkmark_label.config(
                text=checkmark_label.cget("text") + " ✅"
            )

        start_timer()


# ---------------------------- WINDOW SETUP -------------------------------

window = tkinter.Tk()
window.title("Pomodoro")
window.config(
    padx=200,
    pady=50,
    bg=WINDOW_COLOR
)


# ---------------------------- TIMER DISPLAY -------------------------------

canvas = tkinter.Canvas(
    width=200,
    height=224,
    bg=WINDOW_COLOR,
    highlightthickness=0
)

tomato_img = tkinter.PhotoImage(file="tomato.png")

canvas.create_image(
    100,
    110,
    image=tomato_img
)

timer_text = canvas.create_text(
    100,
    133,
    text="00:00",
    fill="white",
    font=(TIMER_FONT, 30, "bold")
)

canvas.grid(column=2, row=2)


# ---------------------------- LABELS -------------------------------

text_label = tkinter.Label(
    text="Timer",
    font=(FONT, 50),
    fg=LABEL_COLOR,
    bg=WINDOW_COLOR,
    highlightthickness=0
)

text_label.grid(column=2, row=1)


checkmark_label = tkinter.Label(
    font=(FONT, 10),
    fg=CHECKMARK_COLOR,
    bg=WINDOW_COLOR,
    highlightthickness=0
)

checkmark_label.grid(column=2, row=4)


# ---------------------------- BUTTONS -------------------------------

start_button = tkinter.Button(
    text="▶ Start",
    font=(FONT, 10),
    fg="white",
    bg=START_COLOR,
    highlightthickness=0,
    relief="flat",
    pady=1,
    padx=3,
    command=start_timer
)

start_button.grid(column=1, row=3)


reset_button = tkinter.Button(
    text="↻ Reset",
    font=(FONT, 10),
    fg="white",
    bg=RESET_COLOR,
    highlightthickness=0,
    relief="flat",
    padx=3,
    pady=1,
    command=reset
)

reset_button.grid(column=3, row=3)


pause_button = tkinter.Button(
    text="⏸ Pause",
    font=(FONT, 10),
    fg="white",
    bg=PAUSE_COLOR,
    highlightthickness=0,
    relief="flat",
    padx=3,
    pady=1,
    command=pause
)

pause_button.grid(column=2, row=3)


# ---------------------------- APPLICATION LOOP -------------------------------

window.mainloop()