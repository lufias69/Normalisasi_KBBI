
from jarowinkler import similarity as sim
#f=open('data/kata_kbbi.txt')
f=open('data/kata_kbbi_new.txt')
f=f.read()
kata_ = sorted(set(f.split()))
#ganti_ = kata_
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
    if kata[0]=='a' or kata[0]=='m' or kata[0]=='p':#or kata[1]=='a' or kata[1]=='m' or kata[1]=='p':
        if kata[0].isalpha():
            n_kata.append(kata[0])
        if kata[1] not in n_kata and kata[1].isalpha():
            n_kata.append(kata[1])
    for hr in kata:
        if hr not in n_kata and hr != 'a' and hr != 'm' and hr != 'p':
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
        print(i)
        f=open('data/kata/'+i+'.txt')
        f=f.read()
        f=f.split()
        corpus+=f
    return corpus

def norm_kbbi(komentar, jm=1):

    if type(komentar)!=list:
        komentar_split = komentar.split()
    for indx, kt in enumerate(komentar_split):
        if len(just_get_text(kt))==0:
            continue
        #kata_2 = new_corpus(kt, jm=jm)
        cek = True
        if kt in kata_:
            #komentar_split[indx]=ganti_[kata_.index(kt)]
            continue
        else:
            list_kemiripan = []
            kata_2 = new_corpus(kt, jm=jm)
            for ix, sl in enumerate(kata_2):
                list_kemiripan.append(simJaro(kt, sl)) 
                if simJaro(kt, sl) >= .96:
                    komentar_split[indx]=kata_2[ix]
                    cek = False
                    print(len(kata_2))
                    break
            if max(list_kemiripan)>=.85 and cek== True:
                print("similarity",kt, str(max(list_kemiripan)))
                komentar_split[indx]=kata_2[list_kemiripan.index(max(list_kemiripan))]
                print(len(kata_2))
    return " ".join(komentar_split)