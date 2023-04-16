
//class to create molecule objects that are listed in table on search page
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

// test object not connected to MongoDB
const test_molecule = new SearchTableMolecule("642ed736c63c3ccac8954cd0", "14mr_N2_1", "No Error", "2023-04-06",
"10:28:10", -0.19396, -0.07194, 0.12202, 16, -2623.60829, "Array", "", "0:5:12:10.3", "0:0:21:6.9", "RB3LYP", "6-31G(d)"
, 0, 1, "Array", "14mr_N2_1_6-31G(d)_RB3LYP");

 
const main = document.querySelector(".searchpagecontent");

// table filled in with molecule objects then run in search.html
// FIXME fix table spacing in CSS
// upload_date, upload_time, cup_time, elapsed_time, and identifier 
// do not need to be shown on the webpage but would be useful for the database
const table_content = `
    <table>
    <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Status</th>
        <th>HOMO</th>
        <th>LUMO</th>
        <th>GAP</th>
        <th>NPROC</th>
        <th>Electronic Energy</th>
        <th>Dipole</th>
        <th>Time</th>
        <th>Functional</th>
        <th>Basis Sets</th>
        <th>Total Charge</th>
        <th>Spin Multiplicity</th>
        <th>Opt XYZ</th>
    </tr>
    <tr>
        <td>${test_molecule.id}</td>
        <td>${test_molecule.name}</td>
        <td>${test_molecule.status}</td>
        <td>${test_molecule.HOMO}</td>
        <td>${test_molecule.LUMO}</td>
        <td>${test_molecule.GAP}</td>
        <td>${test_molecule.NPROC}</td>
        <td>${test_molecule.electronic_energy}</td>
        <td>${test_molecule.dipole}</td>
        <td>${test_molecule.time}</td>
        <td>${test_molecule.functional}</td>
        <td>${test_molecule.basis_sets}</td>
        <td>${test_total_charge}</td>
        <td>${spin_multiplicity}</td>
        <td>${opt_xyz}</td>
    </tr>
    </table>  
`;

main.innerHTML = table_content;