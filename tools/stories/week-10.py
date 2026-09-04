W = "curriculum/p2/week-10/"
PAGES = {
W+"1-the-network-stack.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The letter inside an envelope inside a sack** — how one message travels
  - **Watch headers wrap and unwrap** — in a moving picture
  - **The four layers that matter** — and what each one is responsible for
  - **Follow a real packet yourself** — with a command you can run now
</Card>''',
 story='''{/* TERM LADDER: packet → header → payload → protocol → layer */}

### The letter, the envelope, and the sack

You want to send a birthday card to a friend in another city. You do not think about lorries.

You write the card. You put it in an envelope with an address. The envelope goes into a postbox,
then into a sack, then onto a van, then a plane, then another van, and at the far end everything
is unwrapped in reverse until your friend is holding the card — reading it exactly as you wrote
it, entirely unaware of the plane.

A computer network works the same way, and this is not a loose analogy — it is the actual design.
Your message is wrapped by one layer, which is wrapped by the next, and so on down; then unwrapped
in reverse at the other end. Each wrapper is called a **header**, and it holds only what *that*
layer needs: the postcode-equivalent for one, the street address for another.

{/* ANIM:W10M1 */}

The reason this design has survived fifty years is that each layer can be ignorant of the others.
Your app does not know whether the message travelled by fibre or Wi-Fi, and the Wi-Fi does not know
whether it was carrying a birthday card or a bank transfer.
''',
 answer='''A message travels by being **wrapped, layer by layer** — each one adding a small header with only
    what it needs, and treating everything inside as opaque payload — then unwrapped in reverse at
    the far end. That is why your program never thinks about fibre or Wi-Fi: each layer is
    deliberately ignorant of the others, which is exactly what has let the internet change
    underneath applications for fifty years without breaking them.''',
 dangler='''
### The question this page leaves open

Notice what nobody has promised so far: that your message **arrives at all**. Wrapping does not
prevent a van from crashing, and a network genuinely can lose a packet, deliver two copies, or
deliver five packets in the wrong order.

So who fixes that? There are two answers, and choosing between them shapes everything you build:
[Module 2 — TCP vs UDP](/curriculum/p2/week-10/2-tcp-vs-udp).
''',
 build_open='''Every networking bug you will ever debug lives at one of these layers, and knowing which one
    narrows the search from hours to minutes.''',
 edge_open='''Where the neat layer model leaks — MTU, fragmentation, and middleboxes that read what they
    should not.'''),

W+"2-tcp-vs-udp.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Signed-for post, or a leaflet** — the two ways to send anything
  - **Watch a handshake and a retransmission** — in a moving picture
  - **Numbers and acknowledgements** — how reliability actually works
  - **The bug everyone writes first** — and why it is not a bug in TCP
</Card>''',
 story='''{/* TERM LADDER: segment → sequence number → ACK → retransmission → handshake */}

### Signed-for, or dropped through the letterbox

Two ways to send something in the post.

**Signed-for delivery.** You get confirmation it arrived. If it does not, it is sent again.
Everything arrives, in order, or you find out. It costs more and takes longer.

**A leaflet through the door.** Cheap, instant, and nobody checks. Most arrive. Some do not.
Nobody will ever tell you which.

Networks have exactly these two options, and they are called **TCP** and **UDP**.

{/* ANIM:W10M2 */}

TCP's guarantee is not magic — it is bookkeeping, and you will build the idea yourself. Every
byte gets a **sequence number**. The receiver sends back short notes saying *"I have everything up
to byte N"* — an **ACK**. If the sender does not hear an ACK in time, it sends that data again.
Out-of-order arrivals get reordered by their numbers. That is the whole of reliability.

UDP simply skips all of it, which is the right choice more often than beginners expect: for a
live video call, a packet from two seconds ago is *useless* — resending it would make things
worse, not better.

The page ends on the mistake almost everyone makes with TCP, and it is a lovely one: TCP gives
you a **stream of bytes**, not your messages. Send "HELLO" then "WORLD" and the other side may
receive "HELLOWOR" then "LD". Nothing is broken. TCP never promised to keep your boundaries.
''',
 answer='''Reliability is **bookkeeping, not magic**: every byte carries a sequence number, the receiver
    acknowledges everything it has up to a point, and anything unacknowledged in time is sent
    again — with out-of-order arrivals reordered by number. UDP skips all of that on purpose,
    which wins whenever late data is worthless, like a live call. And TCP delivers a *byte stream*,
    not your messages — so "HELLO" then "WORLD" can arrive as "HELLOWOR" then "LD", and that is
    TCP working correctly.''',
 dangler='''
### The question this page leaves open

You know what the network promises. Now write a program that actually uses it — and meet the
small, strange interface every operating system exposes for talking to another machine.

That interface is one of the oldest in computing, and it has a handful of steps that must happen
in order: [Module 3 — Socket programming](/curriculum/p2/week-10/3-socket-programming).
''',
 build_open='''Choosing TCP by default is right about ninety per cent of the time — and this layer is how to
    recognise the other ten, with numbers.''',
 edge_open='''Congestion control, head-of-line blocking, and why QUIC was worth building.'''),

W+"3-socket-programming.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The oldest interface in networking** — a handful of calls, in a fixed order
  - **Watch a connection be accepted** — in a moving picture
  - **Write an echo server** — in about twenty lines
  - **The short read** — the bug that hides until production
</Card>''',
 story='''{/* TERM LADDER: socket → file descriptor → bind → listen → accept → short read */}

### Answering the phone

A socket is a telephone, and the operating system's interface is the sequence of things you do
with one.

To *receive* calls: get a phone (create the socket), claim a number (**bind** to an address and
port), tell the exchange you are open for business (**listen**), then wait for it to ring
(**accept**). Each accepted call gives you a *separate* line to that one caller, while the
original phone stays free for the next ring.

To *make* a call, it is shorter: get a phone, and dial (**connect**).

{/* ANIM:W10M3 */}

Once connected, you read and write bytes. And this is where Module 2's warning becomes a real bug
in your code, so the page makes you meet it deliberately: you ask for 1,024 bytes and you get 300.
Not because anything failed — because that is all that had arrived at that instant. Beginners
assume one send equals one receive; it does not, and the resulting bug appears only under load or
over slow links, which is to say: in production.
''',
 answer='''A server socket follows a fixed sequence — create it, **bind** an address and port, **listen**,
    then **accept**, which hands you a separate connection per caller while the original keeps
    listening. A client only creates and **connects**. The trap is the short read: asking for 1,024
    bytes and getting 300 is normal, not an error, because that is what had arrived — so any code
    assuming one send equals one receive works on your laptop and fails under load.''',
 dangler='''
### The question this page leaves open

You can move bytes between two machines. Bytes are not a conversation.

The other side needs to know where one message ends and the next begins, what a message *means*,
what happens when a field is missing, and how to notice the other end has silently gone away.
Nobody provides those. You design them, and that is
[Module 4 — Designing an application protocol](/curriculum/p2/week-10/4-designing-an-application-protocol).
''',
 build_open='''Every HTTP library and message queue you use is this interface underneath. Knowing it turns
    "the connection hung" from a mystery into a diagnosis.''',
 edge_open='''Blocking versus non-blocking, what select and epoll actually do, and where the C10K problem
    went.'''),

W+"4-designing-an-application-protocol.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Where does one message end?** — the question bytes cannot answer
  - **Watch a framed message arrive** — in a moving picture
  - **Design a chat protocol on paper** — before writing any code
  - **The silent disconnection** — and the heartbeat that catches it
</Card>''',
 story='''{/* TERM LADDER: wire protocol → framing → serialisation → schema → heartbeat */}

### Where does the message end?

Two programs are connected and bytes are flowing. Here is the problem nobody warned you about:
the receiving side has no idea where one message stops and the next starts. It has a stream of
bytes and no punctuation.

So you invent the punctuation. That is what a **protocol** is — an agreement between two programs
about the shape of what they send, and there are really only two ways to mark a boundary: put a
delimiter at the end of each message (a newline, say), or put the **length at the front** so the
reader knows exactly how many bytes to collect.

{/* ANIM:W10M4 */}

Then the decisions that turn a demo into something usable, which this page walks through by
designing a small chat protocol on paper before writing a line of code: what fields does a message
have, what happens when a newer client sends a field the server has never heard of, and how does
either side notice that the other has silently vanished — because a connection that has gone away
often looks exactly like one where nobody has spoken recently.

That last one is why real protocols have a **heartbeat**: a small message whose only job is to
prove that someone is still there.
''',
 answer='''Bytes have no punctuation, so **you supply it**: either a delimiter at the end of each message,
    or — more robustly — the length written at the front so the reader knows exactly how many bytes
    to collect. Around that you decide the fields, what happens when an older peer meets an unknown
    one, and how a silent disconnection is detected, since a dead connection looks exactly like a
    quiet one until a heartbeat proves otherwise.''',
 dangler='''
### The question this page leaves open

Your protocol works. It is also, right now, completely open: anyone who can see the wire can read
every message, and anyone can pretend to be your server.

That is not acceptable for anything real — and the fix is a handshake that agrees a secret in the
open, which sounds impossible until you see it:
[Module 5 — Network security & operations basics](/curriculum/p2/week-10/5-network-security-operations-basics).
''',
 build_open='''Most "our services cannot talk to each other" incidents are protocol design decisions someone
    made in an afternoon two years ago. This layer is how to make them deliberately.''',
 edge_open='''Schema evolution, backwards compatibility, and why length-prefixing beats delimiters at
    scale.'''),

W+"5-network-security-operations-basics.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Agreeing a secret in public** — and why that is not a contradiction
  - **Watch a handshake happen** — in a moving picture
  - **What a certificate actually proves** — and what it does not
  - **Serve HTTPS locally** — and see three clients react differently
</Card>''',
 story='''{/* TERM LADDER: plaintext → symmetric key → public key → certificate → handshake */}

### Whispering across a crowded room

Two strangers need to agree a secret password — while standing in a crowded room where everybody
can hear every word they say. It sounds impossible.

It is not, and that impossible-sounding thing is what happens in the first fraction of a second of
every secure connection you make.

The trick is a pair of keys instead of one. Anything scrambled with the first can only be
unscrambled with the second. So one side can publish the first key to the entire world — hence
**public key** — and anyone may use it to send something only that side can read. No shared secret
had to be arranged in advance.

{/* ANIM:W10M5 */}

There is one more problem, and it is the one certificates exist for. You can now talk privately to
*somebody* — but how do you know it is your bank and not an impostor who also has a key pair? A
**certificate** is a public key plus a claim about who it belongs to, signed by an authority your
computer already trusts. That signature is the entire basis of "the padlock is showing".

Because that scrambling costs time, the handshake does something pragmatic: use the slow key-pair
method once, only to agree a fast shared key, then use the fast one for the actual conversation.
''',
 answer='''Two strangers agree a secret in public using **a pair of keys**: what one scrambles only the
    other can unscramble, so one key can be published freely and anyone may send something only its
    owner can read — no prior arrangement needed. A certificate then answers *who* you are talking
    to: a public key plus an identity claim, signed by an authority your machine already trusts.
    And because that maths is slow, it is used once to agree a fast shared key, which carries the
    real conversation.''',
 dangler='''
### The question this page leaves open

Machines can now talk to each other, reliably and privately. That is the last piece of the
*systems* foundation.

From here the course turns towards data and the mathematics that acts on it. Not the intimidating
kind — the small, concrete set of ideas that everything in Phases 3 and 4 quietly stands on, taught
the same way this week was: from zero, with pictures. That is
[Week 11 — Linear algebra & calculus for AI](/curriculum/p2/week-11/index).
''',
 build_open='''TLS misconfiguration is one of the most common production incidents there is, and one of the
    easiest to prevent once you know what the handshake is doing.''',
 edge_open='''Certificate chains, revocation, and what actually happens when a client refuses your
    certificate.'''),
}
