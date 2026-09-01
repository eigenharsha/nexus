import numpy as np, time, gc, os
def best(fn,reps=5):
    b=1e18
    for _ in range(reps):
        gc.collect(); t=time.perf_counter(); fn(); b=min(b,time.perf_counter()-t)
    return b
rng=np.random.default_rng(0)
n=4000
C=np.ascontiguousarray(rng.random((n,n)));  F=np.asfortranarray(C)
rows=["operation,C_order_ms,F_order_ms,ratio,note"]
# manual row-major traversal
def rowsum(a):
    s=0.0
    for i in range(a.shape[0]): s+=a[i].sum()
    return s
def colsum(a):
    s=0.0
    for j in range(a.shape[1]): s+=a[:,j].sum()
    return s
for name,fn in (("iterate_rows",rowsum),("iterate_cols",colsum)):
    tc=best(lambda: fn(C),3); tf=best(lambda: fn(F),3)
    rows.append(f"{name},{tc*1e3:.1f},{tf*1e3:.1f},{max(tc,tf)/min(tc,tf):.2f}x,"
                f"{'C wins' if tc<tf else 'F wins'}")
# transpose is a VIEW; making it contiguous is a copy
t=best(lambda: C.T,5); rows.append(f"transpose_view,{t*1e6:.2f} us,-,-,zero copy")
t=best(lambda: np.ascontiguousarray(C.T),3); rows.append(f"ascontiguousarray_of_T,{t*1e3:.1f},-,-,copies {C.nbytes/1e6:.0f} MB")
# matmul with a transposed (non-contiguous) operand
v=rng.random(n)
tc=best(lambda: C@v,5); tf=best(lambda: F@v,5); tt=best(lambda: C.T@v,5)
rows.append(f"matvec,{tc*1e3:.2f},{tf*1e3:.2f},{max(tc,tf)/min(tc,tf):.2f}x,C=row-major")
rows.append(f"matvec_on_transposed_view,{tt*1e3:.2f},-,-,BLAS handles strides")
# einsum vs explicit
A=rng.random((400,400)); B=rng.random((400,400))
t1=best(lambda: np.einsum('ij,jk->ik',A,B),3)
t2=best(lambda: A@B,5)
t3=best(lambda: np.einsum('ij,jk->ik',A,B,optimize=True),3)
rows.append(f"einsum_matmul,{t1*1e3:.1f},-,-,naive einsum")
rows.append(f"einsum_optimize_True,{t3*1e3:.1f},-,-,-")
rows.append(f"operator_matmul,{t2*1e3:.1f},-,-,BLAS; einsum/BLAS={t1/t2:.0f}x")
# accidental copy: float64 op on a float32 array
a32=rng.random(20_000_000).astype(np.float32)
t1=best(lambda: a32*np.float32(2.0),3)
t2=best(lambda: a32*2.0,3)          # python float is float64 -> upcast
r1=(a32*np.float32(2.0)).dtype; r2=(a32*2.0).dtype
rows.append(f"float32_times_float32,{t1*1e3:.1f},-,-,result dtype {r1}")
rows.append(f"float32_times_python_float,{t2*1e3:.1f},-,-,result dtype {r2}")
open("/tmp/nexbench/out/w16m1_order.txt","w").write("\n".join(rows)+"\n")
print("\n".join(rows))
