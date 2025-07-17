const API_BASE_URL = "http://localhost:8001";
let txnMap = new Map();
let chart;
let socket;
let isLoginMode = true;

// --- DOM Elements ---
const authContainer = document.getElementById('auth-container');
const dashboardContainer = document.getElementById('dashboard-container');
const authForm = document.getElementById('auth-form');
const authTitle = document.getElementById('auth-title');
const toggleAuthLink = document.getElementById('toggle-auth-mode');
const authError = document.getElementById('auth-error');
const logoutBtn = document.getElementById('logout-btn');
const viewModeSelect = document.getElementById('view-mode');
const bankFilterSelect = document.getElementById('bank-filter');
const categoryFilterSelect = document.getElementById('category-filter');
const notification = document.getElementById('notification');
const notificationText = document.getElementById('notification-text');

// --- Authentication Logic ---

function checkAuthState() {
  const token = localStorage.getItem('authToken');
  if (token) {
    authContainer.classList.add('hidden');
    dashboardContainer.classList.remove('hidden');
    loadInitialData();
  } else {
    authContainer.classList.remove('hidden');
    dashboardContainer.classList.add('hidden');
  }
}

function toggleAuthMode(e) {
    if (e) e.preventDefault();
    isLoginMode = !isLoginMode;
    authTitle.textContent = isLoginMode ? 'Login' : 'Sign Up';
    toggleAuthLink.innerHTML = isLoginMode ? 'sign up for a new account' : 'log in instead';
    authForm.querySelector('button').textContent = isLoginMode ? 'Sign In' : 'Create Account';
    authError.textContent = '';
}

async function handleAuth(e) {
  e.preventDefault();
  const email = e.target.email.value;
  const password = e.target.password.value;
  const endpoint = isLoginMode ? '/auth/login' : '/auth/signup';
  authError.textContent = '';

  try {
    const options = isLoginMode 
      ? {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({ username: email, password: password })
        }
      : {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        };
    
    const res = await fetch(`${API_BASE_URL}${endpoint}`, options);
    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || 'An error occurred.');
    }

    if (isLoginMode) {
      localStorage.setItem('authToken', data.access_token);
      checkAuthState();
    } else {
      showNotification('Signup successful! Please log in.', 'success');
      toggleAuthMode();
    }
  } catch (err) {
    authError.textContent = err.message;
  }
}

function logout() {
  localStorage.removeItem('authToken');
  if (socket) {
    socket.close();
    socket = null;
  }
  txnMap.clear();
  if(chart) {
    chart.destroy();
    chart = null;
  }
  checkAuthState();
}

// --- API Helper ---
async function fetchWithAuth(endpoint) {
    const token = localStorage.getItem('authToken');
    if (!token) {
        logout();
        throw new Error('Not authenticated');
    }
    const res = await fetch(`${API_BASE_URL}/${endpoint}`, {
        headers: { 
            'Authorization': `Bearer ${token}` 
        }
    });

    if (res.status === 401) {
        logout();
        throw new Error('Session expired. Please log in again.');
    }
    if (!res.ok) {
        throw new Error('Failed to fetch data.');
    }
    return res.json();
}


// --- Dashboard Logic ---

function loadInitialData() {
    const endpoint = viewModeSelect.value === 'all' ? 'all-transactions' : 'suspicious-transactions';
    loadTransactions(endpoint);
    initWebSocket();
}

async function loadTransactions(endpoint) {
  try {
    const data = await fetchWithAuth(endpoint);
    txnMap.clear();
    data.forEach((tx) => txnMap.set(tx.id, tx));
    populateFilters();
    applyFilters();
  } catch(error) {
    console.error(error);
    showNotification(error.message, 'error');
  }
}

function initWebSocket() {
  const token = localStorage.getItem('authToken');
  if (!token) return; // Don't connect if not logged in
  if (socket && socket.readyState === WebSocket.OPEN) return;

  // Append the token as a query parameter
  socket = new WebSocket(`ws://localhost:8001/ws/suspicious?token=${token}`);

  socket.onopen = () => console.log("✅ WebSocket connected with auth token.");
  socket.onmessage = (event) => {
    const rawTxn = JSON.parse(event.data);
    const newTxn = {
      id: rawTxn.txn_id,
      bank: rawTxn.bank,
      amount: rawTxn.amount,
      description: rawTxn.description,
      timestamp: rawTxn.timestamp,
      category: rawTxn.category || "others",
      suspicious_reason: rawTxn.suspicious_reason || "—",
    };

    if (txnMap.has(newTxn.id)) return;
    txnMap.set(newTxn.id, newTxn);
    
    const currentView = viewModeSelect.value;
    if (currentView === 'all' || (currentView === 'suspicious' && newTxn.suspicious_reason !== '—')) {
        applyFilters();
    }
    
    showNotification(`${newTxn.description} - ₹${newTxn.amount}`);
  };
  socket.onclose = () => {
    console.log("❌ WebSocket disconnected.");
    // Only retry if the user is still logged in
    if (localStorage.getItem('authToken')) {
        console.log("Retrying WebSocket connection in 5s...");
        setTimeout(initWebSocket, 5000);
    }
  };
  socket.onerror = (err) => {
    console.error("WebSocket error:", err);
    socket.close();
  };
}

function showNotification(text, type = 'error') {
    notificationText.textContent = text;
    notification.className = `fixed top-5 right-5 p-4 text-white rounded-lg shadow-lg transition-opacity duration-300 ${type === 'error' ? 'bg-red-500' : 'bg-green-500'}`;
    notification.classList.remove('opacity-0');
    setTimeout(() => {
        notification.classList.add('opacity-0');
    }, 4000);
}

function populateFilters() {
  const bankSet = new Set();
  const categorySet = new Set();
  txnMap.forEach((tx) => {
    bankSet.add(tx.bank);
    if (tx.category) categorySet.add(tx.category);
  });

  bankFilterSelect.innerHTML = '<option value="">All Banks</option>';
  categoryFilterSelect.innerHTML = '<option value="">All Categories</option>';

  bankSet.forEach((bank) => {
    const opt = document.createElement("option");
    opt.value = opt.textContent = bank;
    bankFilterSelect.appendChild(opt);
  });
  categorySet.forEach((cat) => {
    const opt = document.createElement("option");
    opt.value = opt.textContent = cat;
    categoryFilterSelect.appendChild(opt);
  });
}

function applyFilters() {
  const bankVal = bankFilterSelect.value;
  const catVal = categoryFilterSelect.value;
  const filtered = Array.from(txnMap.values()).filter(
    (tx) => (!bankVal || tx.bank === bankVal) && (!catVal || tx.category === catVal)
  );
  renderTable(filtered);
  updateSummary(filtered);
  renderChart(filtered);
}

function renderTable(txns) {
  const tbody = document.querySelector("#txn-table tbody");
  tbody.innerHTML = "";
  if (txns.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" class="p-4 text-center text-gray-400">No transactions found.</td></tr>`;
    return;
  }
  txns.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  txns.forEach((tx) => {
    const row = document.createElement("tr");
    row.className = 'hover:bg-gray-700';
    row.innerHTML = `
      <td class="p-3">${tx.id}</td>
      <td class="p-3">${tx.bank}</td>
      <td class="p-3">₹${tx.amount.toLocaleString()}</td>
      <td class="p-3">${tx.description}</td>
      <td class="p-3">${tx.category || "N/A"}</td>
      <td class="p-3 text-red-400">${tx.suspicious_reason || "—"}</td>
    `;
    tbody.appendChild(row);
  });
}

function updateSummary(txns) {
  const total = txns.length;
  const amount = txns.reduce((sum, tx) => sum + tx.amount, 0);
  const summaryDiv = document.getElementById("summary");
  summaryDiv.innerHTML = `
    <div class="grid grid-cols-2 gap-4 text-center md:grid-cols-4">
        <div><p class="text-sm text-gray-400">Total Transactions</p><p class="text-2xl font-bold">${total}</p></div>
        <div><p class="text-sm text-gray-400">Total Amount</p><p class="text-2xl font-bold">₹${amount.toLocaleString()}</p></div>
        <div><p class="text-sm text-gray-400">Highest Transaction</p><p class="text-2xl font-bold">₹${Math.max(0, ...txns.map(t => t.amount)).toLocaleString()}</p></div>
        <div><p class="text-sm text-gray-400">Average Transaction</p><p class="text-2xl font-bold">₹${total > 0 ? (amount / total).toFixed(2) : 0}</p></div>
    </div>
  `;
}

function renderChart(txns) {
  const ctx = document.getElementById("txn-chart").getContext("2d");
  const categoryTotals = {};
  txns.forEach((tx) => {
    const cat = tx.category || "others";
    categoryTotals[cat] = (categoryTotals[cat] || 0) + tx.amount;
  });
  const labels = Object.keys(categoryTotals);
  const values = Object.values(categoryTotals);

  if (chart) chart.destroy();
  chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Amount by Category",
        data: values,
        backgroundColor: 'rgba(79, 70, 229, 0.8)',
        borderColor: 'rgba(99, 102, 241, 1)',
        borderWidth: 1,
        borderRadius: 5
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { 
            beginAtZero: true, 
            ticks: { color: '#9ca3af', callback: (val) => "₹" + val.toLocaleString() },
            grid: { color: 'rgba(255,255,255,0.1)' }
        },
        x: { 
            ticks: { color: '#9ca3af' },
            grid: { display: false }
        },
      },
    },
  });
}

// --- Event Listeners ---
document.addEventListener("DOMContentLoaded", checkAuthState);
authForm.addEventListener('submit', handleAuth);
toggleAuthLink.addEventListener('click', toggleAuthMode);
logoutBtn.addEventListener('click', logout);
viewModeSelect.addEventListener("change", (e) => {
  const endpoint = e.target.value === "all" ? "all-transactions" : "suspicious-transactions";
  loadTransactions(endpoint);
});
bankFilterSelect.addEventListener("change", applyFilters);
categoryFilterSelect.addEventListener("change", applyFilters);
