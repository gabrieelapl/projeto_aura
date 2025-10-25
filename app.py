from flask import Flask, render_template, request, redirect, url_for, session
from db import cursor, db  # supondo que db.py exporte a conexão e o cursor
app = Flask(__name__)
app.secret_key = "aura"  # Pode ser qualquer string segura


# Rota da landing page
@app.route("/")
def index():
    return render_template("index.html")

# Rota de login
@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        cursor.execute(
            "SELECT * FROM usuarios WHERE email=%s AND senha=%s",
            (email, senha)
        )
        usuario = cursor.fetchone()

        if usuario:
            return redirect(url_for("index"))
        else:
            erro = "Usuário ou senha inválidos"

    return render_template("login.html", erro=erro)

# Rota de cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    erro = None
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        try:
            # Verifica se o email já existe
            cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
            usuario = cursor.fetchone()

            if usuario:
                erro = "Esse usuário já existe"  # mesma msg do login
            else:
                cursor.execute(
                    "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                    (nome, email, senha)
                )
                db.commit()
                return redirect(url_for("index"))
        except Exception as e:
            erro = "Erro ao cadastrar usuário: " + str(e)

    return render_template("cadastro.html", erro=erro)

# Rota Gerar Resumo
@app.route("/geraresumo", methods=["GET", "POST"])
def geraresumo():
    return render_template('geraresumo.html')
    # Aqui você pega os dados armazenados na sessão (ou usa valores padrão)
    pdf_url = session.get("uploaded_pdf", "/static/exemplo.pdf")  # PDF padrão
    resumo = session.get("resumo", "Aqui vai o resumo gerado automaticamente.")
    pontos_chave = session.get("pontos_chave", [
        "Ponto chave 1",
        "Ponto chave 2",
        "Ponto chave 3"
    ])
    
    # Renderiza o template passando os dados
    return render_template("geraresumo.html", pdf_url=pdf_url, resumo=resumo, pontos_chave=pontos_chave)

    # Rota para página de áudio
@app.route("/audio", methods=["GET"])
def audio():
    # PDF e áudio podem ser passados via sessão ou valores padrão
    pdf_url = session.get("uploaded_pdf", "/static/pdf/artigocient.pdf")
    audio_url = session.get("audio_url", "/static/audio/exemplo.mp3")  # exemplo de áudio
    return render_template("audio.html", pdf_url=pdf_url, audio_url=audio_url)

@app.route('/selecionar', methods=['GET', 'POST'])
def selecionar_resumo():
    # Pegando valores da sessão ou definindo valores padrão
    pdf_url = session.get("uploaded_pdf", "/static/pdf/artigocient.pdf")
    resumo = session.get("resumo", "Aqui vai o resumo gerado automaticamente.")
    pontos_chave = session.get("pontos_chave", ["Ponto chave 1", "Ponto chave 2", "Ponto chave 3"])

    if request.method == 'POST':
        # processar algo
        return "Resumo processado!"

    return render_template('selecionar.html', pdf_url=pdf_url, resumo=resumo, pontos_chave=pontos_chave)

# Rota Perguntas
@app.route("/perguntas", methods=["GET", "POST"])
def perguntas():
    if request.method == "POST":
        # Aqui você pode processar as respostas das perguntas, salvar no banco, etc.
        resposta_usuario = request.form.get("resposta")  
        # Exemplo: salvar na sessão
        session["resposta"] = resposta_usuario
        return redirect(url_for("index"))  # depois redireciona para a home ou outra página
    
    # GET -> apenas exibe a página
    return render_template("perguntas.html")

@app.route("/classificar", methods=["GET", "POST"])
def classificar():
    # Dados de exemplo; você pode substituir por valores reais
    pdf_url = session.get("uploaded_pdf", "/static/pdf/artigocient.pdf")
    pdf_nome = "Artigo-científico.pdf"
    pdf_tamanho = "0,33 MB"
    
    categorias = [
        {"nome": "Aprendizado de máquina", "percent": 60},
        {"nome": "Processamento de Linguagem Natural", "percent": 50},
        {"nome": "Inteligência artificial", "percent": 40},
        {"nome": "Linguística Computacional", "percent": 30},
    ]
    
    topicos_principais = [
        "Introduz um mecanismo de atenção modificado",
        "Demonstra uma melhoria de 15% em relação aos métodos SOTA",
        "Fornece um procedimento de treinamento mais eficiente",
        "Apresenta desempenho robusto em vários idiomas",
        "Inclui estudos extensivos de ablação"
    ]
    
    return render_template(
        "classificar.html",
        pdf_url=pdf_url,
        pdf_nome=pdf_nome,
        pdf_tamanho=pdf_tamanho,
        categorias=categorias,
        topicos_principais=topicos_principais
    )

@app.route("/citacoes", methods=["GET", "POST"])
def citacoes():
    # Exemplo de dados de citações
    total_citacoes = 10
    referencias = [
        
        {"titulo": "Classificação de Imagens com Redes Neurais Convolucionais Profundas", "autores": "Krizhevsky, Sutskever e Hinton (2012)", "citado": 4},
        {"titulo": "BERT: Pré-treinamento de Representações Profundas de Linguagem", "autores": "Devlin et al. (2018)", "citado": 3},
        {"titulo": "Redes Residuais Profundas para Reconhecimento de Imagens", "autores": "He et al. (2016)", "citado": 2},
        {"titulo": "Transformers: Uma Abordagem Geral para Modelagem de Sequência", "autores": "Wolf et al. (2020)", "citado": 2},
        {"titulo": "GPT-3: Modelos de Linguagem São Aprendizes de Poucos Exemplos", "autores": "Brown et al. (2020)", "citado": 1},
        {"titulo": "T5: Explorar a Transferência de Texto para Texto com um Modelo Unificado", "autores": "Raffel et al. (2020)", "citado": 1},
        {"titulo": "XLNet: Superando o BERT com Modelagem Autoregressiva Generalizada", "autores": "Yang et al. (2019)", "citado": 1},
        {"titulo": "Word2Vec: Eficiência de Vetores de Palavras de Grande Dimensão", "autores": "Mikolov et al. (2013)", "citado": 1},
        {"titulo": "Atenção é Tudo que Você Precisa", "autores": "Vaswani et al. (2017)", "citado": 5},
        {"titulo": "Classificação de Imagens com Redes Neurais Convolucionais Profundas", "autores": "Krizhevsky, Sutskever e Hinton (2012)", "citado": 4},
    ]
    
    return render_template("citacoes.html", total_citacoes=total_citacoes, referencias=referencias)

# Leitor de artigos - GERAR RESUMO
@app.route('/leitorArtigos-gerarResumo')
def leitor_artigos():
    return render_template('leitorArtigos-gerarResumo.html') 

# Leitor de artigos - ÁUDIO
@app.route('/leitorArtigos-audio')
def leitor_artigos_audio():
    return render_template('leitorArtigos-audio.html') 

# Leitor de artigos - SELECIONAR
@app.route('/leitorArtigos-selecionar')
def leitor_artigos_selecionar():
    return render_template('leitorArtigos-selecionar.html') 

# Leitor de artigos - PERGUNTAS
@app.route('/leitorArtigos-perguntas')
def leitor_artigos_perguntas():
    return render_template('leitorArtigos-perguntas.html')

# Leitor de artigos - CLASSIFICAR
@app.route('/leitorArtigos-classificar')
def leitor_artigos_classificar():
    return render_template('leitorArtigos-classificar.html')

# Leitor de artigos - CITAÇÕES
@app.route('/leitorArtigos-citacoes')
def leitor_artigos_citacoes():
    return render_template('leitorArtigos-citacoes.html')

#perfil
@app.route("/perfil")
def perfil():
    # Busca sempre o primeiro usuário da tabela
    cursor.execute("SELECT nome, email, bio FROM usuarios ORDER BY id ASC LIMIT 1")
    usuario = cursor.fetchone()

    if not usuario:
        usuario = {"nome": "Usuário padrão", "email": "email@exemplo.com", "bio": "Bio não definida"}

    return render_template("perfil.html", usuario=usuario)



#/editarperfil
@app.route("/editarperfil", methods=["GET", "POST"])
def editarperfil():
    # Pega o primeiro usuário válido
    cursor.execute("SELECT id, nome, bio FROM usuarios ORDER BY id ASC LIMIT 1")
    usuario = cursor.fetchone()

    if not usuario:
        return "Nenhum usuário encontrado no banco."

    # Dependendo do cursor:
    # Se dictionary=True:
    user_id = usuario["id"]
    # Se não, use: user_id = usuario[0]

    if request.method == "POST":
        novo_nome = request.form["nome"]
        nova_bio = request.form["bio"]

        cursor.execute(
            "UPDATE usuarios SET nome=%s, bio=%s WHERE id=%s",
            (novo_nome, nova_bio, user_id)
        )
        db.commit()

        return redirect(url_for("perfil"))

    return render_template("editarperfil.html", usuario=usuario)

# Rota alterar senha
@app.route("/alterarsenha", methods=["GET", "POST"])
def alterarsenha():
    # Pega o usuário logado na sessão ou o primeiro da tabela
    user_id = session.get("user_id")
    if not user_id:
        cursor.execute("SELECT id FROM usuarios ORDER BY id ASC LIMIT 1")
        usuario = cursor.fetchone()
        if not usuario:
            return render_template("alterarsenha.html", mensagem="Nenhum usuário encontrado no banco.")
        # cursor retorna tupla ou dicionário
        user_id = usuario[0] if isinstance(usuario, tuple) else usuario["id"]

    if request.method == "POST":
        confirmar_senha = request.form.get("confirmar_senha")  # apenas usamos esse campo

        try:
            cursor.execute("UPDATE usuarios SET senha = %s WHERE id = %s", (confirmar_senha, user_id))
            db.commit()
            return render_template("alterarsenha.html", mensagem="Senha alterada com sucesso!")
        except Exception as e:
            db.rollback()
            return render_template("alterarsenha.html", mensagem=f"Erro ao atualizar senha: {e}")

    # GET -> mostra formulário
    return render_template("alterarsenha.html")




#/excluirconta
@app.route("/excluirconta", methods=["POST"])
def excluirconta():
    try:
        # Deleta o usuário com id = 1
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (1,))
        db.commit()
        # Limpa sessão apenas se existir
        session.clear()
        mensagem = "Conta excluída com sucesso!"
    except Exception as e:
        db.rollback()
        mensagem = f"Erro ao excluir conta: {e}"

    # Redireciona para a home ou mostra mensagem
    return render_template("index.html", mensagem=mensagem)


@app.route("/excluirhistorico", methods=["GET", "POST"])
def excluirhistorico():
    # Lógica para apagar histórico do usuário
    # db.execute("DELETE FROM historico WHERE usuario_id = %s", (session['user_id'],))
    # db.commit()
    return redirect(url_for("perfil"))  # volta para perfil

if __name__ == "__main__":
    app.run(debug=True)
    
