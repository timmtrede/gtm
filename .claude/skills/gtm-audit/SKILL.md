# GTM Audit Checklist

## Naming Conventions
- [ ] No leading/trailing whitespace in names
- [ ] Consistent naming pattern across resource types
- [ ] No special characters (<, >, ", ')
- [ ] Names under 100 characters
- [ ] Descriptive names (not "Tag 1", "Trigger copy")

## Resource Health
- [ ] No unused triggers (not referenced by any tag)
- [ ] No duplicate resource names
- [ ] No paused tags that should be cleaned up
- [ ] All tags have at least one firing trigger
- [ ] No orphaned variables (not used by any tag/trigger)

## Consent Compliance
- [ ] Marketing tags require ad_storage consent
- [ ] Analytics tags require analytics_storage consent
- [ ] Essential-only tags marked as not needing consent
- [ ] Custom HTML tags reviewed for consent requirements

## Performance
- [ ] Minimize Custom HTML tags
- [ ] No unnecessary "All Pages" triggers on non-essential tags
- [ ] Tags use appropriate firing priority where needed
- [ ] No redundant tags (same function, different names)

## Security
- [ ] Custom HTML tags reviewed for XSS risks
- [ ] No hardcoded credentials in tag parameters
- [ ] Third-party scripts loaded from trusted domains only
