W = "curriculum/p3/week-22/"
PAGES = {
W+"1-images-as-data-opencv.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **A photograph is a spreadsheet** — and you can prove it in three lines
  - **Watch a picture become numbers** — in a moving picture
  - **Why colour has three layers** — and why the order trips everyone once
  - **Load and manipulate real images** — pixel by pixel
</Card>''',
 story='''{/* TERM LADDER: pixel → channel → resolution → colour space → array shape */}

### A photograph is a spreadsheet

Open a photo of a cat. To you: a cat. To the machine: **a grid of numbers**, and nothing else.

Each little square of the picture — a **pixel** — is a brightness value, 0 for black, 255 for
white. A grey photo is one grid. A colour photo is three grids stacked: how much red, how much
green, how much blue at each position. That is the entire data structure. A 4-megapixel colour
photo is twelve million numbers in a box.

{/* ANIM:W22M1 */}

Which means every tool from Week 21 already applies — a network eats numbers, and this is
numbers. You can brighten a photo by adding 30 to every value, and blur it by replacing each
pixel with the average of its neighbours, and both are true arithmetic on a real image.

This page makes the abstraction concrete before any model appears, plus the practical detail
that catches everyone exactly once: the library that reads your image hands you the colour
channels in an unexpected order, and your beautiful cat comes out blue.
''',
 answer='''A photograph is **a grid of numbers** — one brightness value per pixel, and three stacked grids
    for colour (red, green, blue). That is the whole data structure, which is why the tools from
    Week 21 apply unchanged: a network eats numbers, and an image is numbers. Brightening is
    addition; blurring is replacing each pixel with an average of its neighbours. And the detail
    that catches everyone once: OpenCV hands you channels in BGR order, so an unconverted cat
    comes out blue.''',
 dangler='''
### The question this page leaves open

So feed those twelve million numbers into the network from Week 21. Two problems arrive
instantly.

First, the size: a fully-connected layer over twelve million inputs needs billions of
parameters. Second, and worse — **it does not know that a cat moved two pixels left is still a
cat.** It would have to learn "cat" separately for every possible position.

The network that solves both is [Module 2 — Convolutional neural networks](/curriculum/p3/week-22/2-convolutional-neural-networks).
''',
 build_open='''Half of "the model performs worse in production" for vision teams is a preprocessing
    mismatch — resize, channel order, normalisation. This layer is that surface.''',
 edge_open='''Colour spaces, interpolation choices when resizing, and the artefacts that quietly change
    what your model sees.'''),

W+"2-convolutional-neural-networks.mdx": dict(
 glimpse='''<Card title="In this chapter — about 30 minutes" icon="sparkles">
  - **A cat is a cat anywhere in the frame** — the idea that makes vision work
  - **Watch a filter slide** — edge detection, in a moving picture
  - **The same small window, reused everywhere** — a million parameters becoming a few hundred
  - **See what the early layers learn** — edges, then corners, then shapes
</Card>''',
 story='''{/* TERM LADDER: kernel → convolution → stride → feature map → pooling */}

### Looking through a small window

Here is how *you* find a cat in a photograph. Not by considering all twelve million pixels at
once — your eye moves, examining small patches, and recognises features wherever they happen to
be.

That is exactly the fix. Instead of connecting every pixel to every neuron, take a **small
window** — three pixels by three — and slide it across the whole image, applying the same
handful of numbers at every position. If that window has learned to detect a vertical edge, it
now detects vertical edges *everywhere*, for free.

{/* ANIM:W22M2 */}

Two enormous wins arrive together. **Parameters collapse**: one 3×3 window is nine numbers,
whether the image is a thumbnail or a poster. And **position stops mattering**: the cat is
recognised top-left or bottom-right, because the same detector visits both.

Stack these and something remarkable emerges, which you can actually look at: the first layer
learns edges, the next combines edges into corners and textures, the next into shapes, and by
the deep layers there are units that respond to faces and wheels. Nobody designed that hierarchy
— it falls out of training.
''',
 answer='''A convolution slides **one small window of weights across the whole image**, so a detector
    learned for a vertical edge finds vertical edges anywhere. That single idea buys both wins at
    once: parameters collapse (a 3×3 window is nine numbers regardless of image size) and
    position stops mattering (the same detector visits every location). Stacked, the layers build
    their own hierarchy — edges, then corners and textures, then shapes, then objects — which
    nobody designed and which you can inspect directly.''',
 dangler='''
### The question this page leaves open

You have an architecture. Training it is where new practitioners lose a week — because vision
models have their own well-worn traps: too little data, augmentation done wrong, batch
normalisation behaving differently at test time, and a GPU that sits idle while your data loader
struggles.

Getting a real one to train properly is
[Module 3 — Training a CNN properly](/curriculum/p3/week-22/3-training-a-cnn-properly).
''',
 build_open='''Convolutions are also why vision models are cheap enough to run on a phone. This layer is the
    arithmetic of that, and where the cost actually sits.''',
 edge_open='''Receptive fields, dilation, and what depthwise separable convolutions trade away.'''),

W+"3-training-a-cnn-properly.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Ten thousand photos is not many** — and the trick that makes it more
  - **Watch one image become twenty** — augmentation, in a moving picture
  - **The GPU that sits idle** — and why your bottleneck is probably not the model
  - **Train one to a real accuracy** — with numbers you can defend
</Card>''',
 story='''{/* TERM LADDER: augmentation → batch normalisation → schedule → data loader → checkpoint */}

### Ten thousand photos, and none of them enough

You have ten thousand labelled photos. It sounds like a lot. For a network with millions of
parameters, it is an invitation to memorise.

The classic fix is charming: **make more photos out of the ones you have.** Flip them. Rotate a
few degrees. Crop slightly differently. Adjust the brightness. A cat rotated seven degrees is
still a cat — you know that, and now the network sees fifty variations of every photo and cannot
memorise any single one.

{/* ANIM:W22M3 */}

But augmentation has a rule people break: the transformation must preserve the label. Flipping a
cat horizontally is fine. Flipping a photo of the digit **2** produces something that is not a
2, and teaching your model otherwise makes it worse.

The rest of this page is the practical craft: normalisation layers that behave *differently*
during training and testing (a bug people ship for months), schedules that decay the learning
rate, and the discovery that surprises everyone — your expensive GPU is often idle, waiting for
images to be loaded and decoded by the CPU.
''',
 answer='''Ten thousand photos becomes far more through **augmentation** — flips, small rotations, crops
    and brightness changes — because a rotated cat is still a cat, and the network can no longer
    memorise any single image. The rule people break is that the transformation must preserve the
    label: flipping a "2" does not give you a 2. And the usual bottleneck is not the model: the
    GPU frequently waits on the CPU decoding images, which is why data loading is where the easy
    speed-ups live.''',
 dangler='''
### The question this page leaves open

You can train a vision model — and you needed a lot of data and a lot of GPU hours to get a
mediocre one.

Meanwhile somebody has already trained a network on fourteen million images, and that network
has learned what edges, textures and shapes look like *in general*. Your problem is not
different from theirs in the early layers. Borrowing that work is
[Module 4 — Transfer learning](/curriculum/p3/week-22/4-transfer-learning).
''',
 build_open='''The gap between a tutorial CNN and a working one is entirely in this layer. It is also where
    a week of GPU budget is usually wasted.''',
 edge_open='''What batch norm actually does at test time, and the augmentation policies that beat
    hand-picked ones.'''),

W+"4-transfer-learning.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Somebody already did the hard part** — and you can have it
  - **Watch the early layers stay frozen** — in a moving picture
  - **Freeze or fine-tune?** — the decision, with the numbers behind it
  - **Beat your own model in twenty minutes** — with a hundredth of the data
</Card>''',
 story='''{/* TERM LADDER: pretrained model → frozen layers → feature extraction → fine-tuning → catastrophic forgetting */}

### Standing on somebody else's shoulders

Consider what a radiologist and a botanist have in common. Years of shared groundwork — how to
see, how edges and textures and shapes work — and only then, on top of that, the specialised
knowledge that makes them different.

Neural networks are the same, and it is measurable. Take a model trained on fourteen million
everyday photographs and look inside: the early layers learned edges and textures. Those are not
"cat" features — they are **vision** features, and your medical scans need exactly the same ones.

So do not start from random numbers. Take the trained network, **freeze the early layers**, and
replace only the final part with one that answers *your* question. You are keeping years of
someone else's compute and teaching only the last step.

{/* ANIM:W22M4 */}

The result routinely embarrasses models trained from scratch: better accuracy, a hundredth of
the data, twenty minutes instead of a week. This page is that recipe, the decision about how much
to unfreeze, and the risk when you unfreeze too eagerly — the model forgets what it knew, which
is exactly the catastrophic forgetting Phase 4 meets again with LoRA.
''',
 answer='''Transfer learning works because **the early layers of any vision model learn vision, not the
    task** — edges, textures and shapes are the same for everyday photos and medical scans. So you
    keep a pretrained network, freeze those layers, and retrain only the final part for your
    question: better accuracy than training from scratch, with a fraction of the data and time.
    Unfreeze too much, too fast, and the model overwrites what it knew — catastrophic forgetting,
    which Phase 4 meets again.''',
 dangler='''
### The question this page leaves open

Everything so far answers one question: *what is in this picture?* Real vision work asks
harder ones — **where** is it, how many are there, which pixels belong to it?

And then the question that ends this phase's model-building: your model is excellent, in a
notebook, on your laptop. How does it become something a phone or a server can actually run?
That is [Module 5 — Beyond classification & model export](/curriculum/p3/week-22/5-beyond-classification-model-export).
''',
 build_open='''Almost nobody trains vision models from scratch. This layer is the default professional
    workflow, and where it is right to break the default.''',
 edge_open='''Domain shift between the pretraining data and yours, and how much unfreezing actually pays
    for itself.'''),

W+"5-beyond-classification-model-export.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Where is it, not just what is it** — detection and segmentation, in one picture
  - **Watch a model leave the notebook** — export, in a moving picture
  - **The formats that let it run anywhere** — and what they give up
  - **Ship a model to something that is not your laptop**
</Card>''',
 story='''{/* TERM LADDER: detection → bounding box → segmentation → export → ONNX → quantization */}

### "What is in this picture" is the easy question

A classifier answers one thing: *cat*. Useful, and thin.

Real work asks more. A shop counting stock needs to know **how many** items and **where** each
one is — that is **detection**, and the answer is a set of boxes. A medical tool outlining a
tumour needs the **exact pixels** — that is **segmentation**. A self-driving car needs both,
thirty times a second. Same convolutions underneath, different heads on top and different
labels.

{/* ANIM:W22M5 */}

And then the last step of this phase's model work, and the one courses skip: **getting the model
out of the notebook.** It currently exists as Python plus a checkpoint file plus your exact
library versions — a fragile thing that runs only where you are sitting. Exporting it to a
portable format turns it into an artefact a phone app, a C++ service or a browser can run, with
no Python in sight.

That export is also where you meet quantization for the first time — the same idea that opens
Week 26, arriving here as "make it small enough to fit on a phone".
''',
 answer='''Classification says *what*; detection adds **where** (a set of boxes) and segmentation adds
    **which pixels** — the same convolutional backbone with different heads and different labels.
    Getting it out of the notebook matters just as much: a checkpoint plus your Python versions
    runs only where you sit, while an exported portable format runs in a phone app, a C++ service
    or a browser — and shrinking it for those targets is your first meeting with quantization,
    which returns in Week 26.''',
 dangler='''
### The question this page leaves open

You can now build models that see. The recurring theme of the last two modules is worth naming:
**a model in a notebook is not a product.**

It has no address. Nobody can call it. It cannot be updated, monitored or rolled back. Turning a
trained model into a service that other software can rely on is where Week 23 begins:
[Week 23 — From notebook to production service](/curriculum/p3/week-23/index).
''',
 build_open='''Export is where vision projects meet reality: a model that runs beautifully in a notebook and
    cannot be deployed is not finished. This layer finishes it.''',
 edge_open='''Detection architectures compared, and what export actually changes about your numerics.'''),
}
