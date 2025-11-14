# Time Card Tracker

A professional time tracking Progressive Web App (PWA) for managing project timecards with advanced features including interactive week view calendar and comprehensive history management.

**Developed by:** Shashank Singh Kalra, PhD, PE  
**LinkedIn:** [https://www.linkedin.com/in/shashanksinghkalra/](https://www.linkedin.com/in/shashanksinghkalra/)  
**GitHub:** [https://github.com/drsskalra](https://github.com/drsskalra)  
**Email:** shashank.kalra@arcadis.com

## Features

### Time Tracking
- ⏱️ Real-time timer with start/stop functionality
- 🕒 Clock time tracking (start/end times) for each work session
- 📌 Picture-in-Picture floating timer window
- 💾 Auto-save to browser localStorage
- 🔄 Quick restart last active task

### Dual View System
- 📊 **Table View**: Traditional timecard table with inline editing
- 📅 **Week View**: Interactive calendar timeline with visual time blocks
  - Drag and drop time blocks to reposition
  - Resize blocks to adjust duration
  - Click empty space to add new entries
  - Click blocks to edit or delete
  - Visual representation of work hours throughout the day

### Data Management
- 📥 Import Data from Previous Export with merge/replace options
- 📤 Export current week to Excel (with clock times)
- 📊 Export all historical weeks to multi-sheet Excel workbook
- 💾 Download/restore history as JSON backup
- ✏️ Advanced history editor with project-based organization
- 🗑️ Delete confirmation for safety (requires typing "Delete")

### Smart Features
- 🎯 Intelligent autocomplete for projects, tasks, and comments
- 📝 History tracking organized by project name
- 🔍 Structured history shows related project numbers, tasks, and comments
- ➕ Add new items directly from dropdowns
- 📈 Automatic calculation of totals in decimal hours
- 💬 Comment tracking with green icon for easy visibility
- 🗑️ Red delete icons for quick removal

### Progressive Web App (PWA)
- 📱 Install on mobile or desktop devices
- 🔒 Works offline after first load
- ⚡ Fast performance with service worker caching
- 🔔 Idle timer notifications to prevent lost time
- 🛡️ Single instance enforcement (prevents data conflicts)

## Usage

### Getting Started
1. Visit the website: [https://drsskalra.github.io/timecard-tracker/](https://drsskalra.github.io/timecard-tracker/)
2. Enter your project information:
   - Project Name (e.g., "Client A - Website Redesign")
   - Project Number (e.g., "2024-001")
   - Task Name (e.g., "Frontend Development")
3. Click "Start Timer" to begin tracking time
4. Click "Stop Timer" when finished with the task
5. Your entry is automatically saved with clock times

### Working with Views
- **Table View** (default): See all entries in a traditional table format
- **Week View**: Switch to calendar view to see visual timeline of your week
  - Drag time blocks to different times or days
  - Resize blocks to adjust work duration
  - Click empty timeline space to add new time blocks
  - Click existing blocks to edit details or delete

### Managing History
- Click "✏️ Edit History" to manage your saved suggestions
- Select a project name to view and edit related information
- Add, edit, or delete project numbers, tasks, and comments
- Download history as JSON backup
- Clear all history if needed (requires confirmation)

### Exporting Data
- **Export This Week**: Export current week to Excel (includes clock times)
- **Export All Weeks**: Export entire timecard history to multi-sheet Excel
- **Import from Excel**: Import previously exported timecard data

## Installation as PWA

### Desktop (Chrome, Edge):
- Click the install icon in the address bar
- Or go to Settings → Install Time Card Tracker

### Mobile (Chrome, Safari):
- Tap the menu button
- Select "Add to Home Screen"

## Keyboard Shortcuts & Tips

- **Mini Window**: Click "📺 Mini Window" to open floating Picture-in-Picture timer
- **Quick Restart**: Automatically loads last active task when reopening the app
- **Auto-complete**: Start typing in any field to see matching suggestions
- **Clock Times**: Automatically captured when you start/stop timer
- **Week Navigation**: Use "◀ Previous Week" and "Next Week ▶" to view different weeks
- **Comments**: Click green 💬 icon to view/add comments for each day

## Technical Details

- **Technology**: Single-page HTML application with vanilla JavaScript
- **Storage**: Browser localStorage (no backend server required)
- **Export Format**: Excel (.xlsx) with XLSX.js library
- **PWA Features**: Service worker for offline functionality
- **Browser Support**: Modern browsers (Chrome, Edge, Firefox, Safari)

## Data Privacy

All data is stored locally in your browser. No information is sent to any server. Your timecard data never leaves your device unless you explicitly export it.

## Troubleshooting

- **Timer not running**: Ensure only one instance of the app is open
- **Data not saving**: Check browser localStorage is enabled
- **Import issues**: Ensure Excel file was exported from this application
- **Week view not showing blocks**: Entries need clock time data (start/stop timer to capture)

## Contributing

Issues and suggestions can be reported via GitHub Issues.

## License

© 2025 Shashank Singh Kalra. All rights reserved.
