W = "curriculum/p3/week-20/"
PAGES = {
W+"1-numerical-categorical-features.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Why “London” breaks a model** — and the three ways to fix it
  - **Watch a scale ruin a distance** — in a moving picture
  - **The category with 5,000 values** — what everyone tries, and what works
  - **Transform real columns** — and see the score move
</Card>''',
 story='''{/* TERM LADDER: feature → scaling → one-hot encoding → cardinality → target encoding */}

### The model that cannot read "London"

Everything so far assumed your data arrived as tidy numbers. Real data does not. It arrives as
this:

| customer | city | age | salary |
| --- | --- | --- | --- |
| 1 | London | 34 | 52,000 |

A model multiplies numbers. It cannot multiply *London*. So somebody has to turn that word into
numbers — and the obvious idea, numbering the cities 1, 2, 3, is quietly a disaster: it tells
the model that Birmingham (2) sits exactly halfway between London (1) and Cardiff (3), which is
nonsense it will faithfully learn.

Then look at `age` and `salary`. One runs 18–90; the other runs 20,000–200,000. Any model that
measures distance now thinks salary is a thousand times more important than age — not because it
is, but because of the units somebody happened to record it in.

{/* ANIM:W20M1 */}

This page is the two fixes — putting columns on a comparable scale, and turning categories into
numbers honestly — plus the case that defeats the textbook answer: a column with five thousand
different values.
''',
 answer='''A model cannot multiply "London", and numbering cities 1, 2, 3 **invents an ordering that does
    not exist** — so low-cardinality categories become one column each (one-hot). Scaling matters
    for the same reason in reverse: age 18–90 and salary 20,000–200,000 are not comparable, so
    any distance-based model silently ranks salary a thousand times more important, purely
    because of its units. And the case textbooks skip — five thousand categories — needs target
    or hashed encoding, fitted inside the pipeline so it cannot leak.''',
 dangler='''
### The question this page leaves open

Numbers and categories are the easy columns. The hard ones are the columns that are not really
columns at all: a **timestamp**, which contains a dozen facts (hour, weekday, holiday, how long
since the last order), and a **paragraph of text**, which contains everything and nothing.

Squeezing information out of those is where feature engineering earns its reputation:
[Module 2 — Temporal, text & interaction features](/curriculum/p3/week-20/2-temporal-text-interaction-features).
''',
 build_open='''Most model improvements in a real project come from this layer, not from the model. It is also
    where leakage sneaks in through a scaler fitted at the wrong moment.''',
 edge_open='''Encoding schemes under high cardinality, and what they cost in memory and in leakage risk.'''),

W+"2-temporal-text-interaction-features.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **One timestamp, a dozen facts** — the column that is really twelve
  - **Watch a date unpack** — in a moving picture
  - **Text without a language model** — the cheap tricks that still work
  - **The pair that only matters together** — interaction features
</Card>''',
 story='''{/* TERM LADDER: temporal feature → cyclical encoding → bag of words → TF-IDF → interaction */}

### The column that is really twelve

Here is a single value: `2026-09-04 23:41`.

To a model, that is one meaningless big number. To you, it is a dozen facts — a Friday, nearly
midnight, the first week of September, four days after payday, ninety minutes since this
customer's last order, and a fortnight before their subscription renews. Every one of those
could matter, and every one is invisible until somebody digs it out.

{/* ANIM:W20M2 */}

Two twists this page will not let you miss. First, hours are a **circle**: hour 23 and hour 0
are adjacent, but as plain numbers they look maximally far apart — which is why time needs a
special encoding. Second, **text**: you will meet a paragraph long before you meet a language
model, and the old bag-of-words tricks still carry a surprising amount of a real project.

And then the idea that closes the page: sometimes neither of two columns matters alone, and
their *combination* is the whole signal. Price is fine. Income is fine. Price *relative to*
income is the model.
''',
 answer='''A timestamp is **a dozen facts wearing one column** — weekday, hour, holiday, days since the
    last event, days until the next one — and a model sees none of them until you dig them out.
    Time is also circular, so hour 23 must sit next to hour 0 rather than maximally far from it.
    Text becomes usable with counts and TF-IDF long before you need a language model. And some
    signals exist only in combination: price alone means little, price relative to income is the
    whole story.''',
 dangler='''
### The question this page leaves open

You are now very good at making features — which creates the opposite problem. Four hundred
columns later, some are duplicates, many are noise, and a few are actively harming the model
while making every run slower and every explanation harder.

Choosing which features to keep, with evidence rather than taste, is
[Module 3 — Feature selection & dimensionality](/curriculum/p3/week-20/3-feature-selection-dimensionality).
''',
 build_open='''The features in this layer are the ones that move a real project's metrics, and the ones most
    likely to leak. Both halves matter.''',
 edge_open='''Where handcrafted features still beat learned ones, and the maintenance cost of every one you
    add.'''),

W+"3-feature-selection-dimensionality.mdx": dict(
 glimpse='''<Card title="In this chapter — about 20 minutes" icon="sparkles">
  - **Four hundred columns, forty that matter** — and how to tell which
  - **The feature that looks important and is not** — correlation's favourite trick
  - **Three honest selection methods** — and the one everyone misuses
  - **Cut your feature set in half** — and keep the score
</Card>''',
 story='''{/* TERM LADDER: feature selection → filter → wrapper → importance → multicollinearity */}

### Four hundred columns

Feature engineering is enjoyable, and that is the problem. A month in, your table has four
hundred columns: every rolling average, every ratio, every flag anyone thought of.

More is not better here. Redundant columns make the model slower, harder to explain, more
expensive to serve, and — the part that surprises people — sometimes *worse*, because noise
columns give an overfitting model more ways to memorise.

So which forty matter? The tempting shortcut is to ask the model, and it will happily hand you
an importance ranking. But that ranking has a well-known trick in it: give it two nearly
identical columns and it splits the credit between them, making both look unimportant — so you
delete both, and lose the signal entirely.

This page is the honest methods: cheap statistical filters, model-based importance read
properly, and the one that actually answers the question you are asking — remove the column and
measure whether performance drops.
''',
 answer='''You find the columns that matter by **removing them and measuring**, not by trusting a single
    importance ranking. Cheap filters (variance, correlation with the target) prune obvious junk;
    model importances are useful but have a famous failure — two nearly identical columns split
    the credit and both look worthless, so deleting both loses the signal. Redundant features are
    not free: they slow serving, blur explanations, and give an overfitting model more ways to
    memorise noise.''',
 dangler='''
### The question this page leaves open

Your features are clean, informative, and few. Now look at your target column and count: **0.3%
positives.** Three fraud cases in a thousand. Two failures in a factory-year.

You already know accuracy is useless here (Week 19). What Week 19 did not cover is what to *do*
about it — and most of the popular advice makes things quietly worse. That is
[Module 4 — Imbalanced classification](/curriculum/p3/week-20/4-imbalanced-classification).
''',
 build_open='''Every feature you keep is a thing you must compute, serve and maintain forever. This layer is
    how to justify keeping it.''',
 edge_open='''Permutation importance done correctly, correlated-feature effects, and what SHAP does and
    does not tell you.'''),

W+"4-imbalanced-classification.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Three positives in a thousand rows** — the shape of most valuable problems
  - **Watch resampling help and hurt** — in a moving picture
  - **The advice that quietly breaks your probabilities** — and when to ignore it
  - **The threshold does most of the work** — and it is free
</Card>''',
 story='''{/* TERM LADDER: class imbalance → resampling → SMOTE → class weight → threshold tuning */}

### Three in a thousand

The problems worth solving are almost always rare. Fraud. Equipment failure. The tumour. The
customer about to leave. If the interesting thing happened half the time, you would not need a
model.

So your data has three positives per thousand rows, and everything you learned in Week 17 starts
to wobble: the model can score brilliantly by ignoring the rare class entirely, and its training
signal is drowned out by the 997 boring rows.

{/* ANIM:W20M4 */}

The internet's first suggestion is to rebalance the data — duplicate the rare rows, or invent
synthetic ones (SMOTE). Sometimes that helps. But here is what those tutorials rarely mention:
**resampling breaks your probabilities.** After oversampling, a model that outputs "0.8" no
longer means 80% — you changed the base rate, so every calibrated decision downstream is now
wrong.

Which is why this page's punchline is unglamorous and true: most of the value comes from
class weights and from **moving the decision threshold** — a change that costs nothing, breaks
nothing, and is where practitioners find the win.
''',
 answer='''Rare positives break naive training because **the model can score brilliantly by ignoring them**
    and its learning signal is drowned by the majority. Resampling and SMOTE can help, but they
    change the base rate and therefore **break calibration** — a "0.8" no longer means 80%, so
    every downstream cost calculation is wrong. The reliable moves are class weights (which
    change the loss, not the data) and tuning the decision threshold, which is free, breaks
    nothing, and usually recovers most of the available gain.''',
 dangler='''
### The question this page leaves open

Your features are good and your rare class is handled — in a notebook, on a snapshot of data
someone exported last Tuesday.

Production is different. Features must be computed the *same way* at training and serving time,
from data that keeps moving, without accidentally using values that did not exist yet. Making
that survive contact with reality is
[Module 5 — Production feature pipelines](/curriculum/p3/week-20/5-production-feature-pipelines).
''',
 build_open='''Imbalanced problems are most of the valuable ones, and most of the advice about them is a
    decade out of date. This layer is what actually works.''',
 edge_open='''Why SMOTE's synthetic points are questionable in high dimensions, and what cost-sensitive
    learning does instead.'''),

W+"5-production-feature-pipelines.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The bug that only exists in production** — training and serving disagreeing
  - **Watch a feature drift apart** — in a moving picture
  - **Compute it once, use it twice** — the pattern behind feature stores
  - **Ship features you can trust** — and monitor them like code
</Card>''',
 story='''{/* TERM LADDER: training/serving skew → feature store → point-in-time correctness → drift → monitoring */}

### The same feature, computed twice

Your model works in the notebook and misbehaves in production, and the postmortem finds
something small and awful.

In training, `average_order_value` was computed in pandas over the customer's whole history. In
production, an engineer reimplemented it in the service — subtly differently: they included
cancelled orders. Two functions with the same name, two different meanings, and a model being
fed a number it has never seen the like of.

That is **training/serving skew**, and it is the most common way good models die quietly.

{/* ANIM:W20M5 */}

The cure is a rule rather than a tool: **compute each feature in exactly one place, and use that
same code for both training and serving.** Then the second rule, which is subtler — when
building training rows, every feature must be computed *as of* the moment of the event, using
only data that existed then. Break that and you have reinvented Week 19's leakage in a
distributed system, where it is much harder to see.

And then features need what code needs: tests, versions and monitoring — because a feature can
silently change meaning when an upstream team edits a column, and nothing will fail.
''',
 answer='''Good models die quietly from **training/serving skew** — the same feature computed by two
    different pieces of code that disagree. The rule that fixes it: compute each feature once, in
    one place, and use that identical code in both training and serving. The subtler rule is
    point-in-time correctness: every training row's features must be computed using only data
    that existed at that moment, or you have rebuilt Week 19's leakage inside a distributed
    system. And features need monitoring, because an upstream column can change meaning without
    anything failing.''',
 dangler='''
### The question this page leaves open

Phase 3 has taught you the classical craft: models, honest evaluation, features that survive
production. All of it assumes something you have not questioned — that *you* decide what the
features are.

But how do you engineer features for a photograph? For a sound? For a sentence? At some point
the hand-crafting stops, and the machine has to learn the representation itself. That is where
Week 21 begins: [Week 21 — Neural networks & PyTorch](/curriculum/p3/week-21/index).
''',
 build_open='''This layer is the difference between a model that works in a notebook and one that works on
    Wednesday afternoon in production.''',
 edge_open='''Point-in-time joins, feature stores and the operational cost of every feature you promise to
    keep alive.'''),
}
