from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)  # Permitir requisições do frontend

# Configurações da API (exemplo genérico)
API_KEY = os.getenv('AI_API_KEY')
API_URL = os.getenv('AI_API_URL', 'https://api.exemplo-ia.com/v1/chat')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Obter dados do frontend
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Mensagem não fornecida'}), 400
        
        # Preparar requisição para a API da IA
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'messages': [
                {
                    'role': 'user',
                    'content': user_message
                }
            ],
            'max_tokens': 150,
            'temperature': 0.7
        }
        
        # Fazer requisição para a API da IA
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            ai_response = response.json()
            # Extrair a resposta da IA (formato pode variar)
            bot_message = ai_response.get('choices', [{}])[0].get('message', {}).get('content', 'Desculpe, não consegui processar sua mensagem.')
            
            return jsonify({
                'success': True,
                'response': bot_message
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Erro na comunicação com a IA'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
