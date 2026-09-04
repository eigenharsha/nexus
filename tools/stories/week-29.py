W = "curriculum/p4/week-29/"
PAGES = {
W+"1-what-an-agent-actually-is.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The recipe and the kitchen** — the one decision that matters most in agent work
  - **Watch the loop turn** — think, act, observe, repeat, in a moving picture
  - **Build a whole agent in forty lines** — no framework
  - **Know when NOT to build one** — the arithmetic that saves you a quarter
</Card>''',
 story='''{/* TERM LADDER: LLM → prompt → token → tool → agent loop */}

### The kitchen and the recipe

Everything so far has been a machine that answers. You ask, it answers, it forgets. Even with a
library card, that is all it is: one question, one answer, no hands.

Now imagine two ways of getting dinner.

**The recipe.** You wrote the steps yourself: chop, fry, plate. It runs the same way every
time. It cannot cope with a missing onion, but it will never set the kitchen on fire.

**The kitchen.** You hand someone the keys and say *"make dinner."* They open the fridge — no
onion — decide to walk to the shop, come back, and cook something you never specified. Vastly
more capable. Vastly harder to promise anything about.

That second one is an **agent**: the model is given tools, and *it* decides what to do next,
in a loop, until the job is done. And here is the sentence this whole week rests on — the one
that will save you a wasted quarter: **most business problems are recipes wearing a kitchen
costume.**

{/* ANIM:W29M1 */}

This page shows exactly what the loop is (it is smaller than you think), builds one in forty
lines with no framework, and gives you the arithmetic for choosing between the recipe and the
kitchen.
''',
 answer='''An agent is **a loop, not a personality**: send the conversation to the model; if it asked
    for a tool, run the tool yourself, append the result, and send again; if it did not, stop
    and return the answer. That is the whole mechanism — the model never runs anything, it only
    *asks*. And because each turn multiplies the chance of a wrong step, the honest default is
    the recipe: use a fixed chain when you know the steps, and a kitchen only when you genuinely
    cannot know them in advance.''',
 dangler='''
### The question this page leaves open

The loop only matters if the model can actually *do* something — and doing something means
tools: real functions in your code that the model may ask you to run.

Which raises questions with sharp edges. How do you describe a function so a model uses it
correctly? What happens when it invents an argument, or calls the same tool nine times in a
row, or asks you to delete something? That is
[Module 2 — Tools & function calling](/curriculum/p4/week-29/2-tools-function-calling).
''',
 build_open='''Leadership read about agents and wants one. You have six weeks. The most valuable thing
    this layer gives you is the confidence to say "this is a workflow, not an agent" — and the
    numbers to back it.''',
 edge_open='''Agent loops fail in ways single calls never do: compounding error, runaway cost, and the
    step that succeeded twice.'''),

W+"2-tools-function-calling.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Hand the model your functions** — and watch it choose the right one
  - **The schema is the instruction manual** — vague names, wrong calls
  - **When it invents an argument** — validation as the safety net
  - **The tool you should never expose** — and why deleting is different
</Card>''',
 story='''{/* TERM LADDER: tool → schema → tool call → validation → idempotency */}

### Handing over the keys

You are about to do something that should make you slightly nervous: let a language model
decide when to run your code.

The mechanism is gentler than it sounds. You write a normal function — `get_order(id)` — and
next to it a small card describing it: what it is called, what it does, what arguments it
needs. The model never touches your function. It reads the cards, and when it thinks one
applies, it *asks*: "please run `get_order` with id `TX-4471`". Your code decides whether to
obey.

So the whole quality of a tool-using agent comes down to the cards. A vague card — `run(x)`,
"runs a thing" — gets you a model guessing. A precise card gets you a model that calls the
right function with the right arguments and stops when it is done.

{/* ANIM:W29M2 */}

And then the sharp edges, which this page does not skip: the model will eventually invent an
argument that does not exist, call the same tool nine times, or cheerfully ask you to delete
a customer.
''',
 answer='''The model uses your code correctly because **the schema is the instruction manual, and it is
    the only thing the model can read.** Precise names, typed arguments and a one-line
    description of *when* to use each tool do more for reliability than any prompt engineering.
    Your code stays in charge: it validates every argument before executing, refuses what does
    not typecheck, and treats destructive tools as a different category entirely — confirmed,
    idempotent, and never handed over casually.''',
 dangler='''
### The question this page leaves open

Your agent can act now. Run it for ten minutes and you will meet the next wall: it forgets.
Every turn re-sends the whole conversation, the window fills with tool output, costs climb,
and eventually the earliest — often most important — instructions fall out the back.

An assistant that cannot remember what you told it five minutes ago is not much of an
assistant. Memory, and what to throw away, is
[Module 3 — Memory, context & state](/curriculum/p4/week-29/3-memory-context-state).
''',
 build_open='''The agent works in the demo and calls the wrong tool in front of a customer. Almost always
    the fix is not the model — it is the tool description nobody proofread. This layer is that
    craft, done properly.''',
 edge_open='''Tool calls are an attack surface. Everything here is about what happens when the arguments
    are hostile, or the result is.'''),

W+"3-memory-context-state.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The assistant with no short-term memory** — and the bill for pretending otherwise
  - **Three kinds of memory** — the window, the summary, the notebook
  - **What to throw away** — the decision nobody documents
  - **Give your agent a memory it can search** — with what you built in Week 27
</Card>''',
 story='''{/* TERM LADDER: context window → conversation history → summarisation → long-term memory */}

### The assistant who forgets everything

Your agent has hands now. It also has the memory of a goldfish.

Here is the uncomfortable truth about every chat model, including the famous ones: **there is
no memory.** Each turn, your program re-sends the entire conversation, and the model reads it
fresh, as if for the first time. The illusion of a continuing conversation is maintained
entirely by *you*, re-posting the transcript every single time.

That illusion has a price, and it grows. Turn fifty carries forty-nine turns of history —
including every long tool result — so each turn costs more than the last. Then you hit the
wall: the context window is finite, something must be dropped, and whatever falls out the back
is gone. Usually it is the beginning: the instructions that mattered most.

So the real job is not "add memory". It is **deciding what to forget** — and there are three
honest strategies, which this page walks through: keep the last N turns verbatim, replace old
turns with a summary, or write things down in a notebook you can search later (that notebook
is Week 27's retrieval, pointed inward).
''',
 answer='''The model does not remember anything — **your program re-sends the whole conversation every
    turn**, and the "memory" you feel is that transcript. So memory design is really deletion
    design: keep recent turns verbatim, compress older ones into a running summary, and push
    durable facts into a searchable store you retrieve from on demand. Get it wrong and you pay
    for the same history repeatedly while the instructions that mattered fall silently out of
    the window.''',
 dangler='''
### The question this page leaves open

Your agent thinks, acts and remembers. Now you want it to use the tools your company already
runs — the ticket system, the database, the file server — and you write a bespoke adapter for
each one. So does every other team. Everyone rewrites the same glue, badly.

That is a plug problem, and plug problems are solved with a standard shape. That is
[Module 4 — Model Context Protocol](/curriculum/p4/week-29/4-model-context-protocol-mcp).
''',
 build_open='''Costs grow linearly with conversation length and nobody notices until the invoice. This
    layer is the compaction strategy that keeps long sessions affordable and coherent.''',
 edge_open='''Summarisation is lossy compression applied to the thing your product depends on. Everything
    here is about what gets lost and when it matters.'''),

W+"4-model-context-protocol-mcp.mdx": dict(
 glimpse='''<Card title="In this chapter — about 20 minutes" icon="sparkles">
  - **The adapter drawer** — why everyone rewrote the same glue
  - **One plug shape for tools** — what MCP actually standardises
  - **Run a server, connect a client** — the whole handshake, seen once
  - **The trust question** — what a third-party tool server can do to you
</Card>''',
 story='''{/* TERM LADDER: MCP → server → client → transport → capability */}

### The drawer full of adapters

Everyone has that drawer. Chargers, dongles, adapters for devices nobody owns any more — a
different plug for every gadget, none of them interchangeable.

Agent tooling grew up exactly like that. Your team wrote an adapter so your agent could read
Jira. Another team wrote a different adapter for the same Jira. The vendor wrote a third. Each
one hand-rolled, separately maintained, subtly different.

Then someone did the boring, valuable thing: agreed a **plug shape**. A small protocol saying
how a program offers tools, how an agent discovers them, and how they talk. Write your tool
server once, and any agent that speaks the protocol can use it — no bespoke adapter. That is
the **Model Context Protocol**, and this page is the whole handshake, watched once, slowly.

The last section is the one to read carefully: a tool server is code you did not write,
running with your agent's trust.
''',
 answer='''MCP is **a standard plug shape for tools**: a server advertises what it can do, a client
    (your agent) discovers those capabilities at connect time and calls them over one agreed
    transport. Write the server once and any compliant agent can use it — the adapter drawer
    stops filling up. The price is trust: a tool server is someone else's code inside your
    agent's loop, and its *results* enter your context as text the model will read and act on.''',
 dangler='''
### The question this page leaves open

Your agent now loops, acts, remembers, and plugs into everyone's tools. And it is still held
together by strings: a prompt, a dict of functions, some hopeful parsing, and a wish that the
model returns the right shape.

That is fine for a demo and unpleasant at 3 a.m. What does an agent look like when it is built
like real software — typed, tested, and boring to debug? That is
[Module 5 — Pydantic AI & typed agents](/curriculum/p4/week-29/5-pydantic-ai-typed-agents).
''',
 build_open='''"Can our agent use our internal tools?" is a question with a bad answer (write ten adapters)
    and a good one (speak the protocol once). This layer is the good one, wired end to end.''',
 edge_open='''Protocols are attack surfaces with documentation. Everything here concerns what arrives
    through a server you do not control.'''),

W+"5-pydantic-ai-typed-agents.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **From strings and hope to types and tests** — an agent built like software
  - **Guarantee the shape of the answer** — validated, or retried automatically
  - **Test an agent without paying for it** — dependency injection and fakes
  - **The whole week, assembled** — loop, tools, memory, types
</Card>''',
 story='''{/* TERM LADDER: typed agent → dependency injection → validation → retry → observability */}

### Strings and hope

Look honestly at the agent you have built this week. A prompt held in a string. A dictionary of
functions. Some parsing that assumes the model returns what you asked for. An `except` block
that shrugs.

Now imagine explaining that to the engineer who has to fix it at 3 a.m., or writing a test for
it that does not cost money every run.

Ordinary software solved this a long time ago: **declare the shape, validate at the boundary,
inject what the code depends on, and test with fakes.** Nothing about a language model makes
those ideas stop working — they simply were not applied at first, because agents arrived as
scripts.

This page is the grown-up version. The answer has a declared type; if the model returns
something else, the framework hands it back and asks again — automatically. Tools declare
their dependencies instead of reaching for globals. And the whole agent can run in a test
suite, offline, in milliseconds.
''',
 answer='''You make an agent boring to debug by **treating the model as one more untrusted boundary**:
    declare the output type, validate every response against it, and let the framework retry
    automatically when the shape is wrong. Inject dependencies rather than reaching for globals,
    so the same agent runs against a fake model in a test suite — offline, in milliseconds, for
    free. Strings and hope work in a demo; types and tests are what run on a Tuesday.''',
 dangler='''
### The question this page leaves open

You can now build one agent that is genuinely production-shaped: it loops, uses tools safely,
remembers what matters, plugs into standard servers, and is typed and testable.

One agent. But real work is rarely one worker — it is a research step feeding a drafting step
feeding a review step, some running in parallel, any of which can fail halfway through a
two-hour job. Coordinating many, and surviving failure, is Week 30:
[Week 30 — Multi-agent systems & durable execution](/curriculum/p4/week-30/index).
''',
 build_open='''The prototype is a script; the thing on call must be software. This layer is that
    conversion, with the framework that makes it short.''',
 edge_open='''Type systems meet a probabilistic component. Everything here is about where the guarantees
    genuinely hold and where they only look like they do.'''),
}
