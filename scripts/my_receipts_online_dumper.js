(async function downloadAllQRCodes() {
  // Configuration
  const DELAY_AFTER_CLICK = 1200;
  const DELAY_FOR_QR_RENDER = 600;
  const DELAY_BETWEEN_ITEMS = 800;
  const MAX_ITEMS = 0; // Dump all
  const LOAD_MORE_DELAY = 2000;
  const LOAD_MORE_SELECTOR = 'button.sc-ksdxAp.bCiSNZ.btn-code';

  // Selectors
  const ROW_SELECTOR = '.sc-hkgtOd.hGksJB div[role="row"]';
  const RECEIPT_CONTAINER = '#receipt-container';
  const QR_SVG_SELECTOR = '#receipt-container div.sc-fWCJfs.kjawyH svg[shape-rendering="crispEdges"]';
  const CLOSE_BUTTON_SELECTOR = '#close-icon';
  const OVERLAY_SELECTOR = '[data-reach-dialog-overlay]';

  const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

  async function loadAllReceipts() {
    let button = document.querySelector(LOAD_MORE_SELECTOR);
    let previousCount = 0;
    while (button) {
      button.click();
      await sleep(LOAD_MORE_DELAY);
      button = document.querySelector(LOAD_MORE_SELECTOR);
      const currentRows = document.querySelectorAll(ROW_SELECTOR);
      const dataRows = Array.from(currentRows).filter(row => row.querySelector('img[alt="icon"]'));
      if (dataRows.length !== previousCount) {
        console.log('Expand selection: ' + dataRows.length);
        previousCount = dataRows.length;
      }
    }
  }

  await loadAllReceipts();

  // Get all data rows
  const allRows = document.querySelectorAll(ROW_SELECTOR);
  const rows = Array.from(allRows).filter(row => row.querySelector('img[alt="icon"]'));

  if (!rows.length) {
    console.error('No data rows found. Receipt selector.');
    return;
  }

  const total = MAX_ITEMS > 0 ? Math.min(MAX_ITEMS, rows.length) : rows.length;
  console.log('Receipts to process: ' + total);

  function downloadPNG(svgElement, index) {
    return new Promise((resolve) => {
      const clone = svgElement.cloneNode(true);
      if (!clone.getAttribute('xmlns')) {
        clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
      }
      const svgString = clone.outerHTML;
      const base64 = btoa(unescape(encodeURIComponent(svgString)));
      const dataUri = 'data:image/svg+xml;base64,' + base64;

      const img = new Image();
      img.onload = function () {
        const scale = 4;
        const canvas = document.createElement('canvas');
        canvas.width = 128 * scale;
        canvas.height = 128 * scale;
        const ctx = canvas.getContext('2d');
        ctx.imageSmoothingEnabled = true;
        ctx.imageSmoothingQuality = 'high';
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        const pngDataUrl = canvas.toDataURL('image/png');
        const link = document.createElement('a');
        link.href = pngDataUrl;
        link.download = 'qr_receipt_' + String(index + 1).padStart(4, '0') + '.png';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        console.log('Downloaded ' + (index + 1) + '/' + total);
        resolve();
      };
      img.onerror = function () {
        console.warn('Failed to render SVG ' + (index + 1) + '/' + total + ', falling back to SVG download.');
        try {
          const blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
          const url = URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = 'qr_receipt_' + String(index + 1).padStart(4, '0') + '.svg';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          URL.revokeObjectURL(url);
          console.log('Downloaded SVG fallback ' + (index + 1) + '/' + total);
        } catch (err) {
          console.error('Failed to download ' + (index + 1) + '/' + total, err);
        }
        resolve();
      };
      img.src = dataUri;
    });
  }

  for (let i = 0; i < total; i++) {
    const row = rows[i];

    row.click();
    await sleep(DELAY_AFTER_CLICK);

    let receipt = document.querySelector(RECEIPT_CONTAINER);
    let attempts = 0;
    while (!receipt && attempts < 5) {
      await sleep(200);
      receipt = document.querySelector(RECEIPT_CONTAINER);
      attempts++;
    }
    if (!receipt) {
      console.warn('Receipt ' + (i + 1) + '/' + total + ' did not open, skipping.');
      const overlay = document.querySelector(OVERLAY_SELECTOR);
      if (overlay) overlay.click();
      await sleep(DELAY_BETWEEN_ITEMS);
      continue;
    }

    await sleep(DELAY_FOR_QR_RENDER);

    let qrSvg = document.querySelector(QR_SVG_SELECTOR);
    if (!qrSvg) {
      qrSvg = receipt.querySelector('svg[shape-rendering="crispEdges"]');
    }
    if (!qrSvg) {
      qrSvg = receipt.querySelector('svg:last-of-type');
    }

    if (qrSvg) {
      await downloadPNG(qrSvg, i);
    } else {
      console.warn('QR code not found in receipt ' + (i + 1) + '/' + total + ', skipping.');
    }

    const closeBtn = document.querySelector(CLOSE_BUTTON_SELECTOR);
    if (closeBtn) {
      closeBtn.click();
    } else {
      const overlay = document.querySelector(OVERLAY_SELECTOR);
      if (overlay) overlay.click();
    }

    await sleep(DELAY_BETWEEN_ITEMS);
  }

  console.log('All QR codes downloaded.');
})();