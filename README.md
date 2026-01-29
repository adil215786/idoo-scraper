# T-Mobile Inventory Scraper - GitHub Actions

This scraper automatically runs on GitHub Actions to collect inventory reports from T-Mobile Dealer Ordering system.

## 🚀 Quick Setup Guide

### 1. Create GitHub Repository

1. Go to https://github.com/new
2. Create a **PRIVATE** repository (recommended for security)
3. Name it something like `tmobile-inventory-scraper`
4. **Do NOT** initialize with README (we'll push our own files)

### 2. Upload Your Code to GitHub

```bash
# In your project folder, initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - T-Mobile scraper"

# Add your GitHub repo as remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Add Secrets to GitHub

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

#### Add these secrets:

**Secret 1: CREDENTIALS**
- Name: `CREDENTIALS`
- Value:
```
iotphilly|@unicomMetro11||adil.iot|Batman786!
iotbawa|@unicomMetro11||adil.iot|Batman786!
```

**Secret 2: WEBHOOK_URL** (optional - for Discord/Slack notifications)
- Name: `WEBHOOK_URL`
- Value: Your Discord/Slack webhook URL (leave blank if you don't have one)

### 4. Test the Workflow

#### Manual Test (Run Now):
1. Go to **Actions** tab in your repo
2. Click **T-Mobile Inventory Scraper** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait 3-5 minutes
5. Check the workflow run for success/failure

#### Download Reports:
1. After workflow completes, scroll to bottom of workflow run page
2. Under **Artifacts**, download `inventory-reports-XXX`
3. Unzip to get your Excel files

### 5. Schedule Configuration

The workflow currently runs:
- **Monday, Wednesday, Friday at 9:00 AM EST**

To change the schedule, edit `.github/workflows/scraper.yml`:

```yaml
schedule:
  # Format: 'minute hour day-of-month month day-of-week'
  # Times are in UTC (EST + 5 hours)
  - cron: '0 14 * * 1,3,5'  # Mon/Wed/Fri 9 AM EST
```

#### Common Schedule Examples:

```yaml
# Every day at 8 AM EST
- cron: '0 13 * * *'

# Monday and Thursday at 2 PM EST
- cron: '0 19 * * 1,4'

# Every weekday at 10 AM EST
- cron: '0 15 * * 1-5'
```

Use https://crontab.guru/ to help build cron schedules (remember to add 5 hours for EST to UTC conversion).

## 📊 How It Works

1. GitHub Actions spins up an Ubuntu server
2. Installs Chrome and Python dependencies
3. Creates credentials file from secrets
4. Runs your scraper
5. Uploads Excel reports as artifacts
6. Cleans up and shuts down

## 🔍 Troubleshooting

### View Logs
1. Go to **Actions** tab
2. Click on the workflow run
3. Click on **scrape** job
4. Expand each step to see detailed logs

### Download Logs
- After workflow run, download `scraper-logs-XXX` artifact
- Contains `scraper.log` and any screenshots

### Common Issues

**Issue: "No such file or directory: cred.txt"**
- Solution: Make sure you added the `CREDENTIALS` secret

**Issue: Login failed**
- Solution: Check credentials in the secret are correct
- Download logs artifact to see screenshot of error

**Issue: Workflow doesn't run on schedule**
- Solution: Make sure the repo has had at least one commit recently
- GitHub may disable scheduled workflows on inactive repos

**Issue: Chrome/ChromeDriver version mismatch**
- Solution: This is handled automatically by the workflow
- If issues persist, check the "Install Chrome" step logs

## 📥 Getting Your Reports

### Option 1: Download from GitHub (Current Setup)
1. Go to completed workflow run
2. Scroll to **Artifacts** section
3. Download `inventory-reports-XXX.zip`
4. Unzip to access Excel files

### Option 2: Email Setup (Future)
- We can add email functionality to automatically send reports
- Would require adding email service secrets (Resend, SendGrid, or Gmail)

## 🎯 Next Steps

- [ ] Test manual workflow run
- [ ] Verify both accounts process correctly
- [ ] Check Excel files are generated properly
- [ ] Set up email notifications (optional)
- [ ] Adjust schedule as needed

## 💡 Tips

- GitHub Actions has 2,000 free minutes/month
- Your script takes ~5 minutes, so you can run it ~400 times/month free
- Running 3x/week = ~12 runs/month = ~60 minutes used
- Keep repo private to protect credentials
- Artifacts are kept for 30 days (reports) and 7 days (logs)

## 🆘 Need Help?

Check the workflow logs first - they're very detailed and usually show exactly what went wrong.
