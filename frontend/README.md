# 📱 BB Soundboard Frontend Design Proposal

## 📝 **Overview**

This document outlines the **initial design concept** for the React Native (Expo) frontend to interact with the BB Soundboard backend.

---

## 🎨 **Navigation Structure**

### **🔻 Bottom Tab Bar**

| Icon | Description |
| --- | --- |
| ▶️ **Play** | Navigates to the **Playback Screen**. |
| ⏹ **Stop** | Calls the **stop music endpoint** immediately on press. |
| 🛠 **Setup** | Navigates to the **Setup Screen** for management features. |

---

## 📃 **Screen Details**

### ▶️ **1. Playback Screen**

- **Features:**
  - **Next Batter Song**: Button to start the next batter's walkup song.
  - **Intermission/Break Music**: Button to play break music.
  - **Usage Buttons**: Dynamic list of buttons for each **usage type** (e.g. Homerun, Strikeout) calling their respective playback endpoints.

---

### ⏹ **2. Stop Button**

- **Action:**
  - Calls the backend **`/playback/stop`** endpoint to stop any currently playing music.
- **Placement:**
  - Middle icon in bottom tab bar.

---

### 🛠 **3. Setup Screen**

- **Features:**
  - **Songs Page Button**
    - Navigates to **Songs Page**.
  - **Lineup Page Button**
    - Navigates to **Lineup Page**.

---

#### 🎵 **3.1 Songs Page**

- **Displays:**
  - List of all songs in the system.
- **Actions:**
  - Add new song (file upload, name, artist).
  - View, add, and delete **snippets for each song**.
    - *(Note: Endpoint for **get snippets by song** will be implemented later).*

---

#### 🧢 **3.2 Lineup Page**

- **Displays:**
  - List of all players.
- **Actions:**
  - Create new players (name, walkup snippet).
  - Add players to the lineup.

---

## ✅ **Summary**

This design ensures:

- 🕹 **Efficient control interface** for gameplay and music management.
- 🎶 **Clear navigation** between playback controls and backend data management.
- 🔧 **Extendable structure** for future features such as SocketIO live updates.

---

### 💡 **Next Steps**

- Scaffold **bottom tab navigation** in Expo.
- Implement **API integration layer** using Axios or native Fetch.
- Design **Play** and **Setup screens** first to validate backend connectivity.

---

> ✨ **Author:** Alexander – BB Soundboard v1 Design Plan