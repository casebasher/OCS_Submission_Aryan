async function login() {
    const userid = document.getElementById('userid').value;
    const password = document.getElementById('password').value;
    const password_hash = md5(password);

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userid, password_hash }),
        });

        const data = await response.json();

        if (data.success) {
            displayUserData(data);
        } else {
            alert('Invalid credentials');
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred during login');
    }
}

function displayUserData(data) {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('userData').style.display = 'block';
    document.getElementById('welcome').textContent = `Welcome, ${data.role}`;

    const tableBody = document.getElementById('userTableBody');
    tableBody.innerHTML = '';

    data.data.forEach(user => {
        const row = tableBody.insertRow();
        row.insertCell(0).textContent = user.userid;
        row.insertCell(1).textContent = user.role;
    });
}
