const reader = document.getElementById('reader');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const resultDiv = document.getElementById('result');
const receiptCountDiv = document.getElementById('receiptCount');

let scanner = null;

// HTML Templates
const CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2"><div class="card-body p-3"><pre class="mb-0"><code class="text-white small">{content}</code></pre></div></div>';
const RECEIPT_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2 mb-2"><div class="card-body p-3"><h6 class="card-title mb-2">Чек</h6><div class="small">{content}</div></div></div>';
const RETAILER_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2 mb-2"><div class="card-body p-3"><h6 class="card-title mb-2">Магазин</h6><div class="small">{content}</div></div></div>';
const SHOP_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2 mb-2"><div class="card-body p-3"><h6 class="card-title mb-2">Адрес</h6><div class="small">{content}</div></div></div>';
const EMPLOYEE_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2 mb-2"><div class="card-body p-3"><h6 class="card-title mb-2">Сотрудник</h6><div class="small">{content}</div></div></div>';
const ITEMS_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2 mb-2"><div class="card-body p-3"><h6 class="card-title mb-2">Товары</h6><div class="small">{content}</div></div></div>';
const LOADING_TEMPLATE = '<div class="text-secondary mt-3"><div class="progress" style="height: 4px;"><div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 100%"></div></div></div>';
const ERROR_TEMPLATE = '<div class="text-danger mt-3" style="padding: 10px; border: 1px solid #dc3545; border-radius: 4px; background-color: #f8d7da;">Error: {message}</div>';

function createCard(content) {
  return CARD_TEMPLATE.replace('{content}', content);
}

function formatReceiptData(receipt) {
  return `
<i class="bi bi-calendar3"></i> Дата: ${new Date(receipt.t).toLocaleString('ru-RU')}<br>
<i class="bi bi-currency-ruble"></i> Сумма: ${receipt.s}₽<br>
<i class="bi bi-funnel"></i> ФН: ${receipt.fn}<br>
<i class="bi bi-hash"></i> №: ${receipt.i}<br>
<i class="bi bi-key"></i> ФП: ${receipt.fp}<br>
<i class="bi bi-list-ol"></i> Кол-во: ${receipt.n}
  `.trim();
}

function formatRetailerData(retailer) {
  return `
<i class="bi bi-shop"></i> Название: ${retailer.name}<br>
<i class="bi bi-card-text"></i> ИНН: ${retailer.inn}<br>
<i class="bi bi-person"></i> Физ. лицо: ${retailer.is_individual ? 'Да' : 'Нет'}
  `.trim();
}

function formatShopData(shop) {
  return `
<i class="bi bi-geo-alt"></i> Адрес: ${shop.address}<br>
<i class="bi bi-tag"></i> ID: ${shop.id}
  `.trim();
}

function formatEmployeeData(employee) {
  return `
<i class="bi bi-person-badge"></i> Имя: ${employee.name}<br>
<i class="bi bi-building"></i> ID магазина: ${employee.shop_id}
  `.trim();
}

function formatItemsData(items) {
  if (!items || items.length === 0) return 'Нет товаров';
  
  return items.map(item => `
<i class="bi bi-cart-plus"></i> ${item.name}<br>
<i class="bi bi-currency-ruble"></i> Цена: ${item.price}₽<br>
<i class="bi bi-plus-circle"></i> Кол-во: ${item.quantity}<br>
<i class="bi bi-cash-stack"></i> Сумма: ${item.total}₽<br>
<i class="bi bi-percent"></i> НДС: ${item.nds}%<br>
<i class="bi bi-credit-card"></i> Тип оплаты: ${item.payment}<br>
<i class="bi bi-box"></i> Тип товара: ${item.product}
  `.trim()).join('<br><br>');
}
function createBeautifulCards(data, decodedText) {
  let html = '';

  // Loading indicator
  html += LOADING_TEMPLATE;

  // Receipt Card (main info)
  if (data.receipt) {
    const receiptContent = formatReceiptData(data.receipt);
    html += createReceiptCard(receiptContent);
  }

  // Retailer Card
  if (data.retailer) {
    const retailerContent = formatRetailerData(data.retailer);
    html += createRetailerCard(retailerContent);
  }

  // Shop Card
  if (data.shop) {
    const shopContent = formatShopData(data.shop);
    html += createShopCard(shopContent);
  }

  // Employee Card
  if (data.employee) {
    const employeeContent = formatEmployeeData(data.employee);
    html += createEmployeeCard(employeeContent);
  }

  // Items Card
  if (data.items && data.items.length > 0) {
    const itemsContent = formatItemsData(data.items);
    html += createItemsCard(itemsContent);
  }

  return html;
}

function createReceiptCard(content) {
  return RECEIPT_CARD_TEMPLATE.replace('{content}', content);
}

function createRetailerCard(content) {
  return RETAILER_CARD_TEMPLATE.replace('{content}', content);
}

function createShopCard(content) {
  return SHOP_CARD_TEMPLATE.replace('{content}', content);
}

function createEmployeeCard(content) {
  return EMPLOYEE_CARD_TEMPLATE.replace('{content}', content);
}

function createItemsCard(content) {
  return ITEMS_CARD_TEMPLATE.replace('{content}', content);
}

function createError(message) {
  return ERROR_TEMPLATE.replace('{message}', message);
}

function onScanSuccess(decodedText) {
  const qrHighlighted = hljs.highlight(decodedText, { language: 'plaintext' }).value;
  const qrHtml = createCard(qrHighlighted);
  const loadingHtml = LOADING_TEMPLATE;
  resultDiv.innerHTML = qrHtml + loadingHtml;

  const params = new URLSearchParams(decodedText);
  const url = `/registry?${params.toString()}`;

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then(res => {
      if (!res.ok) {
        return res.text().then(text => {
          throw new Error(text || `HTTP error! status: ${res.status}`);
        });
      }
      return res.json();
    })
    .then(data => {
      const beautifulCards = createBeautifulCards(data, decodedText);
      // Remove loading indicator and show QR + beautiful cards
      resultDiv.innerHTML = qrHtml + beautifulCards.replace(LOADING_TEMPLATE, '');

      if (data.receipt) {
        updateReceiptCount();
      }
    })
    .catch(err => {
      resultDiv.innerHTML = qrHtml + createError(err.message);
    });

  stopScanner();
}

async function startScanner() {
  try {
    scanner = new Html5Qrcode(reader.id);
    const config = {
      fps: 20,
      qrbox: { width: 200, height: 200 },
      videoConstraints: {
        facingMode: "environment",
        zoom: 3
      }
    };
    await scanner.start(
      { facingMode: "environment" },
      config,
      onScanSuccess,
      (err) => { }
    );
    startBtn.style.display = 'none';
    stopBtn.style.display = 'inline-block';
  } catch (err) {
    resultDiv.innerHTML = createError(err.message || err.toString());
  }
}

function stopScanner() {
  if (scanner) {
    scanner.stop()
      .then(() => scanner.clear())
      .catch((err) => {
        console.error('Error stopping scanner:', err);
      });
    scanner = null;
  }
  startBtn.style.display = 'inline-block';
  stopBtn.style.display = 'none';
}

async function updateReceiptCount() {
  try {
    const response = await fetch('/api/receipts/stats/count');
    const data = await response.json();
    receiptCountDiv.textContent = data.count;
  } catch (error) {
    receiptCountDiv.textContent = '';
    console.error('Error fetching receipt count:', error);
  }
}

updateReceiptCount();

startBtn.addEventListener('click', startScanner);
stopBtn.addEventListener('click', stopScanner);
window.addEventListener('beforeunload', stopScanner);
