# Changelog

## Unreleased

### Added
- Dataset abstractions for configuration and storage, including Dataset, DatasetConfig, and DatasetStore.
- Initial experiment runner and experiment model scaffolding under src/core.
- A dedicated experiments/ directory for experiment-related assets and configuration.
- Exported `AnalyzedDocument` from `src/models/documents/__init__.py` for cleaner document model imports.

### Changed
- Refreshed the project documentation to reflect the new dataset and experiment workflow.
- Reorganized the experiment-related layout around loader utilities and core model abstractions.
- Updated README to include analyzed document support in the current state summary.

### Removed
- Legacy toy adapter, toy reader, and toy inverted-index experiment configuration files that are no longer used by the current structure
