W = "curriculum/p4/week-28/"
PAGES = {
W+"1-sparse-retrieval-bm25.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The query the map of meanings cannot answer** — try it and watch it fail
  - **The oldest trick in search, and why it still wins** — the inverted index
  - **BM25 in plain arithmetic** — rare words count more, long documents count less
  - **Search your own corpus by keyword** — in twenty lines
</Card>''',
 story='''    ### "TX-4471"

    Week 27 ended on an embarrassment. A user types **TX-4471** — an order code — and your
    beautiful semantic search returns three passages about shipping delays, none of them the
    right one.

    Think about why. The map of meanings places things by *how they are used*. "Refund" and
    "money back" sit together because they live in the same kinds of sentences. But
    `TX-4471` appears once, in one line, in one document. It has no neighbourhood. It has no
    meaning. **It only has letters** — and letters are exactly what the map threw away.

    Now think about how a librarian found things before anyone had a map: an index at the back
    of the book. Every distinctive word, and the pages it appears on. Look up the word, get the
    pages, done. That is **sparse retrieval** — matching the actual letters — and its modern
    form, **BM25**, is nearly forty years old and still beats fancy models on exactly this kind
    of query.

    {/* ANIM:W28M1 */}

    This page builds the index and the scoring, so you understand why an old idea refuses to
    die.
''',
 answer='''Semantic search misses `TX-4471` because **the map stores meaning, and a code has none —
    only letters.** Sparse retrieval keeps the letters: an inverted index maps every word to
    the documents containing it, and BM25 scores a match with two pieces of common sense — a
    rare word is worth more than a common one, and a hit in a short document counts for more
    than a hit in a long one. That is why a 1994 algorithm still beats a 2026 model on codes,
    names and error numbers.''',
 dangler='''
    ### The question this page leaves open

    So you have two searches, each brilliant where the other is blind: the map finds "money
    back" in a document that says "refund"; the index finds `TX-4471` exactly. Choosing one
    means being wrong for half your users.

    So do not choose — run both. But then two ranked lists arrive with scores in different
    units, and you must merge them into one answer without a false comparison. That is
    [Module 2 — Hybrid search & fusion](/curriculum/p4/week-28/2-hybrid-search-fusion).
''',
 build_open='''Search quality complaints arrive in two flavours nobody connects: "it can't find our SKUs"
    and "it can't find anything unless I use the exact words". They are the same bug seen from
    two sides, and this layer is the half of the fix that ships in an afternoon.''',
 edge_open='''BM25's parameters have been re-derived, re-tuned and re-argued for thirty years. This layer
    is what that argument settled.'''),

W+"2-hybrid-search-fusion.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Two ranked lists, one answer** — and why adding the scores is a trap
  - **Watch two lists become one** — in a moving picture
  - **Reciprocal Rank Fusion** — one line of arithmetic that quietly beats tuning
  - **Fuse your own two searches** — and measure what it bought you
</Card>''',
 story='''    ### Two judges, two scoresheets

    You now run both searches for every query. Two lists come back — and they disagree.

    Here is the trap, and almost everyone falls into it once: you add the scores together. But
    the two searches score in different currencies. The map returns a similarity like `0.83`,
    always between 0 and 1. BM25 returns something like `14.7`, unbounded, and its scale shifts
    with the corpus and the query. Adding them is like adding a temperature in Celsius to a
    distance in miles: the sum is a number, and the number means nothing.

    {/* ANIM:W28M2 */}

    The escape is beautifully simple. Ignore the scores entirely; keep only **the order**. If
    a document is second on one list and fourth on the other, that is all you need. Fuse on
    ranks, not scores — the method is called **Reciprocal Rank Fusion**, it fits on one line,
    and it is remarkably hard to beat.
''',
 answer='''You merge the two lists by **throwing the scores away and keeping only the ranks.** The
    scores are in incompatible currencies — a 0-to-1 cosine and an unbounded BM25 — so adding
    or weighting them compares nothing. Reciprocal Rank Fusion gives each document `1/(k +
    rank)` from every list and adds those: documents both searches liked rise, and neither
    search has to be normalised, tuned, or trusted more than the other.''',
 dangler='''
    ### The question this page leaves open

    Both searches now run, and their answers are fused sensibly. Both, though, still take the
    user's words at face value — and users write things like *"why is it broken"* with no
    product name, no error code, no version.

    No retrieval system can find the right passage for a question that does not say what it is
    about. Before searching, somebody has to make the question searchable. That is
    [Module 3 — Query understanding & transformation](/curriculum/p4/week-28/3-query-understanding-transformation).
''',
 build_open='''Two search systems, two sets of tuning knobs, and a stakeholder asking which weighting is
    right. This layer's answer — stop weighting, fuse on rank — is the one that survives
    contact with a changing corpus.''',
 edge_open='''Fusion looks trivial until you have per-tenant corpora, drifting score distributions and an
    A/B test that says the trivial version wins.'''),

W+"3-query-understanding-transformation.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **"why is it broken"** — the question no search engine can answer
  - **Four things you can do to a question before you search with it**
  - **HyDE: answer first, then search with the answer** — absurd, and it works
  - **Transform your own queries** — and watch recall move
</Card>''',
 story='''    ### "why is it broken"

    Here is a real support question, typed by a real person: *"why is it broken"*.

    No product. No error code. No version. Your retrieval system — dense, sparse, fused,
    beautifully engineered — has nothing to work with, because the question contains no
    information. Every passage in your corpus is equally close to it, which is another way of
    saying none of them is close.

    Now watch what a good support engineer does. They do not run to the documentation. They
    *rewrite the question first*: "broken how — the mobile app crashing on login, on version
    5.2?" Only then do they go looking. The rewrite is where the expertise lives.

    That is this page: the model gets to rewrite the question before the search sees it. Fill
    in the context from the conversation, split a compound question into parts, spell out what
    the user probably meant — and one delightfully strange trick, **HyDE**, where you have the
    model *invent a plausible answer* and search with that instead.
''',
 answer='''You cannot retrieve for *"why is it broken"* because **the question carries no information
    to match on** — so you fix the question before you search, not the search. Four moves do
    it: rewrite it in context, expand it with the words the document would use, decompose a
    compound question into single ones, and HyDE — draft a fake answer and search with *that*,
    because a fake answer speaks the document's language while a question does not.''',
 dangler='''
    ### The question this page leaves open

    Good questions, two searches, fused ranks. Your top ten passages are now genuinely
    relevant — and the *best* one is sitting at position seven, below three that merely look
    right.

    Everything so far judged each passage without ever reading it beside the question, because
    that is what made search fast. What if, just for the final ten, you paid for a slower and
    much sharper judge? That is
    [Module 4 — Re-ranking with cross-encoders](/curriculum/p4/week-28/4-re-ranking-with-cross-encoders).
''',
 build_open='''Retrieval metrics stall and the corpus is fine — the queries are the problem, and nobody
    on the team is looking at them. This layer is the query-side half of every RAG improvement
    you will ship.''',
 edge_open='''Query transformation adds a model call to every search: latency, cost and a new failure
    mode where the rewrite is confidently wrong.'''),

W+"4-re-ranking-with-cross-encoders.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **The sharper judge that is too slow to use** — and the trick that makes it affordable
  - **Watch ten passages get re-ordered** — in a moving picture
  - **Why the fast judge and the sharp judge disagree** — bi- versus cross-encoders
  - **Re-rank your own results** — and measure the jump in precision
</Card>''',
 story='''    ### Sorting the shortlist

    Imagine hiring. Ten thousand CVs arrive. Nobody reads ten thousand CVs — a filter scans for
    keywords and skills and hands you a shortlist of ten. Then, and only then, a human reads
    those ten *beside the job description*, properly, and ranks them.

    Your search is the filter. It was built for speed: every passage was turned into a pin long
    before your question existed, so answering means comparing pins — fast, and shallow,
    because the passage and the question never actually met.

    A **cross-encoder** is the human reading stage. It takes the question and one passage
    **together**, reads them jointly, and scores the pair. Far more accurate — and far too slow
    to run against ten million passages, since nothing can be precomputed.

    {/* ANIM:W28M4 */}

    So you do exactly what the hiring process does: fast filter to ten, sharp judge on the ten.
    That two-stage shape is how every serious retrieval system is built.
''',
 answer='''The best passage moves from seventh to first because **the final ten are judged by a model
    that reads the question and the passage together.** A bi-encoder must turn passages into
    pins in advance, so the two never meet — fast, but shallow. A cross-encoder reads the pair
    jointly and cannot precompute anything, so it is far sharper and far slower. The system is
    fast *and* sharp only because the sharp judge is used on ten candidates, never on ten
    million.''',
 dangler='''
    ### The question this page leaves open

    Your pipeline is now four models deep: rewrite the query, search two ways, fuse, re-rank,
    then generate. Quality is excellent. Now open the bill — and the latency graph.

    Every question pays for all of it, every time, including the forty people who asked the
    same thing this morning. Making that affordable, and keeping it alive at 3 a.m., is
    [Module 5 — Caching, cost & production RAG operations](/curriculum/p4/week-28/5-caching-cost-production-rag-operations).
''',
 build_open='''"Relevance is fine but the top result is often wrong" is the complaint this layer closes —
    usually in a day, with a model small enough to run on CPU.''',
 edge_open='''Re-rankers are where latency budgets go to die. Everything here is about buying precision
    without paying for it twice.'''),

W+"5-caching-cost-production-rag-operations.mdx": dict(
 glimpse='''<Card title="In this chapter — about 25 minutes" icon="sparkles">
  - **Forty people asked the same question this morning** — and you paid forty times
  - **Three caches, three different bugs** — exact, semantic, and prompt-prefix
  - **The cache that answers the wrong question** — and how to stop it
  - **Operate it for real** — what to log, what to alert on, what to re-index
</Card>''',
 story='''    ### Paying forty times for one answer

    Monday morning, your support bot gets the same question forty times: *"how do I reset my
    password?"* Forty query rewrites. Forty pairs of searches. Forty fusions. Forty re-ranks.
    Forty generations. Forty bills, for one answer that did not change.

    The obvious fix is a cache: remember the answer, serve it again. And for the exact same
    words, that is genuinely easy and genuinely free money.

    Then someone types *"how do i reset my pasword"* — one letter different — and the cache
    misses. So you get clever: cache by *meaning*, using the map from Week 27. Now the cache
    hits… and here is where this page earns its place, because a semantic cache set slightly
    too loose will happily serve the password-reset answer to someone asking how to reset
    their **device** — confidently, instantly, and wrongly.

    This page is the three caches, the bug in the clever one, and what running this system in
    production actually asks of you.
''',
 answer='''You stop paying forty times by **caching at three different levels, each with its own risk.**
    Exact-match caching is free money and no danger. Prompt-prefix caching cuts the cost of the
    passages you re-send every time. Semantic caching — "close enough to a question I have
    answered" — saves the most and is the one that can serve a confidently wrong answer, so its
    similarity threshold is a product decision measured on real questions, never a default
    copied from a blog post.''',
 dangler='''
    ### The question this page leaves open

    Week 28 closes with a system that is genuinely good: it finds passages by meaning *and* by
    letters, understands vague questions, ranks the shortlist properly, answers with citations,
    and does it cheaply enough to run.

    And it is still, fundamentally, a machine that **answers one question at a time**. It
    cannot check its own work, cannot call your APIs, cannot take three steps in a row towards
    a goal. Giving your friend hands, memory and a plan is Week 29:
    [Week 29 — Agents](/curriculum/p4/week-29/index).
''',
 build_open='''The AI feature works and Finance has questions about the invoice. This layer is where RAG
    stops being a demo and becomes a system with a unit cost you can defend.''',
 edge_open='''Everything here is month-two knowledge: cache invalidation, index rebuilds under live
    traffic, and the observability that tells you retrieval degraded before a user does.'''),
}
