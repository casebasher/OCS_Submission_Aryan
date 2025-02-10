const SUPABASE_URL = 'YOUR_SUPABASE_PROJECT_URL';
const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';

const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

async function login() {
    const userid = document.getElementById('userid').value;
    const password = document.getElementById('password');
    const password_hash = md5(password.value);
    password.value = '';

    try {
        const { data, error } = await supabase
            .from('users')
            .select('role')
            .eq('userid', userid)
            .eq('password_hash', password_hash)
            .single();

        if (error) throw error;

        if (data) {
            const userData = await getUserData(data.role, userid);
            displayUserData(data.role, userData);
        } else {
            alert('Invalid credentials');
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred during login');
    }
}

async function getUserData(role, userid) {
    try {
        if (role === 'admin') {
            const { data, error } = await supabase
                .from('users')
                .select('userid, role');
            if (error) throw error;
            return data;
        } else {
            const { data, error } = await supabase
                .from('users')
                .select('userid, role')
                .eq('userid', userid);
            if (error) throw error;
            return data;
        }
    } catch (error) {
        console.error('Error fetching user data:', error);
        return null;
    }
}

function displayUserData(role, userData) {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('userData').style.display = 'block';
    document.getElementById('welcome').textContent = `Welcome, ${role}`;

    const tableBody = document.getElementById('userTableBody');
    tableBody.innerHTML = '';

    userData.forEach(user => {
        const row = tableBody.insertRow();
        row.insertCell(0).textContent = user.userid;
        row.insertCell(1).textContent = user.role;
    });
}
