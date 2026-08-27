const reader = document.getElementById('reader');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const resultDiv = document.getElementById('result');
const receiptCountDiv = document.getElementById('receiptCount');

let scanner = null;

// HTML Templates
const CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2"><div class="card-body p-3"><pre class="mb-0"><code class="text-white small">{content}</code></pre></div></div>';

const RECEIPT_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2 mb-2"><div class="card-body p-3"><h6 class="card-title mb-2">Чек</h6><div class="small" style="max-height: 200px; overflow-y: auto;">{content}</div></div></div>';
const RETAILER_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2 mb-2"><div class="card-body p-3"><h6 class="card-title mb-2">Магазин</h6><div class="small" style="max-height: 200px; overflow-y: auto;">{content}</div></div></div>';
const SHOP_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2 mb-2"><div class="card-body p-3"><h6 class="card-title mb-2">Адрес</h6><div class="small" style="max-height: 200px; overflow-y: auto;">{content}</div></div></div>';
const EMPLOYEE_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2 mb-2"><div class="card-body p-3"><h6 class="card-title mb-2">Сотрудник</h6><div class="small" style="max-height: 200px; overflow-y: auto;">{content}</div></div></div>';
const ITEMS_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2 mb-2"><div class="card-body p-3"><h6 class="card-title mb-2">Товары</h6><div class="small" style="max-height: 400px; overflow-y: auto;">{content}</div></div></div>';
const ERROR_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2 mb-2"><div class="card-body p-3"><h6 class="card-title mb-2 text-danger">Ошибка</h6><div class="small">{content}</div></div></div>';

const LOADING_TEMPLATE = '<div class="loading-bar" style="position: fixed; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #007bff, #0056b3, #007bff); background-size: 200% 100%; animation: loading 1.5s linear infinite; z-index: 9999;"></div><style>@keyframes loading { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }</style>';

function formatNumber(num) {
  const str = num.toString();
  if (str.endsWith('.00')) {
    return str.replace('.00', '');
  }
  return str.replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}

function formatReceiptData(receipt) {
  return `
<i class="bi bi-calendar3 text-secondary"></i> Дата: ${new Date(receipt.t).toLocaleString('ru-RU')}<br>
<i class="bi bi-cash-stack text-secondary"></i> Сумма: ${formatNumber(receipt.s)}<br>
<i class="bi bi-funnel text-secondary"></i> ФН: ${receipt.fn}<br>
<i class="bi bi-file-earmark-text text-secondary"></i> ФД: ${receipt.fd}<br>
<i class="bi bi-key text-secondary"></i> ФП: ${receipt.fp}<br>
<i class="bi bi-calculator text-secondary"></i> Тип расчёта: ${receipt.t}<br>`;
}

function formatRetailerData(retailer) {
  const name = retailer.name.replace(/ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ/g, 'ООО');
  return `
<i class="bi bi-shop text-secondary"></i> Название: ${name}<br>
<i class="bi bi-card-text text-secondary"></i> ИНН: ${retailer.inn}<br>
<i class="bi bi-person text-secondary"></i> Физ. лицо: ${retailer.isPhysicalPerson ? 'Да' : 'Нет'}`;
}

function formatShopData(shop) {
  return `
<i class="bi bi-geo-alt text-secondary"></i> Адрес: ${shop.address}`;
}

function formatEmployeeData(employee) {
  return `
<i class="bi bi-person-badge text-secondary"></i> Имя: ${employee.name}`;
}

function formatItemsData(items) {
  return items.map(item => `
<i class="bi bi-cart-plus text-secondary"></i> ${item.name}<br>
<i class="bi bi-cash-coin text-secondary"></i> Цена: ${formatNumber(item.price)}<br>
<i class="bi bi-plus-circle text-secondary"></i> Куплено: ${item.quantity}<br>
<i class="bi bi-cash-stack text-secondary"></i> Сумма: ${formatNumber(item.sum)}<br>
<i class="bi bi-percent text-secondary"></i> НДС: ${item.vat}%<br>
<i class="bi bi-credit-card text-secondary"></i> Тип оплаты: ${item.paymentType}<br>
<i class="bi bi-box text-secondary"></i> Тип товара: ${item.type}<br><br>`).join('');
}

async function createBeautifulCards(data) {
  let cardsHtml = '';
  
  if (data.receipt) {
    cardsHtml += RECEIPT_CARD_TEMPLATE.replace('{content}', formatReceiptData(data.receipt));
  }
  
  if (data.retailer) {
    cardsHtml += RETAILER_CARD_TEMPLATE.replace('{content}', formatRetailerData(data.retailer));
  }
  
  if (data.shop) {
    cardsHtml += SHOP_CARD_TEMPLATE.replace('{content}', formatShopData(data.shop));
  }
  
  if (data.employee) {
    cardsHtml += EMPLOYEE_CARD_TEMPLATE.replace('{content}', formatEmployeeData(data.employee));
  }
  
  if (data.items && data.items.length > 0) {
    cardsHtml += ITEMS_CARD_TEMPLATE.replace('{content}', formatItemsData(data.items));
  }
  
  if (data.error) {
    cardsHtml += ERROR_CARD_TEMPLATE.replace('{content}', data.error);
  }
  
  return cardsHtml;
}

async function getRetailerById(retailerId) {
  try {
    const response = await fetch(`/retailers/${retailerId}`);
    if (!response.ok) throw new Error('Retailer not found');
    return await response.json();
  } catch (error) {
    console.error('Error fetching retailer:', error);
    return null;
  }
}

async function getShopById(shopId) {
  try {
    const response = await fetch(`/shops/${shopId}`);
    if (!response.ok) throw new Error('Shop not found');
    return await response.json();
  } catch (error) {
    console.error('Error fetching shop:', error);
    return null;
  }
}

async function getEmployeeById(employeeId) {
  try {
    const response = await fetch(`/employees/${employeeId}`);
    if (!response.ok) throw new Error('Employee not found');
    return await response.json();
  } catch (error) {
    console.error('Error fetching employee:', error);
    return null;
  }
}

async function getItemsById(itemId) {
  try {
    const response = await fetch(`/items/${itemId}`);
    if (!response.ok) throw new Error('Items not found');
    return await response.json();
  } catch (error) {
    console.error('Error fetching items:', error);
    return null;
  }
}

async function parseQRCode(qrData) {
  try {
    const response = await fetch('/api/parse-qr', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ qr_data: qrData })
    });
    
    if (!response.ok) {
      throw new Error('Failed to parse QR code');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error parsing QR code:', error);
    throw error;
  }
}

async function onScanSuccess(decodedText, decodedResult) {
async function onScanSuccess(decodedText, decodedResult) {
  const qrHtml = CARD_TEMPLATE.replace('{content}', `Отсканирован QR код:\n${decodedText}`);
  const loadingHtml = LOADING_TEMPLATE;
  
  resultDiv.innerHTML = qrHtml + loadingHtml;
  
  // Останавливаем сканер после успешного сканирования
  stopScanner();
  
  try {
    const parsedData = await parseQRCode(decodedText);
    
    if (parsedData.error) {
      const errorHtml = ERROR_CARD_TEMPLATE.replace('{content}', parsedData.error);
      resultDiv.innerHTML = errorHtml;
      return;
    }
    
    const beautifulCards = await createBeautifulCards(parsedData);
    resultDiv.innerHTML = beautifulCards;
    
  } catch (error) {
    console.error('Error processing QR code:', error);
    const errorHtml = ERROR_CARD_TEMPLATE.replace('{content}', `Ошибка: ${error.message}`);
    resultDiv.innerHTML = errorHtml;
  }
}

function onScanFailure(error) {
  console.warn(`QR scan failed: ${error}`);
}
function startScanner() {
  if (scanner) return;
  
  resultDiv.innerHTML = LOADING_TEMPLATE;
  
  scanner = new Html5Qrcode("reader").scan(
    onScanSuccess,
    onScanFailure
  ).catch(err => {
    console.error('Scanner error:', err);
    scanner = null;
    resultDiv.innerHTML = ERROR_CARD_TEMPLATE.replace('{content}', 'Не удалось запустить камеру. Пожалуйста, разрешите доступ к камере.');
  });
}

function stopScanner() {
  if (scanner) {
    scanner.clear().catch(err => {
      console.error('Error stopping scanner:', err);
    }).finally(() => {
      scanner = null;
    });
  }
}

async function updateReceiptCount() {
  try {
    const response = await fetch('/receipts/stats/count');
    if (!response.ok) {
      throw new Error('Failed to fetch receipt count');
    }
    const data = await response.json();
    receiptCountDiv.textContent = `Чеков: ${data.count}`;
  } catch (error) {
    receiptCountDiv.textContent = '';
    console.error('Error fetching receipt count:', error);
  }
}

updateReceiptCount();

startBtn.addEventListener('click', startScanner);
stopBtn.addEventListener('click', stopScanner);
window.addEventListener('beforeunload', stopScanner);
});