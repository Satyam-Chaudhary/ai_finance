let allTxns = [];

async function loadTransactions() {
  const res = await fetch("http://localhost:8001/suspicious-transactions");
  allTxns = await res.json();

  populateFilters();
  renderTable(allTxns);
  updateSummary(allTxns);
  renderChart(allTxns);
}

function populateFilters() {
  const bankSet = new Set();
  const categorySet = new Set();

  allTxns.forEach(tx => {
    bankSet.add(tx.bank);
    categorySet.add(tx.category);
  });

  const bankFilter = document.getElementById("bank-filter");
  const categoryFilter = document.getElementById("category-filter");

  bankSet.forEach(bank => {
    const opt = document.createElement("option");
    opt.value = opt.textContent = bank;
    bankFilter.appendChild(opt);
  });

  categorySet.forEach(cat => {
    const opt = document.createElement("option");
    opt.value = opt.textContent = cat;
    categoryFilter.appendChild(opt);
  });

  // Add event listeners
  bankFilter.addEventListener("change", applyFilters);
  categoryFilter.addEventListener("change", applyFilters);
}

function applyFilters() {
  const bankVal = document.getElementById("bank-filter").value;
  const catVal = document.getElementById("category-filter").value;

  const filtered = allTxns.filter(tx => {
    return (!bankVal || tx.bank === bankVal) &&
           (!catVal || tx.category === catVal);
  });

  renderTable(filtered);
  updateSummary(filtered);
  renderChart(filtered);
}

function renderTable(txns) {
  const tbody = document.querySelector("#txn-table tbody");
  tbody.innerHTML = ""; // clear previous

  txns.forEach(tx => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${tx.id}</td>
      <td>${tx.bank}</td>
      <td>₹${tx.amount}</td>
      <td>${tx.description}</td>
      <td>${tx.category}</td>
      <td>${tx.suspicious_reason || '—'}</td>
    `;
    tbody.appendChild(row);
  });
}

function updateSummary(txns) {
  const total = txns.length;
  const amount = txns.reduce((sum, tx) => sum + tx.amount, 0);

  const categories = {};
  txns.forEach(tx => {
    categories[tx.category] = (categories[tx.category] || 0) + 1;
  });

  const summaryDiv = document.getElementById("summary");
  summaryDiv.innerHTML = `
    🧾 <b>${total}</b> suspicious transactions<br>
    💸 Total amount: <b>₹${amount.toLocaleString()}</b><br>
    📊 Category breakdown:<br>
    <ul>
      ${Object.entries(categories).map(([cat, count]) => `<li>${cat}: ${count}</li>`).join("")}
    </ul>
  `;
}


document.addEventListener("DOMContentLoaded", () => {
  loadTransactions();
});

let chart;  

function renderChart(txns) {
  const ctx = document.getElementById("txn-chart").getContext("2d");

  const categoryTotals = {};
  txns.forEach(tx => {
    const cat = tx.category || "others";
    categoryTotals[cat] = (categoryTotals[cat] || 0) + tx.amount;
  });

  const labels = Object.keys(categoryTotals);
  const values = Object.values(categoryTotals);

  if (chart) chart.destroy(); // Clear old chart if exists

  chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Suspicious ₹ Amount by Category',
        data: values,
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: val => '₹' + val
          }
        }
      }
    }
  });
}
