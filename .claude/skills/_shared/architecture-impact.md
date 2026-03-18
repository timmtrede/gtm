# Architecture Impact — GTM Dependency Model

When making changes to GTM resources, consider the dependency chain:

## Dependency Graph
```
Variables → Triggers → Tags → Versions
```

- **Variables** are referenced by triggers and tags
- **Triggers** fire or block tags
- **Tags** are grouped into versions
- **Versions** are published to make changes live

## Impact Analysis
Before modifying or deleting a resource:
1. Check if any tags reference the trigger being modified
2. Check if any triggers or tags reference the variable being modified
3. Changing a trigger condition affects all tags that use it
4. Deleting a variable may break tags or triggers that reference it

## Safe Change Order
1. Create new resources first (variables → triggers → tags)
2. Update references to point to new resources
3. Remove old resources only after all references are updated
4. Create a version and diff before publishing
