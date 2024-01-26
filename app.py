from flask import Flask, render_template, request, send_file
import requests
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Rota inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar a remoção do fundo
@app.route('/remove_background', methods=['POST'])
def remove_background():
    api_key = 'hwwjbUKqK12eenLDvXENos5t '
    image_source = request.form['image_source']

    if image_source == 'url':
        image_url = request.form['image_url']
        image_response = requests.get(image_url)

        if image_response.status_code == requests.codes.ok:
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': image_response.content},
                data={'size': 'auto'},
                headers={'X-Api-Key': api_key},
            )

            if response.status_code == requests.codes.ok:
                img = Image.open(BytesIO(response.content))
                img.save('static/imagem_sem_fundo.png')  # Salva a imagem no diretório 'static'
                return render_template('result.html', success=True)
            else:
                return render_template('result.html', success=False, error=f'Erro ao remover o fundo: {response.status_code}, {response.text}')
        else:
            return render_template('result.html', success=False, error=f'Erro ao baixar a imagem: {image_response.status_code}, {image_response.text}')
    elif image_source == 'upload':
        if 'image_upload' not in request.files:
            return render_template('result.html', success=False, error='Nenhuma imagem foi enviada.')

        image_upload = request.files['image_upload']

        if image_upload.filename == '':
            return render_template('result.html', success=False, error='Nenhum arquivo selecionado.')

        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': image_upload.read()},
            data={'size': 'auto'},
            headers={'X-Api-Key': api_key},
        )

        if response.status_code == requests.codes.ok:
            img = Image.open(BytesIO(response.content))
            img.save('static/imagem_sem_fundo.png')  # Salva a imagem no diretório 'static'
            return render_template('result.html', success=True)
        else:
            return render_template('result.html', success=False, error=f'Erro ao remover o fundo: {response.status_code}, {response.text}')

# Rota para download da imagem
@app.route('/download_image')
def download_image():
    return send_file('static/imagem_sem_fundo.png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
