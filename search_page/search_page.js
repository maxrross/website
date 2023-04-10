class SearchTableMolecule {
    constructor(
      id,
      name,
      status,
      upload_date,
      upload_time,
      HOMO,
      LUMO,
      GAP,
      NPROC,
      electronic_energy,
      dipole,
      time,
      cpu_time,
      elapsed_time,
      functional,
      basis_sets,
      total_charge,
      spin_multiplicity,
      opt_xyz,
      identifier
    ) {
        this.id = id;
        this.name = name;
        this.status = status;
        this.upload_date = upload_date;
        this.upload_time = upload_time;
        this.HOMO = HOMO;
        this.LUMO = LUMO;
        this.GAP = GAP;
        this.NPROC = NPROC;
        this.electronic_energy = electronic_energy;
        this.dipole = dipole;
        this.time = time;
        this.cpu_time = cpu_time;
        this.elapsed_time = elapsed_time;
        this.functional = functional;
        this.basis_sets = basis_sets;
        this.total_charge = total_charge;
        this.spin_multiplicity = spin_multiplicity;
        this.opt_xyz = opt_xyz;
        this.identifier = identifier;
    }
    // getters
    get_id() {
        return this.id;
    }
    get_name() {
        return this.name;
    }
    // set_name(new_name) {
    //     this.name = new_name;
    // }
    get_status() {
        return this.status;
    }
    get_upload_date() {
        return this.upload_date;
    }
    get_upload_time() {
        return this.upload_time;
    }
    get_HOMO() {
        return this.HOMO;
    }
    get_LUMO() {
        return this.LUMO;
    }
    get_GAP() {
        return this.GAP;
    }
    get_NPROC() {
        return this.NPROC;
    }
    get_electronic_energy() {
        return this.electronic_energy;
    }
    get_dipole() {
        return this.dipole;
    }
    get_time() {
        return this.time;
    }
    get_cpu_time() {
        return this.cpu_time;
    }
    get_elapsed_time() {
        return this.elapsed_time;
    }
    get_functional() {
        return this.functional;
    }
    get_basis_sets() {
        return this.basis_sets;
    }
    get_total_charge() {
        return this.total_charge;
    }
    get_spin_multiplicity() {
        return this.spin_multiplicity;
    }
    get_opt_xyz() {
        return this.opt_xyz;
    }
    get_identifier() {
        return this.identifier;
    }
  }

// FIXME create object for each molecule in database using SearchTableMolecule class
  

const main = document.querySelector(".searchpagecontent");

// table filled in with molecule objects then run in search.html
// FIXME fix table spacing in CSS
const content = `
    <table>
    <tr>
        <th>Name</th>
        <th>HOMO</th>
        <th>LUMO</th>
        <th>GAP</th>
        <th>NPROC</th>
        <th>Electronic Energy</th>
        <th>Total Charge</th>
        <th>Spin Multiplicity</th>
    </tr>
    <tr>
        <td>${molecule.name}</td>
        <td>${molecule.HOMO}</td>
        <td>${molecule.LUMO}</td>
        <td>${molecule.GAP}</td>
        <td>${molecule.NPROC}</td>
        <td>${molecule.electronic_energy}</td>
        <td>${total_charge}</td>
        <td>${spin_multiplicity}</td>
    </table>
        
`;

main.innerHTML = content;