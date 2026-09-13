import QrScanner from 'qr-scanner';

// DOM references
const reader = document.getElementById('reader');
const manualPanel = document.getElementById('manualPanel');
const actionBtn = document.getElementById('actionBtn');
const modeToggleBtn = document.getElementById('modeToggleBtn');
const modeToggleIcon = document.getElementById('modeToggleIcon');
const manualInput = document.getElementById('manualInput');
const resultDiv = document.getElementById('result');
const receiptCountDiv = document.getElementById('receiptCount');

// Manual fields
const fieldT = document.getElementById('fieldT');
const fieldS = document.getElementById('fieldS');
const fieldFn = document.getElementById('fieldFn');
const fieldI = document.getElementById('fieldI');
const fieldFp = document.getElementById('fieldFp');
const fieldN = document.getElementById('fieldN');

// Auth bar
const authUsernameSpan = document.getElementById('authUsername');
const authAdminBadge = document.getElementById('authAdminBadge');
const authActionBtn = document.getElementById('authActionBtn');

// Auth modal
const authForm = document.getElementById('authForm');
const authUsernameInput = document.getElementById('authUsernameInput');
const authPassword = document.getElementById('authPassword');
const authUsernameFeedback = document.getElementById('authUsernameFeedback');
const authUsernameSuccess = document.getElementById('authUsernameSuccess');
const authPasswordFeedback = document.getElementById('authPasswordFeedback');
const authSubmitBtn = document.getElementById('authSubmitBtn');
const authModeLoginTab = document.getElementById('authModeLoginTab');
const authModeRegisterTab = document.getElementById('authModeRegisterTab');

let scanner = null;
let isScanning = false;
let isBusy = false;
let currentMode = 'camera'; // 'camera' | 'manual'
let authToken = localStorage.getItem('authToken');
let authMode = 'login';

// Templates
const RECEIPT_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-3"><div class="card-body p-3"><h6 class="card-title mb-2">Чек</h6><div>{content}</div></div></div>';
const RETAILER_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-3"><div class="card-body p-3"><h6 class="card-title mb-2">Магазин</h6><div>{content}</div></div></div>';
const SHOP_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-3"><div class="card-body p-3"><h6 class="card-title mb-2">Адрес</h6><div>{content}</div></div></div>';
const EMPLOYEE_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-3"><div class="card-body p-3"><h6 class="card-title mb-2">Сотрудник</h6><div>{content}</div></div></div>';
const ITEMS_CARD_TEMPLATE = '<div class="card bg-dark text-white mt-3"><div class="card-body p-3"><h6 class="card-title mb-2">Товары</h6><div>{content}</div></div></div>';
const LOADING_TEMPLATE = '<div class="text-secondary mt-3"><div class="progress" style="height: 4px;"><div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 100%"></div></div></div>';
const ERROR_TEMPLATE = '<div class="card bg-dark text-white mt-3"><div class="card-body p-3"><h6 class="card-title mb-2 text-danger">Ошибка</h6><div class="text-danger">{message}</div></div></div>';

// Field validation helpers
function setFieldError(inputEl, feedbackEl, message) {
  inputEl.classList.add('is-invalid');
  inputEl.classList.remove('is-valid');
  feedbackEl.textContent = message;
}

function setFieldSuccess(inputEl, feedbackEl, message) {
  inputEl.classList.add('is-valid');
  inputEl.classList.remove('is-invalid');
  feedbackEl.textContent = message;
}

function clearFieldState(inputEl) {
  inputEl.classList.remove('is-invalid', 'is-valid');
}

function clearAuthFormState() {
  clearFieldState(authUsernameInput);
  clearFieldState(authPassword);
  authUsernameFeedback.textContent = '';
  authUsernameSuccess.textContent = '';
  authPasswordFeedback.textContent = '';
}

// Busy state
function setBusy(busy) {
  isBusy = busy;
  actionBtn.disabled = busy;
  modeToggleBtn.disabled = busy;
  manualInput.disabled = busy;
  [fieldT, fieldS, fieldN, fieldFn, fieldI, fieldFp].forEach(field => {
    if (field) field.disabled = busy;
  });
  updateActionButton();
}

function updateActionButton() {
  // Action selector
  if (currentMode === 'camera') {
    modeToggleIcon.className = 'bi bi-pencil';
    modeToggleBtn.title = 'Переключить на ручной ввод';
  } else {
    modeToggleIcon.className = 'bi bi-camera';
    modeToggleBtn.title = 'Переключить на камеру';
  }

  // Action buttom
  if (currentMode === 'camera') {
    if (isScanning) {
      actionBtn.textContent = 'Стоп';
      actionBtn.classList.remove('btn-primary');
      actionBtn.classList.add('btn-danger');
    } else {
      actionBtn.textContent = 'Старт';
      actionBtn.classList.remove('btn-danger');
      actionBtn.classList.add('btn-primary');
    }
  } else {
    actionBtn.textContent = 'Проверить';
    actionBtn.classList.remove('btn-danger');
    actionBtn.classList.add('btn-primary');
  }
}

// Auth tabs
function setAuthMode(mode) {
  authMode = mode;
  clearAuthFormState();

  if (mode === 'login') {
    authModeLoginTab.classList.add('active');
    authModeRegisterTab.classList.remove('active');
    authSubmitBtn.textContent = 'Войти';
  } else {
    authModeRegisterTab.classList.add('active');
    authModeLoginTab.classList.remove('active');
    authSubmitBtn.textContent = 'Зарегистрироваться';
  }
}

authModeLoginTab.addEventListener('click', () => setAuthMode('login'));
authModeRegisterTab.addEventListener('click', () => setAuthMode('register'));

// Auth API
async function login(username, password) {
  const response = await fetch('./auth/login', {
    method: 'POST',
    headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  if (!response.ok) throw new Error('Неверное имя пользователя или пароль');
  const data = await response.json();
  authToken = data.access_token;
  localStorage.setItem('authToken', authToken);
  updateAuthUI();
}

async function register(username, password) {
  const response = await fetch('./auth/register', {
    method: 'POST',
    headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  if (!response.ok) throw new Error('Ошибка регистрации');
}

function logout() {
  authToken = null;
  localStorage.removeItem('authToken');
  updateAuthUI();
}

async function getCurrentUser() {
  if (!authToken) return null;
  try {
    const response = await fetch('./auth/me', {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });
    if (!response.ok) throw new Error('Failed to fetch current user');
    return await response.json();
  } catch (error) {
    return null;
  }
}

function getAuthHeaders() {
  return authToken ? { 'Authorization': `Bearer ${authToken}` } : {};
}

function updateAuthUI() {
  if (authToken) {
    authActionBtn.textContent = 'Выйти';
    authActionBtn.classList.remove('btn-primary');
    authActionBtn.classList.add('btn-danger');

    getCurrentUser().then(user => {
      authUsernameSpan.textContent = user ? user.username : 'Пользователь';
      authAdminBadge.style.display = user && user.is_admin ? 'inline' : 'none';
    });
  } else {
    authUsernameSpan.textContent = 'Гость';
    authAdminBadge.style.display = 'none';
    authActionBtn.textContent = 'Войти';
    authActionBtn.classList.remove('btn-danger');
    authActionBtn.classList.add('btn-primary');
  }
  updateReceiptCount();
}

// Formatting helpers
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

// Card builders
function createReceiptCard(content) { return RECEIPT_CARD_TEMPLATE.replace('{content}', content); }
function createRetailerCard(content) { return RETAILER_CARD_TEMPLATE.replace('{content}', content); }
function createShopCard(content) { return SHOP_CARD_TEMPLATE.replace('{content}', content); }
function createEmployeeCard(content) { return EMPLOYEE_CARD_TEMPLATE.replace('{content}', content); }
function createItemsCard(content) { return ITEMS_CARD_TEMPLATE.replace('{content}', content); }
function createError(message) { return ERROR_TEMPLATE.replace('{message}', message); }

function createBeautifulCards(data) {
  let html = '';
  if (data.receipt) html += createReceiptCard(formatReceiptData(data.receipt));
  if (data.items && data.items.length > 0) html += createItemsCard(formatItemsData(data.items));
  if (data.retailer) html += createRetailerCard(formatRetailerData(data.retailer));
  if (data.shop) html += createShopCard(formatShopData(data.shop));
  if (data.employee) html += createEmployeeCard(formatEmployeeData(data.employee));
  return html;
}

// QR scanner
async function onScanSuccess(decodedText) {
  if (isBusy) return;
  manualInput.value = decodedText;
  await stopScanner();
  await fetchReceiptData(decodedText);
}

async function fetchReceiptData(qrCode) {
  setBusy(true);
  resultDiv.innerHTML = LOADING_TEMPLATE;

  try {
    const params = new URLSearchParams(qrCode);
    const url = `./registry/by-fiscal-fields?${params.toString()}`;

    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
    });

    if (!res.ok) {
      const text = await res.text();
      let message = text || `HTTP error! status: ${res.status}`;
      try {
        const errorData = JSON.parse(text);
        if (errorData.detail && typeof errorData.detail === 'string') message = errorData.detail;
      } catch { /* not JSON */ }
      throw new Error(message);
    }

    const data = await res.json();
    resultDiv.innerHTML = createBeautifulCards(data);
    if (data.receipt) await updateReceiptCount();
  } catch (err) {
    resultDiv.innerHTML = `<div class="card bg-dark text-danger mt-3 border border-danger"><div class="card-body p-3"><h6 class="card-title mb-2 text-danger">Ошибка</h6><div class="text-danger"><i class="bi bi-exclamation-triangle text-danger me-2"></i><span class="text-danger">Причина:</span> ${err.message}</div></div></div>`;
  } finally {
    setBusy(false);
  }
}

// Converts "YYYY-MM-DDTHH:mm" to "YYYYMMDDTHHmm"
function formatTimestampField(value) {
  if (!value) return '';
  return value.replace(/[-:]/g, '');
}

// QR Builder
function rebuildManualInputFromFields() {
  const params = new URLSearchParams();

  const t = formatTimestampField(fieldT.value.trim());
  if (t) params.set('t', t);

  if (fieldS.value.trim() !== '') params.set('s', fieldS.value.trim());
  if (fieldFn.value.trim() !== '') params.set('fn', fieldFn.value.trim());
  if (fieldI.value.trim() !== '') params.set('i', fieldI.value.trim());
  if (fieldFp.value.trim() !== '') params.set('fp', fieldFp.value.trim());
  if (fieldN.value.trim() !== '') params.set('n', fieldN.value.trim());

  manualInput.value = params.toString();
}

[fieldT, fieldS, fieldFn, fieldI, fieldFp, fieldN].forEach(field => {
  field.addEventListener('input', rebuildManualInputFromFields);
});

function toggleMode() {
  if (isBusy) return;

  if (currentMode === 'camera') {
    currentMode = 'manual';
    reader.classList.add('d-none');
    manualPanel.classList.remove('d-none');
    updateActionButton();
    if (isScanning) stopScanner();
  } else {
    currentMode = 'camera';
    manualPanel.classList.add('d-none');
    reader.classList.remove('d-none');
    updateActionButton();
  }
}

function onActionClick() {
  if (isBusy) return;

  if (currentMode === 'camera') {
    if (isScanning) {
      stopScanner();
    } else {
      startScanner();
    }
  } else {
    onManualSubmit();
  }
}

function onManualSubmit() {
  if (isBusy) return;
  const inputValue = manualInput.value.trim();
  if (!inputValue) {
    resultDiv.innerHTML = createError('Пожалуйста, введите данные чека');
    return;
  }
  fetchReceiptData(inputValue);
}

async function startScanner() {
  setBusy(true);

  try {
    if (scanner) await stopScannerInternal();

    const video = document.createElement('video');
    video.style.width = '100%';
    video.style.height = '100%';
    video.style.objectFit = 'cover';
    reader.innerHTML = '';
    reader.appendChild(video);

    scanner = new QrScanner(
      video,
      result => { onScanSuccess(result.data); },
      { highlightScanRegion: false, highlightCodeOutline: false }
    );

    await scanner.start();
    isScanning = true;
  } catch (err) {
    resultDiv.innerHTML = createError(err.message || err.toString());
  } finally {
    setBusy(false);
  }
}

async function stopScanner() {
  setBusy(true);
  await stopScannerInternal();
  setBusy(false);
}

// Internal cleanup, doesn't touch busy state
function stopScannerInternal() {
  return new Promise((resolve) => {
    if (scanner) {
      const s = scanner;
      scanner = null;
      const video = reader.querySelector('video');

      const tryStop = (methodName) => {
        if (typeof s[methodName] === 'function') {
          try {
            const result = s[methodName]();
            if (result && typeof result.then === 'function') {
              result
                .then(() => { if (video && video.parentNode) video.remove(); resolve(); })
                .catch(() => { if (video && video.parentNode) video.remove(); resolve(); });
              return true;
            }
          } catch (e) { }
        }
        return false;
      };

      if (tryStop('stop')) return;
      if (tryStop('destroy')) return;

      if (video && video.parentNode) video.remove();
      resolve();
    } else {
      resolve();
    }
  }).then(() => {
    isScanning = false;
    updateActionButton();
  });
}

async function updateReceiptCount() {
  try {
    const response = await fetch('./receipts/stats/count', { headers: getAuthHeaders() });
    const data = await response.json();
    receiptCountDiv.textContent = data.total;
  } catch (error) {
    receiptCountDiv.textContent = '';
    console.error('Error fetching receipt count:', error);
  }
}

// Event listeners
modeToggleBtn.addEventListener('click', toggleMode);
actionBtn.addEventListener('click', onActionClick);
window.addEventListener('beforeunload', () => stopScannerInternal());

// Auth form submit
authForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearAuthFormState();

  if (authMode === 'login') {
    try {
      await login(authUsernameInput.value, authPassword.value);
      const modal = bootstrap.Modal.getInstance(document.getElementById('authModal'));
      modal.hide();
      authForm.reset();
      clearAuthFormState();
    } catch (error) {
      setFieldError(authPassword, authPasswordFeedback, error.message);
    }
  } else {
    try {
      await register(authUsernameInput.value, authPassword.value);
      setFieldSuccess(authUsernameInput, authUsernameSuccess, 'Регистрация успешна, теперь можно войти');
      setAuthMode('login');
    } catch (error) {
      setFieldError(authUsernameInput, authUsernameFeedback, error.message);
    }
  }
});

authActionBtn.addEventListener('click', () => {
  if (authToken) {
    logout();
  } else {
    setAuthMode('login');
    authForm.reset();
    const modal = new bootstrap.Modal(document.getElementById('authModal'));
    modal.show();
  }
});

// Initial render
updateAuthUI();
updateActionButton();
