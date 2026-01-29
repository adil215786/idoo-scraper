# 📁 Project File Structure

```
tmobile-inventory-scraper/
│
├── .github/
│   └── workflows/
│       └── scraper.yml          ← GitHub Actions workflow (runs the scraper)
│
├── scraper.py                   ← Your main scraper script
├── requirements.txt             ← Python dependencies
├── .gitignore                   ← Files to ignore in git
│
├── README.md                    ← Main documentation
└── SETUP_GUIDE.md              ← Step-by-step setup instructions
```

## 📝 File Descriptions

### `.github/workflows/scraper.yml`
- **What it does**: Tells GitHub Actions when and how to run your scraper
- **Schedule**: Mon/Wed/Fri at 9 AM EST
- **Actions**: Installs Chrome, runs scraper, uploads reports

### `scraper.py`
- **What it does**: Your T-Mobile scraper (unchanged from original)
- **Processes**: Both accounts (iotphilly and iotbawa) sequentially
- **Outputs**: Excel files in `download_files/` folder

### `requirements.txt`
- **What it does**: Lists all Python packages needed
- **Auto-installed**: By GitHub Actions on each run

### `.gitignore`
- **What it does**: Prevents sensitive files from being uploaded to GitHub
- **Protects**: `cred.txt`, `.env`, log files, downloads

### `README.md`
- **What it does**: Complete documentation and reference
- **Includes**: How it works, troubleshooting, schedule changes

### `SETUP_GUIDE.md`
- **What it does**: Step-by-step walkthrough for first-time setup
- **Perfect for**: Following along during initial setup

## 🔐 Files NOT Included (On Purpose)

- `cred.txt` - Your credentials (stored as GitHub Secret instead)
- `.env` - Environment variables (not needed for GitHub Actions)
- `download_files/` - Downloaded reports (created during runtime)

## ✅ What to Upload to GitHub

Upload these files:
- ✅ `.github/` folder (with workflows subfolder)
- ✅ `scraper.py`
- ✅ `requirements.txt`
- ✅ `.gitignore`
- ✅ `README.md`
- ✅ `SETUP_GUIDE.md`

DO NOT upload:
- ❌ `cred.txt` (use GitHub Secrets instead)
- ❌ `cred.txt.example` (optional - for your reference only)
- ❌ Any `.xlsx` files
- ❌ Any `.log` files
- ❌ `download_files/` folder

## 🚀 Next Steps

1. Follow `SETUP_GUIDE.md` for detailed setup instructions
2. Refer to `README.md` for ongoing usage and troubleshooting
