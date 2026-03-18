# GTM Version Workflow

## Version Lifecycle
1. **Workspace** — make changes in a named workspace (not Default)
2. **Review** — diff workspace changes against live version
3. **Create Version** — snapshot the workspace into a version
4. **Backup** — export current live version before publishing
5. **Publish** — make the new version live
6. **Verify** — check the live version matches expectations

## Rollback Procedure
If a published version causes issues:
1. List versions: `gtm versions list --container <id>`
2. Identify the previous good version
3. Publish it: this makes the old version live again
4. Investigate what went wrong in the problematic version

## Diff Interpretation
The version diff shows:
- **Added** — new resources in version B not in version A
- **Removed** — resources in version A not in version B
- **Modified** — resources present in both but with different configuration

## Backup Strategy
- Backups are stored in `backups/{container_id}/{date}_v{version}.json`
- Git-tracked for full history
- Run `gtm backup --container <id>` before any publish
- Weekly automated backups via GitHub Actions

## Best Practices
- One logical change per version (don't batch unrelated changes)
- Use descriptive version names and notes
- Always diff before publishing
- Keep a rollback plan for every publish
