<p align="center">
  <img src="./assets/banner.png" width="100%">
</p>

<h1 align="center">IR Lab</h1>

<p align="center">
  Experimental Information Retrieval Systems & Algorithms
</p>

This repository is an educational and experimental lab for studying information retrieval concepts through small, modular Python implementations. The current focus is on building reusable abstractions for datasets, experiments, documents, queries, indexes, and text-processing pipelines rather than shipping a complete production retrieval system.

## Purpose

The project is intended for learning and prototyping:

- core IR abstractions such as documents, datasets, queries, and retrievers
- index and query-processing components that can be tested independently
- experiment scaffolding for defining datasets and running retrieval experiments

## Current Architecture

The codebase is organized around a small set of Python modules:

- src/core/models: shared data models, dataset abstractions, and experiment definitions
- src/loaders: dataset loading utilities and storage adapters
- src/processing: processing pipeline components and query transformation modules
- experiments/: experiment configurations and run entry points

## Project Structure

```text
.
├── experiments/               # experiment configurations and runner assets
├── src/                       # implementation modules
│   ├── core/models/           # document, query, index, dataset, and experiment abstractions
│   ├── loaders/               # dataset loading helpers
│   └── processing/            # linguistic and query transformation pipelines
└── README.md
```

## Recent Changes

The repository has recently evolved around a more explicit experiment workflow:

- introduced dataset abstractions including Dataset, DatasetConfig, and DatasetStore
- added experiment runner and experiment model scaffolding for organizing retrieval runs
- moved experiment-related assets under a dedicated experiments/ directory
- removed older toy adapter, toy reader, and legacy toy experiment configuration files that are no longer part of the current layout

## Design Philosophy

The project favors:

- modularity over monolithic implementations
- extensibility for adding new models and experiments
- experiment-driven development over premature optimization

## Current State

The repository currently contains:

- document and dataset model abstractions
- experiment model and runner scaffolding
- query and executable-query representations, including boolean AST and boolean RPN variants
- basic loader utilities and a foundation for future evaluation work

## Roadmap

Planned work includes:

- boolean retrieval support
- inverted and positional index extensions
- TF-IDF and vector-space retrieval
- BM25 and other ranking models
- evaluation pipelines and benchmark comparisons
