const nameInput = document.getElementById('name-input');
const dateInput = document.getElementById('date-input');
const uploaderInput = document.getElementById('uploader-input');
const searchButton = document.getElementById('search-button');
const resultsTable = document.getElementById('results-table');
const resultsTableBody = document.getElementById('results-table').querySelector('tbody');
let sortAscending = false;
let querydata;
let dataTable;
let line_data;

resultsTableBody.addEventListener('click', async (event) => {
  const row = event.target.parentNode;
  const lineIndex = row.querySelector('td:first-child').textContent-1;
  const _id=querydata[lineIndex]._id
  const db = database.value;
  const url = `http://localhost:3000/search_one?_id=${_id}&database=${db}`;

  try {
    const response = await fetch(url);
    line_data = await response.json();

    let xyz=`${line_data.opt_xyz.length}\n Test\n`;
    line_data.opt_xyz.forEach(line => {
      xyz+=`${line.atom} ${line.x} ${line.y} ${line.z}\n`
    });
    let filename=line_data.name;

    var molecule = ChemDoodle.readXYZ(xyz, 1);
    molecularview.loadMolecule(molecule);

    // Remove the previous highlighted row
    const prevHighlightedRow = resultsTableBody.querySelector('.highlighted');
    if (prevHighlightedRow) {
      prevHighlightedRow.classList.remove('highlighted');
    }
    row.classList.add('highlighted');

    var tableBody = document.getElementById("detail-values");
    tableBody.innerHTML = "";
    // Loop through the JSON data and create table rows for each key-value pair
    for (var key in line_data) {
      var value = line_data[key];
      var detail_row = document.createElement("tr");
      var keyCell = document.createElement("td");
      var valueCell = document.createElement("td");

      keyCell.textContent = key;
      if (key === 'opt_xyz') {
        var downloadLink = document.createElement("a");
        downloadLink.textContent = "Download XYZ";
        downloadLink.href = "data:text/plain;charset=utf-8," + encodeURIComponent(xyz);
        downloadLink.download = `${filename}.xyz`;
        valueCell.appendChild(downloadLink);
      } else {
        valueCell.textContent = JSON.stringify(value);
      }

      detail_row.appendChild(keyCell);
      detail_row.appendChild(valueCell);
      tableBody.appendChild(detail_row);
    }

  } catch (error) {
    console.error(error);
    resultsTable.innerHTML = '<tr><td colspan="4">An error occurred</td></tr>';
  }
});

searchButton.addEventListener('click', async () => {
  const db = database.value;
  const namekeyword = nameInput.value.trim();
  const datekeyword = dateInput.value.trim();
  const uploaderkeyword = uploaderInput.value.trim();

  const url = `http://localhost:3000/search?database=${db}&namekeyword=${namekeyword}&datekeyword=${datekeyword}&uploaderkeyword=${uploaderkeyword}`;

  try {
    document.getElementById("loading").style.display = "block";
    const response = await fetch(url);
    querydata = await response.json();
    document.getElementById("loading").style.display = "none";

    if (dataTable) {
      // If DataTable already exists, destroy it before creating a new one
      dataTable.destroy();
    }

    if (querydata.length === 0) {
      resultsTable.innerHTML = '<tr><td colspan="4">No results found</td></tr>';
    } else {

      let ind=1;
      rows = querydata.map(molecule => [
        ind++,
        molecule.name,
        molecule.upload_date,
        molecule.uploader,
        molecule.basis_sets,
        molecule.functional,
        molecule.electronic_energy,
      ]);

      const columns = [
        { title: "#" },
        { title: "Name" },
        { title: "Upload Date" },
        { title: "Uploader" },
        { title: "Basis Sets" },
        { title: "Functional" },
        { title: "Energy" },
      ];

      dataTable = $(resultsTable).DataTable({
        data: rows,
        columns: columns,
        order: [[0, "asc"]],
        paging: true,
        lengthChange: true,
        searching: true,
        info: true,
        autoWidth: false,
      });
    }
  } catch (error) {
    console.error(error);
    resultsTable.innerHTML = '<tr><td colspan="4">An error occurred</td></tr>';
  }
});

