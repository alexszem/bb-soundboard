# Baseball Walk-Up Song System

This project is an offline-capable, Raspberry Pi-powered walk-up music and sound effects system for baseball games. It allows users to play personalized walk-up songs and situational sound effects via API-triggered events over a local Wi-Fi network, all without needing internet access.

---

## 🎯 Project Goals

- Play custom **walk-up songs** and **sound effects** through speakers controlled by a Raspberry Pi.
- Run a **local Wi-Fi hotspot** from the Pi to receive API requests from a mobile device.
- Host a simple **web server** (Flask/FastAPI) to expose endpoints for triggering audio playback.
- Build a frontend or mobile app (possibly with **React** or **React Native**) to interact with the Pi.
- Eventually support player profiles, sequencing batters, and sound triggers for various game events.

---

## 🛠 Tech Stack (Planned)

- **Backend**: Python (Flask or FastAPI)
- **Device**: Raspberry Pi (Model TBD)
- **Frontend**: React / React Native (TBD)
- **Database**: SQLite or Postgres (for storing players, songs, sound effects)
- **Media Format**: WAV / MP3 files
- **Audio Output**: 3.5mm or USB audio via speakers
- **Networking**: Local Wi-Fi hotspot hosted by Raspberry Pi (no internet needed)

---

## 🔧 Initial Setup Tasks

### Raspberry Pi
- [ ] Choose a suitable Raspberry Pi model with audio and Wi-Fi support
- [ ] Configure Pi to auto-start:
  - Local Wi-Fi hotspot
  - Python web server on boot
- [ ] Ensure speakers are connected and test WAV/MP3 playback

### Backend
- [ ] Set up basic Python project structure with Flask/FastAPI
- [ ] Create API endpoint: `/play?song=<name>` to trigger audio
- [ ] Store songs locally and create mapping from player name to file

### Frontend (Initial)
- [ ] Build simple UI for selecting and triggering players/songs
- [ ] Connect to local Pi-hosted network and send API requests

---

## 🔮 Future Enhancements

- [ ] Build database schema for player profiles and song metadata
- [ ] Add "Next Batter" logic and cycling functionality
- [ ] Integrate situation-based soundboard (e.g., strikeouts, home runs)
- [ ] Add randomization or playlist queue for sound effects
- [ ] Create mobile-first web interface or native mobile app

---

## 📂 Directory Structure (Proposed)
