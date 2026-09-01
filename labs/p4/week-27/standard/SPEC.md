# `standard` — LAB-P4-W27

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 8-10 h

## Acceptance criteria

- Ingest 1,000 real PDFs with robust parsing: multi-column layouts, tables, scanned pages
  (report what fraction failed and why — a parser that silently returns empty text is the failure
  mode here).
- A chunking strategy chosen and justified, with at least three alternatives evaluated
  (fixed-size, recursive, semantic) on the eval set.
- An embedding model chosen by measurement, with at least two compared.
- pgvector with an HNSW index, `m` and `ef_construction` tuned, and `ef_search` swept at query time.
- Metadata filtering (by document type and date) that is correct — the test checks that filtered
  search does not silently drop results that should match.
- A 100-query evaluation set with judged relevance.
- A full ablation report: Recall@1/5/10 and NDCG@10 for every configuration.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

Build the eval set before the index. Twenty queries you wrote by reading the documents beat
100 generated ones, and the number you will care about six weeks from now is whether Week 28's
re-ranker improved anything — which you cannot know without this.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
