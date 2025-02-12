from flask import Flask, request, render_template, session, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = 'chave-secreta'

# Dicionário de usuários simulando um banco de dados
USUARIOS = {
    'admin': 'senha123',
    'user1': 'minhasenha',
    'user2': 'outrasenha'
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Se o usuário já estiver logado, redireciona para o dashboard
    if 'username' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Verifica se o usuário existe e se a senha está correta
        if username in USUARIOS and USUARIOS[username] == password:
            session['username'] = username  # Salva o usuário na sessão

            # Cria um cookie para lembrar o usuário
            resposta = make_response(redirect(url_for('dashboard')))
            resposta.set_cookie('username', username, max_age=60*60*24)  # Cookie válido por 1 dia
            return resposta
        else:
            return render_template('login.html', erro='Usuário ou senha inválidos.')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Verifica se o usuário está na sessão
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))  # Redireciona para o login se não estiver logado
    return render_template('dashboard.html', username=username)

@app.route('/logout')
def logout():
    # Remove o usuário da sessão
    session.pop('username', None)

    # Remove o cookie
    resposta = make_response(render_template('logout.html'))
    resposta.set_cookie('username', '', max_age=0)  # Excluir o cookie
    return resposta

if __name__ == '__main__':
    app.run(debug=True)
