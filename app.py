from flask import Flask, render_template, request, url_for
from converter import gerar_qrcode
from io import BytesIO
import base64
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'imagem' not in request.files:
            return 'Nenhum arquivo enviado.'
        arquivo = request.files['imagem']
        if arquivo.filename == '':
            return 'Arquivo inválido.'
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome_seguro)
        arquivo.save(caminho)
        url_imagem = url_for('static', filename=f'uploads/{nome_seguro}', _external=True)
        qr_img = gerar_qrcode(url_imagem)
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        qr_link = f"data:image/png;base64,{qr_base64}"
        return render_template('resultado.html', imagem_original=url_imagem, qrcode=qr_link)
    return '''
<form method="POST" enctype="multipart/form-data" style="max-width: 400px; margin: 0 auto;">
    <div style="margin-bottom: 1rem;">
        <label for="imagem" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">
            Escolha uma imagem para converter:
        </label>
        <input type="file" name="imagem" id="imagem" 
               accept="image/png, image/jpeg, image/gif, image/webp" 
               style="width: 100%; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px;"
               required>
        <p style="font-size: 0.875rem; color: #666; margin-top: 0.25rem;">
            Tamanho máximo sugerido: 5MB
        </p>
    </div>
    <button type="submit" 
            style="background-color: #4CAF50; color: white; padding: 0.75rem 1.5rem; 
                   border: none; border-radius: 4px; cursor: pointer; font-weight: 600;">
        Converter Imagem
    </button>
</form>
'''

if __name__ == '__main__':
    app.run(debug=True)