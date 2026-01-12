# Quick Start: Detect and Merge Local Historical Data

## What This Does
Automatically detects all your local timecard data (weeks, projects, history) and intelligently merges it with your OneDrive cloud data, preserving everything from both sources.

## Step-by-Step Instructions

### 1. Open Your Timecard Tracker
Open the application in your browser (the index.html file).

### 2. Connect to OneDrive
- If not already connected, click **"☁️ Connect OneDrive"**
- Sign in with your Microsoft account
- Authorize the application

### 3. Detect and Merge Your Data
- Click the new **"🔍 Detect & Merge Local Data"** button
- You'll see a summary like this:
  ```
  📊 Historical Data Detection Summary
  
  LOCAL DATA:
    • Current Week: ✓
    • Historical Weeks: 12
    • Projects in History: 5
  
  CLOUD DATA:
    • Current Week: ✓
    • Historical Weeks: 8
    • Projects in History: 3
  
  Proceed with intelligent merge?
  ```

### 4. Review and Confirm
- Review the numbers to see what data exists locally vs in the cloud
- Click **OK** to proceed with the merge
- Click **Cancel** if you want to skip

### 5. Wait for Completion
- The app will merge all data intelligently
- You'll see: "✅ Successfully merged historical data! X total weeks now in sync."
- All your data is now synchronized!

## What Gets Merged

### ✅ Preserved and Combined:
- **All historical weeks** from both local and cloud
- **All projects** and project numbers
- **All tasks** and comments
- **Current week data** (uses the newer version)
- **Last active task**

### 🔒 Smart Merge Logic:
- **Duplicate weeks**: Entries are combined, duplicates removed
- **Unique weeks**: All preserved from both sources
- **Current week**: Uses whichever has the newer timestamp
- **History**: All projects, tasks, and comments combined

## Safety Features

1. **No data loss** - Everything is preserved
2. **User confirmation** - Always asks before merging
3. **Detailed summary** - Shows exactly what will be merged
4. **Reversible** - Can sync from cloud if needed
5. **Console logging** - Full audit trail in browser console

## Scenarios

### Scenario 1: First Time Syncing
- **Local**: 10 weeks of data
- **Cloud**: No data yet
- **Result**: All 10 weeks uploaded to cloud

### Scenario 2: Using Multiple Devices
- **Local**: Weeks 1-5, Projects A, B
- **Cloud**: Weeks 6-10, Projects C, D
- **Result**: Weeks 1-10, Projects A, B, C, D

### Scenario 3: Overlapping Data
- **Local**: Week 1 (5 entries), Week 2 (3 entries)
- **Cloud**: Week 1 (3 entries), Week 3 (4 entries)
- **Result**: Week 1 (8 unique entries), Week 2, Week 3

## Troubleshooting

### Button Not Visible?
- Make sure you're connected to OneDrive first
- The button appears next to "Sync Now" when connected

### Merge Failed?
- Check your internet connection
- Try clicking "Sync Now" to retry
- Check browser console (F12) for detailed error messages

### Not Sure What to Do?
- The merge is safe - it preserves all data
- When in doubt, click OK to merge
- You can always sync from cloud later if needed

## Additional Tips

### Before Merging:
- Good idea to export your data as backup (optional)
- Close other instances of the app on other devices
- Ensure you have internet connectivity

### After Merging:
- All your devices will now sync to the same merged data
- Use "Sync Now" for regular synchronization
- The app auto-syncs when you make changes

## Console Messages
Open browser console (F12) to see detailed logging:
- Local data detection results
- Cloud data detection results  
- Merge progress
- Success confirmation
- Any errors or warnings

## Need Help?
Check the browser console (F12 → Console tab) for detailed logs of what's happening during the merge process.
