# Quick Start: OneDrive Sync in 5 Minutes

Get your Timecard Tracker syncing across devices quickly!

## What You Need
- Microsoft Account (free)
- 5 minutes

## Step 1: Azure AD Setup (2 minutes)

1. Go to: https://portal.azure.com
2. Sign in → `Azure Active Directory` → `App registrations` → `New registration`
3. Fill in:
   - **Name**: `Timecard Tracker`
   - **Account type**: `Personal and organizational accounts`
   - **Redirect URI**: 
     - Type: `Single-page application (SPA)`
     - URL: Your app URL (e.g., `https://yourdomain.com` or `http://localhost:8080`)
4. Click `Register`
5. **Copy the Client ID** (looks like: `12345678-1234-1234-1234-123456789abc`)
6. Go to `API permissions` → `Add permission` → `Microsoft Graph` → `Delegated`
7. Add: `Files.ReadWrite.AppFolder`
8. Click `Add permissions`

## Step 2: Configure App (1 minute)

1. Open `index.html` in text editor
2. Search for: `YOUR_CLIENT_ID_HERE` (around line 8515)
3. Replace with your Client ID from Step 1.5
4. Save the file

## Step 3: Host Your App

### Option A: GitHub Pages (Recommended)
```bash
# 1. Create GitHub repo and upload files
# 2. Go to Settings → Pages → Enable
# 3. Your URL: https://yourusername.github.io/repo-name
# 4. Add this URL to Azure AD redirect URIs
```

### Option B: Local Testing
```bash
# Run local server
python -m http.server 8080
# Access: http://localhost:8080
# Ensure http://localhost:8080 is in Azure AD redirect URIs
```

### Option C: Azure Static Web Apps (Free)
```bash
# 1. Go to portal.azure.com
# 2. Create Static Web App → Connect GitHub
# 3. Free tier → Deploy
# 4. Your URL: https://yourapp.azurestaticapps.net
# 5. Add this URL to Azure AD redirect URIs
```

## Step 4: Connect & Sync (1 minute)

1. Open your hosted app
2. Scroll to bottom
3. Click `☁️ Connect OneDrive`
4. Sign in with Microsoft account
5. Grant permissions
6. Done! You'll see: `✅ Synced with OneDrive`

## Use on Other Devices

1. Open app URL on another device
2. Click `☁️ Connect OneDrive`
3. Sign in with **same Microsoft account**
4. Your data appears automatically! 🎉

## Quick Tips

- **Manual Sync**: Click `🔄 Sync Now`
- **Auto Sync**: Enabled automatically (syncs on save)
- **Offline**: Works without internet, syncs when back online
- **Disconnect**: Click `☁️ Disconnect OneDrive` anytime

## Troubleshooting

**"OneDrive sync not configured"**
- Did you replace `YOUR_CLIENT_ID_HERE` with actual Client ID?

**Popup blocked**
- Allow popups for your domain

**Authentication failed**
- Check redirect URI matches exactly (including http/https)

**Need more help?**
See [ONEDRIVE_SETUP.md](ONEDRIVE_SETUP.md) for detailed guide.

---

**Total Time**: ~5 minutes  
**Cost**: Free (Azure AD + OneDrive personal account)  
**Result**: Timecard data synced across all your devices! ☁️✨
