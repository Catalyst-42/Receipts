hljs.highlightAll();

const reader = document.getElementById('reader');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const resultDiv = document.getElementById('result');

let scanner = null;

// HTML Templates
const CARD_TEMPLATE = '<div class="card bg-dark text-white mt-2"><div class="card-body p-2"><pre class="mb-0"><code class="text-white small">{content}</code></pre></div></div>';
const LOADING_TEMPLATE = '<div class="text-secondary mt-2"><div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 100%"></div></div></div>';
const ERROR_TEMPLATE = '<div class="text-danger mt-2">Error: {message}</div>';
const VALIDATION_ERROR_TEMPLATE = '<div class="text-danger mt-2">Validation error: {message}</div>';

// Helper function to create HTML with content
function createCard(content) {
  return CARD_TEMPLATE.replace('{content}', content);
}

function createError(message, isValidation = false) {
  const template = isValidation ? VALIDATION_ERROR_TEMPLATE : ERROR_TEMPLATE;
  return template.replace('{message}', message);
}

function parseFiscalQR(decodedText) {
  const cleanText = decodedText.trim();
  const pairs = cleanText.split('&');

  const params = {};

  for (const pair of pairs) {
    const [key, value] = pair.split('=');
    if (key && value) {
      params[key] = value;
    }
  }

  const requiredFields = ['t', 's', 'fn', 'i', 'fp', 'n'];
  for (const field of requiredFields) {
    if (!params.hasOwnProperty(field)) {
      throw new Error(`Missing required field: ${field}`);
    }
  }

  return params;
}

function onScanSuccess(decodedText) {
  try {
    const fiscalData = parseFiscalQR(decodedText);

    // Show original QR code with syntax highlighting
    const qrHighlighted = hljs.highlight(decodedText, { language: 'plaintext' }).value;
    const qrHtml = createCard(qrHighlighted);
    const loadingHtml = LOADING_TEMPLATE;
    resultDiv.innerHTML = qrHtml + loadingHtml;

    // Send already parsed data to server
    fetch('/api/scan-qr', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ qr_code: decodedText, fiscal_data: fiscalData })
    })
      .then(res => res.json())
      .then(data => {
        const jsonStr = JSON.stringify(data, null, 2);
        const highlighted = hljs.highlight(jsonStr, { language: 'json' }).value;
        const jsonHtml = createCard(highlighted);

        // Add parsed data before server result
        const fiscalJsonStr = JSON.stringify(fiscalData, null, 2);
        const fiscalHighlighted = hljs.highlight(fiscalJsonStr, { language: 'json' }).value;
        const parsedDataHtml = createCard(fiscalHighlighted);

        resultDiv.innerHTML = qrHtml + parsedDataHtml + jsonHtml;
      })
      .catch(err => {
        resultDiv.innerHTML = qrHtml + createError(err.message);
      });
    stopScanner();
  } catch (err) {
    // Show validation error
    const errorHtml = createCard(decodedText);
    resultDiv.innerHTML = errorHtml + createError(err.message, true);
    stopScanner();
  }
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

startBtn.addEventListener('click', startScanner);
stopBtn.addEventListener('click', stopScanner);
window.addEventListener('beforeunload', stopScanner);
