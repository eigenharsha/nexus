W = "curriculum/p2/week-11/"
PAGES = {
W+"1-vectors-vector-spaces.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Two numbers on paper** — and the arrow that makes them useful
  - **Watch two arrows agree and disagree** — in a moving picture
  - **The one operation the whole course uses** — the dot product
  - **Do it by hand, then in NumPy** — and get the same answer
</Card>''',
 story='''{/* TERM LADDER: vector → length → scaling → dot product */}

### Where "similar" comes from

Something has been quietly assumed for four weeks. When Phase 4 says two words *mean similar
things*, or Phase 3 says two customers *are alike*, there is always a number underneath deciding
how similar — and until now nobody has said where that number comes from.

It comes from here, and it is smaller than you fear.

Draw two axes on paper and mark the point 3 across and 4 up. Write `[3, 4]`. That is a
**vector** — two numbers in a fixed order — and drawing an arrow from the origin to your dot
turns it into something you can reason about: it has a length, and it points somewhere.

{/* ANIM:W11M1 */}

Once you have arrows, one operation does almost all the work in this course: multiply the
matching numbers of two vectors and add up the results. That is the **dot product**, and it is
this week's single most important line. Its magic is that the answer tells you whether two arrows
point the *same* way — large when they agree, near zero when they are unrelated, negative when
they oppose.

That is "similar", made of arithmetic. Every recommendation, every search result and every
attention weight in Phase 4 is that one operation, repeated.
''',
 answer='''Similarity is **the dot product**: multiply the matching numbers of two vectors and add the
    results. It is large when two arrows point the same way, near zero when they are unrelated and
    negative when they oppose — which is exactly what "alike" means once things are written as
    numbers. A vector is just an ordered list, its length comes from Pythagoras, and scaling one
    changes its size without changing where it points.''',
 dangler='''
### The question this page leaves open

You can describe *things* as arrows. Now describe an **action** on them — rotate everything by
thirty degrees, or stretch it sideways, or squash three dimensions into two.

Doing that arrow by arrow would be endless. There is an object that applies one action to every
arrow at once, and it is the object every neural network layer is made of:
[Module 2 — Matrices & linear transformations](/curriculum/p2/week-11/2-matrices-linear-transformations).
''',
 build_open='''Vector operations are the innermost loop of everything you will run. This layer is where their
    cost and their numerical behaviour become real.''',
 edge_open='''Norms other than Euclidean, numerical stability, and where the geometric intuition stops being
    reliable in high dimensions.'''),

W+"2-matrices-linear-transformations.mdx": dict(
 glimpse='''<Card title="In this chapter — about 30 minutes" icon="sparkles">
  - **A grid of numbers is a verb, not a noun** — the shift that makes it click
  - **Watch a square get stretched and rotated** — in a moving picture
  - **Read a matrix by its columns** — where the corners land
  - **Multiply two by hand** — and know why the shapes must match
</Card>''',
 story='''{/* TERM LADDER: matrix → transformation → basis vector → matrix multiplication → transpose */}

### The grid that is really a verb

Most people meet a matrix as a grid of numbers and quietly decide it is a spreadsheet. That is
the misunderstanding this page exists to fix, because it makes everything afterwards feel
arbitrary.

**A matrix is an action.** It takes every arrow in your space and moves it — rotating, stretching,
squashing, flipping — all at once, in one step.

{/* ANIM:W11M2 */}

And there is a way of reading one that makes it stop being mysterious. Look at the **columns**:
they tell you exactly where the corners of the space end up. If you know where `[1, 0]` and
`[0, 1]` land, you know what happens to *everything*, because every other arrow is built from
those two.

That single insight explains the rest of the page. Multiplying two matrices means doing one
action and then the other — which is why the order matters (rotating then stretching is not the
same as stretching then rotating), and why the shapes have to line up: the output of the first
action must be something the second can accept.

Every layer of every neural network in Phase 3 and 4 is this: a matrix, applied to your data.
''',
 answer='''A matrix is **an action, not a table** — it moves every arrow in the space at once. Read it by
    its columns: they show where the basis arrows `[1, 0]` and `[0, 1]` land, and since every other
    arrow is built from those, that tells you what happens to everything. Multiplying matrices is
    doing one action then the other, which is why order matters and why the shapes must line up.''',
 dangler='''
### The question this page leaves open

Some actions are gentler than they look. Stretch a shape and, hidden inside the chaos, there are
usually a few special directions that *do not turn at all* — they only get longer or shorter.

Those directions turn out to be the skeleton of what a matrix really does, and finding them is
what powers compression, PCA and half of the recommendation systems on the internet:
[Module 3 — Eigen-decomposition, SVD & PCA](/curriculum/p2/week-11/3-eigen-decomposition-svd-pca).
''',
 build_open='''Shape errors are the single most common failure when writing model code, and they stop being
    mysterious once you read matrices as functions.''',
 edge_open='''Memory layout, why the same multiply can differ 10× in speed, and what BLAS is doing for
    you.'''),

W+"3-eigen-decomposition-svd-pca.mdx": dict(
 glimpse='''<Card title="In this chapter — about 30 minutes" icon="sparkles">
  - **The directions that refuse to turn** — a matrix's skeleton
  - **Watch one direction survive a transformation** — in a moving picture
  - **The tool that works on every matrix** — not just the well-behaved ones
  - **Compress something yourself** — and see what you kept
</Card>''',
 story='''{/* TERM LADDER: eigenvector → eigenvalue → SVD → rank → compression */}

### The directions that refuse to turn

Take a rubber sheet with arrows drawn all over it, and stretch it diagonally. Almost every arrow
swings to a new angle.

Almost. If you look carefully, a few arrows do not turn *at all* — they still point exactly where
they did, only longer or shorter. Those are the directions the transformation genuinely acts
along, and everything else it does is a mixture of them.

{/* ANIM:W11M3 */}

Those special directions are called **eigenvectors**, and how much each one stretched is its
**eigenvalue**. Together they are a matrix's skeleton — and once you can see the skeleton, an
enormous practical trick follows: if two of five directions do almost all the stretching, you can
throw the other three away and keep nearly all of the behaviour.

That is compression, and it is the same idea as Week 18's shadow on the wall. It powers
recommendation systems, noise removal, and PCA — and this page also gives you the version that
works for **every** matrix, not just the well-behaved square ones, which is what makes it usable
on real data.
''',
 answer='''Every transformation has **directions it does not turn** — it only stretches or shrinks them.
    Those are its eigenvectors, and the amount of stretch is the eigenvalue; together they are the
    skeleton of what the matrix really does. When a few directions carry most of the stretching,
    discarding the rest keeps nearly all the behaviour — which is compression, PCA and the
    recommendation trick, all the same idea. SVD is the version that works on every matrix, not
    only the tidy ones.''',
 dangler='''
### The question this page leaves open

Everything so far has been about *describing* things. Learning is about **changing** them: nudging
numbers until an answer improves.

To nudge in the right direction you need to know which way is downhill — and that is a different
branch of mathematics, taught here with no more machinery than a slope on a hill:
[Module 4 — Calculus & the chain rule](/curriculum/p2/week-11/4-calculus-the-chain-rule).
''',
 build_open='''These decompositions are the difference between a recommendation system that works and a
    matrix you cannot afford to store.''',
 edge_open='''Truncated SVD, randomised methods, and the numerical realities of decomposing large
    matrices.'''),

W+"4-calculus-the-chain-rule.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **A slope is all a derivative is** — nothing more intimidating than a hill
  - **Watch a curve reveal its slope** — in a moving picture
  - **The five rules you actually need** — and no others
  - **The chain rule** — the one idea that makes training possible
</Card>''',
 story='''{/* TERM LADDER: function → slope → derivative → chain rule → gradient */}

### How steep is it, right here?

Calculus has a reputation it does not deserve. For this course you need one idea and one rule,
and the idea is *how steep is this hill at the exact spot I am standing on*.

That is all a **derivative** is. On a flat stretch, zero. On a steep climb, a big number. Going
downhill, negative. If you can look at a hillside and say "steep here, flat there", you already
have the concept — the mathematics only makes it precise.

{/* ANIM:W11M4 */}

Then the one rule that matters for everything after this page, and it is beautifully simple.
Suppose an increase in **a** makes **b** grow twice as fast, and an increase in **b** makes **c**
grow three times as fast. How fast does **c** grow when **a** does? Two times three: six. You
multiply along the chain.

That is the **chain rule**, and it is not a footnote — it *is* how neural networks learn. When
Week 21 sends blame backwards through a stack of layers, each layer's share is its own local
effect multiplied by the blame arriving from ahead. That is this rule, applied over and over,
and it is the reason a model with a million parameters can be improved without guessing.
''',
 answer='''A derivative is **how steep the hill is at the exact point you are standing on** — zero on the
    flat, large on a climb, negative going down. And the chain rule is multiplication along a
    chain: if a changes b twice as fast and b changes c three times as fast, then a changes c six
    times as fast. That single rule is how blame travels backwards through the layers of a neural
    network, which is why training is possible at all.''',
 dangler='''
### The question this page leaves open

You can find the slope. Now use it: step downhill, again and again, until you reach the bottom.

It sounds foolproof and it is not. Step too far and you fly out of the valley; step too little
and you never arrive; and in more than one dimension the ground has shapes that trap you. Getting
that right is [Module 5 — Optimization](/curriculum/p2/week-11/5-optimization).
''',
 build_open='''You will not differentiate by hand at work, and you will read stack traces from autograd. This
    layer is what those traces are describing.''',
 edge_open='''Partial derivatives, the Jacobian, and what automatic differentiation is really doing to your
    function.'''),

W+"5-optimization.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Roll a ball down a curve** — and then break it on purpose
  - **Watch three step sizes: too big, too small, right** — in a moving picture
  - **The exact point where it diverges** — a threshold you can compute
  - **In two dimensions** — the valleys that make simple descent struggle
</Card>''',
 story='''{/* TERM LADDER: objective → step size → convergence → divergence → local minimum */}

### The ball and the bowl

Put a ball on the inside of a bowl and let go. It rolls to the bottom. That is optimisation, and
this page makes it precise enough to break.

You already have both pieces. The bowl is a function — high where the answer is bad, low where it
is good. The slope under the ball is the derivative from Module 4. So: look at the slope, take a
step downhill, look again, repeat.

{/* ANIM:W11M5 */}

Now break it deliberately, because this is where intuition is built. Take *huge* steps and the
ball does not settle — it flies up the far side, higher each time, and the numbers run away to
infinity. Take *tiny* steps and it creeps so slowly you give up first. Somewhere between is a
range that works, and for a simple curve you can compute exactly where the boundary sits.

Then two dimensions, where the trouble starts: a long narrow valley makes plain downhill steps
zig-zag from wall to wall instead of running along the floor. That specific annoyance is what
momentum in Week 21 exists to fix — and this is where you meet it first, in a picture small
enough to hold in your head.
''',
 answer='''Descent is **look at the slope, step downhill, repeat** — but the step size decides everything.
    Too large and each step overshoots so far that the value grows instead of shrinking, and the
    numbers run to infinity; too small and it converges so slowly you stop first. For a simple
    curve you can compute the exact threshold where that flip happens. And in more dimensions a
    long narrow valley makes plain descent zig-zag across it — the annoyance momentum is designed
    to remove.''',
 dangler='''
### The question this page leaves open

You now have the mathematics of *definite* things: an arrow is here, a slope is that, the step
converges or it does not.

The world is not definite. Will this customer buy? Did the change actually help, or were we
lucky? Reasoning honestly about things that vary is a different toolkit and the last piece of the
foundation: [Week 12 — Probability, statistics & experimentation](/curriculum/p2/week-12/index).
''',
 build_open='''Every "the model will not train" conversation is a conversation about this page's step size.''',
 edge_open='''Convergence rates, conditioning, and what convexity actually buys you when your loss surface
    is not convex.'''),
}
