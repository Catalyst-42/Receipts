hljs.highlightAll();

const reader = document.getElementById('reader');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const resultDiv = document.getElementById('result');
const receiptCountDiv = document.getElementById('receiptCount');

let scanner = null;

// HTML Templates
const CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2"><div class="card-body p-2"><pre class="mb-0"><code class="text-white small">{content}</code></pre></div></div>';
const LOADING_TEMPLATE = '<div class="text-secondary mt-2"><div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 100%"></div></div></div>';
const ERROR_TEMPLATE = '<div class="text-danger mt-2">Error: {message}</div>';

function createCard(content) {
  return CARD_TEMPLATE.replace('{content}', content);
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
  const url = `/api/receipts/by-fiscal-data?${params.toString()}`;

  fetch(url)
    .then(res => {
      if (!res.ok) {
        return res.text().then(text => {
          throw new Error(text || `HTTP error! status: ${res.status}`);
        });
      }
      return res.json();
    })
    .then(data => {
      const jsonStr = JSON.stringify(data, null, 2);
      const highlighted = hljs.highlight(jsonStr, { language: 'json' }).value;
      const jsonHtml = createCard(highlighted);

      resultDiv.innerHTML = qrHtml + jsonHtml;

      if (data.success && data.receipt_id) {
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
    const response = await fetch('/api/receipts/count');
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