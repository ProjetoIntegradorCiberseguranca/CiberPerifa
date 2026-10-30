
import requests
from flask import Flask, send_file, render_template
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from io import BytesIO
from reportlab.lib import colors

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from xml.sax.saxutils import escape

app = Flask(__name__)

URL_CISA = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"


def consultar_cisa():
    resposta = requests.get(URL_CISA, timeout=20)
    resposta.raise_for_status()

    dados = resposta.json()
    return dados["vulnerabilities"]



def desenhar_rodape(pdf, documento):
    pdf.saveState()

    largura, altura = A4

    # Numeração simples no canto superior direito.
    # A capa é contada, mas não exibe o número.
    if documento.page > 1:
        pdf.setFont("Times-Roman", 10)
        pdf.setFillColor(colors.black)
        pdf.drawRightString(
            largura - 2 * cm,
            altura - 2 * cm,
            str(documento.page)
        )

    pdf.restoreState()



def explicar_vulnerabilidade(vulnerabilidade):
    descricao = vulnerabilidade.get(
        "shortDescription", ""
    ).lower()

    # 1. Exposição de informações sensíveis
    if (
        "cleartext storage of sensitive information" in descricao
        or "sensitive user details" in descricao
    ):
        explicacao = (
            "Essa falha pode permitir que informações pessoais ou "
            "outros dados sensíveis sejam descobertos por pessoas "
            "que tenham acesso ao sistema afetado. A descrição da "
            "CISA também informa que essa falha pode ser combinada "
            "com outra vulnerabilidade para possibilitar a execução "
            "remota de código."
        )
        return explicacao

    # 2. Controle de acesso inadequado
    if "improper access control" in descricao:
        return (
            "Essa falha pode permitir que alguém realize operações "
            "sem as restrições de acesso esperadas. Neste caso, "
            "a descrição informa que invasores remotos podem ler "
            "e modificar arquivos que deveriam estar protegidos."
        )

    # 3. Acesso indevido a caminhos de arquivos
    if "path traversal" in descricao or "directory traversal" in descricao:
        explicacao = (
            "Essa falha pode permitir que alguém manipule caminhos "
            "de arquivos para acessar locais que deveriam estar "
            "fora do alcance da operação solicitada."
        )

        if "remote code execution" in descricao:
            explicacao += (
                " A descrição também informa que essa falha pode "
                "possibilitar a execução remota de código."
            )

        return explicacao

    # 4. Injeção de comandos
    if "command injection" in descricao:
        return (
            "Essa falha pode permitir que entradas manipuladas "
            "provoquem a execução de comandos não previstos. "
            "Dependendo das condições do ataque, isso pode permitir "
            "a execução de código no sistema afetado."
        )

    # 5. Indisponibilidade do serviço
    if "denial of service" in descricao:
        return (
            "Essa falha pode comprometer a disponibilidade do "
            "sistema, fazendo com que ele pare de responder ou "
            "fique indisponível para seus usuários."
        )

    # 6. Elevação de privilégios
    if (
        "privilege escalation" in descricao
        or "elevation of privilege" in descricao
    ):
        return (
            "Essa falha pode permitir que alguém obtenha permissões "
            "maiores do que deveria ter, acessando funções ou "
            "recursos restritos."
        )

    # 7. Contorno da autenticação
    if (
        "authentication bypass" in descricao
        or "bypass authentication" in descricao
    ):
        return (
            "Essa falha pode permitir que alguém contorne uma "
            "verificação de identidade e acesse recursos sem "
            "passar pelo mecanismo de autenticação esperado."
        )

    # 8. Injeção de SQL
    if "sql injection" in descricao:
        return (
            "Essa falha pode permitir que entradas manipuladas "
            "alterem consultas ao banco de dados, podendo expor "
            "ou modificar informações conforme as permissões "
            "e condições do sistema."
        )

    # 9. Execução de scripts no navegador
    if (
        "cross-site scripting" in descricao
        or "xss vulnerability" in descricao
    ):
        return (
            "Essa falha pode permitir a execução de scripts "
            "maliciosos no navegador de quem acessa uma página "
            "afetada, podendo comprometer dados ou a interação "
            "com o site."
        )

    # 10. Problemas de memória
    if "buffer overflow" in descricao:
        return (
            "Essa falha ocorre quando um programa manipula dados "
            "além dos limites previstos para uma área de memória. "
            "Isso pode causar erros e, dependendo do caso, "
            "comprometer a segurança do sistema."
        )

    # 11. Execução remota de código, quando não há categoria
    # mais específica reconhecida anteriormente
    if "remote code execution" in descricao:
        return (
            "Essa falha pode permitir que um invasor execute "
            "código no sistema afetado a partir de outro dispositivo. "
            "O impacto depende das condições do ataque e das "
            "permissões disponíveis."
        )

    # 12. Alternativa segura para descrições não reconhecidas
    return (
        "A CISA identificou uma vulnerabilidade neste produto. "
        "O impacto específico depende dos detalhes da falha e "
        "das condições em que ela pode ser explorada. Consulte "
        "a descrição original e a ação recomendada pela CISA "
        "para mais informações."
    )



def gerar_pdf(vulnerabilidades):
    arquivo = BytesIO()

    documento = SimpleDocTemplate(
    arquivo,
    pagesize=A4,
    rightMargin=2 * cm,
    leftMargin=3 * cm,
    topMargin=3 * cm,
    bottomMargin=2 * cm,
    title="Cartilha de Cibersegurança - CiberPerifa",
    author="CiberPerifa"
    )

    estilos = getSampleStyleSheet()

    # Título principal da capa
    titulo = ParagraphStyle(
        "TituloCartilha",
        parent=estilos["Title"],
        fontName="Times-Bold",
        fontSize=16,
        leading=20,
        alignment=1,
        textColor=colors.black,
        spaceAfter=18
    )

    # Subtítulo da capa
    subtitulo = ParagraphStyle(
        "SubtituloCartilha",
        parent=estilos["Normal"],
        fontName="Times-Roman",
        fontSize=12,
        leading=18,
        alignment=1,
        textColor=colors.black,
        spaceAfter=18
    )

    # Títulos das seções
    secao = ParagraphStyle(
        "SecaoCartilha",
        parent=estilos["Heading2"],
        fontName="Times-Bold",
        fontSize=12,
        leading=18,
        alignment=0,
        textColor=colors.black,
        spaceBefore=18,
        spaceAfter=9,
        keepWithNext=True
    )

    # Texto principal
    texto = ParagraphStyle(
        "TextoCartilha",
        parent=estilos["BodyText"],
        fontName="Times-Roman",
        fontSize=12,
        leading=18,
        alignment=4,
        textColor=colors.black,
        spaceAfter=9,
        firstLineIndent=1.25 * cm
    )

    # Texto sem recuo para informações e metadados
    texto_sem_recuo = ParagraphStyle(
        "TextoSemRecuo",
        parent=texto,
        firstLineIndent=0
    )

    # Listas com marcadores
    texto_lista = ParagraphStyle(
        "TextoLista",
        parent=texto,
        firstLineIndent=0,
        leftIndent=0.7 * cm,
        bulletIndent=0.2 * cm,
        spaceAfter=6
    )

    # Destaque simples na capa, sem cor
    destaque = ParagraphStyle(
    "DestaqueCartilha",
    parent=estilos["Normal"],
    fontName="Times-Roman",
    fontSize=12,
    leading=18,
    alignment=1,
    textColor=colors.black,
    firstLineIndent=0,
    leftIndent=0,
    rightIndent=0,
    spaceBefore=5,
    spaceAfter=12
    )

    texto_capa = ParagraphStyle(
    "TextoCapa",
    parent=estilos["Normal"],
    fontName="Times-Roman",
    fontSize=12,
    leading=18,
    alignment=1,
    textColor=colors.black,
    firstLineIndent=0,
    leftIndent=0,
    rightIndent=0,
    spaceAfter=12
)

    conteudo = []

    # CAPA
    conteudo.append(Spacer(1, 3 * cm))
    conteudo.append(Paragraph("CIBERPERIFA", titulo))
    conteudo.append(Paragraph(
        "Cartilha básica de segurança digital",
        subtitulo
    ))

    conteudo.append(Paragraph(
        "Aprenda a reconhecer ameaças, proteger suas contas "
        "e navegar com mais segurança na internet.",
        texto_capa
    ))

    conteudo.append(Spacer(1, 2 * cm))
    conteudo.append(Paragraph(
        "<b>Informação é uma forma de proteção.</b>",
        destaque
    ))

    conteudo.append(Paragraph(
        "Material educativo para ajudar pessoas a desenvolver "
        "hábitos mais seguros no ambiente digital.",
        texto_capa
    ))

    conteudo.append(Spacer(1, 2 * cm))
    conteudo.append(Paragraph(
        "Conteúdo educativo e consulta a dados públicos.",
        subtitulo
    ))

    # CONTEÚDO EDUCATIVO
    conteudo.append(PageBreak())

    conteudo.append(Paragraph(
        "1. O que é cibersegurança?",
        secao
    ))
    conteudo.append(Paragraph(
        "Cibersegurança é o conjunto de práticas usadas para "
        "proteger dispositivos, contas, redes e informações "
        "contra acessos indevidos, golpes e outros ataques digitais.",
        texto
    ))
    conteudo.append(Paragraph(
        "Ela não depende apenas de programas de proteção. "
        "Senhas fortes, atenção aos links, atualizações e cuidado "
        "com os dados pessoais também fazem parte dessa proteção.",
        texto
    ))

    conteudo.append(Paragraph(
        "2. Como reconhecer golpes e phishing",
        secao
    ))
    conteudo.append(Paragraph(
        "Phishing é uma tentativa de enganar uma pessoa para obter "
        "senhas, dados bancários ou outras informações. O golpe pode "
        "chegar por e-mail, mensagem, redes sociais ou sites falsos.",
        texto
    ))

    dicas_phishing = [
        "Desconfie de mensagens que criam urgência ou ameaçam bloquear sua conta.",
        "Confira o endereço completo do site antes de informar seus dados.",
        "Não abra anexos inesperados nem clique em links suspeitos.",
        "Confirme pedidos de dinheiro ou informações por outro canal confiável.",
        "Lembre-se: logotipos e nomes conhecidos também podem ser falsificados."
    ]

    for dica in dicas_phishing:
        conteudo.append(Paragraph(
            escape(dica), texto_lista, bulletText="•"
        ))

    conteudo.append(Paragraph(
        "3. Como proteger suas contas",
        secao
    ))

    dicas_contas = [
        "Use senhas longas, únicas e difíceis de adivinhar.",
        "Evite reutilizar a mesma senha em diferentes serviços.",
        "Considere usar um gerenciador de senhas confiável.",
        "Ative a autenticação em dois fatores sempre que possível.",
        "Nunca compartilhe códigos de autenticação recebidos por mensagem."
    ]

    for dica in dicas_contas:
        conteudo.append(Paragraph(
            escape(dica), texto_lista, bulletText="•"
        ))

    conteudo.append(Paragraph(
        "4. Mantenha seus dispositivos protegidos",
        secao
    ))

    dicas_dispositivos = [
        "Instale atualizações do sistema e dos aplicativos.",
        "Baixe programas somente de fontes confiáveis.",
        "Use bloqueio de tela no celular e no computador.",
        "Faça cópias de segurança dos arquivos importantes.",
        "Evite acessar contas sensíveis em redes Wi-Fi públicas sem proteção adequada."
    ]

    for dica in dicas_dispositivos:
        conteudo.append(Paragraph(
            escape(dica), texto_lista, bulletText="•"
        ))

    conteudo.append(Paragraph(
        "5. O que fazer se você cair em um golpe?",
        secao
    ))

    passos_incidente = [
        "Interrompa o contato com o possível golpista.",
        "Se informou uma senha, altere-a usando o site ou aplicativo oficial.",
        "Encerre sessões desconhecidas e revise as opções de recuperação da conta.",
        "Se houver risco financeiro, entre em contato com o banco pelos canais oficiais.",
        "Guarde mensagens e comprovantes que possam ajudar na investigação.",
        "Denuncie o ocorrido às plataformas e autoridades competentes, conforme o caso."
    ]

    for passo in passos_incidente:
        conteudo.append(Paragraph(
            escape(passo), texto, bulletText="•"
        ))

    conteudo.append(Paragraph(
        "6. Mas afinal, o que são vulnerabilidades?",
        secao
    ))

    conteudo.append(Paragraph(
        "Uma vulnerabilidade é uma falha em um sistema, programa "
        "ou dispositivo que pode afetar sua segurança. O catálogo "
        "da CISA (Cybersecurity and Infrastructure Security Agency) "
        " - Agência do governo dos Estados Unidos responsável por promover a segurança cibernética, "
        " identificar vulnerabilidades em sistemas e divulgar orientações para ajudar organizações e pessoas a se protegerem contra ameaças digitais - " 
        " reúne vulnerabilidades com evidências de exploração, vamos analisar algumas dessas vulnerabilidades no decorrer do arquivo.",
        texto
    ))

    conteudo.append(Paragraph(
        "Data e hora da consulta: "
        + datetime.now().strftime("%d/%m/%Y às %H:%M"),
        texto
    ))

    conteudo.append(Paragraph(
        "Os registros abaixo foram consultados no catálogo oficial. "
        "Descrição e ação recomendada são apresentadas no idioma "
        "original da fonte, quando disponíveis.",
        texto
    ))

    for vulnerabilidade in vulnerabilidades[:5]:
        cve = escape(str(
            vulnerabilidade.get("cveID", "Não informado")
        ))
        fornecedor = escape(str(
            vulnerabilidade.get("vendorProject", "Não informado")
        ))
        produto = escape(str(
            vulnerabilidade.get("product", "Não informado")
        ))
        data = escape(str(
            vulnerabilidade.get("dateAdded", "Não informada")
        ))
        descricao = escape(str(
            vulnerabilidade.get(
                "shortDescription", "Descrição não disponível."
            )
        ))
        acao = escape(str(
            vulnerabilidade.get(
                "requiredAction", "Ação não informada pela fonte."
            )
        ))

        conteudo.append(Paragraph(f"CVE: {cve}", secao))
        conteudo.append(Paragraph(
            f"<b>Fornecedor:</b> {fornecedor}", texto_sem_recuo
        ))
        conteudo.append(Paragraph(
            f"<b>Produto:</b> {produto}", texto_sem_recuo
        ))
        conteudo.append(Paragraph(
            f"<b>Data de inclusão no catálogo:</b> {data}", texto_sem_recuo
        ))
        
        conteudo.append(Paragraph(
            f"<b>Descrição original (CISA):</b> {descricao}",
            texto_sem_recuo
        ))

        explicacao = escape(
            explicar_vulnerabilidade(vulnerabilidade)
        )

        conteudo.append(Paragraph(
            "<b>O que isso significa?</b>",
            texto
        ))
        conteudo.append(Paragraph(
            explicacao,
            texto
        ))

        conteudo.append(Paragraph(
            f"<b>Ação recomendada original (CISA):</b> {acao}",
            texto
        ))


    conteudo.append(Paragraph(
        "Fonte oficial: <link href='https://www.cisa.gov/known-exploited-vulnerabilities-catalog'>"
        "Catálogo de Vulnerabilidades Exploradas da CISA</link>.",
        texto
    ))

    conteudo.append(Paragraph(
        "Este material é educativo e não substitui orientações "
        "técnicas específicas, suporte profissional ou instruções "
        "do fabricante do dispositivo.",
        texto
    ))

    documento.build(
    conteudo,
    onFirstPage=desenhar_rodape,
    onLaterPages=desenhar_rodape
    )

    arquivo.seek(0)
    return arquivo



@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


@app.route("/baixar-pdf")
def baixar_pdf():
    try:
        vulnerabilidades = consultar_cisa()
        arquivo = gerar_pdf(vulnerabilidades)

        return send_file(
            arquivo,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="relatorio_ciberperifa.pdf"
        )

    except (requests.RequestException, KeyError, ValueError) as erro:
        app.logger.error("Erro ao gerar relatório: %s", erro)
        return "Não foi possível consultar e validar os dados da CISA. Tente novamente mais tarde.", 502


if __name__ == "__main__":
    app.run(debug=True)
