---
name: chunkmaster-pro
description: "LLM-agnostic AI agent development skill that instructs any AI model (Claude, GPT-4o, Gemini, Cursor) to prepare documents for RAG pipelines, embeddings, and knowledge bases through five stages: ingest, segment (fixed/semantic/recursive strategies), tag (source, page, section, keywords), export (JSONL/CSV, embeddings-ready), validate - with 256-512 token sizing guidance, 10-20% minimum overlap, and mandatory metadata for retrieval attribution. Use when chunking, tagging, exporting, and indexing documents step-by-step."
---

# Chunkmaster Pro — Document Chunking & Indexing

## Overview
Chunkmaster Pro takes raw documents (PDFs, markdown, text, HTML) and systematically prepares them for RAG pipelines, vector databases, and embedding workflows. It handles chunking strategy, metadata tagging, export formatting, and indexing readiness checks.

## When to Use
- Preparing a corpus for a RAG pipeline (LlamaIndex, LangChain, custom).
- Chunking long documents for embedding into Pinecone, Weaviate, Chroma, or similar.
- Building a knowledge base from a collection of markdown or PDF files.
- Tagging and organizing documents with metadata for semantic search.

## How It Works
The pipeline follows five stages:
1. **Ingest** — Load and normalize the document (extract text, clean encoding).
2. **Segment** — Apply chunking strategy (fixed-size, semantic, recursive, or sentence-aware).
3. **Tag** — Generate metadata per chunk (source, page, section, topics, keywords).
4. **Export** — Format as JSONL, CSV, or direct embeddings-ready arrays.
5. **Validate** — Check chunk overlap, token counts, and metadata completeness.

## Steps
1. **Assess the document.** Identify format, length, structure (headings, tables, code blocks).
2. **Choose chunking strategy.** 
   - Fixed-size (256-1024 tokens): for uniform embedding.
   - Semantic/sentence-aware: for preserving meaning across chunk boundaries.
   - Recursive: for hierarchical docs with nested sections.
3. **Set chunk parameters.** Size, overlap %, separators (newlines, periods, headings).
4. **Run chunking.** Process the document and assign sequential IDs.
5. **Generate metadata.** Source filename, chunk index, section heading, auto-extracted keywords.
6. **Export.** JSONL (preferred for most vector DBs) or CSV. Include embedding-ready text field.
7. **Validate.** Spot-check 3-5 chunks for coherence, token count, and metadata accuracy.

## Common Pitfalls
- **Wrong chunk size.** Too small = lost context. Too large = diluted embeddings. Aim for 256-512 tokens for most general-purpose use.
- **No overlap.** Chunks without overlap can split sentences and break query matching. Minimum 10-20% overlap.
- **Skipping metadata.** Chunks without source/position metadata are nearly useless for retrieval attribution.

## Inputs
- `documents` (list of files, required) - PDFs, markdown, text, HTML
- `strategy` (enum: fixed-size / semantic / recursive / sentence-aware, required)
- `chunk_size` (integer, default: 512) and `overlap_pct` (integer, default: 15) - aim 256-512 tokens, >=10% overlap
- `export_format` (enum: jsonl / csv, default: jsonl)

## Outputs
- Chunked documents with sequential IDs and per-chunk metadata (source, index, section, keywords)
- Export file with an embeddings-ready text field
- Validation report: spot-checks on 3-5 chunks for coherence, token count, metadata accuracy

## Example
Input: a 200-page PDF manual for a Pinecone index.
1. Assess: PDF with headings and tables -> recursive strategy, 512 tokens, 15% overlap.
2. Chunk with sequential IDs; tag each with source filename, page, section heading, keywords.
3. Export JSONL with the embeddings-ready text field.
4. Validate: spot-check 5 chunks for coherence and metadata completeness.
