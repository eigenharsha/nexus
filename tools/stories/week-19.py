W = "curriculum/p3/week-19/"
PAGES = {
W+"1-classification-metrics.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The 99% accurate model that is worthless** — a real, common trap
  - **Watch accuracy lie** — in a moving picture
  - **Precision and recall** — the two questions that actually matter
  - **Choose the metric before you model** — because it decides everything after
</Card>''',
 story='''{/* TERM LADDER: confusion matrix → true positive → precision → recall → F1 */}

### The 99% that means nothing

Build a fraud detector. Report back proudly: **99.1% accurate.**

Now the awkward question. Roughly one transaction in a hundred is fraudulent — so a model that
simply answers *"not fraud"* to everything, always, with no intelligence whatsoever, also scores
99%. Yours may have learned nothing at all. The number cannot tell you.

{/* ANIM:W19M1 */}

This is the most common way a model gets shipped and quietly fails, and the fix is to stop
asking "how often is it right?" and start asking the two questions a person actually cares
about:

- **Of the things it flagged, how many were really fraud?** That is **precision** — and low
  precision means angry innocent customers.
- **Of the real frauds, how many did it catch?** That is **recall** — and low recall means money
  walking out of the door.

Those two pull against each other, always. Which one you favour is not a modelling decision; it
is a decision about whose pain matters more — and this page is how to make it deliberately.
''',
 answer='''Accuracy lies whenever one class is rare: **"always say no" scores 99% on a 1-in-100 problem
    and has learned nothing.** The honest questions are precision (of what you flagged, how much
    was real — the false-alarm cost) and recall (of what was real, how much you caught — the
    missed-fraud cost). They trade against each other by construction, so the metric you optimise
    is a statement about which mistake your business can afford, chosen before you model rather
    than after.''',
 dangler='''
### The question this page leaves open

Precision and recall are for yes-or-no answers. Plenty of models do not answer yes or no — they
predict a *number* (tomorrow's demand), a *ranking* (which ten results to show), or a
*probability* you intend to act on.

Each of those is graded differently, and using the wrong measure is how teams congratulate
themselves on nothing. That is
[Module 2 — Regression, ranking & probabilistic metrics](/curriculum/p3/week-19/2-regression-ranking-probabilistic-metrics).
''',
 build_open='''"The model is 94% accurate" is a sentence that should trigger a follow-up question in every
    review. This layer gives you the question and the vocabulary to insist on an answer.''',
 edge_open='''Metric choice under class imbalance, threshold-free measures, and what AUC does and does not
    promise.'''),

W+"2-regression-ranking-probabilistic-metrics.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Being wrong by £5 versus being wrong by £5,000** — which loss you pick decides
  - **Ranking is graded at the top** — nobody scrolls to result 40
  - **Is 70% confidence really 70%?** — calibration, and why it pays your rent
  - **Pick the right measure for the job** — and say why
</Card>''',
 story='''{/* TERM LADDER: MAE → RMSE → NDCG → calibration → Brier score */}

### Three jobs, three yardsticks

A model that predicts a number, a model that ranks a list, and a model that states a
probability, cannot possibly be graded the same way.

**Predicting a number.** Your delivery-time model is wrong by five minutes on a thousand orders
and wrong by four hours on one. Should that one disaster dominate the score? If a four-hour
delay costs you a customer, then yes — use a measure that squares the errors. If all errors are
merely annoying, no — use one that treats them evenly. The choice *is* the business.

**Ranking a list.** A search model puts the right answer at position 40. It is technically
"correct" and practically useless, because nobody scrolls that far. Ranking measures deliberately
weight the top of the list heavily and the tail barely at all.

**Stating a probability.** The subtlest of the three. When your model says *70% likely to
churn*, are 70 out of every 100 such customers actually leaving? If not, the number is a mood,
not a probability — and every decision that multiplies it by a cost is wrong.
''',
 answer='''Three jobs need three yardsticks. **Numbers**: squaring the errors makes one large mistake
    dominate — the right choice when a big miss is disproportionately expensive, the wrong one
    when it is merely annoying. **Rankings**: measures weight the top of the list, because nobody
    scrolls to position 40. **Probabilities**: calibration asks whether "70%" happens 70% of the
    time — and an uncalibrated probability breaks every downstream decision that multiplies it by
    a cost, no matter how good the ranking looks.''',
 dangler='''
### The question this page leaves open

You now have a metric that fits the job. But you compute it on *some* data — and if you compute
it on the data the model trained on, you already know it will lie.

So which data? Split once? Split five ways? What if your data is a time series, or has multiple
rows per customer? Getting this wrong invalidates every number, and it is
[Module 3 — Validation strategy](/curriculum/p3/week-19/3-validation-strategy).
''',
 build_open='''Picking RMSE over MAE quietly changes what your model optimises for. This layer makes that
    choice deliberate rather than default.''',
 edge_open='''Proper scoring rules, why calibration and discrimination are different virtues, and when to
    fix which.'''),

W+"3-validation-strategy.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Which data gets to grade you** — and why it must never be the training data
  - **Watch cross-validation rotate** — every row gets a turn, in a moving picture
  - **When a random split is a lie** — time, groups and the mistakes they cause
  - **Build a split you can defend** — for your data, not a textbook's
</Card>''',
 story='''{/* TERM LADDER: train/test split → validation set → cross-validation → fold → stratification */}

### Marking your own exam

No school lets students write their own exam and mark it. The reason is not distrust; it is that
the score would mean nothing.

Yet that is exactly what happens when a model is graded on the data it learned from. So you hold
some data back — the model never sees it during training — and grade on that.

One split leaves you nervous, though: what if the held-out slice happened to be easy? So you do
it five times, each time holding out a different fifth, and average. Every row gets a turn as
the exam. That is **cross-validation**, and it is the default for a reason.

{/* ANIM:W19M3 */}

Then the part that separates people who have shipped from people who have not. A *random* split
is only honest if your rows are genuinely independent — and often they are not. Split a time
series randomly and you train on next week to predict last week. Split hospital data randomly
and the same patient appears in both halves. In both cases your score is beautiful and your
model is a fiction.
''',
 answer='''You are graded on data the model has never seen, because a score on training data measures
    memorisation. Cross-validation makes that robust by rotating the held-out fold so every row
    is examined once and the score is averaged. But a *random* split is only valid when rows are
    independent: with time series you must split by time (never train on the future), and with
    repeated subjects you must split by group, or the same person sits on both sides of the exam
    and the number is fiction.''',
 dangler='''
### The question this page leaves open

Even with a perfect split, there is a failure that walks straight past it — and it is the one
most likely to damage your career.

It happens when information about the answer sneaks into your features: a column recorded after
the event, a scaler fitted before the split, an ID that encodes the outcome. Your validation is
clean and your score is still a lie. That is
[Module 4 — Data leakage](/curriculum/p3/week-19/4-data-leakage-the-career-defining-failure-mode).
''',
 build_open='''Most disagreements about a model's quality are really disagreements about its split. This
    layer is how to build one nobody can pick apart.''',
 edge_open='''Nested cross-validation, why tuning on your test set silently invalidates it, and how much
    the variance of a split really matters.'''),

W+"4-data-leakage-the-career-defining-failure-mode.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The 0.99 AUC that ends careers** — how it happens, exactly
  - **Watch the answer leak into a feature** — in a moving picture
  - **The five leaks that catch everyone** — including the two you have already made
  - **Build the habit that prevents it** — before you need it
</Card>''',
 story='''{/* TERM LADDER: leakage → target leakage → train-test contamination → temporal leakage → pipeline */}

### The number too good to be true

You build a model to predict which customers will cancel. It scores **0.99**. You have never
seen a score like it. You present it on Thursday.

In production it is worthless, and the postmortem finds the cause in one column:
`cancellation_reason`. It is empty for everyone who stayed and filled in for everyone who left.
The model did not predict cancellations; it read the answer off the back of the card.

That is **leakage**: information about the outcome present in your features that will not exist
when you actually need a prediction. It does not trip your validation — the split was fine, the
metric was right — because the answer was inside the features all along.

{/* ANIM:W19M4 */}

The reason this module has "career-defining" in its title is that leakage is not a beginner's
mistake. It is subtle, it shows up as *unusually good news*, and unusually good news is the thing
teams are least inclined to challenge. This page is the five common forms and, more usefully, the
one habit that prevents most of them.
''',
 answer='''Leakage is **information about the answer sitting in your features that will not be there at
    prediction time** — a column filled in only after the event, a scaler fitted before the split,
    an ID that encodes the outcome, a random split across a time series. Validation cannot catch
    it, because the split is fine and the answer is inside the inputs. The habit that prevents
    most of it: for every feature, ask *would this value exist, with this content, at the moment I
    need the prediction?* — and put all preprocessing inside a pipeline fitted per fold.''',
 dangler='''
### The question this page leaves open

Your numbers are now trustworthy. That leaves the last, most human part of this week: what you
*do* with them.

Two models score 0.91 and 0.92 — is that a real difference or a coin flip? *Where* is the better
model still wrong, and does that pattern matter? And how do you report all this to people who
will act on it? That is
[Module 5 — Model selection, error analysis & reporting](/curriculum/p3/week-19/5-model-selection-error-analysis-reporting).
''',
 build_open='''The best-scoring model in the room is the one most likely to be leaking. This layer is how to
    check, quickly, before anybody presents anything.''',
 edge_open='''Leakage in feature stores, in time-travel joins, and the ways good infrastructure creates new
    ways to leak.'''),

W+"5-model-selection-error-analysis-reporting.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **0.91 versus 0.92** — is that a win or a coin flip?
  - **Look at what it got wrong** — the hour that beats a week of tuning
  - **The errors that cluster** — and the ones that will embarrass you publicly
  - **Report it like a professional** — what to include, and what to admit
</Card>''',
 story='''{/* TERM LADDER: model selection → statistical significance → error analysis → slice → model card */}

### The two-hundredth of a point

Two models: 0.91 and 0.92. The team wants to ship the second. Someone asks whether the
difference is real, and the room goes quiet — because on 400 test rows, that gap is comfortably
inside the noise. You have been about to make a decision on a coin flip.

That is the first half of this page: knowing when a difference is a difference.

The second half is the highest-value hour in machine learning, and almost nobody spends it.
**Sit down and read the cases your model got wrong.** Not the metric — the actual rows. Patterns
appear within twenty minutes: it fails on new customers, or on weekends, or on anything written
in a second language. Those slices are where the next real improvement lives, and no amount of
hyperparameter tuning will find them.

And then you write it down — honestly, including where the model fails and who it fails for,
because the people who act on your model deserve to know its shape.
''',
 answer='''A gap of 0.01 on a few hundred rows is usually noise, so differences get a confidence interval
    or a paired test before anyone ships anything. And the highest-value hour available to you is
    not tuning: it is **reading the rows the model got wrong**, which reliably reveals clusters —
    new customers, weekends, another language — that point at the next real improvement. Report
    both the score *and* those slices, because the people acting on the model need its shape, not
    just its average.''',
 dangler='''
### The question this page leaves open

You can now build models and prove they are good. Both those things assume something you have
not questioned: **the columns you were given.**

Real data does not arrive as tidy numbers. It arrives as dates, free text, categories with
five thousand values, and a target class that appears in 0.3% of rows. Turning raw data into
things a model can learn from is where most of the actual work lives:
[Week 20 — Feature engineering & imbalanced data](/curriculum/p3/week-20/index).
''',
 build_open='''This layer is the difference between "the model scored 0.92" and a report a stakeholder can
    act on without being misled.''',
 edge_open='''Multiple-comparison problems from repeated model selection, and what a model card should say
    when the answer is uncomfortable.'''),
}
