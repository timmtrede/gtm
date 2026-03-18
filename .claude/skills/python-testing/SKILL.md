# Python Testing with pytest

## Structure
```
tests/
├── conftest.py          # Shared fixtures
├── test_client.py       # Client tests (mocked API)
├── test_operations/     # Operation tests
│   ├── test_tags.py
│   ├── test_triggers.py
│   └── ...
└── test_cli.py          # CLI integration tests
```

## Patterns
- Use `pytest` fixtures for shared setup
- Mock external API calls with `unittest.mock.patch`
- Test Pydantic models with known good/bad data
- Use `typer.testing.CliRunner` for CLI tests

## Running
```bash
pytest                    # All tests
pytest tests/test_cli.py  # Specific file
pytest -k "test_list"     # By name pattern
pytest -v                 # Verbose output
```
