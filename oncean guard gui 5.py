import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk  # Install Pillow with: pip install pillow

class User:
    def __init__(self, name):
        self.name = name
        self.trash_collected = 0  # in kg
        self.ecocoins = 0
        self.location = None
        self.friends = []
        self.posts = []

    def collect_trash(self, amount):
        self.trash_collected += amount
        self.ecocoins += amount * 5  # 5 EcoCoins per kg of trash
        return f"🎉 You collected {amount} kg of trash and earned {amount * 5} EcoCoins!"

    def add_calcium_bicarbonate(self, amount):
        self.ecocoins += amount * 10  # 10 EcoCoins per kg of additive
        return f"🌊 You added {amount} kg of calcium bicarbonate and earned {amount * 10} EcoCoins!"

    def set_location(self, location):
        self.location = location
        return f"📍 Location updated to {location}."

    def add_friend(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)
            return f"👋 You are now friends with {friend.name}!"
        else:
            return f"🤝 You are already friends with {friend.name}."

    def post_update(self, message):
        self.posts.append(message)
        return f"📝 Posted: {message}"

    def view_impact(self):
        return (
            f"=== Your Impact ===\n"
            f"🗑️ Trash Collected: {self.trash_collected} kg\n"
            f"💰 EcoCoins Earned: {self.ecocoins}\n"
            f"🌍 Estimated CO2 Neutralized: {self.trash_collected * 2} kg"
        )

    def view_friends(self):
        if self.friends:
            friend_list = "\n".join([f"👤 {friend.name} - Location: {friend.location}" for friend in self.friends])
            return f"=== Your Friends ===\n{friend_list}"
        else:
            return "You have no friends yet. Add some!"

    def view_posts(self):
        if self.posts:
            posts_list = "\n".join([f"📢 {post}" for post in self.posts])
            return f"=== Community Feed ===\n{posts_list}"
        else:
            return "No posts yet. Be the first to share!"

class OceanGuardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OceanGuard 🌊")
        self.user = None

        # Set window size to 500x500
        self.root.geometry("500x500")

        # Load the NFT background image
        try:
            self.bg_image = Image.open("potionNFT1.png")  # Ensure the image is in the same directory as the script
            self.bg_image = self.bg_image.resize((500, 500), Image.Resampling.LANCZOS)  # Resize to fit the window
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        except FileNotFoundError:
            print("Background image not found. Using a solid color background instead.")
            self.bg_photo = None

        # Create a canvas to set the background
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack(fill="both", expand=True)
        if self.bg_photo:
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        else:
            self.canvas.configure(bg="lightblue")  # Fallback background color

        # Welcome Screen
        self.welcome_label = tk.Label(root, text="Welcome to OceanGuard!", font=("Arial", 25), bg="lightblue")
        self.welcome_label_window = self.canvas.create_window(250, 200, window=self.welcome_label)

        self.name_entry = tk.Entry(root, width=25, font=("Arial", 20))
        self.name_entry_window = self.canvas.create_window(250, 250, window=self.name_entry)
        self.name_entry.insert(0, "Enter your name")

        self.start_button = tk.Button(root, text="Start", command=self.start_app, font=("Arial", 15), bg="lightgreen")
        self.start_button_window = self.canvas.create_window(250, 300, window=self.start_button)

    def start_app(self):
        name = self.name_entry.get()
        if name:
            self.user = User(name)
            self.clear_widgets()
            self.create_main_menu()

    def clear_widgets(self):
        self.canvas.delete("all")
        if self.bg_photo:
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        else:
            self.canvas.configure(bg="lightblue")

    def create_main_menu(self):
        tk.Label(self.root, text=f"Hello, {self.user.name}!", font=("Arial", 14), bg="lightblue").pack(pady=10)

        buttons = [
            ("Log Trash Collected", self.log_trash),
            ("Add Calcium Bicarbonate", self.add_calcium),
            ("Set Your Location", self.set_location),
            ("Add a Friend", self.add_friend),
            ("View Your Impact", self.view_impact),
            ("View Your Friends", self.view_friends),
            ("Post an Update", self.post_update),
            ("View Community Feed", self.view_feed),
            ("Exit", self.root.quit),
        ]

        # Position buttons vertically with spacing
        y_offset = 100
        for text, command in buttons:
            button = tk.Button(self.root, text=text, command=command, width=20, font=("Arial", 10), bg="lightgreen")
            self.canvas.create_window(250, y_offset, window=button)
            y_offset += 40

    def log_trash(self):
        amount = simpledialog.askfloat("Log Trash", "Enter the amount of trash collected (in kg):")
        if amount:
            result = self.user.collect_trash(amount)
            messagebox.showinfo("Trash Collected", result)

    def add_calcium(self):
        amount = simpledialog.askfloat("Add Calcium Bicarbonate", "Enter the amount of calcium bicarbonate added (in kg):")
        if amount:
            result = self.user.add_calcium_bicarbonate(amount)
            messagebox.showinfo("Calcium Bicarbonate Added", result)

    def set_location(self):
        location = simpledialog.askstring("Set Location", "Enter your location (e.g., La Jolla Beach):")
        if location:
            result = self.user.set_location(location)
            messagebox.showinfo("Location Updated", result)

    def add_friend(self):
        # Example friends for testing
        friend1 = User("Bob")
        friend1.set_location("La Jolla Beach")
        friend2 = User("Charlie")
        friend2.set_location("Santa Monica Beach")

        friend_choice = simpledialog.askinteger("Add Friend", "Choose a friend to add:\n1. Bob\n2. Charlie")
        if friend_choice == 1:
            result = self.user.add_friend(friend1)
        elif friend_choice == 2:
            result = self.user.add_friend(friend2)
        else:
            result = "Invalid choice."
        messagebox.showinfo("Add Friend", result)

    def view_impact(self):
        result = self.user.view_impact()
        messagebox.showinfo("Your Impact", result)

    def view_friends(self):
        result = self.user.view_friends()
        messagebox.showinfo("Your Friends", result)

    def post_update(self):
        message = simpledialog.askstring("Post Update", "Write your post:")
        if message:
            result = self.user.post_update(message)
            messagebox.showinfo("Post Update", result)

    def view_feed(self):
        result = self.user.view_posts()
        messagebox.showinfo("Community Feed", result)

if __name__ == "__main__":
    root = tk.Tk()
    app = OceanGuardApp(root)
    root.mainloop()
