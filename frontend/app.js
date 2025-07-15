let txnMap = new Map(); // Ensure uniqueness
let chart;
let socket;

document.addEventListener("DOMContentLoaded", () => {
  loadTransactions("suspicious-transactions");
  initWebSocket();
});

// 1️⃣ Load transactions and populate map
async function loadTransactions(endpoint = "suspicious-transactions") {
  const res = await fetch(`http://localhost:8001/${endpoint}`);
  const data = await res.json();

  txnMap.clear();
  data.forEach((tx) => txnMap.set(tx.id, tx));

  populateFilters();
  applyFilters();
}

// 🔌 WebSocket: Add only unique txns
function initWebSocket() {
  socket = new WebSocket("ws://localhost:8001/ws/suspicious");

  socket.onopen = () => {
    console.log("✅ WebSocket connected");
  };

  socket.onmessage = (event) => {
    const rawTxn = JSON.parse(event.data);
    // console.log(rawTxn);

    // Normalize WebSocket message format to match DB-fetched format
    const newTxn = {
      id: rawTxn.txn_id,
      bank: rawTxn.bank,
      amount: rawTxn.amount,
      description: rawTxn.description,
      timestamp: rawTxn.timestamp,
      account_number: rawTxn.account_number,
      category: rawTxn.category || "others",
      suspicious_reason: rawTxn.suspicious_reason || "—",
    };

    // Avoid duplicates: skip if ID already exists
    if (txnMap.has(newTxn.id)) return;

    // Add to map and update UI
    txnMap.set(newTxn.id, newTxn);
    applyFilters(); // Automatically reflect in current view

    alert(
      `⚠️ Suspicious Transaction:\n${newTxn.description} - ₹${newTxn.amount}`
    );
  };

  socket.onclose = () => {
    console.log("❌ WebSocket disconnected. Retrying in 5s...");
    setTimeout(initWebSocket, 5000);
  };

  socket.onerror = (err) => {
    console.error("WebSocket error:", err);
    socket.close();
  };
}

// 2️⃣ Populate Filters
function populateFilters() {
  const bankSet = new Set();
  const categorySet = new Set();

  txnMap.forEach((tx) => {
    bankSet.add(tx.bank);
    categorySet.add(tx.category);
  });

  const bankFilter = document.getElementById("bank-filter");
  const categoryFilter = document.getElementById("category-filter");

  bankFilter.innerHTML = '<option value="">All Banks</option>';
  categoryFilter.innerHTML = '<option value="">All Categories</option>';

  bankSet.forEach((bank) => {
    const opt = document.createElement("option");
    opt.value = opt.textContent = bank;
    bankFilter.appendChild(opt);
  });

  categorySet.forEach((cat) => {
    const opt = document.createElement("option");
    opt.value = opt.textContent = cat;
    categoryFilter.appendChild(opt);
  });

  bankFilter.addEventListener("change", applyFilters);
  categoryFilter.addEventListener("change", applyFilters);
}

// 3️⃣ Apply Filters
function applyFilters() {
  const bankVal = document.getElementById("bank-filter").value;
  const catVal = document.getElementById("category-filter").value;

  const filtered = Array.from(txnMap.values()).filter(
    (tx) =>
      (!bankVal || tx.bank === bankVal) && (!catVal || tx.category === catVal)
  );

  renderTable(filtered);
  updateSummary(filtered);
  renderChart(filtered);
}

// 4️⃣ Render Table
function renderTable(txns) {
  const tbody = document.querySelector("#txn-table tbody");
  tbody.innerHTML = "";

  txns.forEach((tx) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${tx.id}</td>
      <td>${tx.bank}</td>
      <td>₹${tx.amount}</td>
      <td>${tx.description}</td>
      <td>${tx.category}</td>
      <td>${tx.suspicious_reason || "—"}</td>
    `;
    tbody.appendChild(row);
  });
}

// 5️⃣ Update Summary
function updateSummary(txns) {
  const total = txns.length;
  const amount = txns.reduce((sum, tx) => sum + tx.amount, 0);

  const categories = {};
  txns.forEach((tx) => {
    categories[tx.category] = (categories[tx.category] || 0) + 1;
  });

  const summaryDiv = document.getElementById("summary");
  summaryDiv.innerHTML = `
    🧾 <b>${total}</b> transactions<br>
    💸 Total amount: <b>₹${amount.toLocaleString()}</b><br>
    📊 Category breakdown:<br>
    <ul>
      ${Object.entries(categories)
        .map(([cat, count]) => `<li>${cat}: ${count}</li>`)
        .join("")}
    </ul>
  `;
}

// 6️⃣ Render Chart
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
      datasets: [
        {
          label: "₹ Amount by Category",
          data: values,
          backgroundColor: "rgba(54, 162, 235, 0.5)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: (val) => "₹" + val,
          },
        },
      },
    },
  });
}

// 7️⃣ Toggle View
document.getElementById("view-mode").addEventListener("change", (e) => {
  const endpoint =
    e.target.value === "all" ? "all-transactions" : "suspicious-transactions";
  loadTransactions(endpoint);
});
