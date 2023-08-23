let levelData, facultyData = {}

window.onload = facultiesAndDepartmentsjson()
window.onload = leveljson()

async function facultiesAndDepartmentsjson() {
  const response = await fetch('/api/facs-and-depts');
  facultyData = await response.json();
}

async function leveljson() {
  const response = await fetch('/api/levels');
  levelData = await response.json();
}

function facultyList() {
  let facultySelect = document.getElementById('faculty')
  facultySelect.length = 0
  let defaultOption = document.createElement('option')
  defaultOption.text = 'Select your Faculty'
  defaultOption.disabled = true
  facultySelect.add(defaultOption)
  facultySelect.selectedIndex = 0

  for (let x in facultyData) {
    let option = document.createElement('option')
    option.text = x
    option.value = facultyData[x][0]['id']
    facultySelect.add(option)
  }
}

function updateDepts(selected) {
  let departmentSelect = document.getElementById('department')
  departmentSelect.length = 0
  let defaultOption = document.createElement('option')
  defaultOption.text = 'Select your Department'
  defaultOption.disabled = true
  departmentSelect.add(defaultOption)
  departmentSelect.selectedIndex = 0

  selectedFaculty = selected.options[selected.selectedIndex].text
  for (let x in facultyData[selectedFaculty][1]['departments']) {
    let option = document.createElement('option')
    option.value = facultyData[selectedFaculty][1]['departments'][x]
    option.text = facultyData[selectedFaculty][1]['departments'][x]
    departmentSelect.add(option)
  }
}

// Step 1: Parse the URL to extract the query parameter value
const url = new URL(window.location.href);
const paramValue = url.searchParams.get("matric_no");

// Step 2: Build the request body with the extracted parameter value
const requestBody = JSON.stringify({
  'matric_no': paramValue
});

window.addEventListener("DOMContentLoaded", (event) => {
  document.getElementById("enrollButton").addEventListener("click", function() {
    console.log("clicked")
    fetch('/api/enroll-fingerprint', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: requestBody,
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the backend
        document.getElementById("enroll-message").innerHTML = data.message
        // You can display the fingerprint position in the frontend
        console.log("Fingerprint Position:", data.position);
    })
    .catch(error => {
        console.error('Error:', error);
    });
  })
});