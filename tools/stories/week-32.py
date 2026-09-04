W = "curriculum/p4/week-32/"
PAGES = {
W+"1-tracing-opentelemetry.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **"It was slow for one customer"** — the ticket you cannot answer today
  - **Watch one request become a trace** — every step, timed, in a moving picture
  - **Spans, traces and context** — the vocabulary, earned rather than dumped
  - **Instrument your own pipeline** — and find your slowest step in ten minutes
</Card>''',
 story='''{/* TERM LADDER: span → trace → parent → context propagation → attribute */}

### "It was slow yesterday"

A customer writes: *"Your assistant took thirty seconds yesterday afternoon."*

Go and find out why. Your logs say the request arrived and the request finished. Between those
two lines lived a retrieval, a re-rank, three tool calls and two model calls — and you have no
idea which one took twenty-eight of those thirty seconds. Was the vector search slow? Did a
tool hang? Did the model just take its time?

You cannot answer, and the reason is worth naming: **you logged events, not the shape of the
work.** Logs are diary entries. What you need is a stopwatch on every step, with all the
stopwatches tied together by the one request they belong to.

{/* ANIM:W32M1 */}

That is a **trace**: one request, drawn as nested bars, each step showing exactly when it
started and how long it took. Look at that picture for the customer's slow request and the
answer is not deduced — it is *seen*.
''',
 answer='''You cannot answer "why was it slow" because **logs record events while a trace records the
    shape of the work.** A span is one timed step with a name and attributes; a trace is all the
    spans for one request, linked parent-to-child by a context that travels with the call. Drawn
    as nested bars, the slow step stops being a deduction and becomes something you point at —
    which is why instrumenting the pipeline is the first thing you do in production, not the
    last.''',
 dangler='''
### The question this page leaves open

You can see your pipeline's timing now. But an AI system has questions that generic tracing
never asks: what exactly was in the prompt for this call? What did it cost? Which prompt
version was live? Was this answer good?

Those need a tool that understands models, not just spans. That is
[Module 2 — Langfuse & the LLM observability stack](/curriculum/p4/week-32/2-langfuse-the-llm-observability-stack).
''',
 build_open='''The first production performance ticket you receive will be unanswerable without this
    layer, and trivially answerable with it. That is the whole argument.''',
 edge_open='''Sampling, cardinality and cost: instrumentation that is itself an outage waiting to
    happen.'''),

W+"2-langfuse-the-llm-observability-stack.mdx": dict(
 glimpse='''<Card title="In this chapter — about 20 minutes" icon="sparkles">
  - **The questions only an AI system asks** — prompt, tiles, cost, quality
  - **See the actual prompt that produced a bad answer** — not a reconstruction
  - **Trace, score, compare** — evaluation wired into what is really happening
  - **Wire it up once** — and stop guessing about production
</Card>''',
 story='''{/* TERM LADDER: observation → generation → session → score → prompt version */}

### The screenshot with no explanation

Someone forwards you a screenshot of a wrong answer. No request id, no timestamp, nothing but
the text.

Your generic tracing tells you a model call happened and took 1.4 seconds. It cannot tell you
what you actually need: **what was in that prompt.** Which passages did retrieval put in?
Which prompt version was live? How many tiles went in and came out, and what did that cost?
Did this user then ask the same thing again — the sure sign of an unhelpful answer?

Those are not generic questions, and generic tools do not answer them. Model-aware
observability records the *whole* call: prompt in, answer out, tiles, cost, latency, prompt
version, and the eval score from Week 31 attached to the same record.

Which turns a screenshot into a link, and an argument into a lookup.
''',
 answer='''Generic tracing cannot debug a bad answer because **it records that a call happened, not what
    was in it.** Model-aware observability stores the whole generation — the exact prompt with
    the retrieved passages, the output, tiles in and out, cost, latency and prompt version —
    and lets Week 31's eval scores attach to those same records. Now "why did it say that?"
    becomes a lookup, and "did last week's prompt change help?" becomes a comparison on real
    traffic rather than a debate.''',
 dangler='''
### The question this page leaves open

You can now see everything: how long each step took, what every prompt contained, and what
each call cost.

That last number is about to become somebody's problem. When Finance asks why the AI line item
tripled, "we added a feature" is not an answer, and the fix is rarely "use a cheaper model".
Taking real money out of a working system is
[Module 3 — Cost engineering](/curriculum/p4/week-32/3-cost-engineering).
''',
 build_open='''"Can you find the trace for this screenshot?" is a question you either answer in ten seconds
    or not at all. This layer decides which.''',
 edge_open='''Storing every prompt is a privacy decision as much as an engineering one.'''),

W+"3-cost-engineering.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Where the money actually goes** — measured, and rarely where you guessed
  - **Watch a bill get cut in half** — without changing the model, in a moving picture
  - **The four levers** — cache, shorten, route, batch
  - **Report a cost per answered question** — the number Finance asks for
</Card>''',
 story='''{/* TERM LADDER: unit cost → cost per request → routing → context trimming → batching */}

### The invoice with no story

Finance sends the invoice. The AI line tripled last month, and the question is simple: *why?*

Most teams cannot answer, so they reach for the obvious lever and switch to a cheaper model —
which usually makes quality worse and the bill only slightly better, because the cheaper model
was never where the money was.

Here is what the data usually shows once you look (and after Module 2, you can look): a large
share of spend goes on **re-sending the same context** — the same system prompt, the same
retrieved passages, the same conversation history, again and again. Another large share goes
on questions that were **already answered** this morning. And a share goes on using an
expensive model for work a small one does perfectly.

{/* ANIM:W32M3 */}

So cost engineering is not haggling over model prices. It is four levers — cache what repeats,
shorten what you re-send, route easy work to small models, batch what is not urgent — applied
in the order the data tells you, and reported as one honest number: **cost per answered
question.**
''',
 answer='''You halve the bill without changing the model because **most of the spend is repetition, not
    intelligence** — the same system prompt, passages and history re-sent every turn, and
    questions already answered this morning. The four levers, in the order the data usually
    prefers: cache exact and prefix repeats, trim what you re-send, route easy work to small
    models, and batch what is not urgent. Report it as cost per answered question, because that
    is the number Finance can compare against value.''',
 dangler='''
### The question this page leaves open

Cheap and observable. Now Tuesday happens: p95 latency triples for no visible reason, one
dependency slows down, and the queue backs up while users watch a spinner.

Being cheap is not the same as being dependable, and the two sometimes pull in opposite
directions. Keeping a probabilistic system fast and reliable is
[Module 4 — Reliability, latency & production operations](/curriculum/p4/week-32/4-reliability-latency-production-operations).
''',
 build_open='''You will be asked to cut AI spend by 40% without losing quality. This layer is how that is
    actually done — and why the first suggestion in the room is usually the wrong lever.''',
 edge_open='''Cost and quality trade against each other continuously. Everything here is about making that
    trade explicit instead of accidental.'''),

W+"4-reliability-latency-production-operations.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The Tuesday when p95 tripled** — and how you would find out why
  - **Averages lie** — percentiles, and the user you are actually failing
  - **Streaming changes the feeling, not the number** — and why that matters
  - **What to alert on** — and what to let sleep
</Card>''',
 story='''{/* TERM LADDER: percentile → p95 → SLO → error budget → alert */}

### The average customer is fine

Your dashboard says average response time is 2.1 seconds. Everything looks healthy.

Now stand behind one real user. Their question needed three tool calls, a big retrieval and a
long answer; it took eleven seconds; they refreshed twice and left. The average never noticed
them, because averages are excellent at hiding the people you are failing.

That is why production is measured in **percentiles**. p50 is the typical experience; **p95**
is the slow tail your angriest users live in; p99 is where the tickets come from. When
somebody says "it got slow", they nearly always mean the tail moved — and averages will keep
insisting nothing happened.

Then there is a wrinkle unique to this field: your system *streams*. The first word appears in
400 milliseconds and the answer finishes in nine seconds. Which number is the latency? Both —
one describes how it *feels*, the other what it *costs* — and this page is what to measure, what
to promise, and what deserves to wake somebody up.
''',
 answer='''Averages hide the users you are failing, so production quality is measured in **percentiles**:
    p50 for the typical experience, p95 and p99 for the tail where complaints are born. In a
    streaming system you measure two different things — time to first token (how fast it *feels*)
    and total time (what it *costs*) — and promise them separately. Alert on the tail breaching
    the promise you actually made, not on averages, and spend the error budget deliberately
    rather than discovering it is gone.''',
 dangler='''
### The question this page leaves open

Instrumented, affordable, dependable. One thing remains, and it is the difference between a
project and a product: **shipping it, then keeping it alive.**

Models get deprecated. Prompts need versioning like code. Your corpus changes under a live
index. And someone has to be able to fix it at 3 a.m. with a runbook they did not write. That
is the last module of Phase 4:
[Module 5 — Deploying & maintaining an AI system](/curriculum/p4/week-32/5-deploying-maintaining-an-ai-system).
''',
 build_open='''The first "it got slow" incident is where AI features lose their sponsors. This layer is the
    measurement and the vocabulary that gets you through it.''',
 edge_open='''Tail latency in a system whose slowest component is a model you do not control.'''),

W+"5-deploying-maintaining-an-ai-system.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The email that deprecates your model** — with ninety days' notice
  - **Prompts are code** — versioned, reviewed, rolled back
  - **Ship changes safely** — canaries and shadow traffic for a non-deterministic system
  - **Write the runbook** — for the person who is not you, at 3 a.m.
</Card>''',
 story='''{/* TERM LADDER: deployment → prompt version → canary → shadow traffic → runbook */}

### The email you will get

One Tuesday, an email arrives from your model provider. The version you built on is deprecated;
you have ninety days.

Nothing is broken. Nobody made a mistake. This is simply what living on someone else's model
is like — and it is the perfect illustration of why the last module of this phase is not about
building anything. Everything in Phase 4 has been about making a system *work*. This page is
about keeping it working after you stop paying attention.

Four habits do most of it. **Prompts are code** — versioned, reviewed, and rollback-able, since
a prompt edit is a production change with no compiler to catch it. **Changes ship carefully** —
to a small slice first, or as shadow traffic scored against the live version, because you
cannot diff a non-deterministic system. **The corpus is maintained** — documents change,
indexes go stale, and yesterday's excellent retrieval quietly rots. And **someone else can fix
it** — a runbook naming the symptoms, the dashboards, the levers and the rollback.

That last one is the difference between a system and a hostage situation.
''',
 answer='''A system stays alive by **treating everything unversioned as a future outage**: prompts are
    code with reviews and rollbacks, model versions are pinned and their deprecations diarised,
    corpus and indexes are rebuilt on a schedule rather than when someone complains, and every
    change ships to a slice or as shadow traffic first because you cannot diff a
    non-deterministic system. And it is finished only when someone who is not you can fix it at
    3 a.m. from the runbook.''',
 dangler='''
### Where this leaves you

That is the end of Phase 4 — and of the road you started in Week 1.

Look back at what you can now do. You can explain what happens between a person typing a
sentence and a model answering it, in bytes and tiles. You have built the tokenizer and the
Transformer with your own hands. You have shrunk a model onto your own hardware, taught it with
sticky notes, given it your documents, given it tools, made it survive failure, measured it
honestly, defended it against a hostile user, and run it for real money.

There is no more room in the building you have not seen.

- **[The Week 32 lab](/curriculum/p4/week-32/lab)** — ship the whole thing, instrumented and
  operable.
- **[Your capstone](/projects/capstone)** — the system you defend under hostile questioning,
  and the strongest thing in your portfolio.
''',
 build_open='''This layer is written for the version of you who inherits this system in six months — which,
    statistically, is also you.''',
 edge_open='''Long-lived AI systems fail in slow ways: drift, rot and deprecation. Everything here is
    about the failures that take months to arrive.'''),
}
