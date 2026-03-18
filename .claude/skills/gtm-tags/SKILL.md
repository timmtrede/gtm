# GTM Tag Types Reference

## Common Tag Types

| Type ID | Description | Use Case |
|---------|-------------|----------|
| `gaawc` | GA4 Configuration | Base GA4 config tag |
| `gaawe` | GA4 Event | Custom GA4 events |
| `gclidw` | Google Ads Conversion | Conversion tracking |
| `awct` | Google Ads Remarketing | Remarketing audiences |
| `html` | Custom HTML | Custom scripts, pixels |
| `img` | Custom Image | Pixel tracking |
| `flc` | Floodlight Counter | DCM tracking |
| `fls` | Floodlight Sales | DCM sales tracking |

## GA4 Event Tag Parameters
Key parameters for `gaawe` tags:
- `measurementId` — GA4 measurement ID (or reference to config tag)
- `eventName` — event name
- `eventParameters` — list of {name, value} pairs
- `userProperties` — list of {name, value} pairs

## Consent Mode
Tags that fire pixels or load external scripts should have consent settings:
- `consentSettings.consentStatus` — "needed" or "notNeeded"
- Consent types: `ad_storage`, `analytics_storage`, `functionality_storage`, `personalization_storage`, `security_storage`

## Best Practices
- Use a single GA4 Configuration tag per measurement ID
- GA4 Event tags should reference the config tag, not hardcode the measurement ID
- Custom HTML tags should be minimized — prefer built-in tag types
- All marketing/analytics tags should require consent
