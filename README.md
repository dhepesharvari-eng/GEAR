# 🏁 GEAR - Neon Runner Game

A fast-paced terminal-based racing game with skins, power-ups, and progression system!

## 🎮 Features

- **Account System**: Register and login with persistent progress
- **Racing Gameplay**: Avoid obstacles, collect coins, and beat your high score
- **13 Unique Skins**: Unlock skins with different colors and styles
- **Nitro Boost**: Use nitro charges for speed and extra coin multipliers
- **Progression**: Earn coins, unlock content, and climb the leaderboard
- **4 Tracks**: Race through Neon City, Desert, Cyber Forest, and Void
- **Statistics**: Track your performance and progress

## 🚀 How to Play

### Installation
```bash
python gear.py
```

### Controls
- **Arrow Keys / A/D / 1/3**: Move left/right
- **S / 2**: Move to middle
- **N**: Activate Nitro (costs 1 charge)

### Game Mechanics
- 🚧 Avoid obstacles (costs you the race!)
- 🪙 Collect coins (25 regular, 35 with Nitro)
- ⚡ Use Nitro to go faster and earn more
- 💰 Buy skins in the shop with coins
- 🏆 Beat your high score

## 📊 Game Modes

1. **🏁 Play Race**: Choose a track and start racing
2. **🛒 Shop**: Buy new skins with coins
3. **🚗 Garage**: Equip unlocked skins
4. **📊 Stats**: View your progress
5. **🔄 Reset Nitro**: Recharge nitro (100 coins)

## 💾 Save System

Your progress is automatically saved to `gear_save.json` with:
- Username & password
- Coins balance
- Unlocked skins
- High score
- Total distance
- Nitro charges

## 🎨 Available Skins

| Skin | Price | Color |
|------|-------|-------|
| Basic | Free | White |
| PIXEL | 280 | Cyan |
| MUSIC | 350 | Magenta |
| RDX | 420 | Red |
| SMOKE | 380 | Gray |
| BLOOD | 520 | Dark Red |
| SHADOW | 650 | Blue |
| RACER | 480 | Yellow |
| SYMBIOTE | 720 | Green |
| DESPA | 680 | Purple |
| JUPITER | 850 | Cyan |
| RED MONSTER | 1200 | Red |
| TAZ | 1100 | Yellow |

## 🛠️ Requirements

- Python 3.6+
- No external dependencies required (uses only standard library)

## 🐛 Bug Fixes & Improvements

✅ Completed `garage()` method
✅ Added full account system
✅ Implemented save/load functionality
✅ Added statistics tracking
✅ Fixed input validation
✅ Added error handling
✅ Cross-platform keyboard support
✅ Graceful exit handling

## 📝 License

MIT License - Feel free to modify and distribute!

## 👨‍💻 Author

Created with ❤️ for terminal gaming enthusiasts

---

**Enjoy the race! 🏁⚡**