
#from jarowinkler import similarity as sim
from pyjarowinkler import distance as sim
from numba import cuda
import re
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
#f=open('data/kata_kbbi.txt')
f=open(dir_path + '/' +'data/kata_kbbi_new.txt')
f=f.read()
kata_ = sorted(set(f.split()))
#ganti_ = kata_

# @cuda.jit(device=True)
def simJaro(kata1,kata2):
    return sim.get_jaro_distance(kata1, kata2, winkler=True, scaling=0.01)

def just_get_text(kata):
    kata_n = list()
    for i in kata:
        if i.isalpha():
            kata_n.append(i)
    return ''.join(kata_n)

def distinc_huruf(kata, jm=1):
    kata = just_get_text(kata)
    if len(just_get_text(kata))==0:
        return kata
    n_kata = list()
    if kata[0].isalpha():
        pass
    else:
        if kata[1].isalpha() and kata[1] not in n_kata:
            n_kata.append(kata[1])
    try:
        if kata[0]=='a' or kata[0]=='m' or kata[0]=='p'or kata[0]=='b':#or kata[1]=='a' or kata[1]=='m' or kata[1]=='p':
            if kata[0].isalpha():
                n_kata.append(kata[0])
            if kata[1] not in n_kata and kata[1].isalpha():
                n_kata.append(kata[1])
    except:
        pass
    for hr in kata:
        if hr not in n_kata and hr != 'a' and hr != 'm' and hr != 'p'and hr != 'b':
            if hr.isalpha():
                n_kata.append(hr)
    if len(n_kata)>jm:
        return "".join(n_kata[:jm])
    else:
        return "".join(n_kata)
    #if jm == 1:
        #return "".join(n_kata[0])
    #elif jm==2:
        #return "".join(n_kata[:2])
def new_corpus(kata, jm):

    corpus = list()
    #if len(kata)==0:
        #return []
    for i in distinc_huruf(kata, jm=jm):
        #print(i)
        f=open(dir_path + '/' +'data/kata/'+i+'.txt')
        f=f.read()
        f=f.split()
        corpus+=f
    return corpus

def get_data_split():
    f=open(dir_path + '/' +'data/_replace_.txt')
    f=f.read()
    f=f.split()
    return f


def getData(alamat):
    lineList = list()
    with open(dir_path + '/' + alamat, encoding = "ISO-8859-1") as f:
        for line in f:
            lineList.append(line.rstrip('\n'))
    return lineList

# @cuda.jit(device=True)
def save_gdiganti():
    with open(dir_path + '/' +"data/g_diganti.txt", "w") as f:
        for s in g_diganti:
            f.write(str(s) +"\n")
    with open(dir_path + '/' +"data/last_use_k.txt", "w") as f:
        for s in last_use_k:
            f.write(str(s) +"\n")
    with open(dir_path + '/' +"data/last_use_r.txt", "w") as f:
        for s in last_use_r:
            f.write(str(s) +"\n")
    with open(dir_path + '/' +"data/last_use_s.txt", "w") as f:
        for s in last_use_s:
            f.write(str(s) +"\n")
            
def reduksi_huruf(kata):
#kata = 'siiiiiiapaaaa'
    nkata  = list()
    for i,k in enumerate(kata):
        if i>2:
            if kata[i]== kata[i-1] and kata[i] == kata[i-2]:
                continue
            else:
                nkata.append(k)
        else:
            nkata.append(k)
    return "".join(nkata)

last_use_k = getData('data/last_use_k.txt')
last_use_r = getData('data/last_use_r.txt')
last_use_s = getData('data/last_use_s.txt')

g_diganti = getData('data/g_diganti.txt')
kata_typo = get_data_split()
# @cuda.jit(device=True)
def norm_kbbi(komentar, jm=1):
    if type(komentar)!=list:
        komentar_split = komentar.split()
    for indx, kt in enumerate(komentar_split):
        kt = reduksi_huruf(kt)
        if len(just_get_text(kt))==0:
            continue
        #kata_2 = new_corpus(kt, jm=jm)
        cek = True
        if kt in kata_ or kt in kata_typo or kt in g_diganti:
            #komentar_split[indx]=ganti_[kata_.index(kt)]
            continue
        elif kt in last_use_k:
            last_use_k_index = last_use_k.index(kt)
            komentar_split[indx] = last_use_r[last_use_k_index]
        else:
            list_kemiripan = []
            kata_2 = new_corpus(kt, jm=jm)
            for ix, sl in enumerate(kata_2):
                list_kemiripan.append(simJaro(kt, sl)) 
                if simJaro(kt, sl) >= .96:
                    komentar_split[indx]=kata_2[ix]
                    cek = False
                    #print(len(kata_2))
                    last_use_k.append(kt)
                    last_use_r.append(komentar_split[indx])
                    last_use_s.append(simJaro(kt, sl))
                    break
            if max(list_kemiripan)>=.94 and cek== True:
                #print("similarity",kt, str(max(list_kemiripan)))
                komentar_split[indx]=kata_2[list_kemiripan.index(max(list_kemiripan))]
                last_use_k.append(kt)
                last_use_r.append(komentar_split[indx])
                last_use_s.append(max(list_kemiripan))
                #print(len(kata_2))
            else:
                if kt not in g_diganti:
                    g_diganti.append(kt)
    ret = re.sub(' +', ' '," ".join(komentar_split))
    save_gdiganti()
    return ret.strip()
    #return " ".join(komentar_split)
