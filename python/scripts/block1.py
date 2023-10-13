from str_gen import carbon_flake
import sys


if len(sys.argv) != 4:
    """
    size > 1; 
    flake type: zigzag, armchair, square; 
    add_H: True, False
    """
    print("Usage: python multi_vacancy_generator.py <size> <flake_type> <add_H>")
    sys.exit(1)

size = int(sys.argv[1])
flake_type = sys.argv[2]
add_H=bool(sys.argv[3])

ca=carbon_flake()
ca.create_carbon_flakes(size, flake_type, add_H)
ca.Write_xyz()

# with open ("block1_info.txt","w") as f:
#     f.write( str(size) +","+str(flake_type))