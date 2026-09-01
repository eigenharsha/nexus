"""Trie autocomplete vs sorted-array bisect: latency + memory. Degenerate BST."""
import time, gc, sys, bisect, random
from collections.abc import Mapping, Set

def deep_size(obj, seen=None):
    seen = seen or set()
    oid=id(obj)
    if oid in seen: return 0
    seen.add(oid)
    size=sys.getsizeof(obj)
    if isinstance(obj, dict):
        for k,v in obj.items(): size+=deep_size(k,seen)+deep_size(v,seen)
    elif isinstance(obj,(list,tuple,set,frozenset)):
        for i in obj: size+=deep_size(i,seen)
    elif hasattr(obj,'__dict__'):
        size+=deep_size(obj.__dict__,seen)
    elif hasattr(obj,'__slots__'):
        for s in obj.__slots__:
            if hasattr(obj,s): size+=deep_size(getattr(obj,s),seen)
    return size

def timeit(fn,reps=3):
    best=1e9
    for _ in range(reps):
        gc.collect(); t=time.perf_counter(); fn(); best=min(best,time.perf_counter()-t)
    return best

words=[w.strip().lower() for w in open("/usr/share/dict/words") if w.strip().isascii() and w.strip().isalpha()]
words=sorted(set(words))[:100_000]
print(f"words,{len(words)}")

class TrieNode:
    __slots__=('kids','end')
    def __init__(self): self.kids={}; self.end=False

def build_trie(ws):
    root=TrieNode()
    for w in ws:
        n=root
        for ch in w:
            nxt=n.kids.get(ch)
            if nxt is None:
                nxt=TrieNode(); n.kids[ch]=nxt
            n=nxt
        n.end=True
    return root

def trie_complete(root, prefix, limit=10):
    n=root
    for ch in prefix:
        n=n.kids.get(ch)
        if n is None: return []
    out=[]
    stack=[(n,prefix)]
    while stack and len(out)<limit:
        node,pre=stack.pop()
        if node.end: out.append(pre)
        for ch in sorted(node.kids, reverse=True):
            stack.append((node.kids[ch], pre+ch))
    return out[:limit]

def arr_complete(ws, prefix, limit=10):
    lo=bisect.bisect_left(ws, prefix)
    out=[]
    i=lo
    while i<len(ws) and ws[i].startswith(prefix) and len(out)<limit:
        out.append(ws[i]); i+=1
    return out

trie=build_trie(words)
rng=random.Random(9)
prefixes=[rng.choice(words)[:rng.randrange(1,4)] for _ in range(20_000)]
a=timeit(lambda: [trie_complete(trie,p) for p in prefixes])
b=timeit(lambda: [arr_complete(words,p) for p in prefixes])
print(f"queries,{len(prefixes)}")
print(f"trie_total_ms,{a*1e3:.1f},per_query_us,{a/len(prefixes)*1e6:.1f}")
print(f"bisect_total_ms,{b*1e3:.1f},per_query_us,{b/len(prefixes)*1e6:.1f}")
print(f"trie_mem_MB,{deep_size(trie)/1e6:.1f}")
print(f"sorted_list_mem_MB,{deep_size(words)/1e6:.1f}")
