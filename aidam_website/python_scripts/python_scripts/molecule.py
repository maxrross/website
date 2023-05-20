# molecule class
# has each of these data points: Name,status, time, NPROC, HOMO, LUMO, GAP,Electronic energy, Dipole xyz, Dipole,basis sets, functional,stoichiometry,spin multiplicity, S2, total charge, Mulliken, NBO


class molecule:
    name = ""
    status = ""
    upload_date = ""
    upload_time = ""
    cpu_time = ""
    elapsed_time = ""
    NPROC = ""
    HOMO = 0
    LUMO = 0
    GAP = 0
    electronic_energy = 0
    dipole_xyz = ""
    opt_xyz = []
    dipole = 0
    basis_sets = ""
    functional = ""
    stoichiometry = ""
    spin_multiplicity = ""
    S2 = 0
    total_charge = 0
    Mulliken = ""
    NBO = ""
