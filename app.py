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


@app.route('/leitorArtigos')
def leitor_artigos():
    return render_template('leitorArtigos.html') 

if __name__ == "__main__":
    app.run(debug=True)
    
