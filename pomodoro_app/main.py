import math
from tkinter import *
import winsound
#for sound volume  change
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

def notification():
    current_volume = volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(0.2, None)
    
    winsound.Beep(400, 120)
    winsound.Beep(600, 150)
    winsound.Beep(500, 170)
    
    volume.SetMasterVolumeLevelScalar(current_volume, None)

# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    if timer:window.after_cancel(timer)
    canvas.itemconfig(timer_text, text='00:00')
    tittle_label.config(text="Break", fg=GREEN)
    global reps
    reps=0
    checkmarks.config(text='')

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1
    
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    
    if reps % 8 == 0:
        count_down(long_break_sec)
        tittle_label.config(text="Break", fg=RED)
        window.state(newstate='zoomed')
        window.attributes("-topmost", True)
        notification()
    elif reps % 2 == 0:
        count_down(short_break_sec)
        tittle_label.config(text="Break", fg=PINK)
        window.state(newstate='zoomed')
        window.attributes("-topmost", True)
        notification()
    else:
        count_down(work_sec)
        tittle_label.config(text="Work", fg=GREEN)
        window.attributes("-topmost", False)
        # window.lower()
        window.state(newstate='iconic')
        notification()


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
import time

count = 5


# while True:
#     time.sleep(1)
def count_down(count):
    global reps
    
    canvas.itemconfig(timer_text, text=['0' + str(count // 60), str(count // 60)][len(str(count // 60)) - 1] + ':' +
                                       ['0' + str(count % 60), str(count % 60)][len(str(count % 60)) - 1])
    
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        mark = ""
        for _ in range(math.floor(reps / 2)):
            mark += "✅"
        checkmarks.config(text=mark)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

tittle_label = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 60, "bold"), bg=YELLOW)
tittle_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 132, text="00:00", fill='white', font=(FONT_NAME, 30, 'bold'))

canvas.grid(column=1, row=1)

start_button = Button(text="Start", command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", command=reset_timer)
reset_button.grid(column=2, row=2)

checkmarks = Label(fg=GREEN, bg=YELLOW)
checkmarks.grid(column=1, row=3)

window.mainloop()
