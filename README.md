
<div align="center">
  <img src="https://raw.githubusercontent.com/reversepy/eventia/main/assets/eventia_banner.png" alt="Eventia Banner" width="600"/>
  <h1>🎉 Eventia</h1>
  <p>
<i>The ultimate lightweight event manager bot for Discord communities.</i></p>
  <p>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white" alt="Python" /></a>
  <a href="https://github.com/reversepy"><img src="https://img.shields.io/badge/Made%20by-Reverse-%23ff69b4" alt="Made by Reverse" /></a>
  <a href="https://discord.gg/nitrogang"><img src="https://img.shields.io/discord/1376577777524015105?label=Join%20Discord&logo=discord&color=5865F2" alt="Join Discord" /></a>
  </p>
</div>

---

## ✨ Features

> Eventia helps your community stay active and organized with interactive, RSVP-enabled events.

- 🗓️ **Create Events** via `/createevent`
- ✅ **RSVP Support** with buttons
- 🛎️ **Auto-post Event Reminders**
- 🏆 **Participation Leaderboard**
- 📊 **Track Event Attendance**
- 📁 **JSON File Storage** — no database required!

---

## 📸 Example

> *This is just an example*

```
📅 Movie Night!
📝 We're watching Interstellar together!

🕒 When: June 23, 2025 — 9:00 PM GMT  
📍 Where: #🎬・movie-nights  
🎟️ RSVP: ✅
```

---

## 🛠 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/reversepy/eventia.git
cd eventia
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your environment

Create a `.env` file from the example:

```env
DISCORD_TOKEN=your_token_here
```

### 4. Create required files

```bash
mkdir data
echo "{}" > data/events.json
echo "{}" > data/rsvps.json
```

### 5. Run the bot

```bash
python bot.py
```

---

## 💾 JSON Storage Explanation

Eventia stores all event and RSVP data locally:

| File           | Purpose                           |
|----------------|-----------------------------------|
| `events.json`  | Stores all created event metadata |
| `rsvps.json`   | Tracks RSVPs by event             |

This makes it ideal for small to medium communities without needing a SQL database.

---

## 🚀 Slash Commands

| Command        | Description                              |
|----------------|------------------------------------------|
| `/createevent` | Create a new event                       |
| `/upcoming`    | View upcoming events                     |
| `/postrsvp`    | Post an RSVP button to a channel         |
| `/rsvplist`    | View who RSVPed to an event              |
| `/leaderboard` | View top participants                    |
| `/lhelp` | The rest of the commands                      |

---

## 🧠 Tech Stack

- Python 3.10+
- [discord.py v2.3+](https://github.com/Rapptz/discord.py)
- JSON file-based storage
- Modular Cogs system
- Slash Commands + Buttons

---

## 📚 Future Ideas

- Auto-reminders before each event
- Attendance check-in system
- Calendar feed support (ICS export?)
- Web dashboard for admins

---

## 🧑‍💻 Contributors

| Name        | Role             |
|-------------|------------------|
| `@reverse`  | Creator & Maintainer |
| `@lunatech` | RSVP System Engineer |
| `@omnicron` | Timezone Specialist |
| `@marzdev`  | UX & Embed Polish |

---

## 📄 License

MIT — feel free to use and adapt Eventia for your own community.

---

<div align="center"><sub>Built with ❤️ by Reverse</sub></div>
