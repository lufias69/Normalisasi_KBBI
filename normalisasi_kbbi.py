
f=open('data/kata_kbbi.txt')
f=f.read()
from jarowinkler import similarity as sim
kata_ = sorted(set(f.split()))
#ganti_ = kata_
def simJaro(kata1,kata2):
    return sim.get_jaro_distance(kata1, kata2, winkler=True, scaling=0.01)
def norm_jaro(komentar):
    if type(komentar)!=list:
        komentar_split = komentar.split()
    for indx, kt in enumerate(komentar_split):
        cek = True
        if kt in kata_:
            #komentar_split[indx]=ganti_[kata_.index(kt)]
            continue
        else:
            list_kemiripan = []
            for ix, sl in enumerate(kata_):
                list_kemiripan.append(simJaro(kt, sl)) 
                if simJaro(kt, sl) >= .96:
                    komentar_split[indx]=kata_[ix]
                    cek = False
                    break
            if max(list_kemiripan)>=.85 and cek== True:
                print("similarity",kt, str(max(list_kemiripan)))
                komentar_split[indx]=kata_[list_kemiripan.index(max(list_kemiripan))]
    return " ".join(komentar_split)