from flask import Flask, jsonify
import json
import requests

app = Flask(__name__)

# Função para formatar o RA do aluno
def formatar_ra(ra_aluno):
    numero_str = str(ra_aluno).replace(".", "").replace(" ", "")
    numero_com_ponto = numero_str[:3] + "." + numero_str[3:]
    return numero_com_ponto

# Função para processar as informações dos professores
def processar_informacoes(info):
    parsed_info = [json.loads(item) for item in info]  # Converter strings JSON em objetos
    informacoes = [
        f"👨🏼‍🏫 INFORMAÇÕES \n"
        f"*Professor:* {item['professor']}\n"
        f"*Curso:* {item['curso']}\n"
        f"*Disciplina:* {item['disciplina']}\n\n"
        f"📍 LOCALIZAÇÃO \n"
        f"*Prédio:* {item['predio'] if item['predio'] else 'Não especificado'}\n"
        f"*Bloco:* {item['bloco'] if item['bloco'] else 'Não especificado'}\n"
        f"*Sala:* {item['sala'] if item['sala'] else 'Não especificado'}\n\n"
        f"⏱ DATA E HORA \n"
        f"*Data:* {item['data']}\n"
        f"*Hora Inicial:* {item['horaInicial']}\n"
        f"*Hora Final:* {item['horaFinal']}\n"
        f"=-=-=-="
        for item in parsed_info
    ]
    return "\n\n".join(informacoes)

# Rota da API para GET, com o RA como parte da URL
@app.route('/api/aula/<string:ra>', methods=['GET'])
def buscar_aula(ra):
    # Processar o RA do aluno (remover espaços/pontos e reformatar)
    ra_formatado = formatar_ra(ra)

    # Realiza a requisição para o servidor externo (hostAula)
    try:
        # Substitua pelo seu endpoint real, caso tenha um servidor externo
        response = requests.get(f'https://hostAula/api/consulta?ra={ra_formatado}')
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code == 200:
            result = response.json()  # Supondo que a resposta seja um JSON
        else:
            return jsonify({'error': 'Falha ao consultar servidor externo'}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Erro ao fazer a requisição externa', 'details': str(e)}), 500

    # Processar as informações recebidas do servidor externo
    informacoes = processar_informacoes(result)

    # Retorna o RA formatado e as informações processadas
    return jsonify({
        'raFormatado': ra_formatado,
        'informacoes': informacoes
    })

if __name__ == '__main__':
    app.run(debug=True)
