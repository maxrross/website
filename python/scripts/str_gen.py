from NPC import quantumdot, filter_by_symmetry_DV, filter_by_symmetry_SV,filter_by_symmetry_SW,filter_by_symmetry_MV,\
    get_SV_info,get_DV_info,get_SW_info
import os
import math
from utils import create_sub_dir, Write_xyz, find_metal_and_its_neighbor, get_metal_dopant_symmetry, get_transfered_boundary_index,\
    create_new_H_coor,get_metal_dopant_symmetry_DV,get_transfered_boundary_index_SW,delete_unreasonable_potential_edge
from str_component import filter_carbon_flake_dopant_by_dopant_number, generate_zigzag, generate_armchair,\
 generate_square, get_carbon_flake_with_H, fill_for_vacancy,flatten_list

class carbon_flake():
    cwd = os.getcwd()
    parent_dir = f'{cwd}/OUTPUT'
    available_flakes = ['zigzag', 'armchair', 'square']
    available_coordination_number=[3, 4]
       
    def create_carbon_flakes(self,size:int, flake_type:str, add_H:bool=True):
        if not flake_type.lower() in self.available_flakes:
            raise TypeError('Wrong flake! Available flakes: zigzag, armchair, square')
            
        self.size=size
        self.flake_type=flake_type   
        
        # 1. create pure carbon flakes
        if flake_type=="zigzag":
            _,_,_, coordinates, atom_list, name = generate_zigzag(size)
                
        elif flake_type=="armchair":  
            _,_,_, coordinates, atom_list, name = generate_armchair(size)

        elif flake_type=="square":
            _,_,_, coordinates, atom_list, name = generate_square(size)  
            
        sub_dir=create_sub_dir(flake_type)[0]
        self.sub_dir=sub_dir # save it as a glob variable      
        
        coordinates_H, atom_list_H, name_H = get_carbon_flake_with_H(size, flake_type)
        
        if add_H==True:
            self.coordinates, self.atom_list,self.name_list=[coordinates_H], [atom_list_H], [name_H]
        else:
            self.coordinates, self.atom_list,self.name_list=[coordinates], [atom_list], [name]
        
        self.count_num=1
        self.metal_count=0  # tell whether already add metal or not
        
    def add_metal_site(self, coordination_number:int, metal_type:str, dopant_type:list=[], dopant_number=math.inf, add_H:bool=True):
        """
        if not specify dopant number, then ouput all 
        """
        if not coordination_number in self.available_coordination_number:
            raise TypeError('Wrong coordination number! Available coordination number: 3, 4')
            
        if coordination_number==3:
            vacancy_type="single"
        elif coordination_number==4:
            vacancy_type="double"
        
        if dopant_number!=math.inf:
            self.coordinates,self.atom_list,self.name_list=filter_carbon_flake_dopant_by_dopant_number(self.size,
                                            self.flake_type,coordination_number,metal_type,dopant_type,dopant_number)

        else: 
            self.coordinates,self.atom_list,self.name_list=fill_for_vacancy(self.size,self.flake_type,
                                                                            vacancy_type,metal_type,dopant_type)
        if add_H==False:
            atom_list=[]
            coordinates=[]

            for index,value in enumerate(self.atom_list):
                H_index=[i for i in range(len(value)) if value[i]=="H"]
                coor=[self.coordinates[index][i] for i in range(len(value)) if i not in H_index]  
                ato=[value[i] for i in range(len(value)) if i not in H_index] 
                atom_list.append(ato)
                coordinates.append(coor)
            self.coordinates=coordinates
            self.atom_list=atom_list    
            self.name_list=[ i.replace('-H-', '') for i in self.name_list]                                                                     
            
        self.metal_type=[metal_type] # make it into a list
        self.dopant_type=dopant_type
        self.coordination_number=coordination_number
        self.sub_dir=os.path.join(self.sub_dir,metal_type,"coordination_number_"+str(self.coordination_number))
        if dopant_number!=math.inf:
            self.sub_dir=os.path.join(self.sub_dir,"dopant_number_"+str(dopant_number))
        self.metal_count+=1
        
    def count(self):
        if self.count_num==1:
            return f'{len(self.coordinates)} files can be outputed'
        elif self.count_num==2:
            counts=flatten_list(self.coordinates)
            return f'{len(counts)} files can be outputed'
    
    def create_single_vacancy(self, add_H:bool=True):
        qdot=quantumdot()
        if self.metal_count==0:
            qdot.x=[i[0] for i in self.coordinates[0]]
            qdot.y=[i[1] for i in self.coordinates[0]]
            qdot.z=[i[2] for i in self.coordinates[0]]
            qdot.atom=['C']*len(qdot.x)
            qdot.name=self.flake_type+"-"+str(self.size)
            
            qdot.Getpores()
            qdot.DistanceMatrix()
            ind_list=[i for i in range(len(qdot.atom)) if i not in qdot.boundary]
            self.coordinates,self.atom_list,self.name_list,_,_=filter_by_symmetry_SV(qdot,ind_list)
            self.sub_dir=os.path.join(self.sub_dir,"single_vacancy")
            
        elif self.metal_count==1:
            self.count_num+=1
            self.sub_dir=[os.path.join(self.sub_dir,i,"single_vacancy") for i in self.name_list ]
            coordinates,atom_list,name_list=[],[],[]
            
            for index,value in enumerate(self.atom_list):
                qdot.name=self.name_list[index]
                
                # index of metal and its neighbors
                ind_metal_nbor=find_metal_and_its_neighbor(self.coordinates[index],
                                                           value,self.metal_type,self.coordination_number)
                # coordinates of metal and its neighbors
                metal_nbor_coor=[j for i,j in enumerate(self.coordinates[index]) if i in ind_metal_nbor]
                
                # index for H atoms 
                H_index=[i for i in range(len(value)) if value[i]=="H"]
                
                qdot.atom=[value[i] for i in range(len(value)) if i not in H_index]
                qdot.x=[self.coordinates[index][i][0] for i in range(len(value)) if i not in H_index]
                qdot.y=[self.coordinates[index][i][1] for i in range(len(value)) if i not in H_index]
                qdot.z=[self.coordinates[index][i][2] for i in range(len(value)) if i not in H_index]
                qdot.coordinate=[(a,b,c) for a,b,c in zip(qdot.x,qdot.y,qdot.z)]
                

                new_boundary=get_transfered_boundary_index(self.flake_type,self.size,qdot) 
                ind_list=[i for i in range(len(qdot.atom)) if i not in new_boundary]
                
                ind_metal_nbor_new=[qdot.coordinate.index(i) for i in metal_nbor_coor]
                ind_list=[i for i in ind_list if i not in ind_metal_nbor_new]
                
                # get nonmetal elemetals list of metal neighbors
                nonmetal_ele=[qdot.atom[i] for i in range(len(qdot.atom)) if i in ind_metal_nbor_new[1:]]
                nonmetal_coor=metal_nbor_coor[1:]
                metal_coor=metal_nbor_coor[0]
                # get a new ind_list by using structure symmetry
                new_ind_list=get_metal_dopant_symmetry(self.coordination_number,metal_coor,nonmetal_coor,nonmetal_ele,ind_list,qdot)
                
                coord,ato,nam=get_SV_info(qdot,new_ind_list)
                
                # add H back 
                if add_H==True:
                    H_coor=create_new_H_coor(self.flake_type,self.size)
                    H_atom=["H"]*len(H_coor)
                
                    for i in range(len(ato)):
                        ato[i].extend(H_atom)
                        coord[i].extend(H_coor)
                    # nam[i]=nam[i]+"-H"
                
                coordinates.append(coord)
                atom_list.append(ato)
                name_list.append(nam)
                
            self.coordinates=coordinates
            self.atom_list=atom_list
            self.name_list=name_list
                
    def create_double_vacancy(self, add_H:bool=True):
        q=quantumdot()
        if self.metal_count==0:
            q.x=[i[0] for i in self.coordinates[0]]
            q.y=[i[1] for i in self.coordinates[0]]
            q.z=[i[2] for i in self.coordinates[0]]
            q.atom=['C']*len(q.x)
            q.name=self.flake_type+"-"+str(self.size)
            
            q.Getpores()
            q.DistanceMatrix()
            ind_list=[i for i in range(len(q.atom)) if i not in q.boundary] 
            self.coordinates,self.atom_list,self.name_list,_,_=filter_by_symmetry_DV(q,ind_list)
            self.sub_dir=os.path.join(self.sub_dir,"double_vacancy")
        
        elif self.metal_count==1:
            self.count_num+=1
            self.sub_dir=[os.path.join(self.sub_dir,i,"double_vacancy") for i in self.name_list ]
            coordinates,atom_list,name_list=[],[],[]

            for index,value in enumerate(self.atom_list):
                q.name=self.name_list[index]
                
                # index of metal and its neighbors
                ind_metal_nbor=find_metal_and_its_neighbor(self.coordinates[index],
                                                           value,self.metal_type,self.coordination_number)
                # coordinates of metal and its neighbors
                metal_nbor_coor=[j for i,j in enumerate(self.coordinates[index]) if i in ind_metal_nbor]
                
                # index for H atoms 
                H_index=[i for i in range(len(value)) if value[i]=="H"]
                q.atom=[value[i] for i in range(len(value)) if i not in H_index]
                q.x=[self.coordinates[index][i][0] for i in range(len(value)) if i not in H_index]
                q.y=[self.coordinates[index][i][1] for i in range(len(value)) if i not in H_index]
                q.z=[self.coordinates[index][i][2] for i in range(len(value)) if i not in H_index]
                q.coordinate=[(a,b,c) for a,b,c in zip(q.x,q.y,q.z)]
                q.Analyzer()

                new_boundary=get_transfered_boundary_index(self.flake_type,self.size,q) 
                ind_list=[i for i in range(len(q.atom)) if i not in new_boundary]
                ind_metal_nbor_new=[q.coordinate.index(i) for i in metal_nbor_coor]
                ind_list=[i for i in ind_list if i not in ind_metal_nbor_new]
                # get nonmetal elemetals list of metal neighbors
                nonmetal_ele=[q.atom[i] for i in range(len(q.atom)) if i in ind_metal_nbor_new[1:]]
                nonmetal_coor=metal_nbor_coor[1:]
                metal_coor=metal_nbor_coor[0]
                # find potential edge that can create double vacancy
                potential_edge=[i for i in q.edge if i[0] in ind_list and i[1] in ind_list]
                potential_edge_new=get_metal_dopant_symmetry_DV(self.coordination_number,
                                            metal_coor,nonmetal_coor,nonmetal_ele,potential_edge,q)

                potential_edge_new=delete_unreasonable_potential_edge(potential_edge_new,q)
                potential_edge_index_list=[q.edge.index(i) for i in potential_edge_new]
                
                coord,ato,nam=get_DV_info(q,potential_edge_index_list)
                # add H back 
                if add_H==True:
                    H_coor=create_new_H_coor(self.flake_type,self.size)
                    H_atom=["H"]*len(H_coor)
                    for i in range(len(ato)):
                        ato[i].extend(H_atom)
                        coord[i].extend(H_coor)
                
                coordinates.append(coord)
                atom_list.append(ato)
                name_list.append(nam)
                
            self.coordinates=coordinates
            self.atom_list=atom_list
            self.name_list=name_list                

    def create_Stone_Wales(self, add_H:bool=True):
        q=quantumdot()
        if self.metal_count==0:
            q.x=[i[0] for i in self.coordinates[0]]
            q.y=[i[1] for i in self.coordinates[0]]
            q.z=[i[2] for i in self.coordinates[0]]
            q.atom=['C']*len(q.x)
            q.name=self.flake_type+"-"+str(self.size)
            
            q.Getpores()
            q.DistanceMatrix()
            ind_list=[i for i in range(len(q.atom)) if i not in q.boundary_with_H] 
            self.coordinates,self.atom_list,self.name_list=filter_by_symmetry_SW(q,ind_list)
            self.sub_dir=os.path.join(self.sub_dir,"Stone_Wales")

        elif self.metal_count==1:
            self.count_num+=1
            self.sub_dir=[os.path.join(self.sub_dir,i,"Stone_Wales") for i in self.name_list ]
            coordinates,atom_list,name_list=[],[],[]

            for index,value in enumerate(self.atom_list):
                q.name=self.name_list[index]
                
                # index of metal and its neighbors
                ind_metal_nbor=find_metal_and_its_neighbor(self.coordinates[index],
                                                           value,self.metal_type,self.coordination_number)
                # coordinates of metal and its neighbors
                metal_nbor_coor=[j for i,j in enumerate(self.coordinates[index]) if i in ind_metal_nbor]
                
                # index for H atoms 
                H_index=[i for i in range(len(value)) if value[i]=="H"]
                q.atom=[value[i] for i in range(len(value)) if i not in H_index]
                q.x=[self.coordinates[index][i][0] for i in range(len(value)) if i not in H_index]
                q.y=[self.coordinates[index][i][1] for i in range(len(value)) if i not in H_index]
                q.z=[self.coordinates[index][i][2] for i in range(len(value)) if i not in H_index]
                q.coordinate=[(a,b,c) for a,b,c in zip(q.x,q.y,q.z)]
                q.Analyzer()

                new_boundary=get_transfered_boundary_index_SW(self.flake_type,self.size,q) 
                ind_list=[i for i in range(len(q.atom)) if i not in new_boundary]
                ind_metal_nbor_new=[q.coordinate.index(i) for i in metal_nbor_coor]
                ind_list=[i for i in ind_list if i not in ind_metal_nbor_new]
                # get nonmetal elemetals list of metal neighbors
                nonmetal_ele=[q.atom[i] for i in range(len(q.atom)) if i in ind_metal_nbor_new[1:]]
                nonmetal_coor=metal_nbor_coor[1:]
                metal_coor=metal_nbor_coor[0]
                # find potential edge that can create double vacancy
                potential_edge=[i for i in q.edge if i[0] in ind_list and i[1] in ind_list]
                potential_edge_new=get_metal_dopant_symmetry_DV(self.coordination_number,
                                            metal_coor,nonmetal_coor,nonmetal_ele,potential_edge,q)
                potential_edge_new=delete_unreasonable_potential_edge(potential_edge_new,q) 
                potential_edge_index_list=[q.edge.index(i) for i in potential_edge_new]
                
                coord,ato,nam=get_SW_info(q,potential_edge_index_list)
                # add H back 
                if add_H==True:
                    H_coor=create_new_H_coor(self.flake_type,self.size)
                    H_atom=["H"]*len(H_coor)
                    for i in range(len(ato)):
                        ato[i].extend(H_atom)
                        coord[i].extend(H_coor)
                
                coordinates.append(coord)
                atom_list.append(ato)
                name_list.append(nam)
                
            self.coordinates=coordinates
            self.atom_list=atom_list
            self.name_list=name_list                            
    
    def create_multiple_vacancy(self,vacancy_number:int,pores_allow:bool=True):
        q=quantumdot()
        if self.metal_count==0:
            q.x=[i[0] for i in self.coordinates[0]]
            q.y=[i[1] for i in self.coordinates[0]]
            q.z=[i[2] for i in self.coordinates[0]]
            q.atom=['C']*len(q.x)
            q.name=self.flake_type+"-"+str(self.size)
            
            q.Getpores()
            q.DistanceMatrix()
            ind_list=[i for i in range(len(q.atom)) if i not in q.boundary] 
            self.coordinates,self.atom_list,self.name_list=filter_by_symmetry_MV(q,ind_list,vacancy_number,pores_allow)
            self.sub_dir=os.path.join(self.sub_dir,"multiple_vacancy")
    

    def Write_xyz(self):
        """
        call this function will save the coordinates of carbon flake dopants into xyz file.
        """      
        if self.count_num==1:
            for a,b,c in zip(self.coordinates,self.atom_list,self.name_list):
                Write_xyz(a,b,c,self.sub_dir,self.parent_dir) 
            print(f"Done! {len(self.coordinates)} files are ouputed in {self.parent_dir}/{self.sub_dir}.") 
        
        if self.count_num==2:
            for i,j in enumerate(self.sub_dir):
                for a,b,c in zip(self.coordinates[i],self.atom_list[i],self.name_list[i]):
                    Write_xyz(a,b,c,j,self.parent_dir) 
                    
                print(f"Done! {len(self.coordinates[i])} files are ouputed in {self.parent_dir}/{j}.")                   