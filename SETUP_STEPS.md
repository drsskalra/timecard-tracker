# Fix OneDrive Connection Error - Step by Step

## The Error You're Seeing

**Error**: "unauthorized_client: The client does not exist or is not enabled for consumers"

**Cause**: You haven't created an Azure AD app registration yet.

## Solution: Complete Setup (10 minutes)

### Step 1: Create Azure AD App (5 minutes)

1. **Go to Azure Portal**
   - URL: https://portal.azure.com
   - Sign in with your Microsoft account (personal or work)

2. **Navigate to App Registrations**
   - Search for "Azure Active Directory" (or "Entra ID")
   - Click on it
   - In left menu: Click "App registrations"
   - Click "New registration"

3. **Fill in Registration Form**
   ```
   Name: Timecard Tracker
   
   Supported account types: 
   ✓ Select "Personal Microsoft accounts only"
      (or "Accounts in any organizational directory and personal Microsoft accounts")
   
   Redirect URI:
   - Platform: Single-page application (SPA)
   - URI: http://localhost:8080
   ```

4. **Click "Register"**

5. **COPY YOUR CLIENT ID**
   - You'll see a page with "Application (client) ID"
   - It looks like: `12345678-1234-1234-1234-123456789abc`
   - **COPY THIS!** You'll need it in Step 2

6. **Add API Permissions**
   - Click "API permissions" in left menu
   - Click "Add a permission"
   - Click "Microsoft Graph"
   - Click "Delegated permissions"
   - Search for: `Files.ReadWrite.AppFolder`
   - Check the box next to it
   - Click "Add permissions"

### Step 2: Configure Your App (2 minutes)

1. **Open index.html** in your editor (it's already open)

2. **Find line 8515** (press Ctrl+G and type 8515, or search for `YOUR_CLIENT_ID_HERE`)

3. **Replace the placeholder**:
   
   Change this:
   ```javascript
   clientId: 'YOUR_CLIENT_ID_HERE',
   ```
   
   To this (use your actual Client ID):
   ```javascript
   clientId: '12345678-1234-1234-1234-123456789abc',
   ```

4. **Save the file**

### Step 3: Test (2 minutes)

1. **Refresh your browser** (press F5)
2. **Scroll to bottom** of the page
3. **Click "☁️ Connect OneDrive"**
4. **Sign in** when popup appears
5. **Grant permissions** when asked
6. **Success!** You should see: ✅ Synced with OneDrive

## Still Getting an Error?

### Error: "Redirect URI mismatch"
**Solution**: 
- Go back to Azure Portal → Your App → Authentication
- Click "Add a platform" → "Single-page application"
- Add your exact URL (check browser address bar)
- Examples:
  - `http://localhost:8080`
  - `https://yourusername.github.io/timecard-tracker`
  - `https://yourapp.azurestaticapps.net`

### Error: "Popup blocked"
**Solution**: Allow popups for your domain in browser settings

### Error: "AADSTS50011: Reply URL mismatch"
**Solution**: The URL in Azure must exactly match your app URL (including http/https)

## Need Visual Help?

Screenshots and detailed walkthrough: [ONEDRIVE_SETUP.md](ONEDRIVE_SETUP.md)

## Quick Test Without Azure Setup?

If you just want to test the app without OneDrive sync:
- The app works perfectly without OneDrive
- All data is saved locally in your browser
- You just won't have cross-device sync
- Skip the OneDrive connection and use it as-is!
