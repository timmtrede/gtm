# GTM API v2 Reference

## Base URL
`https://tagmanager.googleapis.com/tagmanager/v2`

## Authentication
Application Default Credentials (ADC) with scopes:
- `tagmanager.readonly` — read operations
- `tagmanager.edit.containers` — create/update/delete tags, triggers, variables
- `tagmanager.edit.containerversions` — create versions
- `tagmanager.publish` — publish versions

## Resource Paths
```
accounts/{accountId}
accounts/{accountId}/containers/{containerId}
accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}
accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/tags/{tagId}
accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/triggers/{triggerId}
accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/variables/{variableId}
accounts/{accountId}/containers/{containerId}/versions/{versionId}
```

## Rate Limits
- 50 requests per second per project
- Use exponential backoff on 429 responses
- The client wrapper handles retry automatically

## Key Endpoints
| Operation | Method | Path |
|-----------|--------|------|
| List containers | GET | accounts/{id}/containers |
| List tags | GET | .../workspaces/{id}/tags |
| Create tag | POST | .../workspaces/{id}/tags |
| Update tag | PUT | .../workspaces/{id}/tags/{id} |
| Delete tag | DELETE | .../workspaces/{id}/tags/{id} |
| Create version | POST | .../workspaces/{id}:create_version |
| Publish version | POST | .../versions/{id}:publish |
| Get live version | GET | .../versions/0:live |
