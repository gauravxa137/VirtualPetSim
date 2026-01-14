```markdown
# 🐾 Pet OS 16 (Virtual Pet Simulator)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![UI Framework](https://img.shields.io/badge/UI-CustomTkinter-green?style=for-the-badge&logo=android)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)

> A modern, "Material You" inspired Virtual Pet Simulator built with Python. Features a dynamic Android 16-style interface, real-time stat decay, evolution systems, and an interactive economy.

---

## 📱 Preview

*(You can add a screenshot here later!)*
> *Experience a clean, card-based UI with Dark Mode support and smooth animations.*

---

## ✨ Features

### 🎨 **Material You UI**
* **Modern Design:** Built using `CustomTkinter` for a native, high-DPI look.
* **Dynamic Colors:** Progress bars change color based on pet health (🟢 Healthy → 🔴 Critical).
* **Tabbed Navigation:** Seamlessly switch between Actions, Inventory, and Shop tabs.
* **Dark Mode:** Native dark theme support inspired by Android 16.

### 🧬 **Evolution System**
Choose your species and watch them grow!
* **Species:** ⚡ Pikachu, 🐶 Dog, 🐱 Cat.
* **Growth Stages:** Egg 🥚 → Baby 👶 → Child 🧒 → Adult 🧑 → Elder 🧓.
* **Visual Changes:** Emoji avatars update automatically as your pet ages.

### ⚙️ **Deep Simulation Mechanics**
* **Real-Time Decay:** Hunger, Happiness, and Energy drop over time.
* **Hygiene System:** Pets make messes! Clean them up or they get sick 🤢.
* **Sickness:** Poor care leads to illness, requiring medicine to cure.
* **Economy:** Play minigames to earn coins and buy food/items from the Shop.

---

## 🛠️ Installation

### Prerequisites
You need **Python 3.x** installed.

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/pet-os-16.git](https://github.com/yourusername/pet-os-16.git)
cd pet-os-16

```

### 2. Install Dependencies

This project uses **CustomTkinter** for the UI.

```bash
pip install customtkinter

```

### 3. Run the Game

```bash
python material_pet_pro.py

```

---

## 🎮 How to Play

### **The Basics**

1. **Keep it Alive:** Monitor the 4 stats bars. If **Health** hits 0, the game ends.
2. **Stats:**
* ❤️ **Health:** Drops if Hygiene is low, Energy is critical, or the pet is Sick.
* 🙂 **Happy:** Decays over time. Fix by Playing or Cleaning.
* ⚡ **Energy:** Drops constantly. Refill by Sleeping.
* ✨ **Hygiene:** Randomly drops (poop events). Clean immediately!



### **Making Money**

* Go to the **Actions Tab**.
* Click **🎮 Play**.
* You will spend Energy to earn randomized cash rewards!

### **Shopping**

* Go to the **Shop Tab**.
* Buy **Apples** 🍎 (Cheap food) or **Steaks** 🥩 (Premium food).
* Buy **Pills** 💊 if your pet gets sick.

---

## 🔮 Future Roadmap

* [ ] **Save/Load System:** Persist pet data across sessions using JSON.
* [ ] **Sound Effects:** Add audio for eating, sleeping, and leveling up.
* [ ] **Notifications:** Desktop alerts when the pet is hungry.
* [ ] **More Minigames:** Add Tic-Tac-Toe or Memory Match.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

```
