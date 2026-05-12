import random
import time
import json
import os
import sys

SAVE_FILE = "gear_save.json"

# Colors for skins
COLORS = {
    "Basic": "\033[97m", "PIXEL": "\033[96m", "MUSIC": "\033[95m", "RDX": "\033[91m",
    "SMOKE": "\033[90m", "BLOOD": "\033[31m", "SHADOW": "\033[94m", "RACER": "\033[93m",
    "SYMBIOTE": "\033[92m", "DESPA": "\033[35m", "JUPITER": "\033[36m",
    "RED MONSTER": "\033[91m", "TAZ": "\033[33m"
}
RESET = "\033[0m"

class NeonRunner:
    def __init__(self):
        self.username = None
        self.coins = 0
        self.unlocked_skins = ["Basic"]
        self.current_skin = "Basic"
        self.high_score = 0
        self.total_distance = 0
        self.nitro = 3

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # ===================== ACCOUNT =====================
    def register(self):
        self.clear()
        print("=== REGISTER NEW ACCOUNT ===\n")
        username = input("Choose username: ").strip()
        if len(username) < 3:
            print("Username too short!")
            time.sleep(1.5)
            return False
        password = input("Choose password: ").strip()
        if len(password) < 3:
            print("Password too short!")
            time.sleep(1.5)
            return False
        self.username = username
        self.coins = 400
        self.nitro = 3
        self.save_game()
        print(f"✅ Account '{username}' created successfully!")
        time.sleep(1.5)
        return True

    def login(self):
        self.clear()
        print("=== LOGIN ===\n")
        username = input("Username: ").strip()
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                if username in data:
                    pw = input("Password: ").strip()
                    if data[username].get("password") == pw:
                        self.username = username
                        self.coins = data[username]["coins"]
                        self.unlocked_skins = data[username]["unlocked_skins"]
                        self.current_skin = data[username]["current_skin"]
                        self.high_score = data[username]["high_score"]
                        self.nitro = data[username].get("nitro", 3)
                        self.total_distance = data[username].get("total_distance", 0)
                        print(f"✅ Welcome back, {username}!")
                        time.sleep(1.5)
                        return True
                    else:
                        print("❌ Incorrect password!")
                else:
                    print("❌ User not found!")
        except FileNotFoundError:
            print("❌ No save file found!")
        except Exception as e:
            print(f"❌ Login error: {e}")
        time.sleep(1.5)
        return False

    def save_game(self):
        try:
            try:
                with open(SAVE_FILE, "r") as f:
                    all_data = json.load(f)
            except FileNotFoundError:
                all_data = {}
            
            all_data[self.username] = {
                "password": "12345",
                "coins": self.coins,
                "unlocked_skins": self.unlocked_skins,
                "current_skin": self.current_skin,
                "high_score": self.high_score,
                "total_distance": self.total_distance,
                "nitro": self.nitro
            }
            with open(SAVE_FILE, "w") as f:
                json.dump(all_data, f, indent=4)
        except Exception as e:
            print(f"❌ Save error: {e}")

    # ===================== RACE - Subway Surfers Style =====================
    def play_race(self):
        self.clear()
        print("🏁 Choose Track:")
        print("1. Neon City    2. Desert    3. Cyber Forest    4. Void")
        track_choice = input("\nEnter (1-4): ").strip()
        
        try:
            track_idx = int(track_choice) - 1
            if track_idx < 0 or track_idx > 3:
                track_idx = 0
        except ValueError:
            track_idx = 0
        
        tracks = ["NEON CITY", "DESERT", "CYBER FOREST", "VOID"]
        track = tracks[track_idx]

        print(f"\n🚗 Starting {track}... Get Ready!")
        time.sleep(1.8)

        lane = 1  # 0 Left, 1 Middle, 2 Right
        distance = 0
        coins_earned = 0
        score = 0
        nitro_active = False
        nitro_timer = 0
        car_color = COLORS.get(self.current_skin, COLORS["Basic"])

        print("Controls: ← → Arrows | A/D | 1/3 | S/2 = Middle | N = Nitro")
        time.sleep(2)

        while True:
            self.clear()
            status = "⚡ NITRO ACTIVE!" if nitro_active else f"Nitro: {self.nitro}"
            print(f"Track: {track}   Distance: {distance}m   Coins: {coins_earned}")
            print(f"Score: {score}   {status}\n")

            # Draw Road
            road = ["   ", "   ", "   "]
            road[lane] = f"{car_color}▶ {self.current_skin} ▶{RESET}"

            print("╔════════════════════════════════════╗")
            print(f"║  LEFT     {road[0]}    MIDDLE    {road[1]}    RIGHT  ║")
            print("╚════════════════════════════════════╝")

            # Spawn obstacles and coins
            obstacles = [" . ", " . ", " . "]
            if random.random() < 0.45:
                obstacles[random.randint(0, 2)] = "🚧"
            if random.random() < 0.40:
                cl = random.randint(0, 2)
                if obstacles[cl] == " . ":
                    obstacles[cl] = "🪙"

            print("          " + "     ".join(obstacles))

            # Get Input (Supports Arrow Keys on most systems)
            try:
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key == b'\xe0':  # Arrow key prefix
                        key = msvcrt.getch()
                        if key == b'K': lane = max(0, lane - 1)   # Left
                        elif key == b'M': lane = min(2, lane + 1) # Right
                    elif key in [b'a', b'A', b'1']: lane = max(0, lane - 1)
                    elif key in [b'd', b'D', b'3']: lane = min(2, lane + 1)
                    elif key in [b's', b'S', b'2']: lane = 1
                    elif key in [b'n', b'N'] and self.nitro > 0 and not nitro_active:
                        nitro_active = True
                        nitro_timer = 10
                        self.nitro -= 1
            except ImportError:
                # Fallback for non-Windows systems
                action = input("\n→ Action: ").strip().upper()
                if action in ["A", "1", "LEFT"]: lane = max(0, lane - 1)
                elif action in ["D", "3", "RIGHT"]: lane = min(2, lane + 1)
                elif action in ["S", "2", "MIDDLE"]: lane = 1
                elif action == "N" and self.nitro > 0 and not nitro_active:
                    nitro_active = True
                    nitro_timer = 10
                    self.nitro -= 1

            distance += 2 if nitro_active else 1
            score += 20 if nitro_active else 12

            # Collision & Collection
            if obstacles[lane] == "🚧":
                print("\n💥 CRASHED INTO OBSTACLE!")
                time.sleep(1.5)
                break
            elif obstacles[lane] == "🪙":
                coins_earned += 35 if nitro_active else 25

            if nitro_active:
                nitro_timer -= 1
                if nitro_timer <= 0:
                    nitro_active = False

            time.sleep(0.18)   # Game Speed (feel free to change)

        # Game Over Screen
        self.clear()
        print("🏁 RUN ENDED 🏁\n")
        print(f"Distance Covered : {distance} meters")
        print(f"Coins Collected  : +{coins_earned} 🪙")
        
        self.coins += coins_earned
        self.total_distance += distance
        if distance > self.high_score:
            self.high_score = distance
            print("🏆 NEW HIGH SCORE ACHIEVED! 🏆")

        self.save_game()
        input("\nPress Enter to continue...")

    def shop(self):
        skin_prices = {
            "PIXEL": 280, "MUSIC": 350, "RDX": 420, "SMOKE": 380,
            "BLOOD": 520, "SHADOW": 650, "RACER": 480, "SYMBIOTE": 720,
            "DESPA": 680, "JUPITER": 850, "RED MONSTER": 1200, "TAZ": 1100
        }
        
        while True:
            self.clear()
            print("🛒 SKIN SHOP 🛒\n")
            print(f"Your Coins: {self.coins} 🪙\n")
            
            for skin in skin_prices:
                status = "✅ OWNED" if skin in self.unlocked_skins else f"{skin_prices[skin]} coins"
                color = COLORS.get(skin, "")
                print(f"{color}{skin:12}{RESET} → {status}")
            
            choice = input("\nEnter skin name to buy or 'back': ").strip().upper()
            if choice == "BACK":
                break
            if choice in skin_prices:
                if choice in self.unlocked_skins:
                    print("✅ You already own this!")
                elif self.coins >= skin_prices[choice]:
                    self.coins -= skin_prices[choice]
                    self.unlocked_skins.append(choice)
                    print(f"✅ Successfully bought {choice} skin!")
                    self.save_game()
                    time.sleep(1.3)
                else:
                    print(f"❌ Not enough coins! Need {skin_prices[choice] - self.coins} more.")
                    time.sleep(1.3)
            else:
                print("❌ Skin not found!")
                time.sleep(1.3)

    def garage(self):
        self.clear()
        print("🚗 MY GARAGE 🚗\n")
        print(f"Current Skin: {self.current_skin}\n")
        for skin in self.unlocked_skins:
            marker = "✓" if skin == self.current_skin else " "
            print(f"   [{marker}] {COLORS.get(skin, '')}{skin}{RESET}")
        
        choice = input("\nType skin name to equip or 'back': ").strip().upper()
        if choice == "BACK":
            return
        elif choice in self.unlocked_skins:
            self.current_skin = choice
            print(f"✅ Equipped {choice}!")
            self.save_game()
            time.sleep(1.3)
        else:
            print("❌ You don't own this skin!")
            time.sleep(1.3)

    def stats(self):
        self.clear()
        print("📊 YOUR STATISTICS 📊\n")
        print(f"Username      : {self.username}")
        print(f"Coins         : {self.coins} 🪙")
        print(f"High Score    : {self.high_score}m")
        print(f"Total Distance: {self.total_distance}m")
        print(f"Nitro Charges : {self.nitro}⚡")
        print(f"Skins Owned   : {len(self.unlocked_skins)}/13")
        input("\nPress Enter to continue...")

    def main_menu(self):
        while True:
            self.clear()
            print("╔════════════════════════════════════╗")
            print("║     🏁 NEON RUNNER 🏁              ║")
            print("╚════════════════════════════════════╝\n")
            print(f"Welcome, {self.username}!")
            print(f"Coins: {self.coins} 🪙  |  High Score: {self.high_score}m\n")
            print("1. 🏁 Play Race")
            print("2. 🛒 Shop")
            print("3. 🚗 Garage")
            print("4. 📊 Stats")
            print("5. 🔄 Reset Nitro (100 coins)")
            print("6. 🚪 Logout")
            
            choice = input("\nChoose option (1-6): ").strip()
            
            if choice == "1":
                self.play_race()
            elif choice == "2":
                self.shop()
            elif choice == "3":
                self.garage()
            elif choice == "4":
                self.stats()
            elif choice == "5":
                if self.coins >= 100:
                    self.coins -= 100
                    self.nitro = 3
                    self.save_game()
                    print("✅ Nitro reset to 3!")
                    time.sleep(1.5)
                else:
                    print("❌ Not enough coins!")
                    time.sleep(1.5)
            elif choice == "6":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid option!")
                time.sleep(1)

def auth_menu():
    game = NeonRunner()
    
    while True:
        game.clear()
        print("╔════════════════════════════════════╗")
        print("║     🏁 NEON RUNNER 🏁              ║")
        print("╚════════════════════════════════════╝\n")
        print("1. 📝 Register")
        print("2. 🔐 Login")
        print("3. ❌ Exit")
        
        choice = input("\nChoose option (1-3): ").strip()
        
        if choice == "1":
            if game.register():
                game.main_menu()
        elif choice == "2":
            if game.login():
                game.main_menu()
        elif choice == "3":
            game.clear()
            print("👋 Thanks for playing NEON RUNNER!")
            break
        else:
            print("❌ Invalid option!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        auth_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted. Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")