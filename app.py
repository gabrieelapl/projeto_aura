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
    """
    Busca o primeiro artigo disponível na tabela 'artigos' e passa
    'resumo' e 'palavras_chave' para o template.
    Não altera o design do template.
    """
    try:
        # Buscar o primeiro artigo (ou ajuste WHERE/ORDER conforme precisar)
        cursor.execute("SELECT id, titulo, resumo, palavras_chave FROM artigos ORDER BY id ASC LIMIT 1")
        artigo = cursor.fetchone()
    except Exception as e:
        # Em caso de erro no DB, mantém valores padrão (para não quebrar o layout)
        artigo = None
        print("Erro ao buscar artigo:", e)

    if artigo:
        # Se cursor retorna dicionário:
        try:
            resumo = artigo.get("resumo", "")
            palavras_chave_raw = artigo.get("palavras_chave", "")
        except Exception:
            # se for tupla (cursor padrão), adaptar índices:
            resumo = artigo[2] if len(artigo) > 2 else ""
            palavras_chave_raw = artigo[3] if len(artigo) > 3 else ""
    else:
        # valores padrão (não altera design)
        resumo = "Aqui vai o resumo gerado automaticamente."
        palavras_chave_raw = "PLN,Revisão Sistemática,Educação,ODS"

    # transformando em lista para facilitar o template (se o template espera spans, isso ajuda)
    palavras_chave = [kw.strip() for kw in (palavras_chave_raw or "").split(",") if kw.strip()]

    # Passa as variáveis para o template sem mudar nenhuma marcação HTML
    return render_template(
        'geraresumo.html',
        resumo=resumo,
        palavras_chave=palavras_chave
    )


    # Rota para página de áudio
@app.route("/audio", methods=["GET"])
def audio():
    # PDF e áudio podem ser passados via sessão ou valores padrão
    pdf_url = session.get("uploaded_pdf", "/static/pdf/artigocient.pdf")
    audio_url = session.get("audio_url", "/static/audio/exemplo.mp3")  # exemplo de áudio
    return render_template("audio.html", pdf_url=pdf_url, audio_url=audio_url)

#selecionarresumo
@app.route('/selecionar', methods=['GET', 'POST'])
def selecionar_resumo():
    try:
        cursor.execute("""
            SELECT sr.resumo, sr.palavras_chave 
            FROM selecionar_resumo sr
            ORDER BY sr.id ASC
            LIMIT 1
        """)
        resultado = cursor.fetchone()
    except Exception as e:
        print("Erro ao buscar resumo selecionável:", e)
        resultado = None

    if resultado:
        try:
            resumo = resultado.get("resumo", "")
            palavras_chave_raw = resultado.get("palavras_chave", "")
        except Exception:
            resumo = resultado[0] if len(resultado) > 0 else ""
            palavras_chave_raw = resultado[1] if len(resultado) > 1 else ""
    else:
        resumo = "Resumo padrão de exemplo."
        palavras_chave_raw = "Exemplo,Resumo,PLN"

    palavras_chave = [kw.strip() for kw in (palavras_chave_raw or "").split(",") if kw.strip()]

    return render_template('selecionar.html', resumo=resumo, palavras_chave=palavras_chave)


# Rota Perguntas
@app.route("/perguntas", methods=["GET", "POST"])
def perguntas():
    if request.method == "POST":
        respostas = request.form.getlist("resposta")  # lista de respostas do usuário
        session["respostas_usuario"] = respostas
        return redirect(url_for("index"))

    # Pega todas as perguntas do artigo 1
    cursor.execute("SELECT * FROM perguntas WHERE artigo_id=%s ORDER BY id ASC", (1,))
    perguntas_db = cursor.fetchall()

    perguntas_formatadas = []
    for p in perguntas_db:
        try:
            # cursor retorna dict
            perguntas_formatadas.append({
                "id": p["id"],
                "pergunta": p["pergunta"],
                "alternativas": {
                    "A": p["alternativa_a"],
                    "B": p["alternativa_b"],
                    "C": p["alternativa_c"],
                    "D": p["alternativa_d"]
                },
                "resposta_correta": p["resposta_correta"]
            })
        except Exception:
            # cursor retorna tupla
            perguntas_formatadas.append({
                "id": p[0],
                "pergunta": p[2],
                "alternativas": {
                    "A": p[3],
                    "B": p[4],
                    "C": p[5],
                    "D": p[6]
                },
                "resposta_correta": p[7]
            })

    return render_template("perguntas.html", perguntas=perguntas_formatadas)


#classificar
@app.route("/classificar", methods=["GET", "POST"])
def classificar():
    # Buscar artigo (opcional)
    cursor.execute("SELECT titulo, resumo FROM artigos ORDER BY id ASC LIMIT 1")
    artigo = cursor.fetchone()

    # Buscar tópicos principais
    cursor.execute("SELECT topico FROM topicos_principais WHERE artigo_id=%s", (1,))
    resultado = cursor.fetchall()
    topicos_principais = [r["topico"] if isinstance(r, dict) else r[0] for r in resultado]

    categorias = [
        {"nome": "Aprendizado de máquina", "percent": 60},
        {"nome": "Processamento de Linguagem Natural", "percent": 50},
        {"nome": "Inteligência artificial", "percent": 40},
        {"nome": "Linguística Computacional", "percent": 30},
    ]

    return render_template(
        "classificar.html",
        pdf_url="/static/pdf/artigocient.pdf",
        pdf_tamanho="0,33 MB",
        categorias=categorias,
        topicos_principais=topicos_principais
    )


#citacoes
@app.route("/citacoes", methods=["GET", "POST"])
def citacoes():
    try:
        cursor.execute("SELECT titulo, autores, citado FROM citacoes WHERE artigo_id=%s ORDER BY id ASC", (1,))
        referencias_db = cursor.fetchall()
        referencias = [
            {
                "titulo": r["titulo"] if isinstance(r, dict) else r[0],
                "autores": r["autores"] if isinstance(r, dict) else r[1],
                "citado": r["citado"] if isinstance(r, dict) else r[2]
            }
            for r in referencias_db
        ]
        total_citacoes = 10  # valor fixo
    except Exception as e:
        print("Erro ao buscar citações:", e)
        referencias = []
        total_citacoes = 0

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
from datetime import datetime

@app.route("/perfil")
def perfil():
    # Busca sempre o primeiro usuário da tabela, incluindo membro_desde
    try:
        cursor.execute("SELECT nome, email, bio, membro_desde FROM usuarios ORDER BY id ASC LIMIT 1")
        usuario = cursor.fetchone()
    except Exception as e:
        print("Erro ao buscar usuário:", e)
        usuario = None

    # Se não achar usuário, usa valores padrão
    if not usuario:
        usuario = {
            "nome": "Usuário padrão",
            "email": "email@exemplo.com",
            "bio": "Bio não definida",
            "membro_desde": "—"
        }
    else:
        # Se o cursor retorna dicionário (dict-like)
        if isinstance(usuario, dict):
            md = usuario.get("membro_desde")
        else:
            # cursor retorna tupla -> índice 3 é membro_desde conforme SELECT
            md = usuario[3] if len(usuario) > 3 else None

        # Normalizar membro_desde para string legível
        if md is None:
            membro_str = "—"
        else:
            # Se já for string (alguns drivers retornam str), tentamos parsear, senão formatamos se for datetime
            if isinstance(md, str):
                # tenta converter "YYYY-MM-DD HH:MM:SS" para datetime, caso falhe mantém a string
                try:
                    dt = datetime.strptime(md.split(".")[0], "%Y-%m-%d %H:%M:%S")
                    membro_str = dt.strftime("%d/%m/%Y")  # ex: 09/03/2025
                except Exception:
                    membro_str = md
            elif isinstance(md, datetime):
                membro_str = md.strftime("%d/%m/%Y")
            else:
                # fallback
                membro_str = str(md)

        # Recria objeto usuario no formato dict que o template espera
        if isinstance(usuario, dict):
            usuario["membro_desde"] = membro_str
        else:
            # transform tupla -> dict (nome, email, bio, membro_desde)
            usuario = {
                "nome": usuario[0],
                "email": usuario[1],
                "bio": usuario[2],
                "membro_desde": membro_str
            }

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
    app.run(debug=True, use_reloader=True)

