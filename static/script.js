hljs.highlightAll();

const reader = document.getElementById('reader');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const resultDiv = document.getElementById('result');

let scanner = null;

function onScanSuccess(decodedText) {
  const qrHtml = `<div class="card bg-dark text-white mt-2"><div class="card-body p-2"><pre class="mb-0"><code class="text-white">${decodedText}</code></pre></div></div>`;
  const loadingHtml = `<div class="text-secondary mt-2"><span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Загрузка данных...</div>`;
  resultDiv.innerHTML = qrHtml + loadingHtml;

  fetch('/api/scan-qr', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ qr_code: decodedText })
  })
    .then(res => res.json())
    .then(data => {
      const jsonStr = JSON.stringify(data, null, 2);
      const highlighted = hljs.highlight(jsonStr, { language: 'json' }).value;
      const jsonHtml = `<div class="card bg-dark text-white mt-2"><div class="card-body p-2"><pre class="mb-0"><code class="text-white small">${highlighted}</code></pre></div></div>`;
      resultDiv.innerHTML = qrHtml + jsonHtml;
    })
    .catch(err => {
      resultDiv.innerHTML = qrHtml + `<div class="text-danger mt-2">Ошибка: ${err.message}</div>`;
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
      (err) => {}
    );
    startBtn.style.display = 'none';
    stopBtn.style.display = 'inline-block';
    resultDiv.innerHTML = '<div class="text-secondary">Сканирование…</div>';
  } catch (err) {
    resultDiv.innerHTML = `<div class="text-danger">Ошибка: ${err.message || err.toString()}</div>`;
    console.error(err);
  }
}

function stopScanner() {
  if (scanner) {
    scanner.stop()
      .then(() => scanner.clear())
      .catch(console.error);
    scanner = null;
  }
  startBtn.style.display = 'inline-block';
  stopBtn.style.display = 'none';
}

startBtn.addEventListener('click', startScanner);
stopBtn.addEventListener('click', stopScanner);
window.addEventListener('beforeunload', stopScanner);