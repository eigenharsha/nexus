W = "curriculum/p3/week-23/"
PAGES = {
W+"1-from-notebook-to-service.mdx": dict(
 glimpse='''<Card title="In this chapter — about 20 minutes" icon="sparkles">
  - **A model with no address** — why a notebook is not a product
  - **Watch a model gain a phone number** — in a moving picture
  - **Everything that was implicit becomes explicit** — versions, inputs, failure
  - **The gap, named** — so the next four modules have a point
</Card>''',
 story='''{/* TERM LADDER: notebook → service → endpoint → request/response → contract */}

### A brilliant employee with no phone

Imagine hiring someone extraordinary who has no phone, no email, no desk, and who only works
when you are personally standing next to them.

That is your model right now. It exists inside a notebook, on your laptop, in a Python session
that dies when you close the lid. Nobody else can use it. No other software can call it. It has
no address.

{/* ANIM:W23M1 */}

Turning it into a **service** changes exactly one thing conceptually — it gets an address other
programs can send requests to — and about ten things practically. Everything you did implicitly
in the notebook now has to be written down: which model version is loaded, what a valid input
looks like, what happens when the input is invalid, how long a caller may wait, and what happens
when two hundred callers arrive at once.

This page is that gap, named precisely, so the rest of the week has a point.
''',
 answer='''A model in a notebook has **no address**: it cannot be called by other software, it dies with
    your Python session, and everything about it is implicit. A service gives it one — and forces
    everything implicit to become explicit: the model version loaded, what a valid input is, what
    happens on an invalid one, the timeout a caller can expect, and the behaviour when many
    callers arrive at once. That list is the whole of this week.''',
 dangler='''
### The question this page leaves open

So give it an address. In Python that means a web framework, and the choice matters less than
how you use it — because a model service has three specific problems ordinary web services do
not: the model is enormous and must be loaded exactly once, predictions can be slow, and inputs
must be validated before they reach a tensor.

Building that properly is [Module 2 — Serving with FastAPI](/curriculum/p3/week-23/2-serving-with-fastapi).
''',
 build_open='''"Can we call your model from the app?" is the question that ends the notebook phase of every
    project. This layer is what that question actually asks for.''',
 edge_open='''Where the notebook-to-service boundary hides assumptions that only fail in production.'''),

W+"2-serving-with-fastapi.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Load the model once, not per request** — the mistake that costs 100× latency
  - **Validate before the tensor** — bad input should never reach your model
  - **Health checks that tell the truth** — including “model not loaded yet”
  - **Serve your Week 22 model** — properly, with tests
</Card>''',
 story='''{/* TERM LADDER: route → schema validation → lifespan → concurrency → health check */}

### The service that reloads the model every time

Here is the first mistake almost everyone makes, and it is instructive because the code looks
perfectly reasonable:

```
def predict(request):
    model = load_model("model.pt")   # ← inside the handler
    return model(request.data)
```

That works in testing and is catastrophic in production: every single request spends two seconds
loading a 400 MB file from disk before doing 20 milliseconds of actual work. Load it **once**,
when the service starts, and keep it in memory.

{/* ANIM:W23M2 */}

The second habit is defensive and cheap: **validate the input before it gets anywhere near your
model.** A request with a missing field, a string where a number belongs, or a 4-gigabyte image
should be rejected at the door with a clear error — not deep inside a tensor operation with a
stack trace nobody can read.

And the third: a health check that actually knows whether the model finished loading, because a
service that answers "I'm fine" while its model is still warming up will be sent traffic it
cannot serve.
''',
 answer='''Load the model **once at startup**, not per request — the reasonable-looking version spends two
    seconds loading a file to do twenty milliseconds of work, and it only shows up under load.
    Validate every input at the door, so bad requests get a clear error instead of a tensor stack
    trace. And make the health check tell the truth about whether the model is actually loaded,
    or the platform will route traffic to a service that cannot yet serve it.''',
 dangler='''
### The question this page leaves open

Your service runs beautifully — on your machine, with your Python version, your CUDA drivers and
the seventeen libraries you installed over three months.

Hand it to a colleague and it breaks. Deploy it to a server and it breaks differently. The
answer to "it works on my machine" is to ship the machine, which is
[Module 3 — Docker](/curriculum/p3/week-23/3-docker).
''',
 build_open='''This layer is the difference between a demo endpoint and a service someone will put in front
    of customers.''',
 edge_open='''Async versus threads for a blocking model call, batching inside a request handler, and where
    the GIL bites.'''),

W+"3-docker.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **“It works on my machine”** — and how to ship the machine
  - **Watch an image build in layers** — in a moving picture
  - **Why your image is 6 GB** — and how it becomes 900 MB
  - **Containerise your service** — and run it somewhere that is not your laptop
</Card>''',
 story='''{/* TERM LADDER: image → container → layer → Dockerfile → multi-stage build */}

### Shipping the machine

The oldest joke in software: *"it works on my machine."* The modern answer: *"then we will ship
your machine."*

A **container** is your application plus everything it needs to run — the Python version, the
libraries, the system packages, the model file — packaged as one artefact that behaves
identically on your laptop, your colleague's, and a server in Frankfurt. Not a virtual machine:
it shares the host's kernel, so it starts in a second rather than a minute.

{/* ANIM:W23M3 */}

The mechanism worth understanding is **layers**. Your image is built as a stack of read-only
slices — the base OS, then the Python install, then your dependencies, then your code — and
anything unchanged is reused from cache. Order those lines badly and every code change
reinstalls every dependency; order them well and rebuilds take four seconds.

The page ends with the file everybody's first Dockerfile produces: six gigabytes, containing a
compiler toolchain, test files and pip's cache — and the two-stage trick that reduces it to a
tenth.
''',
 answer='''A container is **the machine, shipped**: your code, the exact Python and libraries, system
    packages and the model file, in one artefact that behaves the same on any host — sharing the
    kernel, so it starts in a second. The mechanism is layers: each instruction is a cached
    read-only slice, so dependencies must be installed *before* your code is copied, or every
    edit reinstalls everything. And a multi-stage build leaves the compilers and caches behind,
    turning a 6 GB first attempt into a few hundred megabytes.''',
 dangler='''
### The question this page leaves open

You can build an image on your machine and run it anywhere. Notice the phrase: *on your machine*.

Which means the build depends on you remembering to do it, correctly, every time — and that
someone else's change goes out untested unless a human is diligent. That is not a system; that
is a habit. Replacing the habit with a machine is
[Module 4 — CI/CD](/curriculum/p3/week-23/4-ci-cd).
''',
 build_open='''Slow, fat images are one of the most common quiet costs in an ML platform. This layer is where
    that is decided.''',
 edge_open='''Layer caching in CI, base image choice for CUDA, and what actually needs to be inside the
    image versus mounted.'''),

W+"4-ci-cd.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The tests nobody ran** — because running them was somebody's job
  - **Watch a push become a deployment** — in a moving picture
  - **The gates worth having** — and the ones that only slow you down
  - **Build the pipeline** — tests, image, deploy, on every push
</Card>''',
 story='''{/* TERM LADDER: pipeline → trigger → stage → artifact → rollback */}

### The Friday deploy

Every team has the story. Someone deployed on a Friday afternoon, from their laptop, with an
uncommitted change and tests they meant to run. It was fine. It was fine four more times. Then
it was not fine, at 6 p.m., with the person who understood it already on a train.

The fix is not discipline — discipline is a person, and people have trains to catch. The fix is
to make the boring path automatic: **push your code, and a machine runs the tests, builds the
image, and deploys it.** Every time, identically, whether it is Tuesday morning or Friday
evening.

{/* ANIM:W23M4 */}

For a model service the pipeline earns its keep twice over, because there is more that can
silently rot: the code, yes, but also whether the model file still loads, whether the container
still builds, and whether the endpoint still answers correctly after the change.

And the part that matters most when it goes wrong: a pipeline that can deploy in three minutes
can also **roll back** in three minutes, which is what turns a bad release from a crisis into an
inconvenience.
''',
 answer='''You stop relying on discipline by **making the boring path automatic**: a push triggers the
    tests, the image build and the deploy, identically every time, with no human choosing which
    steps to skip. For a model service the pipeline also checks what silently rots — that the
    model file still loads and the endpoint still answers correctly. And its most valuable
    property is symmetric: a pipeline that deploys in three minutes can roll back in three,
    which turns a bad release into an inconvenience.''',
 dangler='''
### The question this page leaves open

Your service is containerised and deploys itself. It is also running on a machine you rented,
which you pay for at 3 a.m. when nobody is using it, and which will fall over the day something
gets popular.

There is a way to run code where you pay only for the milliseconds you use and someone else
handles the machines — with sharp trade-offs for models. That is
[Module 5 — Serverless deployment](/curriculum/p3/week-23/5-serverless-deployment).
''',
 build_open='''This layer is what separates a project people are afraid to change from one where a fix goes
    out in ten minutes.''',
 edge_open='''Pipeline design for expensive artefacts: caching, GPU runners, and testing a model without
    retraining it.'''),

W+"5-serverless-deployment.mdx": dict(
 glimpse='''<Card title="In this chapter — about 20 minutes" icon="sparkles">
  - **Pay for the milliseconds, not the machine** — the promise
  - **The cold start** — the catch, measured in seconds
  - **Watch a request wake a sleeping function** — in a moving picture
  - **The honest decision table** — when serverless suits a model, and when it does not
</Card>''',
 story='''{/* TERM LADDER: serverless → invocation → cold start → memory limit → scale-to-zero */}

### The taxi and the company car

A rented server is a company car. You pay for it every hour of every day, including the
fourteen hours nobody drives it — and if forty people suddenly need a lift, you have one car.

**Serverless** is a taxi. Code sits dormant, costing nothing. A request arrives, a machine spins
up, runs your function, and shuts down. Ten thousand requests? Ten thousand taxis, automatically.
No requests overnight? No bill.

{/* ANIM:W23M5 */}

For a model, that promise meets a specific catch: **the cold start.** When a request arrives at
a sleeping function, the platform must start a container, load your dependencies, and — this is
the painful part — read a 400 MB model file before it can answer. The first user waits several
seconds. If your traffic is spiky, that is *many* users waiting.

So the decision is not ideological, it is arithmetic: bursty, occasional, small-model workloads
suit taxis; steady traffic and heavy models suit the company car. This page gives you the
numbers to choose with.
''',
 answer='''Serverless is a taxi rather than a company car: **you pay per invocation and nothing at all when
    idle**, and it scales to thousands of concurrent requests without you managing machines. The
    catch for models is the cold start — a sleeping function must boot a container, import the
    libraries and read a large model file before the first answer, which costs seconds. So it
    suits bursty, intermittent traffic with modest models, while steady load and heavy models are
    cheaper and faster on a machine that stays warm.''',
 dangler='''
### The question this page leaves open

You can now ship a model as a service, in a container, deployed automatically, on a rented
machine or a serverless platform.

One thing is still missing, and it appears the moment you have more than one of anything: who
decides *how many* copies run, on which machines, what happens when one dies at 3 a.m., and how a
new version goes out without dropping a request? That is Week 24:
[Week 24 — Orchestration & production ML operations](/curriculum/p3/week-24/index).
''',
 build_open='''Serverless for ML is a genuinely good fit for a narrow band of workloads and a trap outside it.
    This layer is the band, with numbers.''',
 edge_open='''Cold-start mitigation, memory-to-CPU coupling, and the total cost curve where serverless stops
    winning.'''),
}
