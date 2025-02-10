const SUPABASE_URL = 'https://hwuzklwcarlsjcyuhulv.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh3dXprbHdjYXJsc2pjeXVodWx2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkyMDQ4MTEsImV4cCI6MjA1NDc4MDgxMX0.XdcIM_6-mmBQa48g0MlHfBckHDG0g4LzMYu01e3y6VA';

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
