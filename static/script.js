hljs.highlightAll();

const reader = document.getElementById('reader');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const resultDiv = document.getElementById('result');
const receiptCountDiv = document.getElementById('receiptCount');

let scanner = null;

// HTML Templates
const CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2"><div class="card-body p-2"><pre class="mb-0"><code class="text-white small">{content}</code></pre></div></div>';
const RECEIPT_CARD_TEMPLATE = '<div class="card bg-gradient-primary text-white mt-2 mb-2 shadow-lg"><div class="card-body"><h6 class="card-title mb-2">📋 Чек</h6><div class="small">{content}</div></div></div>';
const RETAILER_CARD_TEMPLATE = '<div class="card bg-gradient-success text-white mt-2 mb-2 shadow-lg"><div class="card-body"><h6 class="card-title mb-2">🏪 Магазин</h6><div class="small">{content}</div></div></div>';
const SHOP_CARD_TEMPLATE = '<div class="card bg-gradient-info text-white mt-2 mb-2 shadow-lg"><div class="card-body"><h6 class="card-title mb-2">📍 Адрес</h6><div class="small">{content}</div></div></div>';
const EMPLOYEE_CARD_TEMPLATE = '<div class="card bg-gradient-warning text-white mt-2 mb-2 shadow-lg"><div class="card-body"><h6 class="card-title mb-2">👤 Сотрудник</h6><div class="small">{content}</div></div></div>';
const ITEMS_CARD_TEMPLATE = '<div class="card bg-gradient-dark text-white mt-2 mb-2 shadow-lg"><div class="card-body"><h6 class="card-title mb-2">🛒 Товары</h6><div class="small">{content}</div></div></div>';
const CRPT_CARD_TEMPLATE = '<div class="card bg-gradient-secondary text-white mt-2 mb-2 shadow-lg"><div class="card-body"><h6 class="card-title mb-2">🔍 Проверка</h6><div class="small">{content}</div></div></div>';
const LOADING_TEMPLATE = '<div class="text-secondary mt-2"><div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 100%"></div></div></div>';
const ERROR_TEMPLATE = '<div class="text-danger mt-2">Error: {message}</div>';

function createCard(content) {
  return CARD_TEMPLATE.replace('{content}', content);
}

function formatReceiptData(receipt) {
  return `
📅 Дата: ${new Date(receipt.t).toLocaleString('ru-RU')}
💰 Сумма: ${receipt.s}₽
📄 ФН: ${receipt.fn}
🆔 №: ${receipt.i}
🔐 ФП: ${receipt.fp}
📋 Кол-во: ${receipt.n}
  `.trim();
}

function formatRetailerData(retailer) {
  return `
🏪 Название: ${retailer.name}
🆔 ИНН: ${retailer.inn}
👤 Физ. лицо: ${retailer.is_individual ? 'Да' : 'Нет'}
  `.trim();
}

function formatShopData(shop) {
  return `
📍 Адрес: ${shop.address}
🆔 ID: ${shop.id}
  `.trim();
}

function formatEmployeeData(employee) {
  return `
👤 Имя: ${employee.name}
🆔 ID: ${employee.id}
🏪 ID магазина: ${employee.shop_id}
  `.trim();
}

function formatItemsData(items) {
  if (!items || items.length === 0) return 'Нет товаров';
  
  return items.map(item => `
🛒 ${item.name}
   Цена: ${item.price}₽
   Кол-во: ${item.quantity}
   Сумма: ${item.total}₽
   НДС: ${item.nds}%
   Тип оплаты: ${item.payment}
   Тип товара: ${item.product}
  `.trim()).join('\n\n');
}

function formatCrptData(crpt) {
  if (!crpt || !crpt.dump) return 'Нет данных проверки';
  
  const dump = crpt.dump;
  const resolveData = dump.codeResolveData || {};
  
  return `
🆔 ID: ${crpt.id}
📊 Статус: ${dump.status}
📋 Категория: ${dump.category}
🔍 Тип: ${dump.codeType}
📅 Дата проверки: ${new Date(dump.checkDate).toLocaleString('ru-RU')}
✅ Результат: ${dump.checkResult ? 'Успешно' : 'Ошибка'}
📄 Код: ${dump.code}

${resolveData.message ? `⚠️ Сообщение: ${resolveData.message}` : ''}
${resolveData.found ? `🔍 Найдено: ${resolveData.found}` : ''}
${resolveData.verified ? `✅ Проверено: ${resolveData.verified}` : ''}
${resolveData.valid ? `✅ Валидно: ${resolveData.valid}` : ''}
  `.trim();
}

function createBeautifulCards(data, decodedText) {
  let html = '';
  
  // QR Code Card
  const qrHighlighted = hljs.highlight(decodedText, { language: 'plaintext' }).value;
  html += createCard(qrHighlighted);
  
  // Loading indicator
  html += LOADING_TEMPLATE;
  
  // CRPT Card
  if (data.crpt) {
    const crptContent = formatCrptData(data.crpt);
    html += createCrptCard(crptContent);
  }
  
  // Receipt Card
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

function createCrptCard(content) {
  return CRPT_CARD_TEMPLATE.replace('{content}', content);
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
      resultDiv.innerHTML = beautifulCards;

      if (data.crpt && data.crpt.id) {
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
