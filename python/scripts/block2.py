from str_gen import carbon_flake
import sys

# with open("block1_info.txt", "r") as f:
#     content=f.readline().split(",")
#     size=int(content[0])
#     flake_type=content[1]

if len(sys.argv) != 8:
    """
    size > 1; 
    flake type: zigzag, armchair, square; 
    coordination_number: 3 or 4; 
    metal_type: e.g. Fe
    dopant_type: e.g. N,O,S
    dopant_number: 1-3 if coordination_number=3; 1-4 if coordination_number=4;
    add_H: True, False
    """
    print("Usage: python multi_vacancy_generator.py <size> <flake_type> <coordination_number> <metal_type> <dopant_type> <dopant_number> <add_H>")
    sys.exit(1)

size = int(sys.argv[1])
flake_type = sys.argv[2]
flake_type.lower()
coordination_number = int(sys.argv[3])
metal_type = sys.argv[4]
dopant_type = sys.argv[5]
dopant_type_new=dopant_type.split(",")
dopant_number = int(sys.argv[6])
add_H=bool(sys.argv[7])

ca=carbon_flake()
ca.create_carbon_flakes(size, flake_type, add_H)
ca.add_metal_site(coordination_number, metal_type, dopant_type_new, dopant_number, add_H)
ca.Write_xyz()

# with open ("block2_info.txt","w") as f:
#     f.write( str(coordination_number) +","+str(metal_type)+","+str(dopant_type)+","+str(dopant_number))

