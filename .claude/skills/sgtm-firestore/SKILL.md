# sGTM Firestore Integration Reference

## How sGTM Uses Firestore

Server-side GTM has native Firestore API support with four core functions:
- `Firestore.read(path)` — read a single document
- `Firestore.write(path, data)` — write/merge data to a document
- `Firestore.query(collection, conditions)` — query documents
- `Firestore.runTransaction(fn)` — atomic read-then-write

Only **Firestore in Native mode** is supported (not Datastore mode).

## Integration Patterns

### 1. Event Journaling
sGTM writes every event to Firestore for raw data capture.
- **Collection**: `zipmend`
- **Key fields**: `event_name`, `user_id`, `transaction_id`, `value`, `items`
- **Use case**: Raw event backup, debugging, cross-referencing with BQ

### 2. Customer Lookup
sGTM checks if a user is an existing customer to enrich events.
- **Collection**: `existing_customers`
- **Key**: `user_id`
- **Use case**: New vs returning customer segmentation for Google Ads bidding

### 3. Lead Scoring
sGTM looks up company scores by domain to enrich conversion events.
- **Collection**: `scores`
- **Key**: domain name (document ID)
- **Use case**: B2B lead quality scoring, conversion value adjustment

### 4. Domain Filtering
sGTM checks if an email domain is generic (gmail, etc.) vs corporate.
- **Collection**: `generic_domains`
- **Key**: domain name (document ID)
- **Use case**: B2B lead filtering, distinguishing business vs personal signups

### 5. Duplicate Transaction Blocking
Check `transaction_id` in Firestore before forwarding purchase events.
- Prevents duplicate conversion tracking
- Pattern: read → if exists, block; if not, write and forward

### 6. User Stitching
Map anonymous `client_id` to known `user_id` on login events.
- Store in Firestore, read back on subsequent anonymous visits
- Replaces browser-side approaches degraded by cookie restrictions

### 7. COGS/Profit Enrichment (Soteria Pattern)
Look up item-level COGS from Firestore, compute profit server-side.
- Send profit as conversion value to Google Ads (browser never sees margin data)

## Known sGTM Templates

### Built-in
- **Firestore Lookup Variable** — query Firestore, return a field value

### Google Pantheon (gps-sgtm-pantheon)
- **Artemis** — full document lookup for audience segmentation
- **Soteria** — COGS/profit calculation from Firestore

### Stape
- **Firestore Writer Tag** — write event data to Firestore
- **Firestore ReStore Variable** — read docs by user identifier
- **Firestore Request Delay Tag** — batch/delay event processing

## Zipmend Firestore Collections

| Collection | Docs | Updated By | Read By |
|---|---|---|---|
| `zipmend` | ~240k | sGTM (every event) | Analytics, debugging |
| `existing_customers` | ~68k | Backend/sGTM | sGTM (customer lookup) |
| `scores` | ~23k | ML pipeline / manual | sGTM (lead enrichment) |
| `generic_domains` | ~9k | Manual curation | sGTM (domain filtering) |

## Data Flow
```
Browser → Client-side GTM → sGTM Server Container
                                    ↓
                           Firestore (read/write)
                                    ↓
                        GA4 / Google Ads / Meta CAPI / BQ
```
