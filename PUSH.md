# Push to GitHub - Instructions

Follow these steps to push your SmartCut Studio project to GitHub:

## Option 1: Using GitHub CLI (Recommended if you have gh authenticated)

If you've already run `gh auth login`, simply run:

```bash
cd c:/Users/Rohit kumar/Desktop/amit
gh repo create smartcut-studio --public --source=. --push
```

## Option 2: Manual Git Commands

### Step 1: Create a New Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `smartcut-studio`
3. Description: "AI-assisted video editing with automatic scene detection, beat-synced transitions, and Whisper transcription"
4. Select "Public"
5. Click "Create repository" (don't initialize with any options)

### Step 2: Run These Commands in Terminal

```bash
cd c:/Users/Rohit kumar/Desktop/amit
git remote add origin https://github.com/ambrosiusamit/smartcut-studio.git
git branch -M main
git push -u origin main
```

---

**Repository Details:**
- ✅ Owner: ambrosiusamit
- ✅ Repository name: smartcut-studio
- ✅ README.md (with Amit Kumar as author)
- ✅ LICENSE (MIT - Amit Kumar)
- ✅ CONTRIBUTING.md
- ✅ .gitignore (excludes videos and cache files)


