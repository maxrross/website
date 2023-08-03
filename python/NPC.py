#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math


# In[150]:


class quantumdot():
    # initilization
    def __init__(self):
        self.name=''
        self.x=[]
        self.y=[]
        self.z=[]
        self.atom=[]
        # center is the geometric center of the quantum dot
        self.center=[]
        self.edge=[]
        self.conn=[] # index of vertex connected to a vertice
        self.ring=[] # list of 4-8 edge polygons with vertice index
        self.connring=[] # index of rings connected to a vertice
        self.pore=[] # rings that have more than 12 atoms (12 atom is the single vacancy)
        self.adjmatrix=None
        self.dismatrix=None
        self.edgmatrix=None
        self.polygonmatrix=None # something to figure out
        self.metals=[] # index of metal atoms
        self.nonmetals=[] # index of nonmetal atoms
        self.boundary=[] # index of boundary atoms
        
    # analyze structure
    def Analyzer(self):
        # clean previous data
        self.center,self.edge,self.conn,self.ring,self.connring=[],[],[],[],[]
        self.adjmatrix,self.dismatrix,self.edgmatrix=None,None,None
        nonmetal=['C','N','O','F','Cl','S','P']
        # get connection and edge
        for i in range(len(self.x)):
            co=[]
            for j in range(len(self.x)):              
                if i!=j:
                    # depending on the atom type, there is metal-nonmetal and nonmetal-nonmetal
                    # cutoff distance set to 1.6 angstrom for nonmetal-nonmetal bond formation, value can change
                    if self.atom[i] in nonmetal and self.atom[j] in nonmetal:
                        if ((self.x[i]-self.x[j])**2+(self.y[i]-self.y[j])**2+(self.z[i]-self.z[j])**2)**0.5<1.6:
                            co.append(j) # update co for self.conn
                            pair=[i,j] # generate new edge candidate
                            pair.sort()
                            if pair not in self.edge: # save candidate edge to self.edge if not duplicated
                                self.edge.append(pair)
                    # cutoff distance set to 2 for metal-nonmetal bond
                    else:
                        if ((self.x[i]-self.x[j])**2+(self.y[i]-self.y[j])**2+(self.z[i]-self.z[j])**2)**0.5<2:
                            co.append(j) # update co for self.conn
                            pair=[i,j] # generate new edge candidate
                            pair.sort()
                            if pair not in self.edge: # save candidate edge to self.edge if not duplicated
                                self.edge.append(pair)                        
            self.conn.append(co) # update self.conn
            
        # get rings        
        # backtracking algorithm to find ring
        def backtracking(cur,target):
            if len(t)>7:
                return
            if len(t)>=3 and target in self.conn[cur]:
                temp=[target]+t[:]
                temp.sort()
                if temp not in self.ring:
                    self.ring.append(temp)
                ind=self.ring.index(temp)
                if ind not in tracks:
                    tracks.append(ind)
                return
            for i in self.conn[cur]:
                if ha[i]>0:
                    t.append(i)
                    ha[i]-=1
                    backtracking(i,target)
                    ha[i]+=1
                    t.pop()
        
        t=[]
        for i in range(len(self.conn)):
            ha=[1]*len(self.conn)
            ha[i]=0
            tracks=[]
            backtracking(i,i)
            self.connring.append(tracks[:])            
        return
        
    # analyze pores
    # use the same backtracking algorithm to find rings that define pores
    # the termination condition for the backtracking is now: 1. ring size must be larger than 12
    # 2. the connring value of the atom must be smaller than 3
    # 3. additional steps are used to differentiate real pores, boundary and fake loops
    def Getpores(self):
        # first check if Analyzer has been executed
        if self.conn==[]:
            self.Analyzer()

        def backtracking(cur,target):
            if len(self.connring[cur])>2:
                return
            if len(t)>=11 and target in self.conn[cur]:
                temp=t[:]+[target]
                compare=temp.copy()
                compare.sort()
                if compare not in c:
                    p.append(temp)
                    c.append(compare)
                    l.append(len(temp))
                return
            for i in self.conn[cur]:
                if ha[i]>0:
                    t.append(i)
                    ha[i]-=1
                    backtracking(i,target)
                    ha[i]+=1
                    t.pop()
        
        t,p,c,l=[],[],[],[]
        for j in range(len(self.connring)):
            if len(self.connring[j])<3:
                ha=[1]*len(self.connring)
                ha[j]=0
                backtracking(j,j)
    
        # delete fake pores and find quantum dot boundary
        if len(p)==1:
            print('no pore detected')
            self.boundary=p[0][:]
            return
        if len(p)==2:
            if l[0]<l[1]:
                p[0],p[1]=p[1][:],p[0][:]
            self.pore.append(p[1][:])
            self.boundary=p[0][:]
            return
        
        # use shoelace algorithm to determine the boundary atoms: 
        # the boundary should form a polygon that has the largest area
        def shoelace_area(x_list,y_list):
            a1,a2=0,0
            x_list.append(x_list[0])
            y_list.append(y_list[0])
            for j in range(len(x_list)-1):
                a1 += x_list[j]*y_list[j+1]
                a2 += y_list[j]*x_list[j+1]
            l=abs(a1-a2)/2
            return l
        
        max_area=0
        boundary_index=0
        for i in range(len(p)):
            x_list,y_list=[],[]
            for j in p[i]:
                x_list.append(self.x[j])
                y_list.append(self.y[j])
            area=shoelace_area(x_list,y_list)
            if area>max_area:
                self.boundary=p[i][:]
                max_area=area
                boundary_index=i

        p=p[:boundary_index]+p[boundary_index+1:] # remove boundary list from pore list
        l=l[:boundary_index]+l[boundary_index+1:]

        # addtional condition to determine p with more than two elements
        p=[x for _,x in sorted(zip(l,p))] # sort pore list by pore size (length of list)
    
        # first find pores
        # use hash table to determine if a pore list is invalid
        # hypothesis is the one atom can only appear in one pore
        self.pore=[]
        hap=[1]*len(self.x)
        for i in range(0,len(p)):
            ispore=True
            for j in p[i]:
                if hap[j]==0:
                    ispore=False
                    break
            if ispore:
                for j in p[i]:
                    hap[j]=0
                self.pore.append(p[i][:])

    # generate zigzag hexagon quantum dot
    def Hexzigzag(self,size:int):
        a=1.42
        x0,y0=[a*math.sqrt(3)/2,a*math.sqrt(3)],[a/2,a]
        dx,dy=a*math.sqrt(3),a*1.5
        xx,yy=[],[]
        x,y=np.zeros((2*size,4*size)),np.zeros((2*size,4*size))
        for i in range(-size,size):
            xx.extend([x0[0]+dx*i,x0[1]+dx*i])
            yy.extend([y0[0]+dy*0,y0[1]+dy*0])
        xx,yy=np.array(xx),np.array(yy)
        for i in range(-size,size):
            x[i]=xx+dx/2*i
            y[i]=yy+dy*i
        xx,yy=list(x.ravel()),list(y.ravel())
        boundary=max(yy)
        x,y=[],[]
        for i in range(len(xx)):
            temp=xx[i]*math.sqrt(3)/2+yy[i]/2
            if abs(temp)-boundary<0.2:
                x.append(xx[i]/2-yy[i]*math.sqrt(3)/2)
                y.append(temp)
        self.x=x[:]
        self.y=y[:]
        self.z=[0]*len(x)
        self.center=[0,0,0]
        self.atom=['C']*len(x)
        self.name='qd-hex-zigzag-'+str(size)
        print('Number of atoms:'+str(len(self.atom)))
    
    # generate armchair hexagon quantum dot
    def Hexarmchair(self,size:int):
        a=1.42
        self.Hexzigzag(2*size-1) # same raw lattice, different way of cutting
        x,y=[],[]
        for i in range(len(self.x)):
            # rotate 30, 90, 150 and cut
            temp30=self.x[i]*1/2+self.y[i]*math.sqrt(3)/2
            temp90=self.x[i]
            temp_30=-self.x[i]/2+self.y[i]*math.sqrt(3)/2
            boundary=(3*size-2)*math.sqrt(3)/2*a
            if abs(temp30)-boundary<0.2 and abs(temp90)-boundary<0.2 \
            and abs(temp_30)-boundary<0.2:
                x.append(self.x[i]*math.sqrt(3)/2-self.y[i]*1/2)
                y.append(temp30)
        self.x=x[:]
        self.y=y[:]
        self.z=[0]*len(x)
        self.center=[0,0,0]
        self.atom=['C']*len(x)
        self.name='qd-hex-armchair-'+str(size)
        print('Number of atoms:'+str(len(self.atom)))
    
    # generate square ribbon shape of quantum dot
    def Square(self,size:int):
        a=1.42
        self.Hexzigzag(2*size) # same raw lattice, different way of cutting
        x,y=[],[]
        boundary=(2*size+1)*math.sqrt(3)/2*a
        boundary2=(3*size+2)*a/2
        k=(size-1)/2
        if size%2==0:
            boundary3=999
        else:
            boundary3=(4.5*k+2.5)*a
        for i in range(len(self.x)):
            if abs(self.x[i])-boundary<0.2 and abs(self.y[i])-boundary2<0.2 \
            and abs(self.x[i]*math.sqrt(3)/2+self.y[i]/2)-boundary3<0.2 and \
            abs(-self.x[i]*math.sqrt(3)/2+self.y[i]/2)-boundary3<0.2:
                x.append(self.x[i])
                y.append(self.y[i])
        self.x=x[:]
        self.y=y[:]
        self.z=[0]*len(x)
        self.center=[0,0,0]
        self.atom=['C']*len(x)
        self.name='qd-square-'+str(size)
        print('Number of atoms:'+str(len(self.atom)))
    
    # read structure from xyz file
    def Readxyz(self,f:str):
        self.name=f[:-4]
        p=pd.read_table(f,skiprows=2,delim_whitespace=True,names=['atom', 'x', 'y', 'z','a','b','c','d'])
        p=p[p['atom']=='C']
        self.x=p.x.tolist()
        self.y=p.y.tolist()
        self.z=p.z.tolist()
        self.center=[sum(self.x)/len(self.x),sum(self.y)/len(self.y),sum(self.z)/len(self.z)]
        self.atom=p.atom.tolist()
        
    # write structure to xyz file
    def Writexyz(self):
        with open('./output/'+self.name+'.xyz', 'w') as xyz_file:
            xyz_file.write('%d\n%s\n' % ((len(self.atom)-self.atom.count('X')),self.name))
            for i in range(len(self.atom)):
                xyz_file.write("{:4} {:11.6f} {:11.6f} {:11.6f}\n".format(
                    self.atom[i], self.x[i], self.y[i], self.z[i]))
                    
    # adjacency matrix
    def AdjacencyMatrix(self):
        if self.conn==[]:
            self.Analyzer()
        # initialize adjacency matrix with zeros (not directly connected)
        matrix=[[0]*len(self.atom) for _ in range(len(self.atom))]
        for i in range(len(self.conn)):
            for j in self.conn[i]:
                matrix[i][j]=1
        self.adjmatrix=np.array(matrix)
        return np.array(matrix)
    
    # distance matrix
    def DistanceMatrix(self):
        if type(self.adjmatrix)!=np.ndarray:
            adj=self.AdjacencyMatrix() # Distance matrix is derived from adjacency matrix
        else:
            adj=self.adjmatrix.copy()
        # initilzation of the distance matrix
        dis=adj.copy() 
        dis[dis==0]=999 # initialize all d[ij] as 999 except those are already 1
        for i in range(len(dis)):
            dis[i][i]=0 # make d[ii] zero  
        
        def spread(adj,dis,cur,d):
        # adj: adjacency matrix, dis: distance matrix, d: distance (number of bonds)
        # cur: matrix containing current set of atoms to check for connections
            sca=cur[0].copy()
            for i in range(len(self.x)):
                # block: matrix containg the atoms that are connected to atoms that are connecting to atom i
                block=adj*cur[i] 
                for j in range(len(block)):
                    sca[j]=np.sum(block[j]) # reduce the matrix to a scalar by adds up accumulating counts of appeard atoms
                cur[i]=sca # update the cur matrix with sca
            # normalize cur
            temp=cur.copy()
            temp[temp==0]=1
            cur=cur/temp
            nex=cur.copy()           
            # update distance matrix with minimum path value
            cur=cur*d
            cur[cur==0]=999
            dis=np.minimum(dis,cur)

            return dis,nex

        # start with d=2, d=1 and 0 are already in adjacency matrix
        d=2
        cur=adj.copy()
        while 999 in dis and d<=len(self.x): # the stop condition is either all distance has been updated or maximum loops reached
            dis,cur=spread(adj,dis,cur,d)
            d+=1
        self.dismatrix=dis
        return dis
    
    # edge type matrix
    def EdgeMatrix(self):
        if type(self.adjmatrix)!=np.ndarray:
            adj=self.AdjacencyMatrix()
        else:
            adj=self.adjmatrix.copy()
        edg=np.zeros(adj.shape)
        if type(self.dismatrix)!=np.ndarray:
            dis=self.DistanceMatrix()
        else:
            dis=self.dismatrix.copy()
        ind=np.argwhere(adj==1)
        ind=np.sort(ind)
        ind=np.unique(ind,axis=0)
        dic={}
        j=1
        for i in ind:
            code=str(np.sort(dis[i[0]]*dis[i[1]]))# use the product (seems better than sum) of distance matrix of two vertices in a edge to differentiate edges
            if code not in dic.keys():
                dic[code]=j
                j+=1
            edg[i[0],i[1]]=dic[code]
        edg+=edg.T
        self.edgmatrix=edg
        return edg
    
    # vertice convexity matrix
    def ConMatrix(self):
        con=[]
        for i in range(len(self.x)):
            if len(self.conn[i])==3:
                v1=np.array([self.x[self.conn[i][0]]-self.x[self.conn[i][1]],
                            self.y[self.conn[i][0]]-self.y[self.conn[i][1]],
                            self.z[self.conn[i][0]]-self.z[self.conn[i][1]]])
                v2=np.array([self.x[self.conn[i][0]]-self.x[self.conn[i][2]],
                            self.y[self.conn[i][0]]-self.y[self.conn[i][2]],
                            self.z[self.conn[i][0]]-self.z[self.conn[i][2]]])
                vn=np.cross(v1,v2)
                vn=vn/(vn[0]**2+vn[1]**2+vn[2]**2)**0.5
                va=np.array([self.x[self.conn[i][0]]-self.center[0],
                            self.y[self.conn[i][0]]-self.center[1],
                            self.z[self.conn[i][0]]-self.center[2]])
                vb=np.array([self.x[i]-self.center[0],
                            self.y[i]-self.center[1],
                            self.z[i]-self.center[2]])
                print (abs(np.dot(vb,vn))-abs(np.dot(va,vn)))
                if abs(np.dot(vb,vn))-abs(np.dot(va,vn))>0.2:
                    con.append(1)
                elif abs(np.dot(vb,vn))-abs(np.dot(va,vn))<-0.2:
                    con.append(-1)
                else:
                    con.append(0)
            else:
                con.append(0)
        return con
    
    # add H to the quantum dot fringe
    def Hydrogenation(self):
        new_obj=self.Duplicate()
        if new_obj.boundary==[]:
            new_obj.Getpores()
        a,d=1.42,1.08467
        x,y,z=[],[],[]
        for i in range(len(new_obj.x)):
            if i in new_obj.boundary and len(new_obj.conn[i])==2:
                cx=(new_obj.x[new_obj.conn[i][0]]+new_obj.x[new_obj.conn[i][1]])/2
                cy=(new_obj.y[new_obj.conn[i][0]]+new_obj.y[new_obj.conn[i][1]])/2
                cz=(new_obj.z[new_obj.conn[i][0]]+new_obj.z[new_obj.conn[i][1]])/2
                x.append(new_obj.x[i]+(new_obj.x[i]-cx)/(a/2)*d)
                y.append(new_obj.y[i]+(new_obj.y[i]-cy)/(a/2)*d)
                z.append(new_obj.z[i]+(new_obj.z[i]-cz)/(a/2)*d)
        new_obj.x.extend(x)
        new_obj.y.extend(y)
        new_obj.z.extend(z)
        new_obj.atom.extend(['H']*len(x))
        new_obj.name+='-H-terminated'
        new_obj.center,new_obj.edge,new_obj.conn,new_obj.ring,new_obj.connring,new_obj.pore=[],[],[],[],[],[]
        return new_obj
    
    # Colorize structures with certain descriptors and save to png
    def Dyestructure(self):
        # pcolor: atom color determined by distance matrix
        # ecolor: edge color determined by edge matrix
        pcolor,ecolor=[],[]
        if type(self.dismatrix)!=np.ndarray:
            dis=self.DistanceMatrix()
        else:
            dis=self.dismatrix.copy()
        for i in dis:
            pcolor.append(i.sum())
        if type(self.edgmatrix)!=np.ndarray: 
            edg=self.EdgeMatrix()
        else:
            edg=self.edgmatrix.copy()
            
        for i in self.edge:
            ecolor.append(edg[i[0]][i[1]])

        cmap = cm.get_cmap('tab20c') # select colormap
        max_height = max(ecolor)   # get range of colorbars so we can normalize
        min_height = min(ecolor)

        # scale each z to [0,1], and get their rgb values
        rgba=[]
        for k in ecolor:
            rgba.append(cmap((k-min_height)/max_height))
        
        bx,by=max(self.x),max(self.y)
        fig,axs=plt.subplots(1,2,figsize=(10,5))
        for i in self.edge:
            axs[0].plot([self.x[i[0]],self.x[i[1]]],[self.y[i[0]],self.y[i[1]]],c='lightgray',zorder=0)
        axs[0].scatter(self.x,self.y,s=30,c=pcolor,cmap='tab20c',zorder=1)
        axs[0].axis('square')
        axs[0].set_xlim(-bx*1.1,bx*1.1)
        axs[0].set_ylim(-by*1.1,by*1.1)
        axs[0].axis('off') 
        
        for i in range(len(self.edge)):
            axs[1].plot([self.x[self.edge[i][0]],self.x[self.edge[i][1]]],[self.y[self.edge[i][0]],self.y[self.edge[i][1]]],c=rgba[i],zorder=0)
        axs[1].scatter(self.x,self.y,s=30,c='lightgray',alpha=0.5,zorder=1)
        axs[1].axis('square')
        axs[1].set_xlim(-bx*1.1,bx*1.1)
        axs[1].set_ylim(-by*1.1,by*1.1)
        axs[1].axis('off')
        
        plt.tight_layout()
        plt.savefig(self.name+'.png',dpi=300)
        
        print('type of atom: '+str(len(set(pcolor))))
        print('type of edge: '+str(len(set(ecolor))))
        return pcolor,ecolor
    
    # duplicate current object
    def Duplicate(self):
        obj=quantumdot()
        obj.name=self.name
        obj.x,obj.y,obj.z=self.x[:],self.y[:],self.z[:]
        obj.edge,obj.conn,obj.atom,obj.ring,obj.connring,obj.pore,obj.boundary=\
        self.edge[:],self.conn[:],self.atom[:],self.ring[:],self.connring[:],self.pore[:],self.boundary[:]
        return obj
    
    # generate a SW defect from an edge
    def StoneWales(self,e_ind:int):
        new_obj=self.Duplicate()
        if new_obj.edge==[]:
            new_obj.Analyzer()
        if e_ind>len(new_obj.edge):
            print('edge index error')
            return
        # pa, pb: point a and b determined by closest neighboring atoms of edge vertices
        pax=sum([new_obj.x[j] for j in new_obj.conn[new_obj.edge[e_ind][0]]])/len(new_obj.conn[new_obj.edge[e_ind][0]])
        pay=sum([new_obj.y[j] for j in new_obj.conn[new_obj.edge[e_ind][0]]])/len(new_obj.conn[new_obj.edge[e_ind][0]])
        paz=sum([new_obj.z[j] for j in new_obj.conn[new_obj.edge[e_ind][0]]])/len(new_obj.conn[new_obj.edge[e_ind][0]])
        pbx=sum([new_obj.x[j] for j in new_obj.conn[new_obj.edge[e_ind][1]]])/len(new_obj.conn[new_obj.edge[e_ind][1]])
        pby=sum([new_obj.y[j] for j in new_obj.conn[new_obj.edge[e_ind][1]]])/len(new_obj.conn[new_obj.edge[e_ind][1]])
        pbz=sum([new_obj.z[j] for j in new_obj.conn[new_obj.edge[e_ind][1]]])/len(new_obj.conn[new_obj.edge[e_ind][1]])
        # pc: center point of the edge
        pcx=(new_obj.x[new_obj.edge[e_ind][0]]+new_obj.x[new_obj.edge[e_ind][1]])/2
        pcy=(new_obj.y[new_obj.edge[e_ind][0]]+new_obj.y[new_obj.edge[e_ind][1]])/2
        pcz=(new_obj.z[new_obj.edge[e_ind][0]]+new_obj.z[new_obj.edge[e_ind][1]])/2
        pc=np.array([pcx,pcy,pcz])
        # va, vb: two vectors to determine the plane where the rotation happens
        va=np.array([pax-pbx,pay-pby,paz-pbz])
        vb=np.array([new_obj.x[new_obj.edge[e_ind][0]]-new_obj.x[new_obj.edge[e_ind][1]],new_obj.y[new_obj.edge[e_ind][0]]-new_obj.y[new_obj.edge[e_ind][1]],new_obj.z[new_obj.edge[e_ind][0]]-new_obj.z[new_obj.edge[e_ind][1]]])

        angle=math.acos(min(np.dot(va,vb)/np.sqrt(np.sum(va**2))/np.sqrt(np.sum(vb**2)),1))/math.pi*180
        # calculate the angle of va and vb, if they parallel, must use another vector vc to determine the normalized vector
        if angle>5:
            vn=np.cross(va,vb)
        else:
            vc=np.array([new_obj.x[new_obj.conn[new_obj.edge[e_ind][0]][0]]-new_obj.x[new_obj.conn[new_obj.edge[e_ind][0]][1]],\
                         new_obj.y[new_obj.conn[new_obj.edge[e_ind][0]][0]]-new_obj.y[new_obj.conn[new_obj.edge[e_ind][0]][1]],\
                         new_obj.z[new_obj.conn[new_obj.edge[e_ind][0]][0]]-new_obj.z[new_obj.conn[new_obj.edge[e_ind][0]][1]]])
            vn=np.cross(vb,vc)
        # vt: the direction after rotation
        vt=np.cross(vb,vn)
        vt=vt/np.sqrt(np.sum(vt**2))
        d=np.sqrt(np.sum(vb**2))/2
        # mpa, mpb: mutated points a and b
        mpa=pc+vt*d
        mpb=pc-vt*d
        new_obj=new_obj.Duplicate()
        new_obj.x[new_obj.edge[e_ind][0]],new_obj.x[new_obj.edge[e_ind][1]]=mpa[0],mpb[0]
        new_obj.y[new_obj.edge[e_ind][0]],new_obj.y[new_obj.edge[e_ind][1]]=mpa[1],mpb[1]
        new_obj.z[new_obj.edge[e_ind][0]],new_obj.z[new_obj.edge[e_ind][1]]=mpa[2],mpb[2]
        new_obj.name=new_obj.name+'-sw-'+str(new_obj.edge[e_ind][0])+'_'+str(new_obj.edge[e_ind][1])
        new_obj.center=[sum(new_obj.x)/len(new_obj.x),sum(new_obj.y)/len(new_obj.y),sum(new_obj.z)/len(new_obj.z)]
        new_obj.edge,new_obj.conn,new_obj.ring,new_obj.connring,new_obj.pore=[],[],[],[],[]    
        return new_obj
    
    # single point vacancy
    def SingleV(self,p_ind:int):
        new_obj=self.Duplicate()
        if p_ind>len(new_obj.x):
            print('point index error')
            return

        new_obj.x=new_obj.x[:p_ind]+new_obj.x[p_ind+1:]
        new_obj.y=new_obj.y[:p_ind]+new_obj.y[p_ind+1:]
        new_obj.z=new_obj.z[:p_ind]+new_obj.z[p_ind+1:]
        new_obj.atom=new_obj.atom[:p_ind]+new_obj.atom[p_ind+1:]
        new_obj.name=new_obj.name+'-sv-'+str(p_ind)
        new_obj.center=[sum(new_obj.x)/len(new_obj.x),sum(new_obj.y)/len(new_obj.y),sum(new_obj.z)/len(new_obj.z)]
        new_obj.center,new_obj.edge,new_obj.conn,new_obj.ring,new_obj.connring,new_obj.pore=[],[],[],[],[],[]
        return new_obj
    
    # double points vacancy
    def DoubleV(self,e_ind:int):
        new_obj=self.Duplicate()
        if new_obj.edge==[]:
            new_obj.Analyzer()
        if e_ind>len(new_obj.edge):
            print('edge index error')
            return

        i,j=min(new_obj.edge[e_ind]),max(new_obj.edge[e_ind])
        new_obj.x=new_obj.x[:i]+new_obj.x[i+1:j]+new_obj.x[j+1:]
        new_obj.y=new_obj.y[:i]+new_obj.y[i+1:j]+new_obj.y[j+1:]
        new_obj.z=new_obj.z[:i]+new_obj.z[i+1:j]+new_obj.z[j+1:]
        new_obj.atom=new_obj.atom[:i]+new_obj.atom[i+1:j]+new_obj.atom[j+1:]
        new_obj.name=new_obj.name+'-dv-'+str(i)+'_'+str(j)
        new_obj.center=[sum(new_obj.x)/len(new_obj.x),sum(new_obj.y)/len(new_obj.y),sum(new_obj.z)/len(new_obj.z)]
        new_obj.center,new_obj.edge,new_obj.conn,new_obj.ring,new_obj.connring,new_obj.pore=[],[],[],[],[],[]
        return new_obj

    # multiple points vacancy    
    def MultiV(self,p_list:list):
        new_obj=self.Duplicate()
        for i in sorted(p_list,reverse=True):
            new_obj.x=new_obj.x[:i]+new_obj.x[i+1:]
            new_obj.y=new_obj.y[:i]+new_obj.y[i+1:]
            new_obj.z=new_obj.z[:i]+new_obj.z[i+1:]            
            new_obj.atom=new_obj.atom[:i]+new_obj.atom[i+1:]
        for i in sorted(p_list):
            new_obj.name=new_obj.name+'-sv-'+str(i)
        new_obj.center=[sum(new_obj.x)/len(new_obj.x),sum(new_obj.y)/len(new_obj.y),sum(new_obj.z)/len(new_obj.z)]
        new_obj.center,new_obj.edge,new_obj.conn,new_obj.ring,new_obj.connring,new_obj.pore=[],[],[],[],[],[]
        return new_obj            

    # fill vacancy with metal
    def Fill(self,p_ind:list,metal:list):
        new_obj=self.Duplicate()
        if new_obj.pore==[]:
            new_obj.Getpores()
        for i in p_ind:
            if i>len(new_obj.pore)-1:
                print ('pore index error, aborted')
                return
        # calculate the geometric center of the pore
        for p in range(len(p_ind)):
            x,y,z=0,0,0
            tag=''
            for i in new_obj.pore[p_ind[p]]:
                x+=new_obj.x[i]
                y+=new_obj.y[i]
                z+=new_obj.z[i]
            x=x/len(new_obj.pore[p_ind[p]])
            y=y/len(new_obj.pore[p_ind[p]])
            z=z/len(new_obj.pore[p_ind[p]])
            new_obj.x.append(x)
            new_obj.y.append(y)
            new_obj.z.append(z)
            new_obj.atom.append(metal[p])
            tag=tag+'-'+str(p_ind[p])+str(metal[p])
            
        new_obj.name+=tag
        new_obj.center,new_obj.edge,new_obj.conn,new_obj.ring,new_obj.connring,new_obj.pore=[],[],[],[],[],[]
        return new_obj
    
    # swap pore carbon with other elements (e.g., O, N, P, etc.)
    # swap function should not be used to structures that has elements other than carbon
    def Swap(self,p_ind:list,nonmetal:list):
        new_obj=self.Duplicate()
        if new_obj.pore==[]:
            new_obj.Getpores()
        if len(new_obj.x)!=new_obj.atom.count('C'):
            print('warning: the structure has already been modified')
        tag=''
        pore_atoms=[]
        for i in new_obj.pore:
            pore_atoms+=i
        for i in range(len(p_ind)):
            if p_ind[i] not in pore_atoms:
                print('warning: atom does not belong to a vacancy, aborted')
                return
        for i in range(len(p_ind)):        
            new_obj.atom[p_ind[i]]=nonmetal[i]
            tag=tag+'-'+str(p_ind[i])+str(nonmetal[i])
        new_obj.name=self.name+tag
        new_obj.center,new_obj.edge,new_obj.conn,new_obj.ring,new_obj.connring,new_obj.pore=[],[],[],[],[],[]
        return new_obj
    
    # visualize mutation tree
    def Tree(self):
        
        return       
