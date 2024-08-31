from flask import Flask, request, jsonify, render_template_string
import requests
import plotly.graph_objects as go
import plotly.io as pio

# Chave de API do Mapbox
CHAVE_API_MAPBOX = 'pk.eyJ1IjoiYm9zY29ib3NjbyIsImEiOiJjbTBoaTAxZmowYmUwMnFvOGxmNTJkenNlIn0.WsButZ1L2Xbhg_8edUyzkg'

app = Flask(__name__)

def obter_localizacao_por_ip(ip):
    url = f'https://ip-api.com/json/{ip}'
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()  # Verifica se a resposta é 200
        dados = resposta.json()
        if dados['status'] == 'success':
            return {
                'longitude': dados['lon'],
                'latitude': dados['lat'],
                'nome_local': f"{dados['city']}, {dados['regionName']}, {dados['country']}"
            }
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
    return None

def criar_mapa(localizacao, estilo='carto-darkmatter'):
    figura = go.Figure(go.Scattermapbox(
        lat=[localizacao['latitude']],
        lon=[localizacao['longitude']],
        mode='markers+text',
        marker=dict(size=14),
        text=[localizacao['nome_local']],
        textposition='top right'
    ))

    figura.update_layout(
        mapbox=dict(
            accesstoken=CHAVE_API_MAPBOX,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=localizacao['latitude'],
                lon=localizacao['longitude']
            ),
            pitch=0,
            zoom=10,
            style=estilo
        ),
        showlegend=False,
        title_text='Localização do IP'
    )

    figura.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return pio.to_html(figura, full_html=False)

@app.route('/mapa', methods=['GET'])
def mapa():
    ip = request.args.get('ip')
    if not ip:
        return jsonify({'error': 'Parâmetro "ip" é necessário.'}), 400

    localizacao = obter_localizacao_por_ip(ip)
    if localizacao:
        mapa_html = criar_mapa(localizacao)
        return render_template_string(mapa_html)
    else:
        return jsonify({'error': 'Não foi possível obter a localização.'}), 404

if __name__ == "__main__":
    app.run(debug=True)
