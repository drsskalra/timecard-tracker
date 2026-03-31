# Local-First Sync Architecture for TimeCard Tracker

## Overview

This document describes a local-first sync strategy that prioritizes offline functionality and data integrity. The system ensures:
- ✅ Works perfectly offline
- ✅ All historical data is preserved
- ✅ Automatic sync when online
- ✅ Conflict resolution with data preservation
- ✅ Multi-device synchronization

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     User's Browser                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           LOCAL STORAGE (PRIMARY)                        │   │
│  │  - CurrentWeek (actively editing)                        │   │
│  │  - AllWeeks (historical data)                            │   │
│  │  - History (project/task/comment history)                │   │
│  │  - LastTask & Timer State                                │   │
│  │  - SyncMetadata (timestamps, versions, hashes)           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              │ (Auto-save on every change)       │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │        OFFLINE SYNC QUEUE (IndexedDB / LocalStorage)    │   │
│  │  - Pending sync operations                               │   │
│  │  - Change timestamps                                     │   │
│  │  - Retry logic & backoff                                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                    ┌─────────┴─────────┐                         │
│                    │                   │                         │
│             (No Internet)         (Has Internet)                 │
│                    │                   │                         │
│                    ▼                   ▼                         │
│          ┌──────────────────┐  ┌──────────────────┐             │
│          │ User continues   │  │ SYNC MANAGER     │             │
│          │ to work offline  │  │ - Upload changes │             │
│          │ All data saved   │  │ - Download sync  │             │
│          │ to localStorage  │  │ - Merge conflict │             │
│          └──────────────────┘  └──────────────────┘             │
│                                        │                         │
│                                        ▼                         │
│                           ┌───────────────────────┐              │
│                           │  Check OneDrive for   │              │
│                           │  newer data           │              │
│                           └───────────────────────┘              │
│                                        │                         │
│          ┌─────────────────────────────┼──────────────────────┐  │
│          │                             │                      │  │
│    (Local Newer)           (Cloud Newer)            (Equal)   │  │
│          │                             │                      │  │
│          ▼                             ▼                      ▼  │
│    Upload to Cloud   Intelligent Merge + Show User   Use Local  │
│    No Conflict       Option to accept/review changes           │
│          │                             │                      │  │
│          └─────────────────────────────┴──────────────────────┘  │
│                                        │                         │
│                                        ▼                         │
│                           ┌───────────────────────┐              │
│                           │ SYNC COMPLETE         │              │
│                           │ - Local = Cloud       │              │
│                           │ - Metadata updated    │              │
│                           │ - Queue cleared       │              │
│                           └───────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                                   │
                                   │ (OneDrive Connection)
                                   ▼
                        ┌──────────────────────┐
                        │  Microsoft OneDrive  │
                        │  /Apps/TimeCard      │
                        │   Tracker/           │
                        │  - data.json         │
                        │  - metadata.json     │
                        └──────────────────────┘
```

## Data Storage Layers

### Layer 1: LocalStorage (Primary)
```json
{
  "timecard_current_week": { /* Current week data */ },
  "timecard_all_weeks": { /* Historical weeks */ },
  "timecard_history": { /* Project/task/comment history */ },
  "timecard_last_task": { /* Last active task */ },
  "timecard_sync_metadata": {
    "lastSyncTime": "2024-03-31T12:00:00Z",
    "localVersion": "v1.2024-03-31-12-00-00",
    "cloudVersion": "v1.2024-03-31-11-55-00",
    "dataHash": "abc123...",
    "allWeeksHash": "def456...",
    "historyHash": "ghi789...",
    "syncStatus": "synced|syncing|failed|offline",
    "lastError": null,
    "pendingSyncCount": 0
  }
}
```

### Layer 2: Offline Sync Queue (IndexedDB)
```json
{
  "queue": [
    {
      "id": "op-1711900400123",
      "timestamp": "2024-03-31T12:00:00Z",
      "type": "FULL_SYNC" | "PARTIAL_UPDATE",
      "data": { /* Diff only */ },
      "dataHash": "abc123",
      "retryCount": 0,
      "maxRetries": 5,
      "exponentialBackoff": true,
      "status": "pending|retry|failed"
    }
  ],
  "lastProcessed": "op-1711900300000"
}
```

### Layer 3: OneDrive (Cloud)
```json
{
  "metadata": {
    "fileVersion": "1.0",
    "appVersion": "1.2.3",
    "cloudTimestamp": "2024-03-31T12:00:00Z",
    "cloudVersion": "v1.2024-03-31-12-00-00",
    "dataHashes": {
      "currentWeek": "abc123",
      "allWeeks": "def456",
      "history": "ghi789"
    },
    "syncedDevices": [
      {
        "deviceId": "device-1",
        "lastSync": "2024-03-31T12:00:00Z"
      }
    ]
  },
  "data": {
    "currentWeek": { /* Current week */ },
    "allWeeks": { /* All historical weeks */ },
    "history": { /* History */ }
  }
}
```

## Sync Algorithm

### When User Takes Action (Offline or Online)
```
1. User makes change (add/edit/delete entry)
   ↓
2. Update localStorage immediately
   ↓
3. Update syncMetadata (timestamp, version increment)
   ↓
4. Trigger auto-sync (debounced 1-2 seconds)
   ↓
5. Check internet connection
   ├─ NO_INTERNET: Store in offline queue, show offline indicator
   ├─ HAS_INTERNET: Execute sync immediately
```

### Sync Process (When Online)
```
1. Collect pending changes from queue
2. Compare local version with cloud version
3. If local is newer:
   a. Upload local data to cloud
   b. Update cloudVersion in metadata
   c. Mark queue items as synced
4. Else if cloud is newer:
   a. Download cloud data
   b. Perform intelligent merge
   c. Show user notification with changes
   d. Update local data
5. Else if equal:
   a. Do nothing (already synced)
6. Clear sync queue
7. Update lastSyncTime
8. Update syncStatus to "synced"
```

### Conflict Resolution
```
Conflict Types:
1. Local newer than cloud (normal case - user was more active)
   → Upload to cloud
   → No data loss
   
2. Cloud newer than local (another device updated)
   → Show summary of changes
   → Option to review + accept
   → Or keep local if user prefers
   → Always merge historical data
   
3. Both have unique data (concurrent edits on multiple devices)
   → Merge strategy:
     a. Current week: Keep both, merge entries by timestamp
     b. Historical weeks: Combine all weeks (union)
     c. History: Combine all items (union)
     d. Upload merged result to cloud
```

## Implementation Details

### Key Functions

#### 1. `saveDataWithSync(data)`
- Save to localStorage immediately
- Update sync metadata
- Queue for sync
- Debounce cloud sync (1-2 seconds)

#### 2. `syncToCloud()`
- Check internet connection
- Get pending changes
- Calculate data hash
- Compare with cloud version
- Upload if newer or equal
- Update metadata

#### 3. `syncFromCloud()`
- Check cloud version
- Download if available
- Compare hashes
- Perform merge if needed
- Update local storage
- Apply changes to UI

#### 4. `intelligentMerge(local, cloud, metadata)`
- For current week: Keep newest by timestamp
- For all weeks: Union of all weeks
- For history: Union of all items
- Generate new hash
- Return merged result

#### 5. `handleOffline()` / `handleOnline()`
- Network change listeners
- Process sync queue when connectivity restored
- Exponential backoff for failed syncs

### Error Handling & Recovery
```
Failed Sync:
1. Store in retry queue
2. Wait before retry (exponential backoff: 1s, 2s, 4s, 8s, 16s)
3. Max 5 retries
4. If all fail: Show user alert + manual retry button
5. All data remains safe in localStorage

Network Loss:
1. Immediately stop sync attempt
2. Show "offline, changes saved locally" message
3. Store operation in queue
4. Resume when network restored
```

## Features

### 1. Multi-Device Sync
- Each device has unique ID
- Track which devices have synced
- Sync history metadata to cloud
- Detect and notify of activity on other devices

### 2. Data Versioning
- Version format: `v1.YYYY-MM-DD-HH-MM-SS`
- Compare versions to determine sync direction
- Track version history for rollback (optional)

### 3. Hash-Based Change Detection
- Calculate SHA-256 hash of each data section
- Only upload if hash changed
- Detect data corruption

### 4. Sync Status Dashboard
- Current sync status (synced/syncing/offline/failed)
- Last sync timestamp
- Pending changes count
- Data validation status
- Device sync history

### 5. Manual Controls
- "Sync Now" button to force immediate sync
- "View Sync History" to see all syncs
- "Resolve Conflicts" for manual intervention
- "Download/Upload" specific data sections

## Benefits

✅ **Offline-First**: Works perfectly without internet  
✅ **Data Integrity**: All historical data preserved  
✅ **No Data Loss**: Operations queued during offline periods  
✅ **Intelligent Merging**: Combines updates from multiple devices  
✅ **Transparent Syncing**: User always knows sync status  
✅ **Multi-Device**: Seamless sync across all devices  
✅ **Error Recovery**: Automatic retry with backoff  
✅ **Conflict Resolution**: User-friendly merge display  

## Migration Path

1. Keep existing sync logic initially
2. Add sync metadata layer
3. Implement IndexedDB queue for offlineoperations
4. Enhance merge algorithm
5. Add UI for sync status and recovery
6. Test with multiple devices/scenarios

## Testing Scenarios

- [ ] Add entry online → sync to cloud
- [ ] Add entry offline → add another online → both sync when reconnected
- [ ] Modify same entry on two devices → merge intelligently
- [ ] Delete week on one device, add new on another → merge preserves both
- [ ] Network drops during sync → queue + retry
- [ ] Browser restart while offline → resume sync when online
- [ ] Multiple tabs/windows → sync across tabs
- [ ] OneDrive file manually modified → detect and merge
