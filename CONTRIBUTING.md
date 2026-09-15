# Contributing to IR Lab

IR Lab is a small, currently solo-maintained project (more people may join to work
on specific parts over time). Contributions that fit its scope -- new retrieval
models, analysis components, evaluation metrics, or dataset loaders -- are welcome.

By participating, you're expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
For security issues, see [SECURITY.md](SECURITY.md) instead of opening a public issue.

## Getting set up

```bash
git clone https://github.com/omarbounawarapy/IR-lab.git
cd IR-lab
pip install -e ".[dev]"
pytest
```

## Making a change

1. Open an issue first for anything non-trivial (new retrieval model, new metric,
   architectural change), so the approach can be agreed on before you write code.
2. Keep changes scoped: one feature or fix per pull request.
3. Add or update tests for any behavior change. The test suite is organized by
   capability area (`tests/test_*.py`), each covering a stage of the framework's
   capabilities -- add new tests to the file that matches what you're changing, or
   a new file if it doesn't fit an existing one.
4. Update `CHANGELOG.md` under `## Unreleased`.
5. Run `pytest` locally before opening the PR.

## Code style

- Match the existing module structure (`analyzing/`, `indexing/`, `processing/`,
  `evaluation/`, `persistence/`, `core/`, `models/`) -- new components belong next to
  their closest existing counterpart.
- Prefer small, composable classes over large ones, consistent with the rest of the
  codebase.

## Questions

Open an issue -- there's no separate chat/forum for this project.
