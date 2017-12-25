# RandomScripts
Random coded scripts for RNA-Seq Simulation and Analysis.

## RNA-Seq Data Simulation 
### Download Reference Data Set
1. To simulate RNA sequencing reads using Flux Simulator program, you need two files, annotation file and chromosomes file.
2. To download gene annotation file for human genome, Gencode, release 17 (ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_17/gencode.v17.annotation.gtf.gz).
3. To download chromosomes file for human genome, Genecode, release 17 (ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_17/GRCh37.p11.genome.fa.gz).
4. Unzip the files using:
```
gzip -d gencode.v17.annotation.gtf.gz
gzip -d GRCh37.p11.genome.fa.gz

```

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


## Find the Longest PolyAs or PolyTs in a Reference Transcriptome

1. Download a reference transcriptome file for human genome from Genecode release 17 (ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_17/gencode.v17.pc_transcripts.fa.gz)

2. Unzip the files using:
```
gzip -d gencode.v17.pc_transcripts.fa.gz

```
3. Run the following bash commands on the reference transcriptome file `gencode.v17.pc_transcripts.fa` to find the top 10 longest polyAs sequence, the result will be in file `SortedPolyAs.out` :
```
grep -Eo 'A+' gencode.v17.pc_transcripts.fa | awk '{print $1, length($1)}' > PolyAs.out
sort -k 2 -n  -r PolyAs.out > SortedPolyAs.out
head -n 10 SortedPolyAs.out
```
4. Run the following bash commands on the reference transcriptome file `gencode.v17.pc_transcripts.fa` to find the top 10 longest polyTs sequence, the result will be in file `SortedPolyTs.out` :
```
grep -Eo 'T+' gencode.v17.pc_transcripts.fa | awk '{print $1, length($1)}' > PolyTs.out
sort -k 2 -n  -r PolyTs.out > SortedPolyTs.out
head -n 10 SortedPolyTs.out
```

## RNA-Seq kmers counting 
### kmers counting program Jellyfish
1. Download [Jellyfish](https://github.com/gmarcais/Jellyfish/releases/download/v2.2.7/jellyfish-2.2.7.tar.gz)
2. Unzip `jellyfish-2.2.7.tar.gz` using `tar` command and change the path to your desired extracted path: 
```
tar zxvf jellyfish-2.2.7.tar.gz -C /Users/sarael-metwally
```
3. Go to `bin` folder in `jellyfish-2.2.7` and copy the sequencing reads file called `RNA.fastq` there. 
4. Run `jellyfish` using the following two commands: 
```
jellyfish count -m 21 -s 100M -t 10 -C RNA.fastq
jellyfish dump mer_counts.jf > kmer_counts.fa
```
5. The resulted kmers counting file is called `kmer_counts.fa`
6. To get most highly 200 abundant kmers, using the following commands in order:

```
jellyfish dump -c mer_counts.jf > kmer_counts.fa 
sort -k 2 -n  -r  kmer_counts_1.fa > sorted_kmers
head -n 200 sorted_kmers > top_200_kmers 
```
7. The most top 200 kmers will be in file called `top_200_kmers`  

## RNA-Seq LightTrimmer
#### System requirements 
64-bit machine with g++ version 4.7 or higher, [pthreads](http://en.wikipedia.org/wiki/POSIX_Threads),and [zlib](http://en.wikipedia.org/wiki/Zlib) libraries.

#### Installation 
1. Clone the [GitHub repo](https://github.com/SaraEl-Metwally/LightTrimmer), e.g. with `git clone https://github.com/SaraEl-Metwally/LightTrimmer.git`
2. Run `make` in the repo directory for **k <= 31**  or `make k=kmersize` for **k > 31**, e.g. `make k=49`.
3. Copy the resulted Jellyfish kmers count file `kmer_counts.fa` in LightTrimmer directory or provide it's path to the program.
4. Copy the resulted Flux simulated sequencing reads `RNA.fastq`in LightTrimmer directory or provide it's path to the program.  
5. Run the following command:  
``` 
./LightTrimmer -k 21 -c kmer_counts.fa RNA.fastq --verbose 

``` 
#### Outputs
The output of LightTrimmer is the set of the following files:

```
kmers_prob.txt [Comma delimeted file for kmers probability].
kmers_count.txt [Comma delimeted file for kmers count].
kmers_correct.txt [Comma delimeted file for kmers position and correctness (position,1 or 0)].
kmers_info_all.txt [ Spaces delimited file for all information extracted from the reads.
  
```
 The output file `kmers_info_all.txt` has 6 columns, which are `read ID (R)`, `Kmer ID or position in the read (K)`, `Actual kmer count (C)`, `Median kmer (M)`, `Kmer probability (P)`, `Kmer Correct(1)/Incorrect(0) (Co)`, `Probability Computed(1)/Deductive(0) (Ca)` i.e. computed based on median kmer coverage.     
```
R  K   C   M      P        Co  Ca
1  0  19  45  1.0237e-05   1   1
1  1  21  45  5.31115e-05  1   1
1  2  19  45  1.0237e-05   1   1
1  3  21  45  5.31115e-05  1   1
1  4  21  45  5.31115e-05  1   1
1  5  21  45  5.31115e-05  1   1
1  6  21  45  5.31115e-05  1   1
1  7  22  45  0.000112905  1   1
1  8  22  45  0.000112905  1   1

```
#### Plot kmers probability for one read
1. Open R, and On R shell, write the following:
```
df <-read.csv("/Users/sarael-metwally/Documents/LightTrimmer/kmers_prob.txt",check.names=FALSE,header=FALSE)
y <-subset(df, select=V1:V80)
x <-(1:80)
jpeg("/Users/sarael-metwally/Documents/RNA-seq/images/first_read_kmers_prob");
plot(x,y[1,],type="l",xlab="kmers start positions",ylab="kmers probability",main="kmers probability for one read")
dev.off()
```
2. The path provided to `read.csv` is the path to the comma delimited file for `kmers_prob.txt` from LightTrimmer.
3. `y[1,]` means you are working on the kmers from `readID 1`. 
4. The path provided to `jpeg` is the path you wish to store your plots.

#### Plot kmers count for one read
1. Open R, and On R shell, write the following:
```
df <-read.csv("/Users/sarael-metwally/Documents/LightTrimmer/kmers_count.txt",check.names=FALSE,header=FALSE)
y <-subset(df, select=V1:V80)
x <-(1:80)
jpeg("/Users/sarael-metwally/Documents/RNA-seq/images/first_read_kmers_count");
plot(x,y[1,],type="l",xlab="kmers start positions",ylab="kmers counts",main="kmers counts for one read")
dev.off()
```
2. The path provided to `read.csv` is the path to the comma delimited file for `kmers_count.txt` from LightTrimmer.
3. `y[1,]` means you are working on the kmers from `readID 1`. 
4. The path provided to `jpeg` is the path you wish to store your plots.
5. You can change the `plot` by providing limits on `y-axis`,i.e. the maximum value on `y axis is 300`, using the following command: 
```
plot(x,y[2,],ylim=c(1,300),type="l",xlab="kmers start positions",ylab="kmers counts",main="kmers counts for one read")
```


