import time,gc,random,unicodedata,heapq,os,sys
OUT="/tmp/nexbench/out"
def emit(name,lines):
    open(os.path.join(OUT,name+".txt"),"w").write("\n".join(lines)+"\n")
    print(f"--- {name} ---\n"+"\n".join(lines)+"\n",flush=True)
def best_of(fn,reps=5):
    b=1e18
    for _ in range(reps):
        gc.collect(); t=time.perf_counter(); fn(); b=min(b,time.perf_counter()-t)
    return b

def unicode_fix():
    rows=[]
    s_nfc="café"; s_nfd=unicodedata.normalize("NFD","café")
    rows += [f"nfc_code_points,{len(s_nfc)}", f"nfd_code_points,{len(s_nfd)}",
             f"python_equal,{s_nfc==s_nfd}",
             f"equal_after_NFC,{unicodedata.normalize('NFC',s_nfc)==unicodedata.normalize('NFC',s_nfd)}",
             f"nfc_utf8_bytes,{len(s_nfc.encode())}", f"nfd_utf8_bytes,{len(s_nfd.encode())}"]
    fam="👨‍👩‍👧‍👦"
    rows += [f"family_emoji_code_points,{len(fam)}", f"family_emoji_utf8_bytes,{len(fam.encode())}"]
    r=random.Random(3)
    ascii_corpus="".join(r.choice("abcdefgh") for _ in range(2_000_000))
    nfd_corpus=unicodedata.normalize("NFD","".join(r.choice("éèêñüàçãõ") for _ in range(2_000_000)))
    nfc_corpus=unicodedata.normalize("NFC",nfd_corpus)
    t_ascii=best_of(lambda: unicodedata.normalize("NFC",ascii_corpus),3)
    t_nfc  =best_of(lambda: unicodedata.normalize("NFC",nfc_corpus),3)
    t_nfd  =best_of(lambda: unicodedata.normalize("NFC",nfd_corpus),3)
    t_low  =best_of(lambda: nfd_corpus.lower(),3)
    rows += [f"corpus_chars,2000000",
             f"NFC_on_pure_ascii_ms,{t_ascii*1e3:.2f}   (quick-check fast path)",
             f"NFC_on_already_NFC_ms,{t_nfc*1e3:.2f}    (quick-check fast path)",
             f"NFC_on_NFD_input_ms,{t_nfd*1e3:.2f}      (real composition work)",
             f"lower_ms,{t_low*1e3:.2f}",
             f"nfd_over_ascii,{t_nfd/t_ascii:.0f}x"]
    emit("w13m2_unicode",rows)

def vector_topk():
    """Top-K over 1M vectors done the way you would actually do it: numpy scoring,
    then compare K-selection strategies. This is the week-27 brute-force baseline."""
    import numpy as np, resource
    N,D,K=1_000_000,64,10
    rng=np.random.default_rng(4)
    mat=rng.standard_normal((N,D),dtype=np.float32)
    q=rng.standard_normal(D).astype(np.float32)
    rows=[f"vectors,{N}",f"dim,{D}",f"K,{K}",f"matrix_MB,{mat.nbytes/1e6:.1f}"]
    t=best_of(lambda: mat@q,3)
    scores=mat@q
    rows.append(f"numpy_scoring_matvec_ms,{t*1e3:.1f}")
    t1=best_of(lambda: np.sort(scores)[-K:],3)
    t2=best_of(lambda: np.argpartition(scores,-K)[-K:],3)
    t3=best_of(lambda: heapq.nlargest(K,scores.tolist()),3)
    a=np.sort(np.sort(scores)[-K:]); b=np.sort(scores[np.argpartition(scores,-K)[-K:]])
    rows += [f"full_np_sort_ms,{t1*1e3:.1f}",
             f"np_argpartition_ms,{t2*1e3:.1f}",
             f"heapq_nlargest_on_python_list_ms,{t3*1e3:.1f}",
             f"argpartition_over_sort,{t1/t2:.1f}x",
             f"results_agree,{np.allclose(a,b)}",
             f"total_query_ms_scoring_plus_argpartition,{(t+t2)*1e3:.1f}"]
    # pure python scoring, for the contrast
    lst=mat[:50_000].tolist(); ql=q.tolist()
    t4=best_of(lambda: [sum(x*y for x,y in zip(v,ql)) for v in lst],1)
    per=t4/50_000
    rows += [f"pure_python_scoring_50k_ms,{t4*1e3:.0f}",
             f"pure_python_extrapolated_1M_s,{per*N:.1f}",
             f"numpy_over_pure_python,{(per*N)/t:.0f}x"]
    emit("w14m2_topk_vectors",rows)

if __name__=="__main__":
    for a in sys.argv[1:]:
        {"unicode":unicode_fix,"vectors":vector_topk}[a]()
