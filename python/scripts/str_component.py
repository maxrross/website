import math
import numpy as np
from itertools import combinations_with_replacement, permutations, combinations
from collections import defaultdict
from NPC import filter_by_symmetry_SV,filter_by_symmetry_DV, quantumdot

def generate_zigzag(size: int, a=1.42):
    """Generates the hexagon zigzag flake based on the given size

    :param size: the size of the structure
    :type size: int
    
    """
    
    x0, y0 = [a * math.sqrt(3) / 2, a * math.sqrt(3)], [a / 2, a]
    dx, dy = a * math.sqrt(3), a * 1.5
    xx, yy = [], []
    x, y = np.zeros((2 * size, 4 * size)), np.zeros((2 * size, 4 * size))
    
    for i in range(-size, size):
        xx.extend([x0[0] + dx * i, x0[1] + dx * i])
        yy.extend([y0[0] + dy * 0, y0[1] + dy * 0])
    
    xx, yy = np.array(xx), np.array(yy)
    
    for i in range(-size, size):
        x[i] = xx + dx / 2 * i
        y[i] = yy + dy * i
    
    xx, yy = list(x.ravel()), list(y.ravel())
    boundary = max(yy)
    x, y = [], []
    
    for i in range(len(xx)):
        temp = xx[i] * math.sqrt(3) / 2 + yy[i] / 2
        if abs(temp) - boundary < 0.2:
            x.append(xx[i] / 2 - yy[i] * math.sqrt(3) / 2)
            y.append(temp)
    
    z=[0]*len(x)
    atom_list=["C"]*len(x)
    name='zigzag-'+str(size)
    coordinate=list(zip(x,y,z))
    
    return x, y, z, coordinate, atom_list, name 

def generate_armchair(size: int, a=1.42):
    """Generates the hexagon armchair flake based on the given size
        
    :param size: the size of structure
    :type size: int
    """
    xx,yy,_,_,_,_=generate_zigzag(2 * size - 1)  
    
    x, y = [], []
    for i in range(len(xx)):
        # rotate 30, 90, 150 and cut
        temp30 = xx[i] * 1 / 2 + yy[i] * math.sqrt(3) / 2
        temp90 = xx[i]
        temp_30 = -xx[i] / 2 + yy[i] * math.sqrt(3) / 2
        boundary = (3 * size - 2) * math.sqrt(3) / 2 * a
        if abs(temp30) - boundary < 0.2 and abs(temp90) - boundary < 0.2 \
        and abs(temp_30) - boundary < 0.2:
            x.append(xx[i] * math.sqrt(3) / 2 - yy[i] * 1/2)
            y.append(temp30)
    
    # rotate coordinates by 90 degrees
    new_x = [-i for i in y]
    new_y = [i for i in x]
    
    z=[0]*len(x)
    atom_list=["C"]*len(x)
    name='armchair-'+str(size)
    coordinate=list(zip(new_x,new_y,z))  
    
    return new_x, new_y, z, coordinate, atom_list, name 

def generate_square(size: int, a=1.42):
    """Generates the square ribbon based on the given size
        
    :param size: the size of structure
    :type size: int
    
    """
    xx,yy,_,_,_,_=generate_zigzag(2 * size) # same raw lattice, different way of cutting
    
    x, y = [], []
    boundary = (2 * size + 1) * math.sqrt(3) / 2 * a
    boundary2 = (3 * size + 2) * a / 2
    k = (size - 1) / 2
    if size % 2 == 0:
        boundary3 = 999
    else:
        boundary3 = (4.5 * k + 2.5) * a
    for i in range(len(xx)):
        if abs(xx[i]) - boundary < 0.2 and abs(yy[i]) - boundary2 < 0.2 \
        and abs(xx[i] * math.sqrt(3) / 2 + yy[i] / 2) - boundary3 < 0.2 and \
        abs(-xx[i] * math.sqrt(3) / 2 +yy[i] / 2) - boundary3 < 0.2:
            x.append(xx[i])
            y.append(yy[i])
 
    z = [0] * len(x)
    atom_list=["C"]*len(x)
    name='square-'+str(size)
    coordinate=list(zip(x,y,z))  
    
    return x, y, z, coordinate, atom_list, name 

def get_distance_from_center_point(atom_index): 
    return [math.sqrt(i**2+j**2+k**2) for i,j,k in atom_index]

def take_second(elem): # take the second element for sort
    return elem[1]

def get_outermost_layer_index(size:int, flake_type:str):
    a=1.42
    b=math.sqrt(3)*a/2
    
    if flake_type=="zigzag":
    # find upper left index for C_index_potential, because it high symmetric, only need to create vacancy here
        coordinates=generate_zigzag(size)[3]
        upper_left_list=[(x,y,z) for x,y,z in coordinates if x>=0 and y>=0]
        
        C_horizontal_num=math.ceil(size/2)
        C_vertical_num=size
        if size%2==0:
            C_horizontal_x=[(2*i+1)*b for i in range(C_horizontal_num)]
            C_horizontal_y=[(2+3*(C_horizontal_num-1)+0.5)*a]*C_horizontal_num
        else:
            C_horizontal_x=[2*i*b for i in range(C_horizontal_num)]
            C_horizontal_y=[((C_horizontal_num-1)*3+1)*a]*C_horizontal_num
        C_vertical_x=[((2*size-1)*b-i*b) for i in range(C_vertical_num)]
        C_vertical_y=[0.5*a+1.5*a*i for i in range(C_vertical_num)]
        
        C_index_x=C_horizontal_x+C_vertical_x
        C_index_y=C_horizontal_y+C_vertical_y
        C_index_z=[0]*len(C_index_x)
        
        outer_layer_index_list=list(zip(C_index_x,C_index_y,C_index_z))
        
    elif flake_type=="armchair":
        # find upper left index for C_index_potential, because it high symmetric, only need to create vacancy here
        coordinates=generate_armchair(size)[3]
        upper_left_list=[(x,y,z) for x,y,z in coordinates if x>=0 and y>=0]
        
        """
        outmost layer atoms can be divided into two parts, first part is loxotic, second is vertical 
        """
    # find point with max y value and get it nearby point, think two point as a line, \
    # the nums of lines is depend on size. (first part, loxotic )
        point_y_max=sorted(upper_left_list,key=take_second,reverse=True)[0]
        point_y_max_nearest=(point_y_max[0]+b,point_y_max[1]-0.5*a,0)
        # get index for other lines
        ponit_list_loxotic=[(point_y_max[0]+i*3*b,point_y_max[1]-i*1.5*a,0) for i in range(size)]+ \
            [(point_y_max_nearest[0]+i*3*b,point_y_max_nearest[1]-i*1.5*a,0) for i in range(size)]
    # second part(vertiacl)
        # find list with max x, 
        point_list_x_max=sorted(upper_left_list,reverse=True)[:size]
        # remove the duplicated point
        point_list_x_max=[i for i in point_list_x_max if i !=sorted(point_list_x_max,key=take_second,reverse=True)[0]]
    
        outer_layer_index_list=ponit_list_loxotic+point_list_x_max   
    
    elif flake_type=="square":
        coordinates=generate_square(size)[3]
        upper_left_list=[(x,y,z) for x,y,z in coordinates if x>=0 and y>=0]        
        if size%2==0:
            C_horizontal=sorted(upper_left_list,key=take_second,reverse=True)[:size+1]
            C_vertical=sorted(upper_left_list,reverse=True)[:size+1]
        else:
            C_horizontal=sorted(upper_left_list,key=take_second,reverse=True)[:size]
            C_vertical=sorted(upper_left_list,reverse=True)[:size+1]
        
        outer_layer_index_list=C_horizontal+C_vertical
        
    return outer_layer_index_list

def get_symmetric_index(input_list:list):
    """
    input_list is upper_left part atom index in zigzag or armchair structures;
    """
    # use upper-lower symmetric first
    lower_left_list=[(i[0],-i[1],i[2]) for i in input_list]
 
    # use left-right symmetric
    right_total=input_list+lower_left_list
    left_total=[(-i[0],i[1],i[2]) for i in right_total]
    
    # sum to get total list
    total_list=left_total+right_total
    
    def remove_duplicate(total_list):
        return list(set(total_list))
    
    total_list=remove_duplicate(total_list)
    
    return total_list

def add_hydrogen_index(size:int, flake_type="zigzag"):
    a=1.42
    b=math.sqrt(3)*a/2 
    C_H_dist=1.08467
    
    if flake_type=="zigzag":    
        # we can only consider atom index in the upper left corner now, since structure are symmetric
        upper_90_degree_num=math.ceil(size/2)
        upper_30_degree_num=size

        # get upper left area atom index
        if size%2==0:  
            # H in upper 90 degree
            H_list_90_x=[(2*i+1)*b for i in range(upper_90_degree_num)]
            H_list_90_y=[(2+3*(upper_90_degree_num-1)+0.5)*a+C_H_dist]*upper_90_degree_num                
        else: 
            # H in upper 90 degree
            H_list_90_x=[ 2*i*b for i in range(upper_90_degree_num)]
            H_list_90_y=[((upper_90_degree_num-1)*3+1)*a+C_H_dist]*upper_90_degree_num
            
        # H in upper 30 degree
        H_list_30_x=[((2*size-1)*b-i*b)+math.sqrt(3)/2*C_H_dist for i in range(upper_30_degree_num)]
        H_list_30_y=[0.5*a+1.5*a*i+0.5*C_H_dist for i in range(upper_30_degree_num)]
            
        # merge the list
        H_list_x=H_list_90_x+H_list_30_x
        H_list_y=H_list_90_y+H_list_30_y
        H_list_z=[0]*len(H_list_x)
        H_list=list(zip(H_list_x,H_list_y,H_list_z))
                
    elif flake_type=="armchair":
        coordinates=generate_armchair(size)[3]
        upper_left_list=[(x,y,z) for x,y,z in coordinates if x>=0 and y>=0]
        point_y_max=sorted(upper_left_list,key=take_second,reverse=True)[0]
        point_y_max_nearest=(point_y_max[0]+b,point_y_max[1]-0.5*a,0) 
        # H in upper 90 degree
        H_list_90=[(point_y_max[0]+i*3*b,point_y_max[1]-i*1.5*a+C_H_dist,0) for i in range(size)]
        # H in upper 30 degree in loxotic part
        H_list_30_loxotic=[(point_y_max_nearest[0]+i*3*b+math.sqrt(3)/2*C_H_dist,
                         point_y_max_nearest[1]-i*1.5*a+0.5*C_H_dist,0) for i in range(size)]
        # H in upper 30 degree in vertical part
        point_x_max=sorted(upper_left_list,reverse=True)[:size][::-1]
        point_x_max=sorted(point_x_max,key=take_second)
        
        if size%2==0:
            # In vertical:
            lowest_H=(point_x_max[0][0]+math.sqrt(3)/2*C_H_dist,point_x_max[0][1]-0.5*C_H_dist,0)
            second_lowest_H=(point_x_max[1][0]+math.sqrt(3)/2*C_H_dist,point_x_max[1][1]+0.5*C_H_dist,0)
            H_list_30_vertical=[(second_lowest_H[0],second_lowest_H[1]+3*a*i,0) for i in range(int(size/2))]
            # drop duplicated part with loxotic part 
            H_list_30_vertical=sorted(H_list_30_vertical,key=take_second,reverse=True)[1:]
            
            H_list_lower_30=[(lowest_H[0],lowest_H[1]+3*a*i,0) for i in range(int(size/2))]  
        else:
            lowest_H=(point_x_max[0][0]+math.sqrt(3)/2*C_H_dist,point_x_max[0][1]+0.5*C_H_dist,0)
            second_lowest_H=(point_x_max[1][0]+math.sqrt(3)/2*C_H_dist,point_x_max[1][1]-0.5*C_H_dist,0)
            H_list_30_vertical=[(lowest_H[0],lowest_H[1]+3*a*i,0) for i in range(int(size/2))]
#             H_list_30_vertical=sorted(H_list_30_vertical,key=take_second,reverse=True)[1:]
            
            H_list_lower_30=[(second_lowest_H[0],second_lowest_H[1]+3*a*i,0) for i in range(int(size/2))] 
        
        H_list_upper_30=H_list_30_loxotic+H_list_30_vertical
        # add three H list
        H_list=H_list_lower_30+H_list_upper_30+H_list_90    
    
    elif flake_type=="square":
        coordinates=generate_square(size)[3]
        upper_left_list=[(x,y,z) for x,y,z in coordinates if x>=0 and y>=0]        
        if size%2==0:
            C_horizontal=sorted(upper_left_list,key=take_second,reverse=True)[:size+1]
            H_list_90=[(i[0], i[1]+C_H_dist, i[2]) for i in C_horizontal]
            
            C_vertical=sorted(upper_left_list,reverse=True)[:size+1]
            # resort list to get min to max base on x-axis value
            C_vertical=sorted(C_vertical)
            
            H_list_upper_30=[(C_vertical[i][0]+math.sqrt(3)/2*C_H_dist, C_vertical[i][1]+0.5*C_H_dist, 
                              C_vertical[i][2]) for i in range(0,len(C_vertical),2)]
            H_list_lower_30=[(C_vertical[i][0]+math.sqrt(3)/2*C_H_dist, C_vertical[i][1]-0.5*C_H_dist, 
                              C_vertical[i][2]) for i in range(1,len(C_vertical),2)]
        else:
            C_horizontal=sorted(upper_left_list,key=take_second,reverse=True)[:size]
            H_list_90=[(i[0], i[1]+C_H_dist, i[2]) for i in C_horizontal]
            
            C_vertical=sorted(upper_left_list,reverse=True)[:size+1]
            # resort list to get min to max base on y-axis value 
            C_vertical=sorted(C_vertical,key=take_second)
            # not think of point with diiferent x-aixs value first
            H_list_upper_30=[(C_vertical[i][0]+math.sqrt(3)/2*C_H_dist, C_vertical[i][1]+0.5*C_H_dist, 
                              C_vertical[i][2]) for i in range(0,len(C_vertical)-1,2)]
            # add it back to list
            H_list_upper_30+=[(C_vertical[-1][0]+math.sqrt(3)/2*C_H_dist, C_vertical[-1][1]+0.5*C_H_dist,
                               C_vertical[-1][2])]
            
            H_list_lower_30=[(C_vertical[i][0]+math.sqrt(3)/2*C_H_dist, C_vertical[i][1]-0.5*C_H_dist, 
                              C_vertical[i][2]) for i in range(1,len(C_vertical)-1,2)]
        
        H_list=H_list_90+H_list_upper_30+H_list_lower_30
        
    # get toal H atom index by symmetric operation
    H_list_total=get_symmetric_index(H_list)            
        
    # get name list for H atom, this necessary for xyz file to tell element
    atom_list=["H"]*len(H_list_total)    
    
    return H_list_total, atom_list

def get_carbon_flake_with_H(size:int, flake_type="zigzag"):
    if flake_type=="zigzag":
        _,_,_, C_coordinate, C_atom_list, C_name=generate_zigzag(size) 
                
    elif flake_type=="armchair":
        _,_,_, C_coordinate, C_atom_list, C_name=generate_armchair(size)
    
    elif flake_type=="square":
        _,_,_, C_coordinate, C_atom_list, C_name=generate_square(size)
        
    H_coordinate, H_atom_list =add_hydrogen_index(size, flake_type)
    coordinate_list=C_coordinate+H_coordinate
    atom_list=C_atom_list+H_atom_list
    name=flake_type+'-'+str(size)+"-H"
    
    return coordinate_list, atom_list ,name      

def calculate_center_points(input_list):
    """
    e.g. Input: [[(0, 0, 0), (1, 1, 1)], [(1, 1, 1), (2, 2, 2)]];
         Output: [(0.5, 0.5, 0.5), (1.5, 1.5, 1.5)]
    """
    center_points = []
    for pair in input_list:
        center_x = (pair[0][0] + pair[1][0]) / 2
        center_y = (pair[0][1] + pair[1][1]) / 2
        center_z = (pair[0][2] + pair[1][2]) / 2
        center_points.append((center_x, center_y, center_z))

    return center_points

def get_unique_sub_element_list(input_list):
    """
    e.g. Input: [(2.13, [(0.0, 1.42, 0), (0.0, 2.84, 0)]),(1.23, [(0.0, 1.42, 0), (1.22, 0.71, 0)]),
 (2.13,[(1.22, 0.71, 0), (2.45, 1.42, 0)])];
         
         Output: [[(0.0, 1.42, 0), (0.0, 2.84, 0)], [(0.0, 1.42, 0), (1.22, 0.71, 0)]]
    """
    
    unique_first_sub_elements = {}  # To track unique first sub-elements
    output_list = []

    for item in input_list:
        first_sub_element = item[0]
        if first_sub_element not in unique_first_sub_elements:
            unique_first_sub_elements[first_sub_element] = item[1]
            output_list.append(item[1])

    return output_list

def find_indices(l1:list,l2:list):
    return [l2.index(i) for i in l1 if i in l2]   

def rotate_90_to_get_SW_vacancy(vacancy_list:list):
    """
    Creates Stone Wales vacancy based on the carbon that generate double vacancy, just rotate these two atoms 90 
    degree to get Stone Wales vacancy.
    """
    a=1.42 # C-C bond length in carbon flake
    
    point1=vacancy_list[0]
    point2=vacancy_list[1]
    
    x1,y1,z1=point1
    x2,y2,z2=point2
    
    # name new atom index a,b,c
    if round(x1,2)==round(x2,2):
        a1, b1, c1 = x1-1/2*a, (y1+y2)/2, 0
        a2, b2, c2 = x1+1/2*a, (y1+y2)/2, 0
    else:
        center_atom=((x1+x2)/2, (y1+y2)/2, 0)
        a_cen, b_cen, c_cen = center_atom
        
        k,b=find_k_and_b_for_line(point1,point2)
        if k<0:
            a1, b1, c1 = a_cen+abs(y1-b_cen), b_cen+abs(x1-a_cen), 0
            a2, b2, c2 = a_cen-abs(y1-b_cen), b_cen-abs(x1-a_cen), 0
        else:
            a1, b1, c1 = a_cen-abs(y1-b_cen), b_cen+abs(x1-a_cen), 0
            a2, b2, c2 = a_cen+abs(y1-b_cen), b_cen-abs(x1-a_cen), 0
        
    result=[(a1,b1,c1),(a2,b2,c2)]
        
    return sorted(result)

def create_vacancy(size:int, flake_type:str, vacancy_type:str):
    H_index, H_atom_list=add_hydrogen_index(size,flake_type) # get H index 
    
    if flake_type=="zigzag":
        C_index=generate_zigzag(size)[3] # get C index

    elif flake_type=="armchair":
        C_index=generate_armchair(size)[3]
    
    elif flake_type=="square":
        C_index=generate_square(size)[3]
        
    upper_left_list_total=[(x,y,z) for x,y,z in C_index if x>=0 and y>=0]
    outmost_layer_list=get_outermost_layer_index(size,flake_type)
    # get round 2 in case they are different in decimal
    upper_left_list_total_round_2=[(round(x,2),round(y,2),z) for x,y,z in upper_left_list_total]
    outmost_layer_list_round_2=[(round(x,2),round(y,2),z) for x,y,z in outmost_layer_list]
        
    upper_left_list=[upper_left_list_total[i] for i in range(len(upper_left_list_total)) if 
                        upper_left_list_total_round_2[i] not in outmost_layer_list_round_2]
        
    if vacancy_type=="single":
        V="SV" 
        
        # calculate the distance between center to atom index in upper_left_list
        dist=get_distance_from_center_point(upper_left_list)

        # get the index with unique distance, each distance get one index
        # since decimals for distance calculation may be tiny difference, use round function to solve it
        dist=[round(i,3) for i in dist]
        vacancy_potential_list=sorted(list(zip(dist,upper_left_list))) # potential vacancy postions

        # drop items with same distance, since it is symmetric
        def remove_duplicates(input_list):
            unique_dict = {} # Dictionary to store unique values

            for item in input_list: 
                key = item[0] # Use the first item as the key
                if key not in unique_dict:
                    unique_dict[key] = item[1] # only store atom coordinates as value, key is the distance

            output_list = list(unique_dict.values())
            return output_list    

        vacancy_list=remove_duplicates(vacancy_potential_list) # get atom coordinates for possible vacancy 
        
        # get all molecule coordinates with different vacancy 
        def create_output_list_for_single_vacancy(vacancy_list, C_index_list): 
            result_list = []

            for i in vacancy_list:
                if i in C_index_list:
                    filtered_list = [index for index in C_index_list if index != i]
                    result_list.append(filtered_list)

            return result_list

        xyz_C_index_with_vacancy=create_output_list_for_single_vacancy(vacancy_list, C_index) 
    
    else:
        if vacancy_type=="double":
            V="DV" # name for double vacancy

        # find two atoms that dist between them == a.
        def find_pair_atom(input_list,a=1.42):
            n=len(input_list)
            dic={}
            for i in range(n):
                for j in range(i+1,n):
                    dist=get_distance_from_two_point(input_list[i],input_list[j])
                    if round(dist,2)==a:
                        dic[((input_list[i],input_list[j]))]=dist 
            index_list=list(dic.keys())
            return [list(i) for i in index_list]
        
        atom_pair=find_pair_atom(upper_left_list)
        center_point_of_atom_pair=calculate_center_points(atom_pair)
        center_dist=get_distance_from_center_point(center_point_of_atom_pair)
        # get atom index that can be used to create vacancy
        vacancy_list=get_unique_sub_element_list(list(zip(center_dist, atom_pair)))
        
        def drop_double_vacancy_from_C_list(vacancy:list,C_index_list:list):
            indices_to_remove = find_indices(vacancy, C_index_list) # Indices of elements to remove
            result_list = [item for index, item in enumerate(C_index_list) if index not in indices_to_remove]
            
            return result_list        
        
        xyz_C_index_with_vacancy=[drop_double_vacancy_from_C_list(vacancy_list[i],C_index) 
                                         for i in range(len(vacancy_list))]
        if vacancy_type=="sw":
            V="SW"
            vacancy_list=[rotate_90_to_get_SW_vacancy(i) for i in vacancy_list]
                
    C_atom_list=["C"]*len(xyz_C_index_with_vacancy[0]) # get C atom list

    # add H index
    xyz_total_index_with_vacancy=[i+H_index for i in xyz_C_index_with_vacancy]

    # get total atom list
    atom_list=[C_atom_list+H_atom_list]*len(vacancy_list)

    # name list
    name_list=[flake_type+"-"+str(size)+"-H-"+V+str(i) for i in range(1,len(vacancy_list)+1)]
    
    return xyz_total_index_with_vacancy, xyz_C_index_with_vacancy, atom_list, vacancy_list, name_list

def create_SW_vacancy(size:int, flake_type:str, vacancy_type="sw"):
    _,xyz_C_index_with_vacancy,_,vacancy_list,name_list=create_vacancy(size,flake_type,vacancy_type)
    H_index, H_atom_list=add_hydrogen_index(size,flake_type) # get H index 
    
    SW_index_list=[xyz_C_index_with_vacancy[i]+H_index+vacancy_list[i] for i in range(len(vacancy_list))]
    SW_atom_list=[["C"]*len(xyz_C_index_with_vacancy[0])+H_atom_list+["C"]*2]*len(vacancy_list)
    SW_name_list=name_list
    
    return SW_index_list, SW_atom_list, SW_name_list

def get_distance_from_two_point(index1,index2):
    dist=math.sqrt((index1[0]-index2[0])**2+(index1[1]-index2[1])**2+(index1[2]-index2[2])**2)
    return dist

def permutation_result(nonmetal_list):
    """
    e.g. input: ["N", "C", "O",]
    output: [('N', 'C', 'O'),('N', 'O', 'C'),('C', 'N', 'O'),('C', 'O', 'N'),('O', 'N', 'C'),('O', 'C', 'N')]
    """
    result = {}
    
    # Generate all possible combinations of three elements
    all_combinations = list(combinations(nonmetal_list, 3))

    # Generate all possible permutations of three elements
    all_permutations = list(permutations(nonmetal_list, 3))

    # Classify permutations based on their corresponding combinations
    for combination in all_combinations:
        related_permutations = [perm for perm in all_permutations if set(combination) == set(perm)]
        result[combination] = related_permutations
    
    return list(result.values())

def select_unique_3_from_6_combination(input_list, atom_index):
    """
    e.g. input: [('N', 'C', 'O'),('N', 'O', 'C'), ('C', 'N', 'O'),('C', 'O', 'N'),('O', 'N', 'C'),('O', 'C', 'N')]
    if atom_index=2, means last element is unique, so ouput: [('N', 'C', 'O'),('N', 'O', 'C'), ('C', 'O', 'N')]
    """
    output_list = []
    for i in range(len(input_list)):
        if input_list[i][atom_index] not in [x[atom_index] for x in output_list]:
            output_list.append(input_list[i])
    return output_list

def cluster_tuples(data):
    """
    cluster items with same element into a list, e.g. output:  
    Cluster 1: [('N', 'O', 'C'), ('N', 'C', 'O'), ('O', 'N', 'C'), ('O', 'C', 'N'), ('C', 'N', 'O'), ('C', 'O', 'N')]
    Cluster 2: [('N', 'O', 'S'), ('N', 'S', 'O'), ('O', 'N', 'S'), ('O', 'S', 'N'), ('S', 'N', 'O'), ('S', 'O', 'N')]
    Cluster 3: [('N', 'C', 'S'), ('N', 'S', 'C'), ('C', 'N', 'S'), ('C', 'S', 'N'), ('S', 'N', 'C'), ('S', 'C', 'N')]
    Cluster 4: [('O', 'C', 'S'), ('O', 'S', 'C'), ('C', 'O', 'S'), ('C', 'S', 'O'), ('S', 'O', 'C'), ('S', 'C', 'O')]
    """
    # Create a dictionary to hold the clusters
    clusters = defaultdict(list)

    # Iterate through each tuple
    for item in data:
        # Sort the tuple elements to ensure consistent clustering
        sorted_item = tuple(sorted(item))

        # Append the tuple to the corresponding cluster
        clusters[sorted_item].append(item)

    # Convert the dictionary values to lists to get the final result
    clustered_lists = list(clusters.values())
    return clustered_lists

def flatten_list(input_list):
    flat_list = []
    for inner_list in input_list:
        flat_list.extend(inner_list)
    return flat_list

def get_n_atoms_from_center(C_index_with_vacancy, vacancy, atom_num:int):
    distance=[]
    for i in C_index_with_vacancy:
        dist=get_distance_from_two_point(i,vacancy)
        distance.append((dist,i))
    distance=sorted(distance)[:atom_num] 
    distance=[y for x,y in distance] # drop distance value
    return distance

def get_C_list_without_n_atoms(C_index_with_vacancy, atom_index):
        
    C_list=[i for i in C_index_with_vacancy if i not in atom_index]
        
    return C_list

def remove_duplaicted_for_double_vacancy_in_situation_2(input_list,nonmetal_list):
# only need to left situation with first element in first and second postion, since third and forth are symmertirc
    element=nonmetal_list[0]
    first=[i for i in input_list if i[0]==element]
    second=[i for i in input_list if i[1]==element]
    return first+second

# situation 1: all n atoms are the same elements or only 2 elements in all atoms
def get_situation_1(nonmetal_list:list,atom_num:int):
    # Generate all possible combinations of two elements
    combinations = list(combinations_with_replacement(nonmetal_list, atom_num))
    result=[]
    # Form the resulting list with the third element
    for combination in combinations:
        for element in nonmetal_list:
            result.append(list(combination) + [element])
    return result

# situation 2: all n atoms are unique elements, len(nonmetal_list)>2
# here we first use permutation to create all the possiblilty, then use y-axis to delete duplicated items 
def get_situation_2_symmetric(nonmetal_list:list, vacancy_type:str, atom_num:int):
    # Generate all possible permutations of n elements
    permut = list(permutations(nonmetal_list, atom_num))
    # get corresponding unique 
    if vacancy_type=="single":
        result=[select_unique_3_from_6_combination(i,atom_index=1) for i in cluster_tuples(permut)]
        result=flatten_list(result)
    
    elif vacancy_type=="double":
        result=remove_duplaicted_for_double_vacancy_in_situation_2(permut,nonmetal_list)
        
    result=[list(i) for i in result]
        
    return result

def get_situation_2_unsymmetrical(nonmetal_list: list, vacancy_type: str, atom_num: int):
    """
    This is specifically for double vacancy since it will generate unsymmetrical structure
    """
    if vacancy_type == "double":
        permut = list(permutations(nonmetal_list, atom_num))
        result = [list(i) for i in permut]
        return result

# this is for double vacancy, since the structure can be symmetric or unsymmetrical
def find_k_and_b_for_line(point1,point2):
    """
    since z1 and z2 are always zero, we only consider x and y.
    line formula: y=kx+b
    """
    x1,y1,z1=point1
    x2,y2,z2=point2
    if round(x1,2)==round(x2,2):
        k=math.inf
        b=0
    else:
        k=(y2-y1)/(x2-x1)
        b=y1-k*x1
    
    return k,b 

def find_middle_line(p1,p2,p3,p4):
    """
    here, p1 and p2 are points make a line; p3 and p4 make a line; these two lines are parallel.
    """
    k1,b1=find_k_and_b_for_line(p1,p2)
    k2,b2=find_k_and_b_for_line(p3,p4)
    if round(k1,2)==round(k2,2):
        b=(b1+b2)/2
        return k1,b    

def tell_line_with_center_point(input_list,center_atom):
    """
    this function is to tell whether a line pass through center point
    """
    p1,p2,p3,p4=input_list
    # find middle line first
    k,b=find_middle_line(p1,p2,p3,p4)
    
    if k==math.inf:
        if round(center_atom[0],2)==0:
            return True
        else:
            return False
    else:    
        # tell when x=0, whether y==0:
        if round(b,2)==0:
            return True
        else:
            return False

def fill_for_vacancy(size:int, flake_type:str,vacancy_type:str, metal:str, nonmetal_list: list):
    # all metal list
    metal_list=["Li","Na","K","Rb","Cs","Be","Mg","Ca","Sr","Ba","Sc","Y","Ti","Zr","Hf","V","Nb","Ta","Cr","Mo",
                "W","Mn","Tc","Re","Fe","Ru","Os","Co","Rh","Ir","Ni","Pd","Pt","Cu","Ag","Au","Zn","Cd","Hg","Al",
                "Ga","In","Tl","Si","Ge","Sn","Pb","As","Sb","Bi"]
    # all nonmetal list
    nonmetals = ['H', 'He', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Si', 'P', 'S', 'Cl', 'Ar', 'Ge', 'As', 'Se', 'Br', 'Kr', 
                'Te', 'I', 'Xe', 'At', 'Rn', 'Ts', 'Og']
    if metal not in metal_list:
        raise ValueError("input metal_type is not a valid metal element, please check it!")
    
    for i in nonmetal_list:
        if i not in nonmetals:
            raise ValueError("input dopant_type is not a valid nonmetal element, please check it!")

   # get atom index with vacancy and vacancy_list
    # _, xyz_C_index_with_vacancy, _, vacancy_list, _ = create_vacancy(size,flake_type,vacancy_type)
    q=quantumdot()
    if flake_type=="zigzag":
        q.Hexzigzag(size)
    elif flake_type=="armchair":
        q.Hexarmchair(size)
    elif flake_type=="square":
        q.Square(size)
    else:
        print('Unkown structure, try a new one!')
    q.Getpores()
    q.DistanceMatrix()
    ind_list=[i for i in range(len(q.atom)) if i not in q.boundary_with_H]

    ## find the n atoms index that close to vacancy. (Use the middle point of two vacancy C as the center)
    if vacancy_type=="single":
        atom_num=3
        V="Coor3-"
        _,_,_,vacancy_list,xyz_C_index_with_vacancy=filter_by_symmetry_SV(q,ind_list)

        selected_n_atom_index=[get_n_atoms_from_center(xyz_C_index_with_vacancy[i],
                                                vacancy_list[i],atom_num) for i in range(len(vacancy_list))]
    else:
        atom_num=4
        if vacancy_type=="double":
            V="Coor4-"  
            _,_,_,vacancy_list,xyz_C_index_with_vacancy=filter_by_symmetry_DV(q,ind_list)

        elif vacancy_type=="sw": 
            raise ValueError("Stone Wales vacancy can not be filled with metal and nonmetal")
            # V="SW"
        vacancy_center_atom=calculate_center_points(vacancy_list)   
        selected_n_atom_index=[get_n_atoms_from_center(xyz_C_index_with_vacancy[i],
                                                    vacancy_center_atom[i],atom_num) for i in range(len(vacancy_list))] 
    
    # get Carbon list without these n atoms

    selected_C_list=[get_C_list_without_n_atoms(xyz_C_index_with_vacancy[i], 
                                                selected_n_atom_index[i]) for i in range(len(vacancy_list))] 
    ## replace C with nonmetal. 
    # check whether "C" in the list, if not, add it to nonmetal list.
    nonmetal_list=nonmetal_list+["C"] if "C" not in nonmetal_list else nonmetal_list
    nonmetal_list=list(set(nonmetal_list)) # use set to make sure every element is unique in the list
    
    # use X to represent nonmetal elements 
    # situation 1 
    X_atom_index=get_situation_1(nonmetal_list,atom_num-1)  
    name_list_X_elements=['-'.join(i) for i in X_atom_index] # this is for storing name of the xyz files
    
    # fill the vacancy with Metal and H atoms
    H_index, H_atom_list=add_hydrogen_index(size,flake_type)
    
    # atom list to store e.g. ["C","C","O"]
    atom_C_metal_H_list=[["C"]*len(selected_C_list[0])+[metal]+H_atom_list for i in range(len(vacancy_list))] 
    
    # this is for the name of xyz files 
    name_list_C_metal_H=[flake_type+"-"+str(size)+"-H-"+V+str(i)+"-"+metal+"-" for i in range(1,len(vacancy_list)+1)]
    
    # get atom index list
    if vacancy_type=="single":
        xyz_C_metal_H_index=[selected_C_list[i]+[vacancy_list[i]]+H_index for i in range(len(vacancy_list))]
        
    elif vacancy_type=="double":
        xyz_C_metal_H_index=[selected_C_list[i]+[vacancy_center_atom[i]]+H_index for i in range(len(vacancy_list))]
    
    # elif vacancy_type=="sw":
    #     xyz_C_metal_H_index=[selected_C_list[i]+vacancy_list[i]+H_index for i in range(len(vacancy_list))]    
          
    xyz_index_total=[]
    atom_list_total=[]
    name_list_total=[]
    
    # add X elemetns, have many combinations
    for a,b,c,d in zip(xyz_C_metal_H_index,selected_n_atom_index,atom_C_metal_H_list,name_list_C_metal_H):
        for k,l in zip(X_atom_index,name_list_X_elements):
            index_value=a+b
            atom_vlaue=c+k
            name_value=d+l
            xyz_index_total.append(index_value)
            atom_list_total.append(atom_vlaue)
            name_list_total.append(name_value)
            
    if len(nonmetal_list)>atom_num-1:
        # add situation 2 when nonmetal_list > atom_num-1
        if vacancy_type=="single":
            X_atom_index_situation_2=get_situation_2_symmetric(nonmetal_list,vacancy_type,atom_num) 
            name_list_X_elements_situation_2=['-'.join(i) for i in X_atom_index_situation_2]

            for a,b,c,d in zip(xyz_C_metal_H_index,selected_n_atom_index,atom_C_metal_H_list,name_list_C_metal_H):
                for k,l in zip(X_atom_index_situation_2,name_list_X_elements_situation_2):
                    index_value=a+b
                    atom_vlaue=c+k
                    name_value=d+l
                    xyz_index_total.append(index_value)
                    atom_list_total.append(atom_vlaue)
                    name_list_total.append(name_value) 
                    
        elif vacancy_type=="double":
            # divide xyz_C_metal_H_index into 2 cluster, one is symmetric to center point and the other is not. 
            xyz_C_metal_H_index_symmetric=[]
            xyz_C_metal_H_index_unsymmetrical=[]
            selected_n_atom_index_symmetric=[]
            selected_n_atom_index_unsymmetrical=[]
            name_list_C_metal_H_symmetric=[]
            name_list_C_metal_H_unsymmetrical=[]
        
            for a,b,c,d in zip(xyz_C_metal_H_index, selected_n_atom_index, vacancy_center_atom, name_list_C_metal_H):
                symmetry=tell_line_with_center_point(sorted(b),c)
                if symmetry==True:
                    xyz_C_metal_H_index_symmetric.append(a)
                    selected_n_atom_index_symmetric.append(b)
                    name_list_C_metal_H_symmetric.append(d)
                else:
                    xyz_C_metal_H_index_unsymmetrical.append(a)
                    selected_n_atom_index_unsymmetrical.append(b)
                    name_list_C_metal_H_unsymmetrical.append(d)
            
            # symmetric situation
            if xyz_C_metal_H_index_symmetric != []:
                X_atom_index_situation_2_symmetric=get_situation_2_symmetric(nonmetal_list,vacancy_type,atom_num)
                name_list_X_elements_situation_2_symmetric=['-'.join(i) for i in X_atom_index_situation_2_symmetric]

                for a,b,c,d in zip(xyz_C_metal_H_index_symmetric,selected_n_atom_index_symmetric,
                                   atom_C_metal_H_list[:len(selected_n_atom_index_symmetric)],
                                   name_list_C_metal_H_symmetric):

                    for k,l in zip(X_atom_index_situation_2_symmetric,name_list_X_elements_situation_2_symmetric):
                        index_value=a+b
                        atom_vlaue=c+k
                        name_value=d+l
                        xyz_index_total.append(index_value)
                        atom_list_total.append(atom_vlaue)
                        name_list_total.append(name_value)  
            
            # unsymmetrical
            if xyz_C_metal_H_index_unsymmetrical != []:
                X_atom_index_situation_2_unsymmetrical=get_situation_2_unsymmetrical(nonmetal_list,vacancy_type,atom_num)
                name_list_X_elements_situation_2_unsymmetrical=['-'.join(i) for i in X_atom_index_situation_2_unsymmetrical]

                for a,b,c,d in zip(xyz_C_metal_H_index_unsymmetrical,selected_n_atom_index_unsymmetrical,
                                   atom_C_metal_H_list[len(selected_n_atom_index_symmetric):],
                                   name_list_C_metal_H_unsymmetrical):

                    for k,l in zip(X_atom_index_situation_2_unsymmetrical,name_list_X_elements_situation_2_unsymmetrical):
                        index_value=a+b
                        atom_vlaue=c+k
                        name_value=d+l
                        xyz_index_total.append(index_value)
                        atom_list_total.append(atom_vlaue)
                        name_list_total.append(name_value)             
    
    return xyz_index_total,atom_list_total,name_list_total

def filter_carbon_flake_dopant_by_dopant_number(size:int, flake_type:str, coordination_number:int, 
                                                metal_type:str, dopant_type=[], dopant_number=0):
    
    # all metal list
    metal_list=["Li","Na","K","Rb","Cs","Be","Mg","Ca","Sr","Ba","Sc","Y","Ti","Zr","Hf","V","Nb","Ta","Cr","Mo",
                "W","Mn","Tc","Re","Fe","Ru","Os","Co","Rh","Ir","Ni","Pd","Pt","Cu","Ag","Au","Zn","Cd","Hg","Al",
                "Ga","In","Tl","Si","Ge","Sn","Pb","As","Sb","Bi"]
    # all nonmetal list
    nonmetals = ['H', 'He', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Si', 'P', 'S', 'Cl', 'Ar', 'Ge', 'As', 'Se', 'Br', 'Kr', 
                'Te', 'I', 'Xe', 'At', 'Rn', 'Ts', 'Og']

    if dopant_number<0:
        raise ValueError("dopant_number can not be negative")
    
    if coordination_number==3 and len(dopant_type)>3:
        raise ValueError("dopant_number can not be larger than 3 when coordination_number is 3")
    elif coordination_number==4 and len(dopant_type)>4:
        raise ValueError("dopant_number can not be larger than 4 when coordination_number is 4")

    if metal_type not in metal_list:
        raise ValueError("input metal_type is not a valid metal element, please check it!")
    
    for i in dopant_type:
        if i not in nonmetals:
            raise ValueError("input dopant_type is not a valid nonmetal element, please check it!")
    
    if not isinstance(dopant_type, list):
        raise TypeError("The input dopant_type must be a list.e.g. ['N','O'] ")
    
    if size<2:
        raise ValueError("The input size parameter must be greater than 1.")    
    
    if coordination_number==3:
        vacancy_type="single"
    elif coordination_number==4:
        vacancy_type="double"

    a,b,c=fill_for_vacancy(size, flake_type, vacancy_type, metal_type, dopant_type)
    
    nonmetal_list = [x for x in dopant_type if x != "C"]

    def count_C(input_list:list):
        count=0
        for i in input_list:
            if i == "C":
                count+=1
        return count
    
    selected_list_index=[]

    if vacancy_type=="single":
        selected_c=[c[i].split("-")[-3:] for i in range(len(c))]
        if dopant_number==0:
            selected_list_index=[i for i,j in enumerate(selected_c) if count_C(j)==3] 
        elif dopant_number==1:
            selected_list_index=[i for i,j in enumerate(selected_c) if count_C(j)==2] 
        elif dopant_number==2:
            selected_list_index=[i for i,j in enumerate(selected_c) if count_C(j)==1]  
        elif dopant_number==3:
            selected_list_index=[i for i,j in enumerate(selected_c) if count_C(j)==0] 

    elif vacancy_type=="double":
        selected_c=[c[i].split("-")[-4:] for i in range(len(c))]
        if dopant_number==0:
            selected_list_index=[i for i,j in enumerate(selected_c) if count_C(j)==4]
        elif dopant_number==1:
            selected_list_index=[i for i,j in enumerate(selected_c) if count_C(j)==3] 
        elif dopant_number==2:
            selected_list_index=[i for i,j in enumerate(selected_c) if count_C(j)==2]  
        elif dopant_number==3:
            selected_list_index=[i for i,j in enumerate(selected_c) if count_C(j)==1] 
        elif dopant_number==4:
            selected_list_index=[i for i,j in enumerate(selected_c) if count_C(j)==0]    

    xyz_index=[a[i] for i in selected_list_index]
    atom_list=[b[i] for i in selected_list_index]
    name_list=[c[i] for i in selected_list_index]

    return xyz_index, atom_list, name_list