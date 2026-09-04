W = "curriculum/p3/week-24/"
PAGES = {
W+"1-why-orchestration-exists.mdx": dict(
 glimpse='''<Card title="In this chapter — about 20 minutes" icon="sparkles">
  - **The container that died at 3 a.m.** — and nobody noticed until Monday
  - **Watch a dead copy get replaced** — automatically, in a moving picture
  - **What an orchestrator actually does** — four jobs, plainly
  - **Know when you do not need one** — the honest version
</Card>''',
 story='''{/* TERM LADDER: replica → desired state → scheduler → self-healing → orchestration */}

### The container that died at 3 a.m.

Week 23 ended with a container running on a machine. On Sunday at 3 a.m., that container died —
a memory spike, a bad request, a kernel hiccup. It does not matter which.

Nobody noticed until Monday morning, because there was nothing watching, and nothing to restart
it if anything had been.

{/* ANIM:W24M1 */}

Now imagine you say, once: *"I want three copies of this service running, always."* And then a
system takes responsibility for making that sentence true — forever. One dies? It starts
another. A whole machine catches fire? It moves the copies elsewhere. You want a new version?
It replaces them one at a time, keeping the service up throughout.

That is **orchestration**, and the shift is worth naming: you stop giving instructions ("start
this container here") and start declaring an outcome ("three of these should exist"). Everything
else this week follows from that one change of stance — including the honest section at the end,
about when a single machine is genuinely the right answer.
''',
 answer='''Nothing restarted it because **nothing had been told to care.** An orchestrator changes the
    stance: instead of instructions ("run this container here") you declare a desired state
    ("three copies of this, always"), and the system continuously works to make reality match —
    restarting dead copies, rescheduling when a machine dies, and rolling out new versions
    without dropping the service. That single shift is where its four jobs come from.''',
 dangler='''
### The question this page leaves open

"Three copies, always" is a promise — but how do you *write* it down, and how does traffic find
whichever copies happen to be alive at this moment, given they come and go and their addresses
change?

Those two questions are the working core of the tool, and they are
[Module 2 — Deployments, services & configuration](/curriculum/p3/week-24/2-deployments-services-configuration).
''',
 build_open='''Half of platform conversations are people talking past each other about what the orchestrator
    is for. This layer is the shared vocabulary — including permission to not use one.''',
 edge_open='''Control loops, the reconciliation model, and what actually happens when the desired state is
    impossible.'''),

W+"2-deployments-services-configuration.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Write down what you want** — declarative configuration in practice
  - **Watch traffic find a moving target** — service discovery, in a moving picture
  - **Rolling updates** — new version out, nobody notices
  - **Where secrets and settings belong** — not in your image
</Card>''',
 story='''{/* TERM LADDER: deployment → pod → service → config map → secret */}

### The address that keeps moving

You asked for three copies. The system starts them, and each gets its own address. Then one dies
and its replacement gets a *different* address. Then you scale to ten, and there are seven more.

So how does anything call this service without chasing a moving target?

The answer is a **stable name in front of the moving parts**. Callers talk to one fixed address;
behind it, a router keeps an up-to-date list of which copies are alive and healthy and passes
each request to one of them. The copies come and go freely. Nobody outside notices.

{/* ANIM:W24M2 */}

The same page covers the two things that turn this from a demo into a system. **Rolling
updates**: replace the copies one at a time, checking each new one is healthy before removing an
old one, so a deploy never takes the service down. And **configuration**: the same image should
run in test and production, so anything that differs — database URLs, API keys, the model
version — is injected from outside, never baked into the image where it becomes a leaked secret
in a registry.
''',
 answer='''Callers never chase moving copies because **a stable name sits in front of them**: one fixed
    address, behind which a router keeps a live list of healthy copies and forwards each request
    to one. Rolling updates use the same health knowledge — a new copy must prove itself healthy
    before an old one is removed, so deploys do not drop traffic. And configuration is injected
    from outside so one image runs everywhere; secrets baked into an image are secrets published
    to a registry.''',
 dangler='''
### The question this page leaves open

Copies exist and traffic finds them. Now the questions that decide your bill and your uptime:
**how big is each copy, and how many should there be right now?**

Ask for too little memory and the platform kills your model mid-request. Ask for too much and
you pay for idle silicon. And traffic is not constant. That is
[Module 3 — Resources, scheduling & autoscaling](/curriculum/p3/week-24/3-resources-scheduling-autoscaling).
''',
 build_open='''This is the layer where "we use Kubernetes" becomes something you can actually operate rather
    than something you inherit.''',
 edge_open='''Readiness versus liveness in a model service, and rollout strategies that survive a slow
    startup.'''),

W+"3-resources-scheduling-autoscaling.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The pod that keeps dying** — and the one-line reason
  - **Watch traffic double and copies follow** — autoscaling, in a moving picture
  - **Why scaling a model service is different** — the startup problem
  - **Set limits you can defend** — with measurements, not guesses
</Card>''',
 story='''{/* TERM LADDER: request → limit → OOM kill → autoscaling → cooldown */}

### The pod that keeps dying

Your service works for twenty minutes, then vanishes and restarts. No error in your logs. It
happens again. And again.

The cause is almost always the same, and it is not in your code: you told the platform your
container needed 2 GB of memory. Your model needs 3 GB the moment a large request arrives. The
platform, doing exactly what it was told, kills the container the instant it exceeds its limit.

That is the first half of this page: memory and CPU are things you **declare**, the platform
believes you, and being wrong looks like an unexplained crash.

{/* ANIM:W24M3 */}

The second half is scaling, where model services differ sharply from web services. A normal web
app scales in seconds. Your model service takes ninety seconds to start — load libraries, read
weights, warm up — so by the time your new copies are ready, the traffic spike is over and you
have paid for the wrong minute. Which is why scaling models is done on leading signals, with
generous cooldowns, and a floor of copies you keep warm.
''',
 answer='''The pod dies because **you declared how much memory it may use and the platform believes you** —
    exceed the limit and it is killed instantly, with nothing in your logs. So limits must come
    from measurements, including the worst-case request, not from a guess. Scaling a model
    service is different from scaling a web app for one reason: ninety seconds of startup means
    new copies arrive after the spike, so you scale on leading signals, keep a warm floor, and
    set cooldowns that stop it thrashing.''',
 dangler='''
### The question this page leaves open

You have been running a service you wrote yourself. But serving models is a solved problem that
somebody else has solved better — with batching, GPU sharing and model versioning built in.

Knowing when to hand that over, and what you give up by doing so, is
[Module 4 — Model serving frameworks](/curriculum/p3/week-24/4-model-serving-frameworks).
''',
 build_open='''Every ML platform has a story about a pod that died for a month before someone read the exit
    code. This layer is that exit code, explained.''',
 edge_open='''Scheduling with GPUs, bin-packing, and why memory limits behave differently from CPU
    limits.'''),

W+"4-model-serving-frameworks.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Batching, for free** — the throughput trick you should not write yourself
  - **Watch requests queue and go together** — in a moving picture
  - **Version and swap models without a redeploy** — what the frameworks buy you
  - **The honest trade** — what you give up when you stop hand-rolling
</Card>''',
 story='''{/* TERM LADDER: dynamic batching → model repository → versioning → throughput → GPU utilisation */}

### The bus and the taxis

Your FastAPI service processes requests one at a time. Ten requests arrive together; the GPU
handles them one after another, and — here is the waste — a GPU processing *one* request uses a
tiny fraction of its capacity. You are running a bus route with one passenger per bus.

**Dynamic batching** is the fix, and it is counter-intuitive: the server waits a few
milliseconds, gathers whatever requests arrive in that window, and runs them **through the model
together**. Ten requests can cost barely more than one. You add three milliseconds of latency
and multiply your throughput.

{/* ANIM:W24M4 */}

Writing that yourself is possible and unwise; the dedicated serving frameworks have it, along
with model versioning (load v2 alongside v1, shift traffic, roll back instantly — no redeploy),
multiple models sharing one GPU, and metrics you would otherwise build by hand.

The honest trade, which this page does not skip: another system to operate, another set of
failure modes, and less freedom to do something unusual in your request path.
''',
 answer='''A GPU serving one request at a time uses a fraction of its capacity — **dynamic batching**
    fixes that by waiting a few milliseconds, collecting whatever arrives, and running them
    through the model together, so ten requests cost barely more than one. That plus model
    versioning without redeploys, GPU sharing across models, and built-in metrics is what a
    serving framework buys. What you give up is simplicity: another system to operate and less
    freedom in your own request path.''',
 dangler='''
### The question this page leaves open

Everything is running: replicated, scaled, batched, versioned. And a model service has one more
category of problem, which no amount of infrastructure prevents.

The world changes. Your inputs slowly stop resembling the data you trained on, your accuracy
decays quietly, and no alert fires because nothing has *failed*. Operating a model — as opposed
to running a service — is [Module 5 — Operating an ML service](/curriculum/p3/week-24/5-operating-an-ml-service).
''',
 build_open='''"Should we use a serving framework?" is a real decision with a real cost. This layer is how to
    make it with numbers rather than fashion.''',
 edge_open='''Batching's effect on tail latency, and what happens when one enormous request meets a shared
    batch.'''),

W+"5-operating-an-ml-service.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The model that got worse and nothing broke** — drift, and why alerts miss it
  - **Watch the inputs change shape** — in a moving picture
  - **Monitor the data, not just the service** — the metrics nobody sets up first
  - **The retraining question** — when, on what, and who decides
</Card>''',
 story='''{/* TERM LADDER: data drift → concept drift → monitoring → retraining → model registry */}

### The silent decay

Your service has been up for eleven months. Uptime is 99.98%. No errors. Latency is flat. Every
dashboard is green.

And the model is now noticeably worse than the day you shipped it. Nobody has a ticket for it,
because **nothing failed.**

The world moved. Your customers are younger than the ones in the training data. A competitor
changed their pricing and shifted everyone's behaviour. A supplier renamed a product category
and a whole feature quietly became a different thing. The model kept answering — confidently,
and increasingly wrongly.

{/* ANIM:W24M5 */}

That is **drift**, and it is the failure mode unique to systems that learn. Ordinary monitoring
cannot see it: a request that returns 200 with a wrong answer looks exactly like a request that
returns 200 with a right one.

So you monitor a different thing: **the data itself** — the shape of the inputs and the
distribution of predictions, watched over time — plus whatever ground truth eventually arrives.
And then the decision this page ends on, which is organisational as much as technical: who
decides when to retrain, on what data, and who signs off that the new model is better.
''',
 answer='''Nothing alerted because **nothing failed** — a confidently wrong answer returns 200 exactly like
    a right one. What decayed was the match between the world and the training data: drift.
    Catching it means monitoring the *data* — input distributions and prediction mixes over time
    — plus whatever ground truth arrives later, rather than only uptime and latency. And the
    response is a decision, not a cron job: who retrains, on which data, and who certifies the
    new model is actually better.''',
 dangler='''
### Where this leaves you

That is the end of Phase 3 — and of the classical machine-learning craft.

You can build models from the arithmetic up, prove they are good without fooling yourself,
engineer the features that make them work, train networks, teach machines to see, and run all of
it as a service that other people depend on.

Which is exactly the foundation Phase 4 stands on. Everything from here — tokenizers,
Transformers, retrieval, agents — is these same ideas at a different scale:

- **[The Week 24 lab](/curriculum/p3/week-24/lab)** — operate a service properly, one last time.
- **[Week 25 — Tokenizers & Transformer internals](/curriculum/p4/week-25/index)** — the black box opens.
''',
 build_open='''This layer is what "owning a model in production" actually means once the launch excitement is
    over.''',
 edge_open='''Drift detection that does not cry wolf, and retraining cadences that are worth their cost.'''),
}
