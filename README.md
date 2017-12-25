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

```
grep chr10 gencode.v17.annotation.gtf > chr10.gff
```
or
```
grep ^chr10 gencode.v17.annotation.gtf> chr10.gff
```

### Flux Simulator

1. Download [Flux Simulator](http://artifactory.sammeth.net/artifactory/barna/barna/barna.simulator/1.2.1/flux-simulator-1.2.1.tgz)
2. Go to `bin`, create a file called `myParameters.par` and copy the following lines:
```
REF_FILE_NAME   chr10.gff
GEN_DIR         /Users/sarael-metwally/Genome

NB_MOLECULES    5000000
READ_NUMBER     5000000

READ_LENGTH     100

PAIRED_END      YES
# use default 76-bp error model
ERR_FILE        76

# create a fastq file
FASTA           YES

```
3. Do not forget to put `chr10.gff` in `bin` folder of Flux simulator and change the path of `GEN_DIR` parameter in `myParameters.par` file to the folder that has `chr10.fa` 

4. Use the following command to run `Flux` Simulator 
```
bash flux-simulator -p myParameters.par
```
or 
```
bash flux-simulator -x -l -s -p myParameters.par
```
5. You will find three files in `bin` folder: `RNA.bed`, `RNA.lib`, `RNA.fastq`

## RNA-Seq kmers counting 
### kmers counting program Jellyfish
1. Download [Jellyfish](https://github.com/gmarcais/Jellyfish/releases/download/v2.2.7/jellyfish-2.2.7.tar.gz)
2. unzip `jellyfish-2.2.7.tar.gz` using `tar` command and change the path to your desired path: 
```
tar zxvf jellyfish-2.2.7.tar.gz -C /Users/sarael-metwally
```
