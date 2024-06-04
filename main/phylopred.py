import pandas as pd
import os
import subprocess
import glob
from Bio import SeqIO
import Levenshtein
from pymongo import MongoClient
import time
import argparse

def list_of_strings(arg):
    return(arg.split(","))
ver= '0.0.1'

parser = argparse.ArgumentParser(description="""protPhylo {} : a python based phylogenetics based host-pathogen identification package""".format(ver),
usage="""%(prog)s [options]""",
epilog="""Written by Naveen Duhan (naveen.duhan@usu.edu),
Kaundal Bioinformatics Lab, Utah State University,
Released under the terms of GNU General Public Licence v3""",    
formatter_class=argparse.RawTextHelpFormatter )

parser.add_argument("--version", action="version", version= 'protPhylo (version {})'.format(ver), help= "Show version information and exit")
parser.add_argument("--gp", dest='genomePool',help="genomePool")
parser.add_argument("--h", dest='host', help="Host")
parser.add_argument("--p", dest='pathogen', help="Pathogen")
parser.add_argument('--hg', dest='hgenes', type=list_of_strings, help="Genes ids host")
parser.add_argument('--pg', dest='pgenes', type=list_of_strings, help="Genes ids pathogen")
parser.add_argument('--t',dest='threshold', type=float)
parser.add_argument("--hi", dest='hi', type=int, help="Host identitiy for blast filter")
parser.add_argument("--hc", dest='hc',type=int, help="Host coverage for blast filter")
parser.add_argument("--he", dest='he', type=float, help="Host evalue for blast filter")
parser.add_argument("--pi", dest='pi',type=int, help="Pathogen identitiy for blast filter")
parser.add_argument("--pc", dest='pc',type=int, help="Pathogen coverage for blast filter")
parser.add_argument("--pe", dest='pe', type=float, help="Pathogen evalue for blast filter")

def get_sequences(hgenes,pgenes, host, pathogen):
    hostIDs =[]
    pathogenIDs =[]
    numberHost= 0
    numberPathogen= 0
    pattern_host={}
    pattern_pathogen= {}
    
    with open(f"{host}_temp.fa",'w') as fp:
        host_fastas =SeqIO.parse(host,'fasta')
        for hf in host_fastas:
            if hf.id in hgenes:
                fp.write(f">{hf.id}\n{hf.seq}\n")
                numberHost +=1
                hostIDs.append(hf.id)
    with open(f"{pathogen}_temp.fa",'w') as fp:
        pathogen_fastas =SeqIO.parse(pathogen,'fasta')
        for pf in pathogen_fastas:
            if pf.id in pgenes:
                fp.write(f">{pf.id}\n{pf.seq}\n")
                numberPathogen +=1
                pathogenIDs.append(pf.id)
                
    for i in range(numberHost):
        pattern_host[i]=""
    for k in range(numberPathogen):
        pattern_pathogen[k]=""
    
    return hostIDs, pathogenIDs, numberHost, numberPathogen, pattern_host, pattern_pathogen

def select_pool(pool):
    
    if pool =='UP82':
        df = pd.read_csv("phylo/modelPool.txt", sep="\t", names=['genome'])
        poolList= df['genome'].values.tolist()
        genomeNumber = len(poolList)
        poolFolder = "phylo/phyloModelSC"
        nullPool  = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    if pool == 'BC18':
        df = pd.read_csv("phylo/bioconductorPool.txt", sep="\t", names=['genome'])
        poolList= df['genome'].values.tolist()
        genomeNumber = len(poolList)
        poolFolder = "phylo/phyloBioconductor"
        nullPool  = "000000000000000000"
    if pool == 'protphylo490':
        df = pd.read_csv("phylo/phylomodelPool.txt", sep="\t", names=['genome'])
        poolList= df['genome'].values.tolist()
        genomeNumber = len(poolList)
        poolFolder = "phylo/phyloBioconductor"
        nullPool ='0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        
    return genomeNumber, poolFolder, poolList, nullPool

def run_blast(genomeNumber,poolFolder, poolList,host_fasta, pathogen_fasta, evalue, pevalue, host_fasta_out, pathogen_fasta_out):
    host_files =[]
    pathogen_files = []
    for i in range(1, genomeNumber):
        host_files.append(f"{host_fasta_out}_blast_{i}.txt")
        pathogen_files.append(f"{pathogen_fasta_out}_blast_{i}.txt")
        # print(f"working on genome {i}")
        cmd = f" /opt/software/ncbi-blast-2.7.1+-src/c++/bin/blastp --db {poolFolder}/{poolList[i]} -q {host_fasta} --evalue {evalue} --out {host_fasta_out}_blast_{i}.txt --outfmt 6 qseqid sseqid pident evalue bitscore qcovhsp -k 1 --threads 6"
        pcmd =f" /opt/software/ncbi-blast-2.7.1+-src/c++/bin/blastp --db {poolFolder}/{poolList[i]} -q {pathogen_fasta} --evalue {pevalue} --out {pathogen_fasta_out}_blast_{i}.txt --outfmt 6 qseqid sseqid pident evalue bitscore qcovhsp -k 1 --threads 6"
        with open(os.path.join(os.getcwd(), "host.out"), 'w+') as fout:
            with open(os.path.join(os.getcwd(), "host.err"), 'w+') as ferr:
                job_id= subprocess.call(cmd, shell=True, stdout=fout,stderr=ferr)

        with open(os.path.join(os.getcwd(), "pathogen.out"), 'w+') as fout:
            with open(os.path.join(os.getcwd(), "pathogen.err"), 'w+') as ferr:
            
                job_id = subprocess.call(pcmd, shell=True, stdout=fout,stderr=ferr)
    return host_files, pathogen_files

def fill_pattern(pattern_host, pattern_pathogen, host_files, pathogen_files, numberHost,hostIDs, numberPathogen, pathogenIDs, hi, hc, pi,pc):
    for file in host_files:
        blastOutputHostIds=[]
        dd = open(file).readlines()

        for d in dd:
            if d !='':
                m = d.rstrip().split("\t")

                if float(m[2])>hi and float(m[5])>hc:
                    blastOutputHostIds.append(m[0])
        for i in range(numberHost):
            
            if hostIDs[i] in blastOutputHostIds:
                
                pattern_host[i]+='1'
            else:
                pattern_host[i]+='0'
                
    for file in pathogen_files:
        blastOutputPathogenIds=[]
        dd = open(file).readlines()

        for d in dd:
            if d !='':
                m = d.rstrip().split("\t")

                if float(m[2])>pi and float(m[5])>pc:
                    blastOutputPathogenIds.append(m[0])

        
        for i in range(numberPathogen):
            
            if pathogenIDs[i] in blastOutputPathogenIds:
                
                pattern_pathogen[i]+='1'
            else:
                pattern_pathogen[i]+='0'
        
    
    return pattern_host, pattern_pathogen

def get_ppi(numberHost, numberPathogen, pattern_host, pattern_pathogen, nullPool, hostIDs, pathogenIDs, genomeNumber):
    result=[]
    for i in range(numberHost):
        if nullPool != pattern_host[i]:
            for k in range(numberPathogen):
              
                host=hostIDs[i]
                pathogen=pathogenIDs[k]
                sim =(genomeNumber - Levenshtein.distance(pattern_host[i], pattern_pathogen[k]))/genomeNumber
                result.append([host,pathogen,sim, pattern_host[i], pattern_pathogen[k]])
                
    results = pd.DataFrame(result, columns=['Host_Protein', 'Pathogen_Protein', 'Score', 'Host_Pattern', 'Pathogen_Pattern'])
    
    return results

def connection(db):
    client = MongoClient("mongodb://localhost:27017/")

    connectDB = client[db]

    return connectDB

def add_results(data):
    pp =connection('hpinet_results')
    name = f"hpinet{str(round(time.time() * 1000))}results"
    ptable = pp[name]
    ptable.insert_many(data)

    return name

def add_noresults(data):
    pp =connection('hpinet_results')
    name = f"hpinet{str(round(time.time() * 1000))}results"
    ptable = pp[name]
    ptable.insert_one({'result':data})

    return name

def custom_to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None 

def main():
    
    options, unknownargs = parser.parse_known_args() 
    
    host = os.path.join(os.getcwd(), 'phylo/data/'+ options.host + '.fa')
    pathogen =os.path.join(os.getcwd(), 'phylo/data/'+ options.pathogen + '.fa')
    hgenes = options.hgenes
    pgenes = options.pgenes
    hi = options.hi
    he = options.he
    hc = options.hc
    pi = options.pi
    pe = options.pe
    pc = options.pc
    threshold = options.threshold
    pool = options.genomePool
    
    host_fasta = host + "_temp.fa"
    pathogen_fasta = pathogen + "_temp.fa"

    host_fasta_out = os.path.join(os.getcwd(), 'phylo/host/'+ options.host)
    pathogen_fasta_out = os.path.join(os.getcwd(), 'phylo/pathogen/'+ options.pathogen)

    hostIDs, pathogenIDs, numberHost, numberPathogen, pattern_host, pattern_pathogen = get_sequences(hgenes, pgenes,host,pathogen)
    
    genomeNumber, poolFolder,poolList, nullPool = select_pool(pool)

    host_files, pathogen_files = run_blast(genomeNumber, poolFolder, poolList, host_fasta, pathogen_fasta, he, pe, host_fasta_out, pathogen_fasta_out)

    pattern_host, pattern_pathogen = fill_pattern(pattern_host, pattern_pathogen, host_files, pathogen_files, numberHost, hostIDs, numberPathogen, pathogenIDs, hi,hc,pi,pc)
 
    try:
        results = get_ppi(numberHost, numberPathogen, pattern_host, pattern_pathogen, nullPool, hostIDs, pathogenIDs, genomeNumber)
    
        results['Score'] = results['Score'].apply(custom_to_float)
        results = results[results['Score']>=float(threshold)]
        rid = add_results(results.to_dict('records'))
        print(rid)
            
    except Exception:
        rid = add_noresults("no results")
        print(rid)
   
    for i in range(1, genomeNumber):
        f"{host_fasta_out}_blast_{i}.txt"
        f"{pathogen_fasta_out}_blast_{i}.txt"
    os.remove(pathogen_fasta)
    return 

if __name__ == '__main__':
    main()