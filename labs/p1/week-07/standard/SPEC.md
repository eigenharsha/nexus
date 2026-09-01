# `standard` — LAB-P1-W07

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 6-7 h

## Acceptance criteria

- Full normalized schema: users, products, inventory, carts, cart_items, orders, order_items,
  payments, refunds, reviews. Third normal form, with the denormalizations you chose documented
  and justified.
- Every foreign key declared, every `NOT NULL` deliberate, `CHECK` constraints on money and
  quantity, and a partial unique index enforcing one active cart per user.
- `seed.py` generates 1M rows with realistic skew: an 80/20 product popularity distribution and a
  purchase-count distribution that is not uniform.
- 20 analytical queries in `queries/`, each with its `EXPLAIN ANALYZE` output committed, including:
  cohort retention by signup month, top-N products per category (window function), refund rate by
  cohort, and a running 7-day revenue total.
- Money is `NUMERIC`, never `FLOAT`. The test checks the column types.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

The top-N-per-group query is the one that separates people. `ROW_NUMBER() OVER (PARTITION BY
category ORDER BY revenue DESC)` in a subquery, filtered outside. If you find yourself writing a
correlated subquery per category, stop and read the window-function section again.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
