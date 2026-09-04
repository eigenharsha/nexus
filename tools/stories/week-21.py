W = "curriculum/p3/week-21/"
PAGES = {
W+"1-from-linear-models-to-neural-networks.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The problem a straight line can never solve** — see it, in one picture
  - **Watch a bend appear** — how stacking layers creates curves
  - **The one ingredient that matters** — and why without it, depth is pointless
  - **Build a two-layer network by hand** — and solve the unsolvable problem
</Card>''',
 story='''{/* TERM LADDER: layer → weight → activation function → non-linearity → hidden layer */}

### The problem the line cannot solve

Here is a puzzle that broke the field for a decade.

Put four points on a page: two in opposite corners marked ✓, two in the other corners marked ✗.
Now separate the ticks from the crosses **with a single straight line**.

You cannot. No angle works. And every model in Week 17 was, underneath, a straight line — so
none of them can solve a problem this simple. That is not a small gap; that shape appears
everywhere in real data.

{/* ANIM:W21M1 */}

The escape is to stack: run the input through a line, **bend the result**, and feed it into
another line. The bend is the entire trick — it is called an **activation function**, and it is
one line of code (keep positives, zero the negatives). Without it, stacking a hundred layers
just gives you a slightly more expensive straight line. With it, a stack of simple parts can
approximate any shape at all.

That is a **neural network**: layers of straight lines with bends between them, and nothing
more mysterious than that.
''',
 answer='''A straight line cannot separate points arranged in opposite corners — and every Week 17 model
    is a straight line underneath. Stacking fixes it, but **only if you bend the output between
    layers**: without an activation function, a hundred stacked layers collapse into one line, so
    depth buys nothing. With that one bend, layers of simple parts can approximate any shape,
    which is all a neural network is.''',
 dangler='''
### The question this page leaves open

Your network has a shape and some numbers in it. Those numbers are currently random, and its
predictions are nonsense.

Week 17 taught the fix in principle: measure the error, nudge the parameters downhill. But that
was one line with two parameters. This has thousands, arranged in layers, where each one's
effect passes through everything after it. Working out each parameter's share of the blame is
[Module 2 — Forward pass, loss & backpropagation](/curriculum/p3/week-21/2-forward-pass-loss-backpropagation).
''',
 build_open='''You will not hand-build networks at work, and you will constantly debug them. This layer is
    where the intuition for "why is it not learning" is formed.''',
 edge_open='''Universal approximation, what depth buys over width, and which activations survived and
    why.'''),

W+"2-forward-pass-loss-backpropagation.mdx": dict(
 glimpse='''<Card title="In this chapter — about 30 minutes" icon="sparkles">
  - **Who is to blame for the error?** — assigning credit through a stack of layers
  - **Watch blame flow backwards** — in a moving picture
  - **The chain rule, in plain language** — one idea, applied repeatedly
  - **Differentiate a network by hand** — then let PyTorch confirm you were right
</Card>''',
 story='''{/* TERM LADDER: forward pass → loss → chain rule → backpropagation → gradient */}

### Whose fault was that?

A restaurant sends out a bad dish. Whose fault?

Some of it belongs to the chef who cooked it, some to the sous chef who prepared the sauce, some
to the supplier whose tomatoes were poor. The blame does not sit in one place — it flows
*backwards* along the chain that produced the result, and each step gets the share it deserves.

That is **backpropagation**, and it is the entire reason deep learning works.

Forwards, the network computes: input → layer → bend → layer → prediction, then one number
saying how wrong it was. Backwards, that error flows the other way: the last layer's share is
easy, and every earlier layer's share is *its own local effect multiplied by the blame that
arrived from in front of it.*

{/* ANIM:W21M2 */}

Multiply the local effect by the incoming blame, pass it further back. That is the chain rule —
one small idea, applied over and over — and it is why a network with a million parameters can be
improved without ever guessing.
''',
 answer='''Every parameter's share of the blame is **its own local effect multiplied by the blame arriving
    from the layers in front of it** — the chain rule, applied repeatedly from the loss backwards
    to the input. The forward pass computes the prediction and one error number; the backward
    pass distributes that error to every parameter, in one sweep, at roughly the same cost as the
    forward pass. That efficiency is the whole reason training networks with millions of
    parameters is possible at all.''',
 dangler='''
### The question this page leaves open

You have the mathematics. Now run it — and meet the reality that the equations do not mention.

The loss explodes to infinity. Or it flatlines and nothing happens. Or it looks perfect for
twenty epochs and then falls apart. None of these are bugs in your derivation; they are the
*dynamics* of training, and knowing them is the difference between a model that trains and a
week of misery: [Module 3 — Training dynamics](/curriculum/p3/week-21/3-training-dynamics).
''',
 build_open='''Autograd hides this and then hands you a NaN at 2 a.m. This layer is what to picture when
    that happens.''',
 edge_open='''Reverse-mode differentiation, memory-versus-recompute trade-offs, and what the graph really
    stores.'''),

W+"3-training-dynamics.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The loss went to NaN** — the three usual causes, and how to tell them apart
  - **Watch a learning rate be too big, too small, and right** — in a moving picture
  - **Reading a loss curve** — the diagnosis skill nobody teaches
  - **Fix a broken training run** — deliberately broken, then repaired
</Card>''',
 story='''{/* TERM LADDER: epoch → batch → learning rate → loss curve → vanishing gradient */}

### Reading the loss curve

Every deep learning practitioner develops one skill early, and it is not mathematical: they
learn to look at a wiggly line and know what is wrong.

The loss curve is the patient's chart. A curve that **shoots up to infinity** means your steps
are too big — you are bouncing out of the valley instead of walking into it. A curve that is
**flat from the start** means the signal never reached the early layers. A curve that **drops
beautifully then diverges from the validation line** is Week 17's memorising student, in a new
costume. And a curve that is **noisy but descending** is usually just fine.

{/* ANIM:W21M3 */}

This page is that diagnostic vocabulary, learned properly rather than by folklore: what each
shape means, which knob to reach for, and why the learning rate is the single most important
number in the entire process — worth more attention than the architecture almost everybody
argues about instead.
''',
 answer='''You read the curve like a chart: **exploding** means the learning rate is too large — the steps
    overshoot the valley; **flat** means no gradient is reaching the early layers; **beautiful
    training loss with rising validation loss** is overfitting; **noisy but descending** is
    healthy. The learning rate matters more than the architecture, which is why the reliable
    procedure is to sweep it first, watch the curve, and change one thing at a time.''',
 dangler='''
### The question this page leaves open

You can now diagnose a training run and fix it by hand. Everyone hit the same problems, and the
field built standard tools for them: smarter step rules that adapt as they go, and
regularisation designed specifically for deep networks.

Using them well — rather than pasting the defaults from a blog post — is
[Module 4 — Optimizers & regularization in practice](/curriculum/p3/week-21/4-optimizers-regularization-in-practice).
''',
 build_open='''Most "the model does not train" tickets are one of four curve shapes. This layer is how to
    name the shape in thirty seconds instead of an afternoon.''',
 edge_open='''Why gradients vanish and explode, and what normalisation and residuals are really doing about
    it.'''),

W+"4-optimizers-regularization-in-practice.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Momentum, in one image** — why a ball rolls better than a hiker walks
  - **What Adam actually does** — a step size per parameter, explained plainly
  - **Dropout: getting better by breaking things** — deliberately
  - **The settings to start from** — and the ones worth tuning
</Card>''',
 story='''{/* TERM LADDER: momentum → adaptive learning rate → Adam → dropout → weight decay */}

### The ball and the hiker

Back to Week 17's foggy hillside, where you stepped downhill by feeling the slope.

A hiker who only feels the local slope has two problems: they stop in every small dip, and they
zig-zag across narrow valleys. **A ball rolling down the same hill does neither** — it carries
speed, so it rolls through dips and smooths its own path. Giving each step a memory of the last
one is **momentum**, and it is one of the cheapest improvements in the field.

Then the second idea, and it is where **Adam** comes from: not every parameter needs the same
step size. Some sit on steep slopes, some on flat ground. Adam keeps a running feel for each
parameter's terrain and scales its step accordingly — which is why it works well with almost no
tuning, and why it is the default nearly everywhere.

{/* ANIM:W21M4 */}

And the ideas that stop networks memorising, one of which sounds absurd: **randomly switch off
neurons during training**. It works because a network that cannot rely on any one unit is forced
to spread its knowledge — a crowd rather than an expert, which is Week 18's lesson again from
another direction.
''',
 answer='''Momentum gives each step **a memory of the last one**, so training rolls through small dips and
    stops zig-zagging across narrow valleys. Adam adds a per-parameter step size, keeping a
    running feel for each one's terrain, which is why it works with almost no tuning. And dropout
    — randomly switching units off during training — improves a network by preventing it from
    leaning on any single unit, forcing the knowledge to spread; it is Week 18's crowd argument
    arriving from another direction.''',
 dangler='''
### The question this page leaves open

You now understand the whole machine — and you have been writing every derivative by hand, which
nobody does past this week.

There is one library the entire field runs on, and it is worth learning properly rather than by
copying: what a tensor really is, how autograd builds its graph, and where a GPU changes the
rules. That is [Module 5 — PyTorch fundamentals](/curriculum/p3/week-21/5-pytorch-fundamentals).
''',
 build_open='''Everyone pastes AdamW with lr=3e-4. This layer is knowing when that is right, when it is
    lazy, and what to change first when it is not working.''',
 edge_open='''Optimiser state memory, why weight decay and L2 differ in adaptive methods, and schedule
    choices that matter more than the optimiser.'''),

W+"5-pytorch-fundamentals.mdx": dict(
 glimpse='''<Card title="In this chapter — about 30 minutes" icon="sparkles">
  - **A tensor is an array that remembers** — where it came from
  - **Watch the graph build itself** — in a moving picture
  - **The training loop, memorised once** — five lines you will write forever
  - **Move it to a GPU** — and understand what actually changed
</Card>''',
 story='''{/* TERM LADDER: tensor → device → autograd → computational graph → training loop */}

### The array that remembers

You already know NumPy arrays. A **tensor** is one of those with two extra abilities, and both
matter enormously.

First, it can live somewhere else — on a GPU, a chip with thousands of small cores that does the
same arithmetic to thousands of numbers at once. Moving a tensor there is one call, and it is
the difference between training overnight and training over a fortnight.

Second — and this is the beautiful part — **a tensor remembers how it was made**. Multiply two
tensors and the result quietly records "I came from these two, by multiplication". Do a whole
forward pass and you have built, without writing a line of extra code, the exact graph that
Module 2's backpropagation needs. Ask for the gradients and the library walks that graph
backwards for you.

{/* ANIM:W21M5 */}

The rest of this page is the training loop itself — five lines, in a fixed order, with one line
that everybody forgets on their first try — and what actually goes wrong when a tensor is on the
wrong device.
''',
 answer='''A tensor is an array with two extra powers: it can live on a **GPU**, and it **remembers how it
    was made** — every operation records its inputs, so a forward pass silently builds the exact
    graph backpropagation needs. That is why you never write derivatives again: the library walks
    the recorded graph backwards. The training loop is five lines in a fixed order, and the one
    everybody forgets is zeroing the gradients — without it, this batch's blame is added to the
    last one's.''',
 dangler='''
### The question this page leaves open

You can now build and train a network on tables of numbers. But the data that made deep learning
famous is not a table — it is **pictures**.

A photograph is a million numbers where position means everything: a cat is a cat whether it
sits top-left or bottom-right, and no fully-connected layer knows that. Networks that understand
space are Week 22: [Week 22 — Computer vision & transfer learning](/curriculum/p3/week-22/index).
''',
 build_open='''This is the library the rest of your career runs on. This layer is the mental model that stops
    the errors everybody gets in their first month.''',
 edge_open='''What the graph costs in memory, when to detach, and where the CPU-GPU boundary quietly
    dominates your step time.'''),
}
