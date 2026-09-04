W = "curriculum/p4/week-30/"
PAGES = {
W+"1-graphs-as-the-right-abstraction.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **When one worker is not enough** — and why a to-do list is the wrong shape
  - **Draw the work as a map** — nodes, edges, and what must finish before what
  - **Watch a graph run** — branches in parallel, in a moving picture
  - **The shape that makes resuming possible** — a hint about Wednesday's 3 a.m. failure
</Card>''',
 story='''{/* TERM LADDER: node → edge → dependency → graph → state */}

### The job that is not a list

Your agent from Week 29 is one worker with one loop. Now look at an actual piece of work —
say, producing a market report:

*Research three competitors. Pull our own numbers. Draft a section on each. Have a reviewer
check them. Assemble. Send.*

Read that again and notice something: **it is not a list.** The three competitor researches
have nothing to do with each other — they could all happen at once. Drafting cannot start
before its research finishes. The review depends on the drafts. Assembly waits for everything.

That is not a to-do list. That is a **map**: boxes of work, with arrows saying *this must
finish before that starts*. In computing, a map like that is a **graph** — nodes joined by
edges — and it is the honest shape of nearly all real work.

{/* ANIM:W30M1 */}

Drawing the work as a graph buys you three things at once, and this page is about all three:
things that do not depend on each other run **in parallel**; the work has an explicit
**state** you can look at; and — Wednesday's problem — when step seven of nine dies at 3 a.m.,
you know precisely which steps already finished.
''',
 answer='''Real work is a graph, not a list, because **the dependencies are the truth and the ordering is
    just one flattening of them.** Nodes are units of work, edges say what must finish first,
    and everything not joined by an edge can run at the same time. The shape pays three ways:
    parallelism you get for free, a state you can inspect while it runs, and — the one that
    matters at 3 a.m. — a precise record of which nodes already succeeded.''',
 dangler='''
### The question this page leaves open

You can draw the work. Now, who does each node? One agent wearing different hats, or several
specialists — a researcher, a writer, a critic — each with its own tools and instructions?

Both are used in production, they fail differently, and the fashionable answer is usually the
wrong one. That is
[Module 2 — Multi-agent patterns](/curriculum/p4/week-30/2-multi-agent-patterns).
''',
 build_open='''The prototype is one agent with a very long prompt, and adding the sixth capability broke
    the third. This layer is the refactor: make the work a graph before it becomes folklore.''',
 edge_open='''Graph execution engines all look alike in a diagram and differ where it matters: state,
    concurrency and failure.'''),

W+"2-multi-agent-patterns.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **One generalist or a team of specialists** — measured, not preferred
  - **The four patterns that actually ship** — and the one everyone tries first
  - **The cost of a conversation between agents** — every handoff is tiles
  - **When two agents are genuinely better than one** — with the evidence
</Card>''',
 story='''{/* TERM LADDER: orchestrator → worker → handoff → specialist prompt → supervisor */}

### The meeting that could have been an email

There is a seductive idea in agent work: give every job its own expert. A researcher agent, a
writer agent, a critic agent, a manager agent to coordinate them. It feels like building a
company. It demos beautifully.

Now count the cost of a company. Every handoff is a conversation — and conversations between
agents are made of tiles you pay for. The manager re-explains the task to the researcher. The
researcher returns three pages. The writer reads all three. The critic reads the draft *and*
the research. What one agent could have done in four turns takes twenty, and every extra turn
is another chance to go subtly wrong.

Sometimes the team is still right — specialists genuinely outperform generalists when the jobs
need different tools, different instructions, or different *models*. But "sometimes" is the
whole content of this page: the four patterns that ship, what each one costs, and the honest
test for whether your problem needs a team or just a better prompt.
''',
 answer='''A team beats a generalist only when **the jobs genuinely differ — different tools, different
    instructions, or different models — and the handoffs are few.** Otherwise you have paid for
    a meeting: every handoff re-sends context in tiles, adds latency, and adds one more chance
    for a subtle error. The four patterns that survive production (orchestrator-workers,
    sequential handoff, parallel fan-out with a merge, and supervisor-critic) all share one
    trait: they minimise conversation between agents rather than celebrating it.''',
 dangler='''
### The question this page leaves open

Your graph runs, and your workers — however many — do their jobs. Then it happens: node seven
of nine, ninety minutes into a two-hour run, the API times out and the process dies.

Start again from the beginning? That is ninety minutes and a real bill, thrown away, for a
step that already succeeded. Software solved this problem long ago, and this is where agents
must borrow the answer:
[Module 3 — Durable execution](/curriculum/p4/week-30/3-durable-execution-checkpoint-resume).
''',
 build_open='''"Let's make it multi-agent" is a plan that doubles your bill and halves your reliability
    unless someone asks why. This layer is how you be that someone, with numbers.''',
 edge_open='''Coordination failures are the hardest to debug because every agent looks correct in
    isolation.'''),

W+"3-durable-execution-checkpoint-resume.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Ninety minutes in, node seven dies** — what you do about it
  - **Save the game** — checkpoints, and what belongs in one
  - **Watch a run resume from step seven** — in a moving picture
  - **The step that must never run twice** — idempotency, for real this time
</Card>''',
 story='''{/* TERM LADDER: checkpoint → resume → idempotency → replay → durable execution */}

### Save the game

Every long game you have played had a save system, for one obvious reason: nobody accepts
losing ninety minutes of progress because something crashed near the end.

Your agent graph is a long game. Two hours of work, nine nodes, real money spent at each one —
and it runs on the internet, where things time out. When node seven dies, restarting from node
one is not merely slow; it re-runs six steps that already succeeded, pays for them again, and
in the worst case *re-sends six emails*.

{/* ANIM:W30M3 */}

So the graph needs a save file. After each node finishes, write down what happened; when a run
resumes, skip anything already recorded and pick up where it stopped. That is **durable
execution** — and it comes with one sharp requirement this page will not let you skip: some
steps *must not* run twice, so the code that resumes has to know the difference between "do
this" and "do this exactly once".
''',
 answer='''You survive a 3 a.m. failure by **writing down every node's result the moment it succeeds**,
    so a resumed run skips completed work and restarts at the node that died. The save file is
    the graph's state, not the model's memory. And the requirement that makes it real is
    idempotency: any step with an external effect — sending mail, charging a card, filing a
    ticket — must carry a key that lets the second attempt recognise the first and do nothing.''',
 dangler='''
### The question this page leaves open

Your run survives crashes. It does not yet survive *success* — the kind where the agent loops
happily, calling a tool two hundred times, spending real money on a job that was never going
to finish.

Crashes are loud and honest. Runaway agents are quiet and expensive. Putting a hard edge
around what a run may consume is
[Module 4 — Resilience, budgets & failure handling](/curriculum/p4/week-30/4-resilience-budgets-failure-handling).
''',
 build_open='''The first long-running agent job that dies in production is the moment the team learns
    what "durable" means. Better to learn it now, in this layer, than at 3 a.m.''',
 edge_open='''Exactly-once is a promise almost nothing can keep. Everything here is about getting the
    closest honest thing.'''),

W+"4-resilience-budgets-failure-handling.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The agent that spent £400 in a loop** — and the four lines that stop it
  - **Budgets are a feature** — tiles, turns, wall-clock, money
  - **Retry without making it worse** — backoff, and the retry storm
  - **Fail like an adult** — partial results, clear errors, and knowing when to stop**
</Card>''',
 story='''{/* TERM LADDER: budget → retry → backoff → circuit breaker → graceful degradation */}

### The £400 Tuesday

A true story shape, repeated at company after company. An agent is asked to reconcile some
records. A tool returns a slightly wrong result. The agent, being diligent, tries again with a
different approach. That fails too. It tries again. And again.

Nobody is watching, because it is Tuesday afternoon and the job usually takes four minutes.
By the time someone notices the graph on Thursday, the loop has run two hundred thousand
times and spent £400 on an answer that was never coming.

Nothing here is exotic. It is the oldest problem in automation: **a system with no limit will
find a way to consume everything you give it.** Which is why every serious agent run carries
hard edges — a tile budget, a turn limit, a wall-clock timeout, a spend cap — and why the code
that retries has to be careful not to become the outage.

This page is those edges, plus the three habits that keep a failing system from taking its
dependencies with it: back off, break the circuit, and degrade honestly.
''',
 answer='''You stop a runaway by **giving every run hard edges and enforcing them in code, not in the
    prompt** — a tile budget, a turn limit, a wall-clock timeout and a spend cap, each of which
    ends the run cleanly with a partial result rather than a surprise invoice. Retries get
    exponential backoff and a cap, because naive retrying turns one slow dependency into an
    outage; a circuit breaker stops calling what is already broken; and when the budget is
    spent, the honest behaviour is to return what you have and say plainly that it is partial.''',
 dangler='''
### The question this page leaves open

You now have every piece: the work as a graph, the right number of workers, saves that survive
crashes, and hard edges that survive success.

What is missing is judgement — the architecture-level decisions that no library makes for you.
Where do humans sit in this? Which parts should never be an agent? What does this look like as
a system somebody has to run? That is
[Module 5 — Architecting a real agentic system](/curriculum/p4/week-30/5-architecting-a-real-agentic-system).
''',
 build_open='''Every "AI spend was 12× forecast" postmortem ends at the same missing four lines. This layer
    is those lines, and the retry policy that does not become the outage.''',
 edge_open='''Failure handling in a system whose components are probabilistic: where classic patterns
    apply, and where they quietly do not.'''),

W+"5-architecting-a-real-agentic-system.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The whole week, drawn as one system** — and every decision in it named
  - **Where the human belongs** — approval gates that are not theatre
  - **What should never be an agent** — the list worth arguing about
  - **A design you can defend** — the questions a review will actually ask
</Card>''',
 story='''{/* TERM LADDER: architecture → human-in-the-loop → approval gate → blast radius → runbook */}

### The whiteboard at the end of the week

Picture the design review. Your diagram is on the whiteboard, and around the table sit the
people who will carry the pager: the engineer who gets woken, the finance lead who sees the
bill, and the lawyer who asks what happens when it is wrong.

They will not ask which framework you used. They will ask:

*Where does a human approve? What is the worst thing this can do before someone notices? What
happens when the model is confidently wrong? What does it cost on a bad day? Who fixes it at
3 a.m., and with what?*

Every one of those questions is architecture, not code — and none of them is answered by
adding another agent. This page is how to answer them: where approval gates belong (and where
they are only theatre), how to keep the blast radius small, which parts of your system should
never be an agent at all, and what the runbook has to say.
''',
 answer='''A real agentic system is defined by **its edges, not its cleverness**: where a human approves,
    how small the blast radius is when the model is confidently wrong, what a bad day costs, and
    what the person on call actually does at 3 a.m. Approval gates belong wherever an action is
    expensive, irreversible or public — and nowhere else, because a gate nobody reads is worse
    than none. And the parts that are deterministic, high-volume or legally binding should stay
    ordinary software: an agent is for the steps you genuinely cannot enumerate.''',
 dangler='''
### The question this page leaves open

You can now design a system that works, survives failure, and stays inside its budget. One
question remains, and it is the one that ends most AI projects: **how do you know it is any
good — and how do you know it is still good after you change the prompt?**

"It seemed better" is not an answer when the thing is non-deterministic. Week 31 is how you
measure a system that gives different answers every time:
[Week 31 — Evaluation, safety & guardrails](/curriculum/p4/week-31/index).
''',
 build_open='''This is the layer you read the night before the design review — the one that turns a
    working prototype into a system other people are willing to run.''',
 edge_open='''Architecture is where the failures you have not had yet get decided.'''),
}
