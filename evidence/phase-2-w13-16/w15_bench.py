"""Week 15: CSV vs Parquet, column pruning, predicate pushdown, row-group skipping."""
import os, time, gc, sys
OUT="/tmp/nexbench/out"
def emit(name,lines):
    open(os.path.join(OUT,name+".txt"),"w").write("\n".join(lines)+"\n")
    print(f"--- {name} ---\n"+"\n".join(lines)+"\n",flush=True)
def best(fn,reps=3):
    b=1e18
    for _ in range(reps):
        gc.collect(); t=time.perf_counter(); r=fn(); b=min(b,time.perf_counter()-t)
    return b,r

def formats():
    import duckdb, pyarrow.parquet as pq, pyarrow as pa, os
    D="/tmp/nexbench/data"
    csv=f"{D}/txns.csv"; parq=f"{D}/txns.parquet"
    # also write gzip csv and uncompressed/zstd parquet for the size table
    t=pq.read_table(parq)
    pq.write_table(t, f"{D}/txns_none.parquet", compression="none")
    pq.write_table(t, f"{D}/txns_zstd.parquet", compression="zstd")
    import gzip, shutil
    if not os.path.exists(f"{D}/txns.csv.gz"):
        with open(csv,'rb') as fi, gzip.open(f"{D}/txns.csv.gz",'wb',compresslevel=6) as fo:
            shutil.copyfileobj(fi,fo,1024*1024)
    rows=["format,bytes,MB,ratio_vs_csv"]
    base=os.path.getsize(csv)
    for label,p in (("csv",csv),("csv.gz",f"{D}/txns.csv.gz"),
                    ("parquet_none",f"{D}/txns_none.parquet"),
                    ("parquet_snappy",parq),("parquet_zstd",f"{D}/txns_zstd.parquet")):
        s=os.path.getsize(p)
        rows.append(f"{label},{s},{s/1e6:.1f},{base/s:.2f}x")
    emit("w15m1_sizes",rows)

    con=duckdb.connect()
    rows=["operation,source,seconds,note"]
    t1,_=best(lambda: con.execute(f"SELECT count(*) FROM read_csv_auto('{csv}')").fetchall(),1)
    rows.append(f"count_all_rows,csv,{t1:.2f},full parse")
    t2,_=best(lambda: con.execute(f"SELECT count(*) FROM '{parq}'").fetchall(),3)
    rows.append(f"count_all_rows,parquet,{t2:.4f},reads footer metadata only")
    t3,_=best(lambda: con.execute(f"SELECT sum(amount) FROM read_csv_auto('{csv}')").fetchall(),1)
    rows.append(f"sum_one_column,csv,{t3:.2f},must parse every column")
    t4,_=best(lambda: con.execute(f"SELECT sum(amount) FROM '{parq}'").fetchall(),3)
    rows.append(f"sum_one_column,parquet,{t4:.3f},column pruning: reads 1 of 8 columns")
    t5,_=best(lambda: con.execute(f"SELECT count(*) FROM '{parq}' WHERE txn_id < 1000").fetchall(),3)
    rows.append(f"selective_filter,parquet,{t5:.4f},row-group skipping via min/max stats")
    t6,_=best(lambda: con.execute(f"SELECT count(*) FROM '{parq}' WHERE amount > 150").fetchall(),3)
    rows.append(f"nonselective_filter,parquet,{t6:.3f},no skipping possible")
    rows.append(f"count_speedup_parquet_over_csv,{t1/t2:.0f}x,-,-")
    rows.append(f"sum_speedup_parquet_over_csv,{t3/t4:.0f}x,-,-")
    emit("w15m1_scans",rows)

    # column pruning: how many bytes each column costs
    md=pq.ParquetFile(parq).metadata
    rows=["column,compressed_bytes,MB,pct_of_file"]
    total=0; per={}
    for rg in range(md.num_row_groups):
        for c in range(md.num_columns):
            col=md.row_group(rg).column(c)
            per[col.path_in_schema]=per.get(col.path_in_schema,0)+col.total_compressed_size
            total+=col.total_compressed_size
    for k,v in sorted(per.items(), key=lambda kv:-kv[1]):
        rows.append(f"{k},{v},{v/1e6:.1f},{100*v/total:.1f}%")
    rows.append(f"TOTAL,{total},{total/1e6:.1f},100.0%")
    rows.append(f"row_groups,{md.num_row_groups},-,-")
    rows.append(f"rows_per_row_group,{md.row_group(0).num_rows},-,-")
    emit("w15m1_columns",rows)

def scraping():
    """lxml vs html.parser, measured."""
    from bs4 import BeautifulSoup
    import urllib.request
    # Build a realistic synthetic page rather than hitting a live site.
    rows_html="\n".join(
        f'<tr class="r"><td class="sym">SYM{i:04d}</td><td class="px">{100+i%900}.{i%100:02d}</td>'
        f'<td class="chg">{"+" if i%2 else "-"}{i%15}.{i%100:02d}%</td>'
        f'<td class="vol">{i*137%10**7}</td></tr>' for i in range(20_000))
    html=f"""<!doctype html><html><head><title>Prices</title></head><body>
    <div id="wrap"><table id="quotes"><thead><tr><th>Symbol</th><th>Price</th>
    <th>Change</th><th>Volume</th></tr></thead><tbody>{rows_html}</tbody></table></div>
    </body></html>"""
    open("/tmp/nexbench/data/page.html","w").write(html)
    rows=[f"page_bytes,{len(html)}", f"table_rows,20000"]
    for parser in ("html.parser","lxml"):
        def go():
            soup=BeautifulSoup(html, parser)
            return [ (tr.select_one(".sym").get_text(), tr.select_one(".px").get_text())
                     for tr in soup.select("#quotes tbody tr") ]
        t,r=best(go,3)
        rows.append(f"{parser},parse_and_extract_seconds,{t:.3f},rows_extracted,{len(r)}")
    # raw lxml, no BeautifulSoup
    from lxml import html as LH
    def raw():
        doc=LH.fromstring(html)
        return [(e.text_content() for e in tr) for tr in doc.cssselect("#quotes tbody tr")]
    t,_=best(lambda: LH.fromstring(html).xpath('//*[@id="quotes"]/tbody/tr/td[1]/text()'),3)
    rows.append(f"lxml_xpath_direct,parse_and_extract_seconds,{t:.3f},-,-")
    emit("w15m3_parsers",rows)

if __name__=="__main__":
    for a in sys.argv[1:]:
        {"formats":formats,"scraping":scraping}[a]()
