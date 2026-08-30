const reader = document.getElementById('reader');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const resultDiv = document.getElementById('result');
const receiptCountDiv = document.getElementById('receiptCount');

let scanner = null;

// HTML Templates
const CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2"><div class="card-body p-3"><pre class="mb-0"><code class="text-white small">{content}</code></pre></div></div>';

const RECEIPT_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-3"><div class="card-body p-3"><h6 class="card-title mb-2">Чек</h6><div class="small">{content}</div></div></div>';
const RETAILER_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-3"><div class="card-body p-3"><h6 class="card-title mb-2">Магазин</h6><div class="small">{content}</div></div></div>';
const SHOP_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-3"><div class="card-body p-3"><h6 class="card-title mb-2">Адрес</h6><div class="small">{content}</div></div></div>';
const EMPLOYEE_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-3"><div class="card-body p-3"><h6 class="card-title mb-2">Сотрудник</h6><div class="small">{content}</div></div></div>';
const ITEMS_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-3"><div class="card-body p-3"><h6 class="card-title mb-2">Товары</h6><div class="small">{content}</div></div></div>';
const LOADING_TEMPLATE = '<div class="text-secondary mt-3"><div class="progress" style="height: 4px;"><div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 100%"></div></div></div>';
const ERROR_TEMPLATE = '<div class="card bg-dark text-white mt-3"><div class="card-body p-3"><h6 class="card-title mb-2 text-danger">Ошибка</h6><div class="small text-danger">{message}</div></div></div>';

function formatNumber(num) {
  const str = num.toString();
  if (str.endsWith('.00')) {
    return str.replace('.00', '').replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  }
  return str.replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}

function formatReceiptData(receipt) {
  return `<i class="bi bi-hash text-secondary"></i> <span class="text-secondary">ID:</span> ${receipt.id}<br>
<i class="bi bi-calendar3 text-secondary"></i> <span class="text-secondary">Дата:</span> ${new Date(receipt.t).toLocaleString('ru-RU').replace(',', '')}<br>
<i class="bi bi-cash-coin text-secondary"></i> <span class="text-secondary">Сумма:</span> ${formatNumber(receipt.s)}₽<br>
<i class="bi bi-funnel text-secondary"></i> <span class="text-secondary">ФН:</span> ${receipt.fn}<br>
<i class="bi bi-hash text-secondary"></i> <span class="text-secondary">ФД:</span> ${receipt.i}<br>
<i class="bi bi-key text-secondary"></i> <span class="text-secondary">ФП:</span> ${receipt.fp}<br>
<i class="bi bi-calculator text-secondary"></i> <span class="text-secondary">Тип расчёта:</span> ${receipt.n}`;
}

function formatRetailerData(retailer) {
  const name = retailer.name;
  const type = retailer.is_individual ? 'Индивидуальный' : 'Организация';
  return `<i class="bi bi-hash text-secondary"></i> <span class="text-secondary">ID:</span> ${retailer.id}<br>
<i class="bi bi-shop text-secondary"></i> <span class="text-secondary">Название:</span> ${name}<br>
<i class="bi bi-card-text text-secondary"></i> <span class="text-secondary">ИНН:</span> ${retailer.inn}<br>
<i class="bi bi-person text-secondary"></i> <span class="text-secondary">Тип:</span> ${type}`;
}

function formatShopData(shop) {
  return `<i class="bi bi-hash text-secondary"></i> <span class="text-secondary">ID:</span> ${shop.id}<br>
<i class="bi bi-geo-alt text-secondary"></i> <span class="text-secondary">Адрес:</span> ${shop.address}`;
}

function formatEmployeeData(employee) {
  return `<i class="bi bi-hash text-secondary"></i> <span class="text-secondary">ID:</span> ${employee.id}<br>
<i class="bi bi-person-badge text-secondary"></i> <span class="text-secondary">Имя:</span> ${employee.name}`;
}

function formatItemsData(items) {
  if (!items || items.length === 0) return 'Нет товаров';

  return items.map(item => `<i class="bi bi-hash text-secondary"></i> <span class="text-secondary">ID:</span> ${item.id}<br>
<i class="bi bi-cart-plus text-secondary"></i> <span class="text-secondary">Название:</span> ${item.name}<br>
<i class="bi bi-cash-coin text-secondary"></i> <span class="text-secondary">Цена:</span> ${formatNumber(item.price)}₽<br>
<i class="bi bi-plus-circle text-secondary"></i> <span class="text-secondary">Количество:</span> ${item.quantity}<br>
<i class="bi bi-cash-stack text-secondary"></i> <span class="text-secondary">Сумма:</span> ${formatNumber(item.total)}₽<br>
<i class="bi bi-percent text-secondary"></i> <span class="text-secondary">Тип налоговой ставки:</span> ${item.nds}<br>
<i class="bi bi-credit-card text-secondary"></i> <span class="text-secondary">Тип оплаты:</span> ${item.payment}<br>
<i class="bi bi-box text-secondary"></i> <span class="text-secondary">Тип товара:</span> ${item.product}`).join('<br><br>');
}

function createCard(content) {
  return CARD_TEMPLATE.replace('{content}', content);
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

function createBeautifulCards(data) {
  let html = '';

  // Receipt Card (first)
  if (data.receipt) {
    const receiptContent = formatReceiptData(data.receipt);
    html += createReceiptCard(receiptContent);
  }

  // Items Card (second)
  if (data.items && data.items.length > 0) {
    const itemsContent = formatItemsData(data.items);
    html += createItemsCard(itemsContent);
  }

  // Retailer Card (third)
  if (data.retailer) {
    const retailerContent = formatRetailerData(data.retailer);
    html += createRetailerCard(retailerContent);
  }

  // Shop Card (fourth) - may not exist
  if (data.shop) {
    const shopContent = formatShopData(data.shop);
    html += createShopCard(shopContent);
  }

  // Employee Card (fifth) - may not exist
  if (data.employee) {
    const employeeContent = formatEmployeeData(data.employee);
    html += createEmployeeCard(employeeContent);
  }

  return html;
}

function onScanSuccess(decodedText) {
  const qrHtml = createCard(decodedText);
  const loadingHtml = LOADING_TEMPLATE;
  resultDiv.innerHTML = qrHtml + loadingHtml;

  const params = new URLSearchParams(decodedText);
  const url = `https://localhost:8800/registry/by-fiscal-fields?${params.toString()}`;

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then(res => {
      if (!res.ok) {
        return res.text().then(text => {
          try {
            const errorData = JSON.parse(text);
            const detail = errorData.detail;
            if (detail && typeof detail === 'string') {
              throw new Error(detail);
            } else {
              throw new Error(text || `HTTP error! status: ${res.status}`);
            }
          } catch {
            throw new Error(text || `HTTP error! status: ${res.status}`);
          }
        });
      }
      return res.json();
    })
    .then(data => {
      const beautifulCards = createBeautifulCards(data);
      // Remove loading indicator and show only beautiful cards (no QR card)
      resultDiv.innerHTML = beautifulCards;

      if (data.receipt) {
        updateReceiptCount();
      }
    })
    .catch(err => {
      const errorHtml = `<div class="card bg-dark text-danger mt-3 border border-danger"><div class="card-body p-3"><h6 class="card-title mb-2 text-danger">Ошибка</h6><div class="small text-danger"><i class="bi bi-exclamation-triangle text-danger me-2"></i><span class="text-danger">Причина:</span> ${err.message}</div></div></div>`;
      resultDiv.innerHTML = errorHtml;
    });

  stopScanner();
}

function onManualSubmit() {
  const manualInput = document.getElementById('manualInput');
  const inputValue = manualInput.value.trim();
  
  if (!inputValue) {
    resultDiv.innerHTML = createError('Пожалуйста, введите данные чека');
    return;
  }

  const loadingHtml = LOADING_TEMPLATE;
  resultDiv.innerHTML = loadingHtml;

  try {
    const params = new URLSearchParams(inputValue);
    const url = `https://localhost:8800/registry/by-fiscal-fields?${params.toString()}`;

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(res => {
        if (!res.ok) {
          return res.text().then(text => {
            try {
              const errorData = JSON.parse(text);
              const detail = errorData.detail;
              if (detail && typeof detail === 'string') {
                throw new Error(detail);
              } else {
                throw new Error(text || `HTTP error! status: ${res.status}`);
              }
            } catch {
              throw new Error(text || `HTTP error! status: ${res.status}`);
            }
          });
        }
        return res.json();
      })
      .then(data => {
        const beautifulCards = createBeautifulCards(data);
        resultDiv.innerHTML = beautifulCards;

        if (data.receipt) {
          updateReceiptCount();
        }
      })
      .catch(err => {
        const errorHtml = `<div class="card bg-dark text-danger mt-3 border border-danger"><div class="card-body p-3"><h6 class="card-title mb-2 text-danger">Ошибка</h6><div class="small text-danger"><i class="bi bi-exclamation-triangle text-danger me-2"></i><span class="text-danger">Причина:</span> ${err.message}</div></div></div>`;
        resultDiv.innerHTML = errorHtml;
      });
  } catch (error) {
    resultDiv.innerHTML = createError('Ошибка формата данных. Пожалуйста, проверьте ввод.');
  }
}

async function startScanner() {
  try {
    scanner = new Html5Qrcode(reader.id);
    const config = {
      fps: 20,
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
    const response = await fetch('https://localhost:8800/receipts/stats/count');
    const data = await response.json();
    receiptCountDiv.textContent = data.total;
  } catch (error) {
    receiptCountDiv.textContent = '';
    console.error('Error fetching receipt count:', error);
  }
}

updateReceiptCount();

startBtn.addEventListener('click', startScanner);
stopBtn.addEventListener('click', stopScanner);
document.getElementById('submitBtn').addEventListener('click', onManualSubmit);
window.addEventListener('beforeunload', stopScanner);