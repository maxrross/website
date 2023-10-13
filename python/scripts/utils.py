import os
import math
from NPC import quantumdot
from str_component import generate_zigzag, generate_armchair, generate_square, get_distance_from_two_point,find_k_and_b_for_line,\
     get_carbon_flake_with_H, create_vacancy, create_SW_vacancy, fill_for_vacancy, get_n_atoms_from_center,get_distance_from_center_point,\
        get_distance_from_two_point

# write structure to xyz file
def Write_xyz(coordinates, atom_list, name, sub_dir: str, parent_dir: str):
    if not os.path.exists(f"{parent_dir}/{sub_dir}") : os.makedirs(f"{parent_dir}/{sub_dir}")
    file_name = f'{parent_dir}/{sub_dir}/' + name + '.xyz'
    num_atoms = len(atom_list)
    
    with open(file_name, 'w') as xyz_file:
        xyz_file.write(f"{num_atoms}\n") # Write the number of atoms as the first line
        xyz_file.write(f"{name}\n") 
        for (x,y,z), atom in zip(coordinates,atom_list):
            xyz_file.write(f"{atom} {x:.6f} {y:.6f} {z:.6f}\n")

def Write_xyz_2(coordinates, atom_list, name, sub_dir: str, sub_sub_dir:str, parent_dir: str):
    if not os.path.exists(f"{parent_dir}/{sub_dir}/{sub_sub_dir}") : os.makedirs(f"{parent_dir}/{sub_dir}/{sub_sub_dir}")
    file_name = f'{parent_dir}/{sub_dir}/{sub_sub_dir}/' + name + '.xyz'
    num_atoms = len(atom_list)
    
    with open(file_name, 'w') as xyz_file:
        xyz_file.write(f"{num_atoms}\n") # Write the number of atoms as the first line
        xyz_file.write(f"{name}\n") 
        for (x,y,z), atom in zip(coordinates,atom_list):
            xyz_file.write(f"{atom} {x:.6f} {y:.6f} {z:.6f}\n")

def create_sub_dir(flake_type:str):
    name1=flake_type+"_flakes"
    name2=flake_type+"_flakes_H"
    name3=flake_type+"_flakes_vacancy"
    name4=flake_type+"_flakes_dopant"
    return [name1,name2,name3,name4]

def find_metal_and_its_neighbor(coordinates,atom_list,metal_type,atom_num=3):
    metal_coor=[]
    atom_list_new=[i for i in atom_list if i !="H"]
    coordinates_without_H=[coordinates[i] for i in range(len(atom_list)) if atom_list[i]!="H"]
    for i,j in enumerate(atom_list_new):
        if j!="C" and j in metal_type:
            metal_coor.append(coordinates_without_H[i])
            
    coordinates_without_metal=[i for i in coordinates_without_H if i not in metal_coor]
    # get metal neighbor coordinates by distance 
    neighbor_coordinates=get_n_atoms_from_center(coordinates_without_metal,metal_coor[0],atom_num)
    neighbor_coordinates=metal_coor+neighbor_coordinates
    # return a index only has metal and its neighbors
    output=[coordinates.index(i) for i in neighbor_coordinates] 
    return output

def are_two_elements_in_all_same(nonmetal_coor,atom_list):
    # if vacacncy if single, and when two element on two sides of symmetric axis, then is symmetric 
    count=0
    dist=[round(get_distance_from_center_point([i])[0],2) for i in nonmetal_coor]
    
    for i in range(len(atom_list)):
        for j in range(i+1,len(atom_list)):
            if atom_list[i]==atom_list[j] and dist[i]==dist[j]:
                count+=1
                
    if count!=0 :
        return True
    else:
        return False

def are_all_elements_same(input_list):
    if not input_list:
        return True  # An empty list is considered to have all elements the same (no elements to compare).

    first_element = input_list[0]
    for element in input_list:
        if element != first_element:
            return False  # Found an element that is different, so not all elements are the same.

    return True  # All elements in the list are the same.

def get_metal_dopant_symmetry(coordination_number,metal_coor, nonmetal_coor, nonmetal_atom,ind_list,q:object):
    a=1.42
    
    if coordination_number==3:
        # first think of metal element, whether it on symmetric axis or not
        if round(get_distance_from_center_point([metal_coor])[0],2) % a == 0 and \
        are_two_elements_in_all_same(nonmetal_coor, nonmetal_atom)==True:
            # find the line that pass through center point and metal atom
            k,b=find_k_and_b_for_line(metal_coor,[0,0,0])
            if k==math.inf:
                # only left atoms whose x value >=0 
                new_ind_list=[i for i in ind_list if q.x[i]>=0]
            else:
                # select half dot that lie in the two side of symmetric line
                new_ind_list=[i for i in ind_list if round(q.x[i]*k+b,1) <= round(q.y[i],1)]
        else:
            new_ind_list=ind_list
    
    elif coordination_number==4:   
        if round(get_distance_from_center_point([metal_coor])[0],2) % (a/2) == 0 and are_all_elements_same(nonmetal_atom)==True:
            # find the line that pass through center point and metal atom
            k,b=find_k_and_b_for_line(metal_coor,[0,0,0])
            if k==math.inf:
                # only left atoms whose x value >=0 
                new_ind_list=[i for i in ind_list if q.x[i]>=0]
            else:
                # select half dot that lie in the two side of symmetric line
                new_ind_list=[i for i in ind_list if round(q.x[i]*k+b,1) <= round(q.y[i],1)]
        else:
            new_ind_list=ind_list
        
    return new_ind_list   

def get_metal_dopant_symmetry_DV(coordination_number,metal_coor,nonmetal_coor,nonmetal_atom,potential_edge,q:object):
    a=1.42
    
    if coordination_number==3:
        # first think of metal element, whether it on symmetric axis or not
        if round(get_distance_from_center_point([metal_coor])[0],2) % a == 0 and \
        are_two_elements_in_all_same(nonmetal_coor, nonmetal_atom)==True:
            # find the line that pass through center point and metal atom
            k,b=find_k_and_b_for_line(metal_coor,[0,0,0])
            if k==math.inf:
                # only left atoms whose x value >=0 
                new_potential_edge=[i for i in potential_edge if q.x[i[0]]>=0 and q.x[i[1]]>=0]
            else:
                # select half dot that lie in the two side of symmetric line
                new_potential_edge=[i for i in potential_edge if round(q.x[i[0]]*k+b,1) <= round(q.y[i[0]],1)
                                   and round(q.x[i[1]]*k+b,1) <= round(q.y[i[1]],1)] 
        else:
            new_potential_edge=potential_edge
    
    elif coordination_number==4:   
        if round(get_distance_from_center_point([metal_coor])[0],2) % (a/2) == 0 and are_all_elements_same(nonmetal_atom)==True:
            # find the line that pass through center point and metal atom
            k,b=find_k_and_b_for_line(metal_coor,[0,0,0])
            if k==math.inf:
                # only left atoms whose x value >=0 
                new_potential_edge=[i for i in potential_edge if q.x[i[0]]>=0 and q.x[i[1]]>=0]
            else:
                # select half dot that lie in the two side of symmetric line
                new_potential_edge=[i for i in potential_edge if round(q.x[i[0]]*k+b,1) <= round(q.y[i[0]],1)
                                   and round(q.x[i[1]]*k+b,1) <= round(q.y[i[1]],1)] 
        else:
            new_potential_edge=potential_edge
        
    return new_potential_edge 

def get_transfered_boundary_index(flake_type, size, qdot:object):
    """
    give the right index of boundary atoms after it do add metal and nonmetal atoms.  
    """
    Q=quantumdot()
    if flake_type=="zigzag":
        Q.Hexzigzag(size)
    elif flake_type=="armchair":
        Q.Hexarmchair(size)
    elif flake_type=="square":
        Q.Square(size)
    Q.coordinate=[(a,b,c) for a,b,c in zip(Q.x,Q.y,Q.z)]
    Q.Getpores()
    boundary_coor=[Q.coordinate[i] for i in Q.boundary]
    # get rid of data is not in Q.coordinate
    new_boundary_coor=[i for i in qdot.coordinate if i in boundary_coor]
    new_boundary=[qdot.coordinate.index(i) for i in new_boundary_coor]
    
    return new_boundary

def get_transfered_boundary_index_SW(flake_type, size, qdot:object):
    """
    give the right index of boundary atoms after it do add metal and nonmetal atoms.  
    Difference between this function and get_transfered_boundary_index is that this function is for boundary num are different.
    In SW, we should also consider points on the edge of the flake.
    """
    Q=quantumdot()
    if flake_type=="zigzag":
        Q.Hexzigzag(size)
    elif flake_type=="armchair":
        Q.Hexarmchair(size)
    elif flake_type=="square":
        Q.Square(size)
    Q.coordinate=[(a,b,c) for a,b,c in zip(Q.x,Q.y,Q.z)]
    Q.Getpores()
    boundary_coor=[Q.coordinate[i] for i in Q.boundary_with_H]
    # get rid of data is not in Q.coordinate
    new_boundary_coor=[i for i in qdot.coordinate if i in boundary_coor]
    new_boundary=[qdot.coordinate.index(i) for i in new_boundary_coor]
    
    return new_boundary


def create_new_H_coor(flake_type,size):
    q=quantumdot()
    if flake_type=="zigzag":
        q.Hexzigzag(size)
    elif flake_type=="armchair":
        q.Hexarmchair(size)
    elif flake_type=="square":
        q.Square(size)

    q2=q.Duplicate()
    q2=q2.Hydrogenation()
    q2.coordinate=[(a,b,c) for a,b,c in zip(q2.x,q2.y,q2.z)]
    H_coor=[q2.coordinate[i] for i,j in enumerate(q2.atom) if j=="H"]
    
    return H_coor

def delete_unreasonable_potential_edge(potential_edge: list, q: object):
    reasonable_edges = []
    for edge in potential_edge:
        index1 = q.coordinate[edge[0]]
        index2 = q.coordinate[edge[1]]
        if get_distance_from_two_point(index1, index2) < 1.5:
            reasonable_edges.append(edge)
    return reasonable_edges
    
# def create_carbon_vacancy(size:int, flake_type:str, vacancy_type:str):
#     flake_type=flake_type.lower()
#     vacancy_type=vacancy_type.lower()

#     cwd = os.getcwd()
#     parent_dir = f'{cwd}/OUTPUT'
    
#     if flake_type=="zigzag":
#         _,_,_, coordinates, atom_list, name = generate_zigzag(size)
            
#     elif flake_type=="armchair":  
#         _,_,_, coordinates, atom_list, name = generate_armchair(size)

#     elif flake_type=="square":
#         _,_,_, coordinates, atom_list, name = generate_square(size)
    
#     if vacancy_type!="sw":
#         coordinates, _, atom_list, _, name_list=create_vacancy(size,flake_type,vacancy_type)
#     else:
#         coordinates, atom_list, name_list=create_SW_vacancy(size,flake_type,vacancy_type)

#     sub_dir=create_sub_dir(flake_type)[2]
#     sub_sub_dir=vacancy_type+"_vacancy"

#     for a,b,c in zip(coordinates,atom_list,name_list):
#         Write_xyz_2(a,b,c,sub_dir,sub_sub_dir,parent_dir)    

# def create_carbon_flakes(size:int, flake_type:str, vacancy_type:str, metal:str, nonmetal_list:list): 
#     flake_type=flake_type.lower()
#     vacancy_type=vacancy_type.lower()

#     cwd = os.getcwd()
#     parent_dir = f'{cwd}/OUTPUT'
    
#     if not isinstance(nonmetal_list, list):
#         raise TypeError("The input nonmetal parameter must be a list.")
    
#     if size<2:
#         raise ValueError("The input size parameter must be greater than 1.")
    
#     else: 
#         # 1. create pure carbon flakes
#         if flake_type=="zigzag":
#             _,_,_, coordinates, atom_list, name = generate_zigzag(size)
                
#         elif flake_type=="armchair":  
#             _,_,_, coordinates, atom_list, name = generate_armchair(size)

#         elif flake_type=="square":
#             _,_,_, coordinates, atom_list, name = generate_square(size)
        
#         else: 
#             raise ValueError("Unkown structure, try a new one!")

#         sub_dir=create_sub_dir(flake_type)[0]
#         Write_xyz(coordinates, atom_list, name, sub_dir, parent_dir)
        
#         # 2.create carbon flake with Hydrogen
#         coordinates, atom_list, name = get_carbon_flake_with_H(size,flake_type)
#         sub_dir=create_sub_dir(flake_type)[1]
#         Write_xyz(coordinates,atom_list,name,sub_dir,parent_dir) 
        
#         # 3.create carbon flake with vacancy
#         coordinates, _, atom_list, _, name_list=create_vacancy(size,flake_type,vacancy_type)
#         sub_dir=create_sub_dir(flake_type)[2]
#         sub_sub_dir=vacancy_type+"_vacancy"
#         for a,b,c in zip(coordinates,atom_list,name_list):
#             Write_xyz_2(a,b,c,sub_dir,sub_sub_dir,parent_dir)
        
#         # 4.create carbon flake with metal and nonmetal
#         coordinates, atom_list, name_list=fill_for_vacancy(size,flake_type,vacancy_type,metal,nonmetal_list)
#         sub_dir=create_sub_dir(flake_type)[3]
#         sub_sub_dir=vacancy_type+"_vacancy"
#         for a,b,c in zip(coordinates,atom_list,name_list):
#             Write_xyz_2(a,b,c,sub_dir,sub_sub_dir,parent_dir) 
        
#         print(f"Done! The output files are in {parent_dir}.")



