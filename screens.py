import tkinter as tk
import tkinter.messagebox as msg


def callback(string):
    return string.isnumeric() or not string


def start():
    global level

    if not (level := levelbox.get()):
        msg.showwarning("Empty Field", "Please enter required Level")
        return
    if (level := int(level)) not in range(1, 4):
        msg.showwarning("Invalid Value", "Level must be between 1 - 3")
        return

    root.destroy()


def ending(text):
    temp = tk.Tk()
    temp.withdraw()

    return msg.askyesno(
        title="Sudoku Solved", message=f"{text} Do you want to play Again?",
        parent=temp
    )


def main():
    global root, levelbox

    root = tk.Tk()
    root.title("Welcome to the game")

    tk.Label(
        text="Enter the required level: \n1, 2 or 3 for EASY, MEDIUM or HARD",
        font=("consolas", 12, "bold")
    ).pack()

    levelbox = tk.Entry(
        root, width=35, bd=3, font=("consolas", 12, "bold"),
        validate="key", validatecommand=(root.register(callback), "%P")
    )
    levelbox.pack()
    levelbox.bind("<Return>", lambda evt: start())

    tk.Button(
        root, text="Start", width=35, bd=3, font=("consolas", 12, "bold"),
        command=start
    ).pack()

    root.mainloop()


if __name__ == "__main__":
    main()
    print(level)