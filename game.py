import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random

root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("900x600")
root.resizable(False, False)

# LOAD GIF FRAMES
def load_gif_frames(path, size=(280, 280)):
    gif = Image.open(path)
    frames = []
    for frame in ImageSequence.Iterator(gif):
        frame = frame.copy().resize(size)
        frames.append(ImageTk.PhotoImage(frame))
    return frames

gif1_frames = load_gif_frames("Rock Paper Scissors GIF (1).gif")
gif2_frames = load_gif_frames("Rock Paper Scissors GIF.gif")
gif3_frames = load_gif_frames("Sign Language Rock GIF.gif")

# CANVAS
canvas = tk.Canvas(root, width=900, height=600, highlightthickness=0, bg="black")
canvas.pack(fill="both", expand=True)

# GIFs
gif1 = canvas.create_image(200, 300, image=gif1_frames[0])
gif2 = canvas.create_image(450, 300, image=gif2_frames[0])
gif3 = canvas.create_image(700, 300, image=gif3_frames[0])

# GAME VARIABLES
game_mode = None
p1_choice = None
player_score = 0
computer_score = 0
p1_score = 0
p2_score = 0
player1_name = "You"
player2_name = "Computer"
best_of_n = 3
current_round = 0
player_streak = 0
computer_streak = 0

# RAINBOW COLORS
rainbow_colors = [
    "#FF0000", "#FF7F00", "#FFFF00",
    "#00FF00", "#0000FF", "#4B0082", "#9400D3"
]
rainbow_index = 0

# CANVAS TEXT ITEMS
result_text = canvas.create_text(450, 40, text="", fill="white", font=("Arial", 26, "bold"))
score_text = canvas.create_text(450, 95, text="", fill="white", font=("Arial", 20))
menu_text = canvas.create_text(450, 500, text="", fill="white", font=("Arial", 22, "bold"))
timer_text = canvas.create_text(450, 150, text="", fill="white", font=("Arial", 22, "bold"))

# BUTTON IMAGES
rock_img = ImageTk.PhotoImage(Image.open("rock.png").resize((100, 100)))
paper_img = ImageTk.PhotoImage(Image.open("paper.png").resize((100, 100)))
scissors_img = ImageTk.PhotoImage(Image.open("scissors.png").resize((100, 100)))

# BUTTONS
rock_btn = tk.Button(root, image=rock_img, bd=0, command=lambda: choose("rock"))
paper_btn = tk.Button(root, image=paper_img, bd=0, command=lambda: choose("paper"))
scissors_btn = tk.Button(root, image=scissors_img, bd=0, command=lambda: choose("scissors"))
reset_btn = tk.Button(root, text="Reset", font=("Arial", 12), command=lambda: reset_game())
menu_btn = tk.Button(root, text="Menu", font=("Arial", 12), command=lambda: go_menu())
single_btn = tk.Button(root, text="Single Player", font=("Arial", 20, "bold"), command=lambda: get_names("single"))
multi_btn = tk.Button(root, text="Multiplayer", font=("Arial", 20, "bold"), command=lambda: get_names("multi"))
all_buttons = [single_btn, multi_btn, rock_btn, paper_btn, scissors_btn, reset_btn, menu_btn]

# ANIMATE GIFS
frame_index = 0
def animate_gifs():
    global frame_index
    frame_index += 1
    canvas.itemconfig(gif1, image=gif1_frames[frame_index % len(gif1_frames)])
    canvas.itemconfig(gif2, image=gif2_frames[frame_index % len(gif2_frames)])
    canvas.itemconfig(gif3, image=gif3_frames[frame_index % len(gif3_frames)])
    root.after(80, animate_gifs)
animate_gifs()

# LETTER-BY-LETTER RAINBOW ANIMATION
def animate_colors():
    global rainbow_index
    rainbow_index = (rainbow_index + 1) % len(rainbow_colors)
    canvas.itemconfig(result_text, fill=rainbow_colors[rainbow_index])
    canvas.itemconfig(score_text, fill=rainbow_colors[(rainbow_index + 2) % len(rainbow_colors)])
    canvas.itemconfig(menu_text, fill=rainbow_colors[(rainbow_index + 4) % len(rainbow_colors)])
    canvas.itemconfig(timer_text, fill=rainbow_colors[(rainbow_index + 5) % len(rainbow_colors)])
    for btn in all_buttons:
        btn.config(fg=rainbow_colors[rainbow_index])
    root.after(120, animate_colors)
animate_colors()

# SUBTLE BACKGROUND PARTICLES
particles = []
for _ in range(30):
    x, y = random.randint(0,900), random.randint(0,600)
    dx, dy = random.uniform(-0.5,0.5), random.uniform(0.2,1)
    color = random.choice(["#444", "#666", "#888", "#aaa"])
    p = canvas.create_oval(x,y,x+3,y+3,fill=color,outline="")
    canvas.tag_lower(p)
    particles.append([p,x,y,dx,dy,color])

def animate_particles():
    for i, (p,x,y,dx,dy,color) in enumerate(particles):
        x += dx
        y += dy
        if x<0: x=900
        if x>900: x=0
        if y<0: y=600
        if y>600: y=0
        canvas.coords(p,x,y,x+3,y+3)
        particles[i] = [p,x,y,dx,dy,color]
    root.after(100, animate_particles)
animate_particles()

# CONFETTI ON WIN
confetti_items = []

def launch_confetti():
    global confetti_items
    confetti_items = []
    for _ in range(50):
        x, y = random.randint(100, 800), random.randint(50, 300)
        size = random.randint(5,10)
        color = random.choice(rainbow_colors)
        confetti = canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
        dx = random.uniform(-3,3)
        dy = random.uniform(2,5)
        confetti_items.append([confetti, dx, dy])
    animate_confetti()

def animate_confetti():
    global confetti_items
    if not confetti_items: return
    for item in confetti_items:
        confetti, dx, dy = item
        canvas.move(confetti, dx, dy)
        coords = canvas.coords(confetti)
        if coords[1] > 600:
            canvas.delete(confetti)
            confetti_items.remove(item)
    if confetti_items:
        root.after(50, animate_confetti)

# TIMER
timer_seconds = 10
timer_id = None

def start_timer():
    global timer_seconds, timer_id
    if timer_id:  # cancel previous timer
        root.after_cancel(timer_id)
    timer_seconds = 10
    countdown()

def countdown():
    global timer_seconds, p1_choice, timer_id
    if timer_seconds >= 0:
        canvas.itemconfig(timer_text, text=f"{timer_seconds} seconds")
        timer_seconds -= 1
        timer_id = root.after(1000, countdown)  # 1 second per tick
    else:
        # timer expired, auto-select random choice
        if game_mode=="single":
            choose(random.choice(["rock","paper","scissors"]))
        elif game_mode=="multi":
            if p1_choice is None:
                choose(random.choice(["rock","paper","scissors"]))
            else:
                choose(random.choice(["rock","paper","scissors"]))

# TEXT UPDATE
def update_text(result="", score=""):
    canvas.itemconfig(result_text, text=result)
    canvas.itemconfig(score_text, text=score)

# NAME POPUP + BEST-OF-N
active_popups = []

def get_names(mode):
    global player1_name, player2_name, best_of_n

    popup = tk.Toplevel(root)
    popup.title("Enter Name(s)")
    popup.geometry("400x250")
    popup.resizable(False, False)
    popup.configure(bg="black")
    active_popups.append(popup)

    lbl1 = tk.Label(popup, text="Player 1 Name:", font=("Arial", 14, "bold"), bg="black", fg="white")
    lbl1.pack(pady=5)
    entry1 = tk.Entry(popup, font=("Arial", 14), fg="white", bg="black", insertbackground="white")
    entry1.pack()

    if mode=="multi":
        lbl2 = tk.Label(popup, text="Player 2 Name:", font=("Arial", 14, "bold"), bg="black", fg="white")
        lbl2.pack(pady=5)
        entry2 = tk.Entry(popup, font=("Arial", 14), fg="white", bg="black", insertbackground="white")
        entry2.pack()
    else:
        entry2 = None

    lbl3 = tk.Label(popup, text="Rounds (Best of N):", font=("Arial", 14, "bold"), bg="black", fg="white")
    lbl3.pack(pady=5)
    rounds_entry = tk.Entry(popup, font=("Arial", 14), fg="white", bg="black", insertbackground="white")
    rounds_entry.insert(0,"3")
    rounds_entry.pack()

    def submit_names():
        global player1_name, player2_name, best_of_n, current_round
        player1_name = entry1.get().strip() or "Player 1"
        player2_name = entry2.get().strip() if entry2 else "Computer"
        if not player2_name: player2_name="Computer"
        try: best_of_n = int(rounds_entry.get())
        except: best_of_n=3
        current_round = 0
        popup.destroy()
        active_popups.remove(popup)
        start_game(mode)

    submit_btn = tk.Button(popup, text="Start Game", font=("Arial", 14, "bold"),
                           command=submit_names, bg="black", fg="white")
    submit_btn.pack(pady=10)

# GAMEPLAY FUNCTIONS
def play_single(choice):
    global player_score, computer_score, player_streak, computer_streak, current_round
    if timer_id: root.after_cancel(timer_id)
    comp = random.choice(["rock","paper","scissors"])
    if comp==choice:
        result="Tie!"
    elif (choice=="rock" and comp=="scissors") or (choice=="paper" and comp=="rock") or (choice=="scissors" and comp=="paper"):
        result=f"{player1_name} Wins!"
        player_score+=1
        player_streak+=1
        computer_streak=0
        launch_confetti()
    else:
        result=f"{player2_name} Wins!"
        computer_score+=1
        computer_streak+=1
        player_streak=0
    current_round+=1
    update_text(f"{player1_name}:{choice} | {player2_name}:{comp}\n{result}",
                f"Score → {player1_name}:{player_score} {player2_name}:{computer_score}")
    check_best_of_n()
    start_timer()

def play_multiplayer(choice):
    global p1_choice, p1_score, p2_score, player_streak, computer_streak, current_round
    if timer_id: root.after_cancel(timer_id)
    if p1_choice is None:
        p1_choice = choice
        update_text(f"{player2_name}'s Turn","")
        start_timer()
        return
    p2_choice = choice
    if p1_choice==p2_choice: result="Tie!"
    elif (p1_choice=="rock" and p2_choice=="scissors") or (p1_choice=="paper" and p2_choice=="rock") or (p1_choice=="scissors" and p2_choice=="paper"):
        result=f"{player1_name} Wins!"
        p1_score+=1
        player_streak+=1
        computer_streak=0
        launch_confetti()
    else:
        result=f"{player2_name} Wins!"
        p2_score+=1
        computer_streak+=1
        player_streak=0
    current_round+=1
    update_text(f"{player1_name}:{p1_choice} | {player2_name}:{p2_choice}\n{result}",
                f"Score → {player1_name}:{p1_score} {player2_name}:{p2_score}")
    p1_choice=None
    check_best_of_n()
    start_timer()

def check_best_of_n():
    if game_mode=="single":
        if player_score>(best_of_n//2) or computer_score>(best_of_n//2):
            winner = player1_name if player_score>computer_score else player2_name
            update_text(f"GAME OVER! {winner} wins!", f"Final Score → {player1_name}:{player_score} {player2_name}:{computer_score}")
            hide_all_buttons()
    elif game_mode=="multi":
        if p1_score>(best_of_n//2) or p2_score>(best_of_n//2):
            winner = player1_name if p1_score>p2_score else player2_name
            update_text(f"GAME OVER! {winner} wins!", f"Final Score → {player1_name}:{p1_score} {player2_name}:{p2_score}")
            hide_all_buttons()

# CHOICE ROUTER
def choose(choice):
    if timer_id: root.after_cancel(timer_id)
    if game_mode=="single": play_single(choice)
    elif game_mode=="multi": play_multiplayer(choice)

# RESET + MENU
def reset_game():
    global player_score, computer_score, p1_score, p2_score, p1_choice
    player_score = computer_score = p1_score = p2_score = 0
    p1_choice = None
    update_text("Make your move!","Scores Reset")
    start_timer()

def go_menu():
    show_menu()

# SHOW / HIDE BUTTONS
def hide_all_buttons():
    canvas.delete("btn")

def show_menu():
    hide_all_buttons()
    canvas.itemconfig(menu_text,text="Select a Mode Below")
    canvas.create_window(350,550,window=single_btn,tags="btn")
    canvas.create_window(550,550,window=multi_btn,tags="btn")

def start_game(mode):
    global game_mode
    hide_all_buttons()
    game_mode=mode
    reset_game()
    canvas.itemconfig(menu_text,text="")
    canvas.create_window(330,520,window=rock_btn,tags="btn")
    canvas.create_window(450,520,window=paper_btn,tags="btn")
    canvas.create_window(570,520,window=scissors_btn,tags="btn")
    canvas.create_window(820,40,window=reset_btn,tags="btn")
    canvas.create_window(820,85,window=menu_btn,tags="btn")
    start_timer()
# START
show_menu()
root.mainloop()

