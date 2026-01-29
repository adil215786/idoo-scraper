# 🎯 QUICK START GUIDE - GitHub Actions Setup

## ⏱️ Time Required: 15-20 minutes

---

## STEP 1: Create GitHub Repository (3 minutes)

1. Open https://github.com/new in your browser
2. Fill in:
   - **Repository name**: `tmobile-inventory-scraper` (or any name you prefer)
   - **Description**: "Automated T-Mobile inventory scraper"
   - **Private**: ✅ CHECK THIS (keeps your code private)
   - **Add README**: ❌ LEAVE UNCHECKED
3. Click **Create repository**
4. **KEEP THIS TAB OPEN** - you'll need it in Step 3

---

## STEP 2: Prepare Your Local Files (2 minutes)

### Option A: If you don't have Git installed

1. Download all files from this folder as a ZIP
2. Extract to a new folder on your computer
3. Skip to **STEP 3 (Upload via GitHub Web Interface)**

### Option B: If you have Git installed

Open terminal/command prompt in the folder with these files and run:

```bash
git init
git add .
git commit -m "Initial commit"
```

Now skip to **STEP 3 (Upload via Command Line)**

---

## STEP 3: Upload Code to GitHub

### Option A: Upload via GitHub Web Interface (EASIEST)

1. Go back to your new repository page on GitHub
2. Click **uploading an existing file**
3. Drag and drop ALL files from your folder:
   - `.github` folder
   - `scraper.py`
   - `requirements.txt`
   - `.gitignore`
   - `README.md`
4. **DO NOT upload**: `cred.txt` or `cred.txt.example`
5. Write commit message: "Initial commit"
6. Click **Commit changes**

### Option B: Upload via Command Line (if you have Git)

Replace `YOUR_USERNAME` and `tmobile-inventory-scraper` with your details:

```bash
git remote add origin https://github.com/YOUR_USERNAME/tmobile-inventory-scraper.git
git branch -M main
git push -u origin main
```

---

## STEP 4: Add Credentials as Secrets (5 minutes)

1. In your GitHub repository, click **Settings** (top menu)
2. In left sidebar, click **Secrets and variables** → **Actions**
3. Click **New repository secret** (green button)

### Add Secret #1: CREDENTIALS

- **Name**: `CREDENTIALS` (must be exact - all caps)
- **Secret**: Copy and paste this exactly:
```
iotphilly|@unicomMetro11||adil.iot|Batman786!
iotbawa|@unicomMetro11||adil.iot|Batman786!
```
- Click **Add secret**

### Add Secret #2: WEBHOOK_URL (OPTIONAL)

- **Name**: `WEBHOOK_URL`
- **Secret**: Your Discord/Slack webhook URL (or leave blank for now)
- Click **Add secret**

✅ You should now see 1-2 secrets listed (with green checkmarks)

---

## STEP 5: Test Your Workflow (5 minutes)

### Run It Manually (First Test)

1. Click **Actions** tab (top of your repo)
2. You should see **"T-Mobile Inventory Scraper"** workflow
3. Click on it
4. Click **Run workflow** button (right side)
5. Keep "Branch: main" selected
6. Click green **Run workflow** button
7. Wait 5-10 seconds, then refresh the page
8. You'll see a workflow run appear with a yellow dot (running)

### Watch It Run

1. Click on the workflow run (it will have a title like "T-Mobile Inventory Scraper")
2. Click on **scrape** job
3. Watch each step execute in real-time
4. Look for:
   - ✅ Green checkmarks = success
   - ❌ Red X = failure (click to see error details)

**Expected runtime**: 3-5 minutes

---

## STEP 6: Download Your Reports (2 minutes)

### After Workflow Completes Successfully:

1. Go back to the workflow run summary page
2. Scroll to bottom
3. Under **Artifacts** section, you'll see:
   - `inventory-reports-XXX` ← **YOUR EXCEL FILES ARE HERE**
   - `scraper-logs-XXX` ← Logs and screenshots
4. Click to download (downloads as ZIP)
5. Unzip to access your files

**You should see**:
- `IDOO-IOTPHILLY-MM-DD-YYYY.xlsx`
- `IDOO-IOTBAWA-MM-DD-YYYY.xlsx`

---

## STEP 7: Set Up Automatic Schedule (ALREADY DONE!)

Your scraper is already scheduled to run:
- **Monday at 9:00 AM EST**
- **Wednesday at 9:00 AM EST**
- **Friday at 9:00 AM EST**

### Want to Change the Schedule?

1. In your repo, navigate to `.github/workflows/scraper.yml`
2. Click the pencil icon (Edit)
3. Find this line:
```yaml
    - cron: '0 14 * * 1,3,5'
```
4. Change to your preferred schedule:

**Examples:**
```yaml
# Every day at 10 AM EST
- cron: '0 15 * * *'

# Monday, Wednesday, Friday at 2 PM EST  
- cron: '0 19 * * 1,3,5'

# Tuesday and Thursday at 8 AM EST
- cron: '0 13 * * 2,4'
```

**Remember**: GitHub uses UTC time, so add 5 hours to EST
- 8 AM EST = 13 (1 PM UTC)
- 9 AM EST = 14 (2 PM UTC)
- 10 AM EST = 15 (3 PM UTC)

5. Click **Commit changes**

---

## 🎉 YOU'RE DONE!

Your scraper will now run automatically on schedule and you can:
- ✅ Download reports from GitHub Actions artifacts
- ✅ Run manually anytime via "Run workflow" button
- ✅ View detailed logs if anything fails
- ✅ Get screenshots of errors automatically

---

## 🔧 TROUBLESHOOTING

### Problem: "Secret not found: CREDENTIALS"
**Solution**: Go back to Step 4 and make sure you typed `CREDENTIALS` exactly (all caps)

### Problem: Login failed
**Solution**: 
1. Download `scraper-logs-XXX` artifact
2. Look at screenshots to see what went wrong
3. Double-check credentials in your secret

### Problem: Workflow doesn't appear
**Solution**: 
- Make sure you uploaded the `.github/workflows/scraper.yml` file
- Check that the file structure is: `.github/workflows/scraper.yml` (two nested folders)

### Problem: Chrome/Driver errors
**Solution**: This is handled automatically - check the workflow logs in the "Install Chrome" step

### Problem: "No such file or directory"
**Solution**: Make sure all files were uploaded properly - check the repo file list

---

## 📞 NEED MORE HELP?

1. Check the workflow logs (Actions → Click on run → Click on "scrape" job)
2. Download the `scraper-logs-XXX` artifact for detailed logs
3. The logs are VERY detailed and usually show exactly what went wrong

---

## 🚀 NEXT STEPS (OPTIONAL)

- [ ] Set up email notifications to automatically send reports
- [ ] Add more accounts to CREDENTIALS secret
- [ ] Customize schedule
- [ ] Set up error notifications via Discord/Slack webhook

Enjoy your automated scraper! 🎊
