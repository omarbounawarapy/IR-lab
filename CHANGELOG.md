# Changelog

## Unreleased

### Added
- Boolean RPN query support through a new executable query type and transformer.
- A retrieval abstraction layer and a binary retriever entry point for query-driven retrieval.
- Experiment configuration updates for toy inverted-index comparisons using the boolean RPN transformer.

### Changed
- Refactored query-processing modules to separate query abstractions from executable query implementations.
- Updated the retrieval and processing layout to better reflect the current boolean retrieval workflow.
- Adjusted the repository documentation to describe the new architecture and workflow.

### Removed
- Older retriever scaffolding that was superseded by the new retrieval abstractions.
