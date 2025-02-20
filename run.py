

import pickle as pkl

import numpy as np
import sys
import os
import argparse
import copy
parser = argparse.ArgumentParser(description="Run .")
parser.add_argument('--mode',default='attack')
parser.add_argument('--apaths',nargs='+',type=str,default=['no','DeepBlueAI'])
parser.add_argument('--evaluate',nargs='+',type=str,default=['arbitary'])
parser.add_argument('--gpu',default='0')
args=parser.parse_args()
if isinstance(args.apaths,str):
    args.apath=[args.apath]
if isinstance(args.evaluate,str):
    args.evaluate=[args.evaluate]
print("mode",args.mode)

os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu
base_adj=pkl.load(open("dset/testset_adj.pkl",'rb'))
base_features=np.load("dset/features.npy")
labels=np.load("dset/labels_test.npy")

start=len(base_features)-50000
end=len(base_features)

def check_injection(adj,features):
    # adj: 500*650000
    m=np.max(np.abs(features))
    if len(features[0])!=100:
        print("dimension mismatch!")
        return 1
    
    if m>2:
        print("feature too large!")
        return 1
    for i in range(len(adj.data)):
        if (adj.data[i]!=1) and (adj.data[i]!=0):
            adj.data[i]=1
    
    rowsum=adj.sum(1)
    #print(rowsum)
    for i in range(len(rowsum[0])):
        if rowsum[0][i]>100:
            print("too large degree at node ",i," !")
            return 1
    row,col=adj.shape
    asp=adj[:,-row:]
    ass=asp-asp.transpose()
    wc=np.abs(ass.data.sum())
    if wc>0:
        print("matrix not consistent! ")
        return 1
    '''
    for i in range(row):
        if asp[i,i]>0:
            print("contain self-loop!")
            return 1
    '''
    return 0
    
    
    
    
def evaluate_adversaries(adj,features,labels):
    from adversaries import predict
    feat=copy.copy(features)
    ad=copy.copy(adj)
    label_predict=predict.predict(ad,feat)[start:end]
    kr=(label_predict==labels).sum()
    print("accuracy ADVERSARIES",kr/50000)
    return kr

def evaluate_speit(adj,features,labels):
    from speit import defender
    feat=copy.copy(features)
    ad=copy.copy(adj)
    label_predict=defender.predict(ad,feat)[start:end]
    kr=(label_predict==labels).sum()
    print("accuracy SPEIT",kr/50000)
    return kr

def evaluate_dminer(adj,features,labels):
    
    from dminer import pred
    feat=copy.copy(features)
    ad=copy.copy(adj)
    label_predict=pred.predict(ad,feat)[start:end]
    kr=(label_predict==labels).sum()
    print("accuracy Dminers",kr/50000)
    return kr

def evaluate_daftstone(adj,features,labels):
    from daftstone import defense
    feat=copy.copy(features)
    ad=copy.copy(adj)
    label_predict=defense.validate(ad,feat)[start:end]
    kr=(label_predict==labels)
    kr=kr.sum()
    print("accuracy Daftstone",kr/50000)
    return kr
    
def evaluate_ntt(adj,features,labels):
    from ntt import app
    feat=copy.copy(features)
    ad=copy.copy(adj)
    label_predict=app.nmain(ad,feat)[start:end]
    kr=(label_predict==labels)
    kr=kr.sum()
    print("accuracy NTT DOCOMO LABS",kr/50000)
    return kr

def evaluate_u1234(adj,features,labels):
    from u1234 import umain
    feat=copy.copy(features)
    ad=copy.copy(adj)
    label_predict=umain.umain(ad,feat)[start:end]
    kr=(label_predict==labels)
    kr=kr.sum()
    print("accuracy u1234x1234",kr/50000)
    return kr
    
def evaluate_cccn(adj,features,labels):
    sys.path.append("cccn/")
    from cccn import cmain
    feat=copy.copy(features)
    ad=copy.copy(adj)
    label_predict=cmain.predict(ad,feat)[start:end]
    kr=(label_predict==labels)
    kr=kr.sum()
    print("accuracy cccn",kr/50000)
    sys.path.remove("cccn/")
    return kr

def evaluate_tsail(adj,features,labels):
    sys.path.append("tsail/")
    from tsail import tmain
    feat=copy.copy(features)
    ad=copy.copy(adj)
    label_predict=tmain.predict(ad,feat)[start:end]
    kr=(label_predict==labels)
    kr=kr.sum()
    print("accuracy tsail",kr/50000)
    sys.path.remove("tsail/")
    return kr

def evaluate_idvl(adj,features,labels):
    sys.path.append("idvl/")
    from idvl import main2
    feat=copy.copy(features)
    ad=copy.copy(adj)
    label_predict=main2.predict(ad,feat)[start:end]
    kr=(label_predict==labels)
    kr=kr.sum()
    print("accuracy idvl",kr/50000)
    sys.path.remove("idvl/")
    return kr
 
def evaluate_msupsu(adj,features,labels):
    sys.path.append("msupsu/")
    from msupsu import mdefender
    feat=copy.copy(features)
    ad=copy.copy(adj)
    label_predict=mdefender.predict(ad,feat)[start:end]
    kr=(label_predict==labels)
    kr=kr.sum()
    print("accuracy MSU-PSU-DSE",kr/50000)
    sys.path.remove("msupsu/")
    return kr
def evaluate_neutrino(adj,features,labels):
    sys.path.append("neutrino/")
    from neutrino import run
    feat=copy.copy(features)
    ad=copy.copy(adj)
    label_predict=run.predict(ad,feat)[start:end]
    kr=(label_predict==labels)
    kr=kr.sum()
    print("accuracy Neutrino",kr/50000)
    sys.path.remove("neutrino/")
    return kr

def evaluate_simong(adj,features,labels):
    sys.path.append("simong/")
    from simong import smain
    feat=copy.copy(features)
    ad=copy.copy(adj)
    label_predict=smain.predict(ad,feat)[start:end]
    kr=(label_predict==labels)
    kr=kr.sum()
    print("accuracy simongeisler",kr/50000)
    sys.path.remove("simong/")
    return kr
    
def evaluate_arbitary(adj,features,labels):
    sys.path.append("arbitary/")
    from arbitary import defend
    feat=copy.copy(features)
    ad=copy.copy(adj)
    label_predict=defend.predict(ad,feat)[start:end]
    kr=(label_predict==labels)
    kr=kr.sum()
    print("accuracy arbitary model",kr/50000)
    sys.path.remove("arbitary/")
    return kr
    
def combine_features(adj,features,name):
    import scipy.sparse as sp

    if name=="no":
        return adj,features
    add_adj=pkl.load(open("submissions/"+name+"/adj.pkl",'rb'))
    add_features=np.load("submissions/"+name+"/feature.npy")
    ww=check_injection(add_adj,add_features)
    if ww==1:
        print("format inappropriate, not adding")
        return adj,features
    nfeature=np.concatenate([features,add_features],0)
    
    total=len(features)
    adj_added1=add_adj[:,:total]
    adj=sp.vstack([adj,adj_added1])
   # print(adj_added.shape)
    
    adj=sp.hstack([adj,add_adj.transpose()])
    for i in range(len(adj.data)):
        if (adj.data[i]!=0) and (adj.data[i]!=1):
            adj.data[i]=1
    return adj.tocsr(),nfeature

if __name__ == "__main__":
    
    from dminer.dmain import GraphSAGE
    import torch
    list_evaluate=['ADVERSARIES','cccn','DaftStone','darkhorse','DeepBlueAI','Dminers','fashui01','Fengari','GraphOverflow','hhhvjk','idvl','MSU_PSU_DSE','kaige','zhangs','shengz','sc','Neutrino','NTTDOCOMOLABS','RunningZ','Selina','simongeisler','SPEIT','tofu','TSAIL','tzpppp','u1234x1234','yama','yaowenxi']
    weights=[24,18,12,10,8,7,6,5,4,3,2,1]
    if args.mode=="quick":
        r_evaluate=args.apaths
        
                
        for i in r_evaluate:
            print("Evaluating ",i," attack")
            adj=base_adj
            features=base_features
            adj,features=combine_features(adj,features,i)
            start=len(base_features)-50000
            end=len(base_features)
            scores=[]
            score_speit=evaluate_dminer(adj,features,labels)
            scores.append(['dminer',score_speit])
            
            print('attack score=',scores[0][1]/50000)
    if args.mode=="attack":
        r_evaluate=args.apaths
    
            
        for i in r_evaluate:
            print("Evaluating ",i," attack")
            adj=base_adj
            features=base_features
            adj,features=combine_features(adj,features,i)
            
            start=len(base_features)-50000
            end=len(base_features)
            print(start,end)
            scores=[]
            score_simong=evaluate_simong(adj,features,labels)
            scores.append(['simong',score_simong])
            torch.cuda.empty_cache()
            score_neutrino=evaluate_neutrino(adj,features,labels)
            torch.cuda.empty_cache()
            scores.append(['neutrino',score_neutrino])
            score_msupsu=evaluate_msupsu(adj,features,labels)
            torch.cuda.empty_cache()
            scores.append(['msupsu',score_msupsu])
            score_idvl=evaluate_idvl(adj,features,labels)
            torch.cuda.empty_cache()
            scores.append(['idvl',score_idvl])
            score_tsail=evaluate_tsail(adj,features,labels)
            torch.cuda.empty_cache()
            scores.append(['tsail',score_tsail])
            score_cccn=evaluate_cccn(adj,features,labels)
            torch.cuda.empty_cache()
            scores.append(['cccn',score_cccn])
            score_u1234=evaluate_u1234(adj,features,labels)
            torch.cuda.empty_cache()
            scores.append(['u1234',score_u1234])
            score_ntt=evaluate_ntt(adj,features,labels)
            torch.cuda.empty_cache()
            scores.append(['ntt docomo',score_ntt])
            score_daftstone=evaluate_daftstone(adj,features,labels)
            torch.cuda.empty_cache()
            scores.append(['daftstone',score_daftstone])
            score_dminer=evaluate_dminer(adj,features,labels)
            torch.cuda.empty_cache()
            scores.append(['dminer',score_dminer])
            score_speit=evaluate_speit(adj,features,labels)
            torch.cuda.empty_cache()
            scores.append(['speit',score_speit])
            score_adversaries=evaluate_adversaries(adj,features,labels)
            torch.cuda.empty_cache()
            scores.append(['adversaries',score_adversaries])
            scores.sort(key=lambda x:x[1],reverse=True)
            sc=[]
            for item in scores:
                sc.append(item[1])
            print("average score=",np.average(sc)/50000)
            
            for j in range(3):
                print(scores[j])
            sumscore=0
            for j in range(12):
                sumscore+=scores[j][1]*weights[j]*0.01
            print('3-avg score=',np.average(sc[:3])/50000)
            print('attack score=',sumscore/50000)
        
    if args.mode=="defend":
        allscores=[]
        for j in args.evaluate:
            print("Evaluating defend model ",j)
            defend_function='score=evaluate_'+j+"(adj,features,labels)"
            scores=[]
            for i in list_evaluate:
                print(i)
                adj=base_adj
                features=base_features
                adj,features=combine_features(adj,features,i)
                
                start=len(base_features)-50000
                end=len(base_features)
                
                exec(defend_function)
                torch.cuda.empty_cache()
                scores.append([i,score])
            scores.sort(key=lambda x:x[1])
            sc=[]
            for item in scores:
                sc.append(item[1])
            print("average score=",np.average(sc)/50000)
            for k in range(3):
                print(scores[k])
            print('defend score=',np.average(sc[:3])/50000)
                
