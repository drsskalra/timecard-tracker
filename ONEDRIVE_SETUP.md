# OneDrive Cloud Sync Setup Guide

This guide will help you set up OneDrive cloud synchronization for your Timecard Tracker application, enabling automatic data syncing across all your devices.

## Overview

The OneDrive sync feature allows you to:
- 📱 Access your timecard data from any device
- ☁️ Automatic backup to Microsoft cloud
- 🔄 Real-time synchronization across devices
- 🔒 Secure authentication using Microsoft Account
- 💾 Offline-first architecture (works without internet)

## Prerequisites

1. A Microsoft Account (personal, work, or school)
2. Azure Active Directory (Azure AD) app registration (free)
3. Your Timecard Tracker hosted on a web server (local or remote)

## Step 1: Create Azure AD App Registration

1. **Go to Azure Portal**
   - Visit: https://portal.azure.com
   - Sign in with your Microsoft account

2. **Register a New Application**
   - Navigate to: `Azure Active Directory` → `App registrations` → `New registration`
   - Fill in the details:
     - **Name**: `Timecard Tracker` (or any name you prefer)
     - **Supported account types**: Select one of:
       - `Accounts in any organizational directory and personal Microsoft accounts` (recommended for personal use)
       - `Accounts in this organizational directory only` (for work/organization only)
     - **Redirect URI**: 
       - Platform: `Single-page application (SPA)`
       - URI: Your app URL (e.g., `http://localhost:8080` or `https://yourdomain.com`)
   - Click `Register`

3. **Note Your Client ID**
   - After registration, you'll see the application **Overview** page
   - Copy the **Application (client) ID** - you'll need this later
   - Example: `12345678-1234-1234-1234-123456789abc`

4. **Configure API Permissions**
   - In your app registration, go to `API permissions`
   - Click `Add a permission` → `Microsoft Graph` → `Delegated permissions`
   - Add these permissions:
     - `User.Read` (usually already added)
     - `Files.ReadWrite.AppFolder`
   - Click `Add permissions`
   - Optional: Click `Grant admin consent` (if you're an admin)

## Step 2: Configure Your Application

1. **Open index.html**
   - Locate the `initializeMSAL()` function (around line 8515)
   - Find this line:
     ```javascript
     clientId: 'YOUR_CLIENT_ID_HERE',
     ```
   - Replace `YOUR_CLIENT_ID_HERE` with your actual Client ID from Step 1.3

2. **Update Redirect URI (if different)**
   - In the same function, verify the `redirectUri`:
     ```javascript
     redirectUri: window.location.origin
     ```
   - This automatically uses your current URL. If you need a specific URL, change it to:
     ```javascript
     redirectUri: 'https://yourdomain.com'
     ```

## Step 3: Host Your Application

### Option A: GitHub Pages (Free, Recommended)

1. **Create a GitHub Repository**
   - Go to GitHub and create a new repository
   - Upload your `index.html` and `manifest.json` files

2. **Enable GitHub Pages**
   - Go to repository `Settings` → `Pages`
   - Source: `Deploy from a branch`
   - Branch: `main` / `master` → `/ (root)`
   - Click `Save`
   - Your site will be available at: `https://yourusername.github.io/repository-name`

3. **Update Azure AD Redirect URI**
   - Go back to Azure Portal → Your App Registration → `Authentication`
   - Add your GitHub Pages URL as a redirect URI
   - Save changes

### Option B: Local Development Server

For local testing:

```bash
# Using Python 3
python -m http.server 8080

# Using Node.js (npx)
npx serve

# Using PHP
php -S localhost:8080
```

Then access: `http://localhost:8080`

**Important**: Ensure `http://localhost:8080` is added as a redirect URI in Azure AD.

### Option C: OneDrive/Personal Cloud Hosting

Since you want to host on Microsoft cloud:

1. **Host HTML on OneDrive**
   - Upload `index.html` to your OneDrive
   - Right-click → `Share` → `Anyone with the link can view`
   - However, OneDrive doesn't execute HTML by default for security

2. **Better Option: Azure Static Web Apps (Free Tier)**
   - Go to: https://portal.azure.com
   - Create a new `Static Web App`
   - Connect to your GitHub repository
   - Free tier includes: 100GB bandwidth/month, custom domains, SSL
   - URL will be: `https://yourapp.azurestaticapps.net`

3. **Update Azure AD Redirect URI**
   - Add your Azure Static Web App URL to redirect URIs

## Step 4: Using OneDrive Sync

1. **Open Your Application**
   - Navigate to your hosted Timecard Tracker

2. **Connect to OneDrive**
   - Scroll to the bottom action buttons
   - Click `☁️ Connect OneDrive`
   - A Microsoft login popup will appear
   - Sign in with your Microsoft account
   - Grant permissions when prompted

3. **Sync Your Data**
   - After successful connection, you'll see:
     - Button changes to `☁️ Disconnect OneDrive`
     - A new `🔄 Sync Now` button appears
     - Status indicator showing sync status
   - Click `🔄 Sync Now` to perform manual sync
   - Data automatically syncs on changes

4. **Using on Multiple Devices**
   - Open the app on another device
   - Click `☁️ Connect OneDrive`
   - Sign in with the same Microsoft account
   - Your data will automatically sync!

## How It Works

### Data Storage
- All data is stored in your OneDrive app folder: `/Apps/TimecardTracker/`
- Data file: `timecard_data.json`
- Only your application can access this folder
- Data includes:
  - Current week entries
  - All historical weeks
  - Project/task history
  - Last active task

### Sync Behavior
1. **Manual Sync**: Click `🔄 Sync Now`
2. **Auto Sync**: Enabled automatically after connection
3. **Conflict Resolution**: 
   - If cloud data is newer: Prompts to choose
   - If local data is newer: Uploads to cloud
4. **Offline Support**: 
   - App works offline using localStorage
   - Syncs automatically when connection restored

### Sync Status Indicators
- 🔄 **Syncing**: Currently syncing with OneDrive
- ✅ **Synced**: Data is up to date (shows last sync time)
- ❌ **Error**: Sync failed (click Sync Now to retry)

## Troubleshooting

### "OneDrive sync not configured" Error
- Ensure you replaced `YOUR_CLIENT_ID_HERE` with your actual Client ID
- Clear browser cache and reload

### Popup Blocked
- Allow popups for your domain in browser settings
- Try clicking the button again

### Authentication Failed
- Check that redirect URI in Azure AD matches your app URL exactly
- Ensure app is hosted via HTTPS (or HTTP for localhost)
- Clear browser cookies for login.microsoftonline.com

### Sync Failed
- Check internet connection
- Verify Microsoft account has OneDrive access
- Try disconnecting and reconnecting

### Data Not Syncing Across Devices
- Ensure using the same Microsoft account on all devices
- Click `🔄 Sync Now` manually on each device
- Check that cloud data exists: Should show "Synced with OneDrive"

## Security & Privacy

- ✅ Your data is stored in YOUR OneDrive
- ✅ Only you can access the app folder
- ✅ Authentication via Microsoft (industry standard)
- ✅ All traffic encrypted (HTTPS)
- ✅ No third-party servers involved
- ✅ Data never shared with app developer

## Advanced Configuration

### Enable Auto-Sync
Currently auto-sync triggers after each save. To customize:

1. Find `autoSyncEnabled` variable in code
2. Add a settings toggle in UI
3. Adjust debounce timeout (currently 1 second)

### Change Sync File Name
In code, modify:
```javascript
const ONEDRIVE_DATA_FILE = 'timecard_data.json';
```

### Multiple App Instances
Each Azure AD app registration is isolated. To run multiple instances:
1. Create separate app registrations
2. Use different client IDs
3. Data won't sync between different registrations

## Support

For issues:
1. Check browser console for errors (F12)
2. Verify all setup steps completed
3. Test with incognito/private window
4. Check Azure AD app permissions granted

## Cost

- **Azure AD App Registration**: Free
- **Microsoft Graph API**: Free tier (sufficient for this app)
- **OneDrive Storage**: Uses your OneDrive quota
  - Typical timecard data: < 1MB per year
  - Free OneDrive: 5GB
- **GitHub Pages / Azure Static Web Apps**: Free tier available

## Next Steps

1. Complete Steps 1-3 above
2. Test on one device first
3. Connect from second device to verify sync
4. Bookmark your hosted URL on all devices
5. Install as PWA on mobile devices (Add to Home Screen)

---

**Need Help?**
- Azure Portal: https://portal.azure.com
- Microsoft Graph Docs: https://docs.microsoft.com/graph
- MSAL.js Docs: https://aka.ms/msal-js
