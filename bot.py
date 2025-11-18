from flask import Flask, request, jsonify
import hmac
import hashlib
import os

app = Flask(__name__)

# Секретный ключ для вебхука (установите в переменных окружения)
WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET', '')

def verify_webhook_signature(data, signature):
    """Проверка подписи вебхука"""
    if not WEBHOOK_SECRET:
        return True  # Пропускаем проверку если секрет не установлен
    
    mac = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        msg=data,
        digestmod=hashlib.sha256
    )
    expected_signature = 'sha256=' + mac.hexdigest()
    return hmac.compare_digest(expected_signature, signature)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Обработчик вебхуков от GitHub"""
    # Проверяем подпись
    signature = request.headers.get('X-Hub-Signature-256', '')
    if not verify_webhook_signature(request.data, signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    event_type = request.headers.get('X-GitHub-Event', '')
    payload = request.json
    
    # Обрабатываем разные события
    if event_type == 'issues' and payload.get('action') == 'opened':
        return handle_new_issue(payload)
    elif event_type == 'pull_request' and payload.get('action') == 'opened':
        return handle_new_pr(payload)
    elif event_type == 'issue_comment' and payload.get('action') == 'created':
        return handle_new_comment(payload)
    
    return jsonify({'status': 'ok'})

def handle_new_issue(payload):
    """Обработка нового issue"""
    issue = payload['issue']
    user = issue['user']['login']
    issue_number = issue['number']
    repo = payload['repository']['full_name']
    
    # Отправляем приветственное сообщение
    message = f"Привет, @{user}! 👋 Спасибо за создание issue #{issue_number}! Я скоро его рассмотрю."
    
    # Здесь должен быть код для отправки комментария через GitHub API
    # Для этого нужен токен доступа
    
    print(f"Нужно ответить на issue #{issue_number}: {message}")
    return jsonify({'status': 'issue handled'})

def handle_new_pr(payload):
    """Обработка нового pull request"""
    pr = payload['pull_request']
    user = pr['user']['login']
    pr_number = pr['number']
    
    message = f"Привет, @{user}! 🎉 Спасибо за ваш pull request #{pr_number}! Я проверю его в ближайшее время."
    
    print(f"Нужно ответить на PR #{pr_number}: {message}")
    return jsonify({'status': 'pr handled'})

def handle_new_comment(payload):
    """Обработка нового комментария"""
    comment = payload['comment']
    user = comment['user']['login']
    
    # Проверяем, упомянули ли бота
    if '@github-bot' in comment['body']:
        message = f"Привет, @{user}! 🤖 Я бот, готовый помочь! Чем могу быть полезен?"
        
        print(f"Бота упомянули: {message}")
    
    return jsonify({'status': 'comment handled'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
