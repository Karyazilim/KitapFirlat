# Classroom Chaos - Desktop Game

A fun desktop game built with Pygame where you throw books and pens at moving targets in a chaotic classroom setting!

## Features

- **Main Menu**: Stylish interface matching the design specification with bouncing title animation
- **Arcade Gameplay**: Throw books (10 points) and pens (5 points) at moving student targets
- **Physics**: Realistic projectile motion with gravity
- **Scoring System**: Points with streak multipliers (up to 3x bonus)
- **Timed Rounds**: 60-second gameplay sessions
- **Settings**: Difficulty levels (Easy/Normal/Hard) and sound toggle
- **Responsive Controls**: Full keyboard and mouse support

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Karyazilim/KitapFirlat.git
   cd KitapFirlat
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the game:**
   ```bash
   python -m src.main
   ```

## How to Play

### Main Menu
- **Navigation**: Use arrow keys or mouse to navigate
- **Play Button**: Start a new game
- **Settings Button**: Adjust difficulty and sound

### Gameplay
- **Aim**: Move mouse to aim your shots
- **Left Click**: Throw a book (10 points)
- **Right Click**: Throw a pen (5 points)
- **ESC**: Return to main menu

### Scoring
- Books: 10 points per hit
- Pens: 5 points per hit
- Streak multiplier: Build consecutive hits for up to 3x bonus points
- Time limit: 60 seconds per round

### Settings
- **Difficulty Levels**:
  - Easy: Slower targets, longer spawn intervals
  - Normal: Balanced gameplay
  - Hard: Faster targets, more frequent spawning
- **Sound**: Toggle game audio on/off

## Project Structure

```
KitapFirlat/
├── src/
│   ├── main.py              # Entry point and game state management
│   ├── ui/
│   │   ├── components.py    # Reusable UI components (Button, Label, etc.)
│   │   ├── main_menu.py     # Main menu screen
│   │   └── settings_menu.py # Settings screen
│   └── game/
│       ├── entities.py      # Game objects (Player, Projectile, Target)
│       ├── game_screen.py   # Main gameplay screen
│       └── game_over_screen.py # End game screen
├── assets/
│   └── banner.png          # Cached banner image (auto-downloaded)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Technical Details

### Dependencies
- **pygame >= 2.5.0**: Main game framework
- **requests >= 2.28.0**: For downloading banner image

### Display
- **Resolution**: 450x800 (mobile-friendly aspect ratio)
- **Frame Rate**: 60 FPS
- **Color Scheme**: Primary color #ee6c2b (orange), with professional UI styling

### Architecture
- **State Machine**: Clean separation between menu, settings, game, and game-over states
- **Component System**: Reusable UI components with focus management
- **Entity System**: Modular game objects with physics and collision detection
- **Asset Management**: Graceful handling of missing files and network resources

## Controls Reference

### Keyboard Navigation
- **Arrow Keys**: Navigate menus and options
- **Enter/Space**: Activate focused button
- **ESC**: Return to previous screen or main menu

### Mouse Controls
- **Point & Click**: Navigate menus
- **Mouse Movement**: Aim in game
- **Left Click**: Throw book
- **Right Click**: Throw pen

## Screenshots

*[Screenshots will be added when the game is running]*

## Development

### Running in Development
```bash
python -m src.main
```

### Testing Components
The game is designed with modular components that can be individually tested. Each screen and component is self-contained with clear interfaces.

## License

MIT License - see LICENSE file for details.

## Contributing

Feel free to contribute to this project! Areas for potential improvement:
- Sound effects and background music
- Additional target types and animations
- Power-ups and special abilities
- Leaderboard system
- More visual effects and polish

---

**Classroom Chaos** - Turn your classroom into a chaotic but fun throwing game! 🎯📚✏️