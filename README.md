# MotismaMecha - Desktop Pet UI

An interactive, transparent desktop companion inspired by Rotom (Motisma), built with Python and PyQt6. The UI dynamically changes its shape and color based on real-time states read from a local text file.

## Features
- **Frameless & Transparent Window:** Stays on top of all other windows, rendering only the character without any ugly background borders.
- **Fluid Physics Engine:** Includes smooth movement with friction and a built-in dodge mechanic when the mouse cursor gets too close.
- **Dynamic Form Shifting:** Mutates between different shapes based on current status (`listening`, `thinking`, `speaking`, `error`).
- **Interactive Eye Tracking:** Rotom's eyes smoothly follow your mouse cursor around the screen.

## Prerequisites

Make sure you have Python installed, then install the required dependency:

```bash
pip install PyQt6