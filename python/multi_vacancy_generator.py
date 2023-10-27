import NPC # import the non-periodic carbon package
import numpy as np
from tqdm import tqdm
from itertools import combinations
import os
import sys

if len(sys.argv) != 6:
    print("Usage: python multi_vacancy_generator.py <structure> <size> <vacancies> <pores_allowed> <output_structures>")
    sys.exit(1)
    
structure = sys.argv[1]
size = int(sys.argv[2])
vnum = int(sys.argv[3])
pores_allowed = sys.argv[4]
output_struclocktures = sys.argv[5]



# generate quantum dot base
q = NPC.quantumdot()

if structure == '2':
    q.Hexarmchair(size)
elif structure == '1':
    q.Hexzigzag(size)
elif structure == '3':
    q.Square(size)
else:
    print('Invalid input, abort')
    sys.exit(1)


# get whitelist for atoms that can be removed
q.Getpores()
q.DistanceMatrix()
ind_list=[i for i in range(len(q.atom)) if i not in q.boundary]
print(f'there are {len(ind_list)} atoms to manipulate')

# generate combination, and remove those have overlap neighboring atoms, which will lead to dangling atom
comb = list(combinations(ind_list, vnum))
res=[]

for i in tqdm(range(len(comb)),desc='Filtering structures by dangling bonds...'):
    _unique=[]
    skip=False
    for j in comb[i]:
         for k in q.conn[j]:
            if k not in _unique:
                _unique.append(k)
            elif k not in comb[i]:
                skip=True
    if not skip:
        res.append(comb[i])
print(f'{len(comb)} before, {len(res)} after')

# use the product of distance vector to differentiate combinations of vacancies
res2=[]
res_dis=[]
for i in tqdm(range(len(res)),desc='Filtering structures by symmetry...'):
    sum_dis=np.array([1.0]*len(q.atom))
    for j in res[i]:
        sum_dis*=q.dismatrix[j]
    temp=list(sorted(sum_dis))
    string=''.join([str(int(k))+',' for k in temp])
    if string not in res_dis:
        res_dis.append(string)
        res2.append(res[i])
print(f'{len(res)} before, {len(res2)} after')

# whether generate big holes
if pores_allowed!='y':

    res3=[]
    for i in tqdm(range(len(res2)),desc='Filtering structures by pores...'):
        l=[item for j in res2[i] for item in q.connring[j]]
        if len(l)==len(set(l)):
            res3.append(res2[i])

    print(f'{len(res2)} before, {len(res3)} after')
    res2=res3.copy()

#create output folder
output_dir=("output")
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)
    print("creat folder: ",output_dir)
else:
    print(output_dir, "folder already exists.")

# batch process and output
if output_structures!='n': 
    for i in tqdm(range(len(res2)),desc='writing structures...'):
        q2=q.Duplicate()
        q2=q2.Hydrogenation()
        q2=q2.MultiV(res2[i])
        q2.Writexyz()
else:
    print('aborted')
