W = "curriculum/p2/week-09/"
PAGES = {
W+"1-boolean-algebra-logic-gates.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Build a thinking machine from light switches** — starting with nothing
  - **Watch one gate answer a question** — in a moving picture
  - **The astonishing fact** — one single gate can build every other one
  - **Draw the tables yourself** — and check every answer by hand
</Card>''',
 story='''{/* TERM LADDER: bit → gate → truth table → functionally complete */}

### Two switches and a light

Forget computers for a moment. Picture two ordinary light switches wired to one bulb.

Wire them so the bulb lights **only when both switches are on**. That arrangement has a name —
it is called an **AND** gate. Wire them so the bulb lights when **either** switch is on, and you
have an **OR** gate. Add a device that turns on when its switch is off, and you have a **NOT**.

That is the entire vocabulary of digital hardware. A switch position is a **bit**: on or off, `1`
or `0`. A wiring arrangement is a **gate**. And because there are only so many ways switches can
be set, you can write down the complete behaviour of any gate in a small table — every possible
input on the left, the resulting output on the right. That is a **truth table**, and for two
inputs it has exactly four rows.

{/* ANIM:W9M1 */}

Here is the fact this week is built on, and it should feel too good to be true: **one particular
gate can build all the others.** Not "in principle" — you will do it on this page. From that one
gate you get NOT, AND, OR and everything after it, all the way up to the processor you are
reading this on.
''',
 answer='''A gate is **a wiring arrangement whose output depends only on its inputs**, and a truth table
    writes down every case: two inputs give four rows, three give eight, `n` give `2^n`. The
    astonishing part is completeness — a NAND gate on its own is enough to build NOT, AND, OR and
    therefore *every* possible truth table. That is why a processor can be made from one repeated
    part, and why this week can start from nothing and still reach a working CPU.''',
 dangler='''
### The question this page leaves open

You can now build any gate you like. But a gate answers yes-or-no questions, and a computer has
to do **arithmetic** — 7 + 5, on numbers stored as bits.

Nobody wired addition in as a special feature. It has to be built out of the same little gates
you just made, and the first step is smaller than you expect: adding *one* bit to *one* bit.
That is [Module 2 — Combinational arithmetic](/curriculum/p2/week-09/2-combinational-arithmetic).
''',
 build_open='''Hardware description is a different way of thinking from writing code: nothing runs in
    sequence, everything is a wiring diagram. This layer is that shift, done properly.''',
 edge_open='''Gate delay, fan-out, and why the physical properties of a circuit decide how fast software can
    ever run.'''),

W+"2-combinational-arithmetic.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Add 1 + 1 with light switches** — and watch a carry appear
  - **Chain sixteen of them** — in a moving picture
  - **Why subtraction needs no new hardware** — a genuinely clever trick
  - **The number that has no positive twin** — and where it comes from
</Card>''',
 story='''{/* TERM LADDER: half adder → carry → full adder → ripple-carry → two's complement */}

### One plus one

Start with the smallest possible sum: add one bit to one bit.

Three of the four cases are easy: 0+0 is 0, 0+1 is 1, 1+0 is 1. Then 1+1, which in binary is not
2 — it is **10**: a zero, and a one carried into the next column, exactly as you carry when
adding 7+5 by hand.

So this tiny adder needs *two* outputs: the digit that stays, and the **carry** that moves left.
And here is the pleasing part — you can build both from gates you already have.

{/* ANIM:W9M2 */}

Chain sixteen of these side by side, each one taking the carry from its right-hand neighbour,
and you can add any two 16-bit numbers. That chain is called a **ripple-carry adder**, because
the carry ripples along it like a rumour.

Then the trick that saves an enormous amount of hardware. You might expect subtraction to need a
subtractor. It does not: with the right way of writing negative numbers — **two's complement** —
`a − b` is just `a + NOT(b) + 1`, so the adder you already built does subtraction too. The one
oddity of that scheme, which you will see for yourself: in 16 bits the range is −32,768 to
+32,767. There is one more negative number than positive, because zero takes up a slot on the
positive side.
''',
 answer='''Addition is built from gates because **1 + 1 in binary is 10** — a digit that stays and a carry
    that moves left — so a one-bit adder needs two outputs, and both are ordinary gates. Chain
    sixteen and you can add any two 16-bit numbers, the carry rippling along. Subtraction then
    comes free: in two's complement, `a − b` equals `a + NOT(b) + 1`, so no subtractor is ever
    built — which is also why the 16-bit range is asymmetric, −32,768 to +32,767.''',
 dangler='''
### The question this page leaves open

You can add and subtract. A processor must also compare, negate, and compute AND and OR on whole
numbers — and it must choose *which* of those to do, instruction by instruction, at speed.

So the next step is not another operation. It is a single unit that can perform many operations,
selected by a few extra wires. That unit is the calculator at the centre of every CPU:
[Module 3 — The ALU](/curriculum/p2/week-09/3-the-alu).
''',
 build_open='''Adder design is where hardware's real constraint appears: correctness is easy, and doing it
    fast is the whole engineering problem.''',
 edge_open='''Carry-lookahead, why ripple-carry latency grows with width, and what that costs at
    gigahertz.'''),

W+"3-the-alu.mdx": dict(
 glimpse='''<Card title="In this chapter — about 30 minutes" icon="sparkles">
  - **One box, eighteen operations** — chosen by six wires
  - **Watch the control bits select an answer** — in a moving picture
  - **Work one operation by hand** — every bit, checked
  - **The two extra outputs** — that make loops and if-statements possible
</Card>''',
 story='''{/* TERM LADDER: ALU → data input → control input → flag → bus */}

### One box, many jobs

You now have circuits that add, and circuits that do AND and NOT. A processor cannot afford a
separate box for every operation, wired permanently — it needs *one* box that can do any of
them, chosen fresh for each instruction.

That box is the **ALU** — the Arithmetic Logic Unit — and it is the calculator at the centre of
the CPU. It takes two 16-bit numbers in, and six extra wires called **control inputs** that say
which operation to perform right now. Flip those six wires and the same hardware computes
`x + y`, or `x - y`, or `x AND y`, or `-1`, or simply `x` unchanged.

{/* ANIM:W9M3 */}

The design you will build has a lovely economy to it: rather than eighteen separate circuits,
each control bit performs one small transformation on the inputs before the arithmetic happens —
zero this input, flip that one, negate the output — and the combinations produce the whole
operation table.

And two small extra outputs, which look like an afterthought and are anything but: one says *the
result was zero*, the other says *the result was negative*. Those two bits are how a computer
will later answer "are these equal?" and "is this less than that?" — which is to say, they are
where every if-statement and every loop you have ever written begins.
''',
 answer='''One box does many jobs because **six control wires reshape the inputs before the arithmetic**:
    zero an input, flip its bits, negate the output — and those small transformations combine into
    the whole operation table, instead of eighteen separate circuits. The two status bits matter
    just as much: "the result was zero" and "the result was negative" are what later let a
    computer compare things at all, which is where every if-statement and loop comes from.''',
 dangler='''
### The question this page leaves open

Your ALU is fast, correct — and completely forgetful. Give it the same inputs and it gives the
same answer, always, instantly. It has no idea what it computed a moment ago.

A computer that cannot remember anything cannot run a program: no variables, no counters, no
next instruction. Remembering, it turns out, needs one strange trick — wiring an output back
into an input — and that is
[Module 4 — Sequential logic, memory & the clock](/curriculum/p2/week-09/4-sequential-logic-memory-clock).
''',
 build_open='''The ALU is where "the CPU is magic" stops being true for good — you will have built the thing
    that computes.''',
 edge_open='''Why this control encoding was chosen over the obvious one, and what modern ALUs do
    differently.'''),

W+"4-sequential-logic-memory-clock.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **How a circuit remembers** — the loop that holds a bit still
  - **Watch a clock tick and a value stay** — in a moving picture
  - **From one bit to a register to RAM** — the building sequence
  - **Why everything happens on the tick** — and what breaks without it
</Card>''',
 story='''{/* TERM LADDER: combinational → sequential → feedback → clock → flip-flop → register */}

### How does a circuit remember?

Every circuit so far has been forgetful by design: the output depends only on what is on the
input wires *right now*. Take the inputs away and nothing remains.

So how can a machine made of such circuits remember anything at all?

The answer is a small piece of self-reference: **wire an output back into an input.** Now the
circuit's next state depends on its own current state — it can hold a value in place, feeding
itself the same answer over and over. That is memory, made of the same gates as everything else.

{/* ANIM:W9M4 */}

But a loop like that is dangerously twitchy. Without discipline the value can race around the
loop and settle who-knows-where, differently every time. So the whole machine is given a
**clock** — a signal that ticks 0, 1, 0, 1 forever — and memory is only allowed to change *on
the tick*. Between ticks, everything holds still, and the arithmetic has time to settle.

That is the deal underneath every computer you have used: a heartbeat, and a rule that nothing
moves in between. One such cell holds a bit; sixteen side by side hold a number (a **register**);
thousands of registers become RAM.
''',
 answer='''A circuit remembers by **feeding its own output back into its input**, so its next state
    depends on its current one — memory built from the same gates as everything else. That loop
    is twitchy on its own, so a **clock** disciplines it: values may change only on the tick, and
    between ticks everything holds still while the arithmetic settles. One cell holds a bit,
    sixteen make a register, and many registers make RAM.''',
 dangler='''
### The question this page leaves open

You now have both halves of a computer: something that computes, and something that remembers.
They are still just parts on a table.

What turns them into a machine that *runs a program* is one more idea — that the memory can hold
not only numbers but **instructions**, and that a small circuit can fetch them one after another
and make the ALU obey. That last assembly is
[Module 5 — From CPU to program](/curriculum/p2/week-09/5-from-cpu-to-program).
''',
 build_open='''Timing is where hardware stops being combinational logic and starts being engineering: setup,
    hold, and the reason clock speed has a ceiling.''',
 edge_open='''Metastability, clock domains, and what actually limits the frequency of a real chip.'''),

W+"5-from-cpu-to-program.mdx": dict(
 glimpse='''<Card title="In this chapter — about 30 minutes" icon="sparkles">
  - **Instructions are just numbers** — the idea the whole industry stands on
  - **Watch fetch, decode, execute** — in a moving picture
  - **Hand-execute five instructions** — you are the CPU
  - **Write a loop in assembly** — and see your Python from underneath
</Card>''',
 story='''{/* TERM LADDER: machine code → assembly → instruction set → program counter → fetch-decode-execute */}

### The number that is an instruction

Here is the idea that makes computers possible, and it is stranger than it sounds.

Memory holds numbers. You have been thinking of those numbers as *data* — a price, a pixel, a
count. But nothing about a number says what it is for. So: **let some of those numbers be
instructions.** Read one, treat its bits as a command — "add these two things", "jump back to
there" — and obey it.

That is the whole trick. Programs are data. The machine reads them the way it reads anything
else.

{/* ANIM:W9M5 */}

Making that work needs one more small register, the **program counter**, which holds the address
of the next instruction. And then the machine simply repeats three steps forever: **fetch** the
instruction at the program counter, **decode** what its bits mean, **execute** it with the ALU
and the registers — then move the counter on, and do it again. Billions of times a second.

You will hand-execute five instructions yourself on this page, being the CPU. It is the moment
the whole stack stops being folklore: the Python you write becomes instructions, which become
control bits, which become gates, which are the switches you wired together on Monday.
''',
 answer='''A computer runs programs because **instructions are numbers too** — memory holds both, and
    nothing about a number says which it is. The machine keeps one register, the program counter,
    holding the address of the next instruction, then repeats three steps forever: fetch it,
    decode what its bits mean, execute it with the ALU and registers. Everything above — Python,
    a browser, a model — is that loop, running very fast.''',
 dangler='''
### The question this page leaves open

You have built a computer from switches and watched it run a program. One machine, doing one
thing at a time, entirely on its own.

Almost nothing you use is like that. Every interesting program today talks to other machines —
and the moment two computers must agree on anything, an entirely new set of problems appears:
lost messages, wrong order, and no shared clock. That is Week 10:
[Week 10 — Networking & raw sockets](/curriculum/p2/week-10/index).
''',
 build_open='''Understanding the fetch-decode-execute loop is what makes performance work make sense later:
    cache misses, branch prediction and pipelines all live here.''',
 edge_open='''Pipelining, hazards, and how far modern CPUs have travelled from this simple loop while
    pretending they have not.'''),
}
