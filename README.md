# Information Retrieval Lab

This repository is an educational and experimental laboratory for studying Information Retrieval concepts through small, modular implementations. It is currently focused on establishing the foundations of an experiment-driven IR framework rather than delivering a complete retrieval system.

## Purpose

The project is intended for learning and prototyping:

- core IR abstractions such as documents, queries, datasets, and retrievers
- indexing and retrieval components that can be tested independently
- experiment configurations and evaluation hooks for comparing approaches

## Current Architecture

The codebase is organized around a small set of Python modules:

- src/core: shared data models and abstractions
- src/io: readers, adapters, and parsers for ingesting datasets
- src/processing: text processing pipeline components
- src/indexers: index construction logic, including an inverted indexer scaffold
- src/retrieval: retrieval implementations and retrieval-model stubs
- src/experiment: experiment configuration and runner entry points
- src/evaluation: evaluation utilities and metrics hooks

## Project Structure

```text
.
├── datasets/        # corpora and sample datasets
├── docs/            # notes and technical write-ups
├── scripts/         # dataset download helpers
├── src/             # implementation modules
└── README.md
```

## Design Philosophy

The project favors:

- modularity over monolithic implementations
- extensibility for adding new models and experiments
- experiment-driven development over premature optimization

## Current State

The repository currently contains initial scaffolding for:

- toy dataset loading and adaptation
- a document and dataset model layer
- an inverted indexer prototype
- a linguistic processing pipeline
- retrieval module placeholders and experiment configuration directories

## Roadmap

Planned work includes:

- Boolean retrieval
- positional and inverted index extensions
- TF-IDF and vector-space retrieval
- BM25 and other ranking models
- evaluation pipelines and benchmark comparisons
