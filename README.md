# RandomScripts
Random coded scripts for RNA-Seq Simulation and Analysis.

## RNA-Seq Data Simulation 
### Download Reference Data Set
1. To simulate RNA sequencing reads using Flux Simulator program, you need two files, annotation file and chromosomes file.
2. To download gene annotation file for human genome, Gencode, release 17 (ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_17/gencode.v17.annotation.gtf.gz) 
3. To download chromosomes file for human genome, Genecode, release 17 (ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_17/gencode.v17.annotation.gtf.gz).

### Preparing Data Set
1. To extract one chromosome, i.e. `chr10` from genome file `GRCh37.p11.genome.fa`, use the following bash command, the resulting chromosome file is `chr10.fa`:

```
perl -ne 'if(/^>(\S+)/){$c=grep{/^$1$/}qw(chr10)}print if $c' GRCh37.p11.genome.fa > chr10.fa
```
2. To extract one chromosome annotation, i.e. `chr10` from genome annotation file `gencode.v17.annotation.gtf `, use the following bash command, the resulting annotation file is `chr10.gff`:  


