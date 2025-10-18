**Takes text file of kmers and assembles genome sequence using de bruijn graph + dfs** 

**Text file example (see txt.txt):**

```{txt}
ATG
GGA
CCT
TTA
TAT
```

**Usage:**

```{bash}
python main.py kmer-file.txt
```

Currently returns nodes in order of contiguous sequence and plots graph. 
