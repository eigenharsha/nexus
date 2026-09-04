W = "curriculum/p3/week-17/"
PAGES = {
W+"1-what-learning-from-data-actually-is.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The rule nobody wrote** — how a machine can know something you never told it
  - **Watch a line find its own slope** — learning, in a moving picture
  - **The three pieces every learner has** — a guess, a score, a nudge
  - **Train your first model** — five lines, on your own laptop
</Card>''',
 story='''{/* TERM LADDER: example → feature → label → model → loss → learning */}

### The rule nobody wrote down

Here is a small mystery. Suppose I show you five houses:

| size | price |
| --- | --- |
| 50 m² | £150,000 |
| 70 m² | £210,000 |
| 90 m² | £270,000 |
| 110 m² | £330,000 |
| 130 m² | £390,000 |

Now: what is a 100 m² house worth? You said £300,000 without meaning to. Nobody gave you a
formula. You looked at examples and *the rule fell out of them*.

That — exactly that, with nothing mystical added — is what a machine does when it "learns". It
is handed examples, it makes a guess, it measures how wrong the guess was, and it adjusts. Do
that a few thousand times and the rule nobody wrote down is sitting inside a handful of
numbers.

{/* ANIM:W17M1 */}

This page names the three parts of that loop — the **model** (the shape of the guess), the
**loss** (how wrong it was), and the **nudge** (how it improves) — and by the end you will have
trained one yourself and watched the numbers move.
''',
 answer='''A machine learns by **guessing, measuring the error, and adjusting** — nothing more mystical
    than that. The model is the shape of the guess (here, a straight line); the loss is one
    number saying how wrong today's guess is across all the examples; and training is the
    repeated nudge of the model's numbers in whichever direction makes that one number smaller.
    Do it enough times and a rule nobody wrote down ends up stored in a handful of parameters.''',
 dangler='''
### The question this page leaves open

You have seen the loop. But "nudge it in the direction that makes the loss smaller" is doing a
lot of work in that sentence — *which* direction, and *how far*?

For the straight line above, that question has an exact answer you can derive with pen and
paper, and doing so once will teach you more than a hundred library calls. That is
[Module 2 — Linear regression from mathematical scratch](/curriculum/p3/week-17/2-linear-regression-from-mathematical-scratch).
''',
 build_open='''Every ML conversation at work assumes this vocabulary — features, labels, loss, fitting. This
    layer is that vocabulary made precise, so the rest of the phase is not spent guessing.''',
 edge_open='''What "learning" means when you look closely: capacity, optimisation and the assumptions
    hiding in every loss function.'''),

W+"2-linear-regression-from-mathematical-scratch.mdx": dict(
 glimpse='''<Card title="In this chapter — about 30 minutes" icon="sparkles">
  - **Derive the nudge yourself** — the gradient, with pen and paper
  - **Two ways to fit a line** — the exact formula, and walking downhill
  - **Why anyone walks when a formula exists** — the answer is about size
  - **Implement it in NumPy** — and match scikit-learn to six decimals
</Card>''',
 story='''{/* TERM LADDER: parameter → gradient → learning rate → gradient descent → normal equation */}

### Downhill in the fog

Picture yourself on a hillside in thick fog, trying to reach the bottom. You cannot see the
valley. But you *can* feel which way the ground slopes under your feet — so you take a step
that way, and repeat.

That is the whole of **gradient descent**, and it is how almost every model in this course
learns, including the one behind ChatGPT. The hillside is the loss: high where the model is
wrong, low where it fits. The slope under your feet is the **gradient** — and for a straight
line you can work it out exactly, by hand, in about six lines of algebra.

There is a twist worth knowing early. For this particular problem you do not *need* to walk at
all: there is a formula that jumps straight to the bottom in one step. It is exact, it is
beautiful — and almost nobody uses it, for a reason that has nothing to do with mathematics
and everything to do with size.

This page does both, so you know exactly what you are choosing between.
''',
 answer='''You find the nudge by **taking the derivative of the loss with respect to each parameter** —
    the gradient — and stepping the opposite way, scaled by the learning rate. Too big a step
    overshoots and diverges; too small and training crawls. For a straight line there is also a
    closed-form answer (the normal equation) that lands at the bottom in one move, exactly. It
    is abandoned in practice because it requires inverting a matrix that grows with your feature
    count, which becomes impossible long before your data does.''',
 dangler='''
### The question this page leaves open

Your line predicts a *number*: a price, a temperature, a duration. But an enormous share of
real problems are not numbers at all — they are **yes or no**. Is this transaction fraud? Will
this customer leave? Is this email spam?

You cannot fit a straight line to "yes", and squeezing one to fit produces nonsense like a 140%
probability. Making a line answer a yes-or-no question is
[Module 3 — Logistic regression & classification](/curriculum/p3/week-17/3-logistic-regression-classification).
''',
 build_open='''You will rarely implement least squares at work — and you will constantly debug things whose
    behaviour only makes sense if you have. This layer is that grounding, plus the API you
    actually use.''',
 edge_open='''Conditioning, collinearity and the numerical reasons the beautiful closed form is a trap at
    scale.'''),

W+"3-logistic-regression-classification.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Making a line say “yes” or “no”** — the squash that changes everything
  - **Probabilities, not verdicts** — and why that difference pays your rent
  - **The threshold is a business decision** — not a modelling one
  - **Fit a real classifier** — and read what it actually predicted
</Card>''',
 story='''{/* TERM LADDER: classification → probability → sigmoid → decision threshold → log loss */}

### The line that cannot say "yes"

Fit a straight line to a yes/no question and watch it embarrass itself. Feed it a big enough
input and it predicts a probability of **1.4**. Feed it a negative one and it predicts
**−0.3**. Neither exists.

The fix is one of the neatest moves in this field: keep the straight line exactly as it is, and
then **squash its output** into the range 0 to 1 with a curve that flattens at both ends. Large
positive numbers become "almost certainly yes". Large negative numbers become "almost certainly
no". The middle stays sensitive. That squash is the **sigmoid**, and a line plus a sigmoid is a
**logistic regression** — still, in 2026, the first model you should try on any yes/no problem.

The part everyone skips comes next. The model gives you a *probability* — 0.73 — not a verdict.
Turning 0.73 into "yes, block this transaction" needs a **threshold**, and choosing that number
is not mathematics. It is a business decision about which mistake hurts more: the fraud you let
through, or the customer you falsely accuse.
''',
 answer='''A line answers yes/no by **squashing its output through a sigmoid**, which maps any number
    into 0–1 so the result is a genuine probability rather than an impossible 1.4. Training
    minimises log loss, which punishes confident mistakes far more harshly than uncertain ones.
    And the model never gives a verdict: converting a probability into an action needs a
    threshold, and that number belongs to the business — it is where you decide whether a missed
    fraud or a wrongly-blocked customer costs you more.''',
 dangler='''
### The question this page leaves open

Your classifier scores 99% on the data it was trained on. Congratulations — that number may be
worthless, because a model can score perfectly by *memorising* the examples instead of learning
the rule, and memorisation fails on the very next customer.

Spotting that, and building models that deliberately refuse to memorise, is
[Module 4 — Regularization & the bias-variance trade-off](/curriculum/p3/week-17/4-regularization-the-bias-variance-trade-off).
''',
 build_open='''Logistic regression is the model your team will actually ship first, and the baseline every
    fancier model must beat. This layer is how to fit it well and read it honestly.''',
 edge_open='''Calibration, class weights and what the coefficients do and do not mean.'''),

W+"4-regularization-the-bias-variance-trade-off.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The student who memorised the textbook** — and failed the exam
  - **Watch a model overfit** — in a moving picture
  - **Two ways to be wrong** — too simple, and too eager
  - **Tune the dial** — and see the test score turn around
</Card>''',
 story='''{/* TERM LADDER: training error → test error → overfitting → underfitting → regularization */}

### The student who memorised the book

Two students revise for an exam.

The first memorises every worked example, word for word. Ask them a question from the book and
they are flawless. Change one number and they are lost — they learned *the answers*, not the
subject.

The second skimmed one summary page. They are calm about new questions and wrong about most of
them, because they never learned enough to be right.

Every model you ever train sits somewhere between those two students, and this page is about
finding the spot in the middle. Memorising is called **overfitting** — perfect on the training
data, useless on anything new. Skimming is **underfitting**. And the reason a model's score on
its own training data is not evidence of anything is precisely student one.

{/* ANIM:W17M4 */}

The cure is a dial that penalises the model for being too eager, called **regularization** —
and turning it is one of the few genuinely reliable ways to make a model better.
''',
 answer='''A perfect training score can be worthless because the model may have **memorised the examples
    rather than learned the rule** — that is overfitting, and it fails on the very next unseen
    case. The opposite failure, underfitting, is a model too simple to capture the pattern at
    all. Regularization is the dial between them: it penalises large, eager parameters so the
    model prefers a simpler explanation, and the only honest way to set it is by watching the
    score on data the model has never seen.''',
 dangler='''
### The question this page leaves open

You can now build a model from scratch, make it answer yes/no, and stop it memorising. But you
have been writing every loop by hand — and no working data scientist does that.

There is one library the entire industry uses for models like these, with a single interface
you will meet again and again. Learning it properly is
[Module 5 — scikit-learn: the industry surface](/curriculum/p3/week-17/5-scikit-learn-the-industry-surface).
''',
 build_open='''Every "the model was great in testing and terrible in production" story starts here. This
    layer is the vocabulary and the dial that prevents it.''',
 edge_open='''Double descent, effective capacity, and the ways the classical picture of this trade-off is
    incomplete for modern models.'''),

W+"5-scikit-learn-the-industry-surface.mdx": dict(
 glimpse='''<Card title="In this chapter — about 20 minutes" icon="sparkles">
  - **The four verbs that run the industry** — fit, predict, transform, score
  - **Pipelines** — and the bug they exist to prevent
  - **Replace your handwritten model** — same numbers, five lines
  - **Read the docs like a professional** — the pattern under every estimator
</Card>''',
 story='''{/* TERM LADDER: estimator → fit → predict → transform → pipeline */}

### The same four verbs, every time

You have written gradient descent by hand. That was worth doing once, and doing it twice would
be a waste of your afternoon.

Here is the thing nobody tells beginners about the industry-standard library: **it is much
smaller than it looks.** Hundreds of models, one interface. Every model in it is an object with
the same few verbs — `fit` to learn from data, `predict` to answer, `transform` to reshape,
`score` to grade. Learn those four and swapping a logistic regression for a random forest is a
one-line change.

Then there is **the pipeline**, which exists for a reason worth taking seriously. If you scale
your data before splitting it, information from the test set leaks into training and your
scores become fiction — a mistake so common and so quietly destructive that Week 19 devotes a
whole module to it. A pipeline makes that mistake structurally difficult, which is the best
kind of safety.
''',
 answer='''The library is small because **every model wears the same four verbs**: `fit` learns from data,
    `predict` answers, `transform` reshapes, `score` grades — so changing model is a one-line
    change and the rest of your code stands. Pipelines chain those steps into one object so that
    preprocessing is fitted only on the training fold; that is not tidiness, it is the structural
    prevention of leakage, the failure mode that makes a model look excellent and behave
    terribly.''',
 dangler='''
### The question this page leaves open

Straight lines and squashed lines are honest workhorses, but they share one assumption: that
the pattern is roughly a smooth slope. Plenty of real problems are not — they are a *sequence
of questions*. Is the applicant employed? If yes, for how long? If under a year, what is the
deposit?

That is not a line. It is a flowchart, and machines can learn flowcharts too. Week 18 begins
there: [Week 18 — Trees, ensembles & unsupervised learning](/curriculum/p3/week-18/index).
''',
 build_open='''This is the library your team already uses. This layer is how to use it without the three
    mistakes that show up in every code review.''',
 edge_open='''What the estimator API hides, where it fights you, and when to leave it.'''),
}
