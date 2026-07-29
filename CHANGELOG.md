# Changelog

## Unreleased

### Added
- Component-builder utilities in src/ir_lab/core for composing retrieval components from declarative configuration.
- Fully working analysis pipeline 
- Structured model packages for documents, queries, executable queries, datasets, experiments, and tokens.
- Indexing and retrieval scaffolding, including indexer abstractions and parser/retriever interfaces.
- An evaluation package skeleton for future metrics and benchmarking work.
- fully working incidence matrix

### Changed
- Reworked the project around a more explicit IR pipeline architecture with separate packages for analysis, indexing, ingestion, retrieval, and evaluation.
- Moved analysis-related functionality out of the older processing-oriented layout and into the current analyzing package.
- Refreshed the README to describe the current architecture and the evolution from earlier toy-oriented versions.
- Updated the package layout to better reflect the experiment-driven, modular structure used by the current codebase.

### Removed
- Older toy-oriented processing assumptions and legacy experiment placeholders that no longer match the current structure.
