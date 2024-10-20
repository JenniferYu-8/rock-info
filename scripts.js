function loadCSV() {
    // change background color of the table heading
    const tableHeading = document.querySelector('#artistTable tr');
    tableHeading.style.backgroundColor = "#0d939d";
    
    fetch('artists_info.csv')
        .then(response => response.text())
        .then(data => {
            const rows = data.split('\n');
            const tableBody = document.querySelector('#artistTable tbody');
            tableBody.innerHTML = ''; // clear any existing content

            rows.forEach((row, index) => {
                if (index === 0 || row.trim() === '') return; // skip header and empty rows
                const cols = parseCSVRow(row);

                const tr = document.createElement('tr');
                
                // artist
                const artistTd = document.createElement('td');
                artistTd.textContent = cols[0];
                tr.appendChild(artistTd);

                // listeners
                const listenersTd = document.createElement('td');
                listenersTd.textContent = cols[1];
                tr.appendChild(listenersTd);

                // years active
                const yearsTd = document.createElement('td');
                yearsTd.textContent = cols[2];
                tr.appendChild(yearsTd);

                // members
                const membersTd = document.createElement('td');
                const members = cols[3].split(', ');
                members.forEach(member => {
                    const memberDiv = document.createElement('div');
                    memberDiv.textContent = member;
                    membersTd.appendChild(memberDiv);
                });
                tr.appendChild(membersTd);

                // URL (as <a> tag)
                const urlTd = document.createElement('td');
                const a = document.createElement('a');
                a.href = cols[4];
                a.textContent = "More about " + cols[0];
                a.target = "_blank";
                urlTd.appendChild(a);
                tr.appendChild(urlTd);

                tableBody.appendChild(tr);
            });
        })
        .catch(error => {
            console.error('Error loading CSV file:', error);
        });
}

// Function to handle commas inside quotes
function parseCSVRow(row) {
    const regex = /,(?=(?:(?:[^"]*"){2})*[^"]*$)/;
    return row.split(regex).map(col => col.replace(/^"|"$/g, ''));
}

// Function to load and display JSON data
function loadJSON() {
    // change background color of the table heading
    const tableHeading = document.querySelector('#artistTable tr');
    tableHeading.style.backgroundColor = "#0d4e9d";

    fetch('artists_info.json')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#artistTable tbody');
            tableBody.innerHTML = ''; // clear existing table

            data.forEach(artist => {
                const rowElement = document.createElement('tr');

                // create artist name, listeners, and years active cells
                const artistRow = [
                    artist.Artist,
                    artist.Listeners,
                    artist['Years Active']
                ];

                artistRow.forEach(col => {
                    const cell = document.createElement('td');
                    cell.textContent = col;
                    rowElement.appendChild(cell);
                });

                // create members cell
                const membersCell = document.createElement('td');
                membersCell.innerHTML = artist.Members.replace(/, /g, '<br>'); // Replace commas with <br> for new lines
                rowElement.appendChild(membersCell);

                // Create URL cell with <a> tag
                const urlCell = document.createElement('td');
                const link = document.createElement('a');
                link.style.color = "#0d4e9d";
                link.href = artist.URL.trim(); // Ensure the URL has no leading or trailing spaces
                link.textContent = 'More about '+  artist.Artist;
                link.target = '_blank'; // Open link in new tab
                urlCell.appendChild(link);
                rowElement.appendChild(urlCell);

                tableBody.appendChild(rowElement);
            });
        })
        .catch(error => console.error('Error loading JSON data:', error));
}
