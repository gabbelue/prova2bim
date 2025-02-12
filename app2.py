from flask import Flask, request, render_template, session, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = 'chave-secreta'

# Lista para armazenar usuários cadastrados
usuarios_registrados = []

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        username = request.form['username']
        password = request.form['password']
        funcao = request.form.get('funcao', 'usuário')  # Padrão: usuário
        
        # Verificar se o usuário já existe
        for usuario in usuarios_registrados:
            if usuario['username'] == username:
                return render_template('cadastro.html', erro='Usuário já cadastrado.')

        # Adicionar novo usuário à lista
        usuarios_registrados.append({'nome': nome, 'username': username, 'password': password, 'funcao': funcao})
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validar credenciais
        for usuario in usuarios_registrados:
            if usuario['username'] == username and usuario['password'] == password:
                session['username'] = username
                session['funcao'] = usuario['funcao']  # Armazena a função do usuário na sessão

                resposta = make_response(redirect(url_for('dashboard')))
                resposta.set_cookie('username', username, max_age=60*60*24)
                return resposta

        return render_template('login.html', erro='Usuário ou senha inválidos.')

    if 'username' in session:
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    return render_template('dashboard.html', username=username)

@app.route('/usuarios')
def listar_usuarios():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Filtrar usuários da mesma função (apenas um tipo de usuário vê sua categoria)
    funcao_usuario = session.get('funcao', 'usuário')
    usuarios_filtrados = [u for u in usuarios_registrados if u['funcao'] == funcao_usuario]

    return render_template('usuarios.html', usuarios=usuarios_filtrados)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('funcao', None)  # Remove a função também

    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie('username', '', max_age=0)
    return resposta

if __name__ == '__main__':
    app.run(debug=True)
