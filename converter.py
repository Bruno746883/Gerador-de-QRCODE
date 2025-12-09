import qrcode


def gerar_qrcode(url):
    qr = qrcode.QRCode(version=None, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")