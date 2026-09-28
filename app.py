import tkinter as tk
from PIL import Image, ImageTk


class WaterReminder:
    def __init__(self, root):
        self.root = root

        # =========================
        # SETTINGS
        # =========================

        # Reminder interval in minutes
        self.interval_minutes = 1

        # Sticker display duration in milliseconds
        self.sticker_duration = 5000

        # Hide main window
        self.root.withdraw()

        # Start timer
        self.start_timer()

    def start_timer(self):
        milliseconds = self.interval_minutes * 60 * 1000

        self.root.after(
            milliseconds,
            self.show_sticker
        )

    def show_sticker(self):
        # Create popup window
        sticker_window = tk.Toplevel(self.root)

        # Remove title bar and borders
        sticker_window.overrideredirect(True)

        # Keep above other applications
        sticker_window.attributes("-topmost", True)

        # =========================
        # TRANSPARENT BACKGROUND
        # =========================

        transparent_color = "magenta"

        sticker_window.configure(
            bg=transparent_color
        )

        sticker_window.wm_attributes(
            "-transparentcolor",
            transparent_color
        )

        # =========================
        # LOAD STICKER
        # =========================

        image = Image.open("sticker.png").convert("RGBA")

        # Maximum size
        image.thumbnail((250, 250))

        # Convert image for Tkinter
        sticker_image = ImageTk.PhotoImage(image)

        # Keep reference to image
        sticker_window.sticker_image = sticker_image

        # =========================
        # DISPLAY STICKER
        # =========================

        label = tk.Label(
            sticker_window,
            image=sticker_image,
            bg=transparent_color,
            borderwidth=0
        )

        label.pack()

        # =========================
        # CLICK TO DISMISS
        # =========================

        label.bind(
            "<Button-1>",
            lambda event: self.close_sticker(
                sticker_window
            )
        )

        # =========================
        # POSITION
        # =========================

        screen_width = sticker_window.winfo_screenwidth()
        screen_height = sticker_window.winfo_screenheight()

        sticker_width = image.width
        sticker_height = image.height

        # Bottom-right corner
        x = screen_width - sticker_width - 40
        y = screen_height - sticker_height - 80

        sticker_window.geometry(
            f"{sticker_width}x{sticker_height}+{x}+{y}"
        )

        # =========================
        # AUTO CLOSE
        # =========================

        sticker_window.after(
            self.sticker_duration,
            lambda: self.close_sticker(
                sticker_window
            )
        )

    def close_sticker(self, sticker_window):
        # Close sticker
        sticker_window.destroy()

        # Start next reminder
        self.start_timer()


# =========================
# START APPLICATION
# =========================

root = tk.Tk()

app = WaterReminder(root)

root.mainloop()