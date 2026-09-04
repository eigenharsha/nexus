W = "curriculum/p3/week-18/"
PAGES = {
W+"1-decision-trees.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The model you can explain to your grandmother** — a flowchart the machine wrote
  - **Watch a tree pick its own questions** — in a moving picture
  - **What makes a good question** — purity, measured
  - **Grow one, then watch it memorise** — and learn where to stop
</Card>''',
 story='''{/* TERM LADDER: split → node → leaf → purity → depth → pruning */}

### Twenty questions

Think about how a loan officer actually decides. Not with a formula — with questions.

*Is the applicant employed?* Yes. *For more than a year?* No. *Is the deposit over 20%?* Yes.
→ approve.

That is a flowchart, and it is nothing like the smooth slope of Week 17. It has no coefficients
to interpret, no line to plot. It is a sequence of yes/no questions ending in a decision — and
a machine can *learn which questions to ask*, in which order, purely from examples.

{/* ANIM:W18M1 */}

The trick is choosing each question well. A good question splits a messy pile into two tidier
piles — mostly-approve on one side, mostly-decline on the other. Machines measure "tidier" with
one number and simply try every possible question to find the best one.

And a **decision tree** has a quality no other model in this phase can match: you can print it
out and hand it to a regulator, a doctor, or your grandmother, and they can follow exactly why
it decided what it did. That readability is also the trap this page ends on — left alone, a
tree will grow a branch for every single customer, which is Week 17's memorising student
wearing a new hat.
''',
 answer='''A tree learns **which questions to ask** by trying every possible split and keeping the one
    that leaves the two resulting piles tidiest — purity, measured with one number. Repeat inside
    each pile and a flowchart grows itself. Its superpower is that a human can follow the whole
    decision; its weakness is that, unstopped, it grows a branch per example and memorises. So
    every tree needs a limit — a depth, a minimum leaf size, or pruning after the fact.''',
 dangler='''
### The question this page leaves open

One tree is readable and unstable: change a handful of training rows and it can pick different
questions and give different answers. Readable but jumpy is a hard thing to ship.

There is a wonderfully simple fix that turns that instability into an *advantage* — grow many
different trees and let them vote. That is
[Module 2 — Bagging & random forests](/curriculum/p3/week-18/2-bagging-random-forests).
''',
 build_open='''When someone asks "why did the model decline this application?", a tree can answer and a
    neural network cannot. This layer is when that matters more than accuracy.''',
 edge_open='''Split criteria, categorical handling and the instability that makes single trees a poor
    production choice.'''),

W+"2-bagging-random-forests.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Ask a crowd instead of an expert** — why many wrong models beat one careful one
  - **Watch votes cancel each other's mistakes** — in a moving picture
  - **The two kinds of randomness** — different rows, different questions
  - **Fit a forest** — and get an honest score for free
</Card>''',
 story='''{/* TERM LADDER: bootstrap → bagging → variance → feature subsampling → out-of-bag */}

### Ask the crowd

Here is a strange fact about guessing. Ask one person how many sweets are in a jar and they
will be well off. Ask five hundred people and *average their guesses*, and the average lands
remarkably close — because individual mistakes point in different directions and cancel out.

That is the entire idea of this page, applied to trees.

One tree is jumpy: shuffle a few rows and it changes its mind. So grow *hundreds* of trees,
each on a slightly different random sample of the data, and let them vote. Each one is
individually mediocre. Their mistakes are made in different directions. The vote is far steadier
than any single tree — and dramatically better.

{/* ANIM:W18M2 */}

**Random forests** add a second dash of randomness, which sounds like sabotage and is the
opposite: each split may only consider a random subset of the features. That stops every tree
from leaning on the same dominant column, so the trees disagree *more* — and disagreement is
precisely what makes the vote work.
''',
 answer='''Many mediocre models beat one careful one because **their errors point in different directions
    and cancel in the vote.** Bagging builds that disagreement by training each tree on a
    different bootstrap sample of the rows; random forests add a second source by letting each
    split see only a random subset of features, which stops every tree from leaning on the same
    dominant column. Deliberately weakening the individuals is what makes the crowd strong — and
    the rows each tree never saw give you an honest score for free.''',
 dangler='''
### The question this page leaves open

Forest trees are grown independently, in parallel, each ignorant of the others' mistakes. Which
is fine, and slightly wasteful — nobody learns from anybody.

What if each new tree were built specifically to fix what the current ensemble still gets
wrong? That small change produces the model that wins more real-world tabular competitions than
anything else: [Module 3 — Gradient boosting & XGBoost](/curriculum/p3/week-18/3-gradient-boosting-xgboost).
''',
 build_open='''A random forest is the strongest thing you can fit in ten minutes with no tuning, which
    makes it the baseline every fancier model has to beat. This layer is how to fit and read one
    properly.''',
 edge_open='''Why bagging reduces variance and not bias, and what the out-of-bag estimate is really
    measuring.'''),

W+"3-gradient-boosting-xgboost.mdx": dict(
 glimpse='''<Card title="In this chapter — about 30 minutes" icon="sparkles">
  - **Learning from your own mistakes** — one small correction at a time
  - **Watch the errors shrink** — round after round, in a moving picture
  - **Why it beats forests on tabular data** — and where it does not
  - **Fit XGBoost properly** — the four parameters that actually matter
</Card>''',
 story='''{/* TERM LADDER: residual → weak learner → boosting → learning rate → early stopping */}

### Marking your own homework

A forest is a crowd of independent guessers. Boosting is one student, revising.

Round one: make a rough prediction. Look at what you got wrong — the **residuals**, the leftover
errors. Round two: train a *small* new tree whose only job is to predict those errors, and add a
fraction of its opinion to your answer. Look at what is still wrong. Round three: same again.

Do that a few hundred times, each round nudging the answer toward what is still missing, and
you get the single most effective model for tables of numbers that anyone has found — the thing
that wins competitions and quietly runs credit scoring, demand forecasting and fraud detection
across the industry.

{/* ANIM:W18M3 */}

There is a catch, and it is the mirror of Week 17's lesson. A model that relentlessly hunts its
own remaining errors will, given enough rounds, start fitting the noise — so boosting comes with
a brake (a small learning rate) and a stopping rule (watch a held-out set and stop when it stops
improving).
''',
 answer='''Boosting works by **training each new tree on what the ensemble still gets wrong** — the
    residuals — and adding a fraction of its correction, hundreds of times. That sequential
    error-hunting is why it beats a forest on tabular data, and it is exactly why it can overfit:
    a model that chases every remaining error will eventually chase noise. The brake is a small
    learning rate plus early stopping on a held-out set, which is why the two most important
    parameters are the ones that slow it down.''',
 dangler='''
### The question this page leaves open

Everything so far — lines, trees, forests, boosting — needed one thing: **labels**. Someone had
to tell the model the right answer for every training example.

Most data has no labels. Nobody has tagged your million customers with which "type" they are;
the categories are not written down anywhere. Finding structure with no answer key is
[Module 4 — Unsupervised learning: clustering](/curriculum/p3/week-18/4-unsupervised-learning-clustering).
''',
 build_open='''If the data is a table, this is the model you will ship. This layer is the parameters worth
    tuning, the ones that are noise, and the stopping rule that saves you from yourself.''',
 edge_open='''Second-order boosting, regularised objectives, and why the library's defaults are as good as
    they are.'''),

W+"4-unsupervised-learning-clustering.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Finding groups nobody labelled** — structure without an answer key
  - **Watch k-means settle** — points changing sides, in a moving picture
  - **How many groups?** — the question the algorithm cannot answer for you
  - **Cluster real customers** — then decide whether the groups mean anything
</Card>''',
 story='''{/* TERM LADDER: unsupervised → cluster → centroid → k-means → silhouette */}

### Sorting the laundry

Tip a basket of clean laundry on the bed and start sorting. Nobody handed you categories — you
invent them as you go: work shirts, gym things, the socks. When you are done, the piles are
obvious, and you could not have written the rules in advance.

Most real data arrives exactly like that basket. You have a million customers and no idea which
"kinds" of customer exist, because nobody has ever written them down. That is **unsupervised
learning** — finding structure with no answer key — and its workhorse is beautifully simple:

Drop a few markers anywhere. Assign every point to its nearest marker. Move each marker to the
middle of the points that chose it. Repeat until nothing moves. That is **k-means**, and it
settles in seconds.

{/* ANIM:W18M4 */}

The honest part of this page is what the algorithm will never tell you: **how many piles there
should be**, and whether the piles mean anything at all. k-means will happily split your
customers into four groups whether or not four groups exist — and reading meaning into arbitrary
piles is the classic way this technique embarrasses people.
''',
 answer='''You find groups without labels by **letting the data settle**: place k markers, assign every
    point to its nearest one, move each marker to the centre of its points, and repeat until
    nothing changes. What the algorithm cannot do is tell you k, or whether the clusters mean
    anything — it will produce four tidy groups from data that has none. So the number comes from
    quality measures like the silhouette score *plus* a human check that the groups correspond to
    something real.''',
 dangler='''
### The question this page leaves open

Clustering asked "which points sit together?" — in however many dimensions your data has. And
that is where a quiet problem lives: with two hundred columns, "near" and "far" stop behaving
the way your intuition expects, and every point ends up roughly the same distance from every
other.

Squeezing data down to a few meaningful dimensions — and the idea behind the embeddings you met
in Phase 4 — is
[Module 5 — Dimensionality reduction & representation](/curriculum/p3/week-18/5-dimensionality-reduction-representation).
''',
 build_open='''"Segment our customers" arrives as a request with no success criterion. This layer is how to
    do it and, more importantly, how to tell whether the result is real.''',
 edge_open='''Where k-means fails — non-spherical clusters, scale sensitivity — and what to reach for
    instead.'''),

W+"5-dimensionality-reduction-representation.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **When “near” stops meaning anything** — the curse, demonstrated
  - **The shadow that keeps the shape** — projection, in a moving picture
  - **PCA in plain language** — keep the directions that carry the variation
  - **The idea behind every embedding** — including the ones in Phase 4
</Card>''',
 story='''{/* TERM LADDER: dimension → projection → variance → principal component → representation */}

### The shadow on the wall

Hold a chair between a lamp and the wall. The shadow is flat — you have thrown away a whole
dimension — and yet anyone looking at it says "chair". Turn the chair to the wrong angle and the
shadow becomes an unreadable smudge.

That is this page in one image: **you can throw away most of the dimensions and keep the
meaning, if you choose the direction well.**

You need this more than you might think. With two hundred columns, distances stop being
informative — in high dimensions almost every point is roughly equidistant from every other, so
"nearest neighbour" quietly becomes meaningless, and the clustering you just learned stops
working.

{/* ANIM:W18M5 */}

The classic tool, **PCA**, finds the angle that casts the most informative shadow: the
directions along which your data actually varies. And when you understand that, you understand
what an embedding *is* — Phase 4's map of meanings was exactly this idea, learned rather than
computed: a small set of numbers chosen to preserve what matters about something much larger.
''',
 answer='''You can drop most dimensions and keep the meaning by **choosing the direction of the shadow
    well** — projecting onto the axes along which the data actually varies, which is what PCA
    computes. It matters because in very high dimensions distances stop discriminating: almost
    every point sits about as far from every other, so neighbours and clusters become
    meaningless. And this is precisely what an embedding is — a compact representation that keeps
    what matters about something much bigger.''',
 dangler='''
### The question this page leaves open

You now have a toolbox: lines, trees, forests, boosting, clusters, projections. Any of them will
give you a model, and every one of them will give you a *number* that claims it is good.

Which brings the most dangerous question in this phase — **is that number telling the truth?**
Accuracy can be 99% on a model that is worthless, and a validation split can lie to you outright.
Week 19 is how you find out: [Week 19 — Evaluation, metrics & validation](/curriculum/p3/week-19/index).
''',
 build_open='''PCA before clustering is one of those steps that quietly decides whether the result is
    meaningful. This layer is when it helps, when it hurts, and how to tell.''',
 edge_open='''What PCA assumes, why scaling changes everything, and where non-linear methods earn their
    keep.'''),
}
