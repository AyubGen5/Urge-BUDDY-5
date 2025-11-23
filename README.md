# Urge-BUDDY-5
A private urge logger and tracker to help you manage habits, visualize progress, and analyze triggers.
[README_Version2.md](https://github.com/user-attachments/files/22621009/README_Version2.

## Features

- Log urges (timestamp, intensity, note)
- View streaks, trends, and triggers in charts
- Export logs to CSV/JSON for backup or sharing
- Secure authentication (email/password, optionally GitHub OAuth)
- Responsive web UI (React + Chart.js)
- Backend REST API (Node.js/Express + MongoDB)
- Private local mode (if you prefer privacy over sync)

## Setup

### 1. Clone the repo

```sh
git clone https://github.com/yourusername/urge-buddy.git
cd urge-buddy
```

### 2. Install server dependencies

```sh
cd server
npm install
```

Create a `.env` file with:

```
MONGO_URI=your_mongo_connection
JWT_SECRET=your_jwt_secret
```

### 3. Install client dependencies

```sh
cd ../client
npm install
```

### 4. Start development

In two terminals:

```sh
cd server && npm run dev
cd client && npm start
```

### 5. Deployment

See `client/README.md` and `server/README.md`.

---

*For privacy,use local mode (browser only). For multi-device sync, run the server and register/login.*


*For privacy, use local mode (browser only). For multi-device sync, run the server and register/login.*


**Local CLI logger:** See `USAGE.md` for a tiny local CLI that appends timestamped urge entries to `data/urges.jsonl`.
