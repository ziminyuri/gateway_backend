qr_code_template = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body>
<canvas id="qr"></canvas>

<script src="https://cdnjs.cloudflare.com/ajax/libs/qrious/4.0.2/qrious.min.js"></script>
<script>
  (function () {
    var qr = new QRious({
      element: document.getElementById('qr'),
      value: '%s'
    });
  })();
</script>
<p>Просканируйте QR-код с помощью TOTP-приложения и введите код</p>
</body>
</html>
'''