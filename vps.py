import customtkinter as ctk
from tkinter import messagebox
import random
import time

# --- CONFIGURATION ---
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Material You Colors (Android 16 Palette)
COLORS = {
    "surface": "#2b2930",       # Dark Card Background
    "primary": "#d0bcff",       # Light Lavender (Accents)
    "danger":  "#f2b8b5",       # Soft Red
    "success": "#b1f0b0",       # Soft Green
    "text":    "#e6e0e9",       # Off-white
    "bg":      "#141218"        # distinct deep background
}

SPECIES_DATA = {
    "Dog":     {"Baby": "🐶", "Child": "🐕", "Adult": "🐕‍🦺", "Elder": "🐺"},
    "Cat":     {"Baby": "🐱", "Child": "🐈", "Adult": "🐆", "Elder": "🐅"},
    "Pikachu": {"Baby": "🥚", "Child": "🐭", "Adult": "🐹", "Elder": "⚡"}
}

ITEMS = {
    "Apple":  {"cost": 5, "val": 10, "type": "food", "icon": "🍎"},
    "Pizza":  {"cost": 15, "val": 25, "type": "food", "icon": "🍕"},
    "Steak":  {"cost": 50, "val": 50, "type": "food", "icon": "🥩"},
    "Pill":   {"cost": 20, "val": 30, "type": "meds", "icon": "💊"},
    "Elixir": {"cost": 100,"val": 100,"type": "meds", "icon": "🧪"}
}

class MaterialPetPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Pet OS 16")
        self.geometry("450x800")
        self.configure(fg_color=COLORS["bg"])
        self.resizable(False, False)

        # Game State
        self.species = "Pikachu" # Default
        self.name = "Sparky"
        self.money = 100
        self.age = 0
        self.stage = "Baby"
        self.stats = {"Health": 100, "Happy": 100, "Energy": 100, "Hygiene": 100}
        self.inventory = {k: 0 for k in ITEMS}
        self.is_alive = True
        self.is_sick = False

        self.setup_ui()
        self.game_loop()

    def setup_ui(self):
        # --- 1. HEADER CARD ---
        self.header = ctk.CTkFrame(self, fg_color=COLORS["surface"], corner_radius=20)
        self.header.pack(fill="x", padx=15, pady=15)

        self.lbl_name = ctk.CTkLabel(self.header, text=self.name, font=("Roboto Medium", 24), text_color=COLORS["text"])
        self.lbl_name.pack(pady=(10, 0))

        self.lbl_money = ctk.CTkLabel(self.header, text=f"${self.money}", font=("Roboto", 16), text_color=COLORS["primary"])
        self.lbl_money.pack(pady=(0, 10))

        # --- 2. PET VISUAL ---
        self.pet_canvas = ctk.CTkLabel(self, text="🥚", font=("Segoe UI Emoji", 140))
        self.pet_canvas.pack(pady=20)

        self.lbl_status = ctk.CTkLabel(self, text="Status: Normal", font=("Roboto", 12), text_color="gray")
        self.lbl_status.pack()

        # --- 3. STATS (Progress Bars) ---
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=20, pady=10)

        self.bars = {}
        for stat in ["Health", "Happy", "Energy", "Hygiene"]:
            row = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            ctk.CTkLabel(row, text=stat, width=60, anchor="w", font=("Roboto", 12)).pack(side="left")
            
            bar = ctk.CTkProgressBar(row, height=12, corner_radius=6)
            bar.set(1.0) # 1.0 = 100%
            bar.pack(side="right", fill="x", expand=True, padx=(10, 0))
            
            self.bars[stat] = bar

        # --- 4. NAVIGATION TABS (Android Style) ---
        # This acts like a bottom sheet / control panel
        self.tab_view = ctk.CTkTabview(self, corner_radius=20, fg_color=COLORS["surface"])
        self.tab_view.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.tab_view.add("Actions")
        self.tab_view.add("Inventory")
        self.tab_view.add("Shop")

        self.setup_actions_tab()
        self.setup_inventory_tab()
        self.setup_shop_tab()

    def setup_actions_tab(self):
        tab = self.tab_view.tab("Actions")
        
        # Grid layout for buttons
        actions = [
            ("🚿 Clean", self.action_clean, COLORS["primary"]),
            ("💤 Sleep", self.action_sleep, COLORS["primary"]),
            ("🎮 Play", self.action_play, "#EDB1F1") # Pinkish
        ]
        
        for i, (txt, cmd, col) in enumerate(actions):
            btn = ctk.CTkButton(tab, text=txt, command=cmd, fg_color=col, 
                                text_color="#1d1b20", font=("Roboto", 14, "bold"),
                                height=50, corner_radius=15, hover_color="white")
            btn.pack(fill="x", pady=5, padx=10)

    def setup_inventory_tab(self):
        self.inv_frame = ctk.CTkScrollableFrame(self.tab_view.tab("Inventory"), fg_color="transparent")
        self.inv_frame.pack(fill="both", expand=True)
        self.refresh_inventory_ui()

    def setup_shop_tab(self):
        shop_frame = ctk.CTkScrollableFrame(self.tab_view.tab("Shop"), fg_color="transparent")
        shop_frame.pack(fill="both", expand=True)

        for name, data in ITEMS.items():
            card = ctk.CTkFrame(shop_frame, fg_color=COLORS["bg"], corner_radius=10)
            card.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(card, text=f"{data['icon']} {name}", font=("Roboto", 14)).pack(side="left", padx=10)
            ctk.CTkButton(card, text=f"${data['cost']}", width=60, 
                          command=lambda n=name: self.buy_item(n),
                          fg_color=COLORS["surface"], hover_color=COLORS["primary"]).pack(side="right", padx=10, pady=10)

    # --- DYNAMIC UI UPDATES ---
    def refresh_inventory_ui(self):
        # Clear previous widgets
        for widget in self.inv_frame.winfo_children():
            widget.destroy()

        empty = True
        for name, count in self.inventory.items():
            if count > 0:
                empty = False
                card = ctk.CTkFrame(self.inv_frame, fg_color=COLORS["bg"], corner_radius=10)
                card.pack(fill="x", pady=5, padx=5)
                
                ctk.CTkLabel(card, text=f"{ITEMS[name]['icon']} {name} (x{count})").pack(side="left", padx=10)
                ctk.CTkButton(card, text="Use", width=50, fg_color=COLORS["success"], text_color="black",
                              command=lambda n=name: self.use_item(n)).pack(side="right", padx=10, pady=10)
        
        if empty:
            ctk.CTkLabel(self.inv_frame, text="Inventory Empty", text_color="gray").pack(pady=20)

    def update_bars(self):
        for stat, val in self.stats.items():
            bar = self.bars[stat]
            bar.set(val / 100) # Convert 0-100 to 0.0-1.0
            
            # Dynamic Colors
            if val < 30: bar.configure(progress_color=COLORS["danger"])
            elif val > 70: bar.configure(progress_color=COLORS["success"])
            else: bar.configure(progress_color=COLORS["primary"])

    def update_visuals(self):
        # Update Name/Money
        self.lbl_name.configure(text=f"{self.name} ({self.stage})")
        self.lbl_money.configure(text=f"${self.money}")
        
        # Update Emoji
        emoji = SPECIES_DATA[self.species][self.stage]
        if not self.is_alive: emoji = "💀"
        elif self.is_sick: emoji = "🤒"
        elif self.stats["Hygiene"] < 30: emoji = "💩"
        elif self.stats["Energy"] < 20: emoji = "😴"
        self.pet_canvas.configure(text=emoji)

    # --- GAME LOGIC ---
    def game_loop(self):
        if not self.is_alive: return

        # Stats Decay
        self.stats["Happy"] -= 0.5
        self.stats["Energy"] -= 0.2
        
        # Random Events
        if random.randint(1, 100) < 3:
            self.stats["Hygiene"] -= 20
            self.lbl_status.configure(text="Pet made a mess!", text_color=COLORS["danger"])

        # Sickness/Health Logic
        if self.stats["Hygiene"] < 30: self.stats["Health"] -= 0.1
        if self.stats["Health"] < 50 and random.random() < 0.02: self.is_sick = True
        if self.is_sick: 
            self.stats["Health"] -= 0.5
            self.lbl_status.configure(text="Pet is Sick!", text_color=COLORS["danger"])

        # Aging
        self.age += 0.1
        if self.age < 15: self.stage = "Baby"
        elif self.age < 35: self.stage = "Child"
        elif self.age < 65: self.stage = "Adult"
        else: self.stage = "Elder"

        # Death Check
        if self.stats["Health"] <= 0:
            self.is_alive = False
            self.lbl_status.configure(text="GAME OVER", text_color="red")
        
        # Clamp Values
        for k in self.stats:
            self.stats[k] = max(0, min(100, self.stats[k]))

        self.update_bars()
        self.update_visuals()
        self.after(1000, self.game_loop)

    # --- INTERACTION ---
    def buy_item(self, name):
        cost = ITEMS[name]['cost']
        if self.money >= cost:
            self.money -= cost
            self.inventory[name] += 1
            self.refresh_inventory_ui() # Refresh the inv tab
        else:
            self.lbl_status.configure(text="Not enough money!", text_color=COLORS["danger"])

    def use_item(self, name):
        if self.inventory[name] > 0:
            self.inventory[name] -= 1
            item_data = ITEMS[name]
            
            if item_data['type'] == 'food':
                self.stats["Health"] += item_data['val']
                self.stats["Energy"] += 5
                # Poop chance
                if random.random() < 0.3: self.stats["Hygiene"] -= 15
                
            elif item_data['type'] == 'meds':
                self.stats["Health"] += item_data['val']
                self.is_sick = False

            self.refresh_inventory_ui()
            self.lbl_status.configure(text=f"Used {name}", text_color=COLORS["success"])

    def action_clean(self):
        self.stats["Hygiene"] = 100
        self.stats["Happy"] += 5
        self.lbl_status.configure(text="Sparkling Clean!", text_color=COLORS["success"])

    def action_sleep(self):
        self.stats["Energy"] = 100
        self.stats["Health"] += 5
        self.lbl_status.configure(text="Zzz... Well rested.", text_color=COLORS["primary"])

    def action_play(self):
        if self.stats["Energy"] < 20:
            self.lbl_status.configure(text="Too tired to play...", text_color=COLORS["danger"])
            return
        
        win = random.randint(5, 20)
        self.money += win
        self.stats["Happy"] += 15
        self.stats["Energy"] -= 20
        self.lbl_status.configure(text=f"Played Games! Won ${win}", text_color=COLORS["success"])

if __name__ == "__main__":
    app = MaterialPetPro()
    app.mainloop()