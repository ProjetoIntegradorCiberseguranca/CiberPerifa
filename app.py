
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

    # Faixa decorativa superior
    pdf.setFillColor(colors.HexColor("#4527A0"))
    pdf.rect(0, altura - 8, largura, 8, fill=1, stroke=0)

    # Identificação e número da página
    pdf.setStrokeColor(colors.HexColor("#D1C4E9"))
    pdf.line(2 * cm, 1.6 * cm, largura - 2 * cm, 1.6 * cm)

    pdf.setFont("Helvetica", 8)
    pdf.setFillColor(colors.HexColor("#555555"))
    pdf.drawString(2 * cm, 1.1 * cm, "CiberPerifa | Cartilha educativa")
    pdf.drawRightString(
        largura - 2 * cm,
        1.1 * cm,
        f"Página {documento.page}"
    )

    pdf.restoreState()


def gerar_pdf(vulnerabilidades):
    arquivo = BytesIO()

    documento = SimpleDocTemplate(
        arquivo,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Cartilha de Cibersegurança - CiberPerifa",
        author="CiberPerifa"
    )

    estilos = getSampleStyleSheet()

    titulo = ParagraphStyle(
        "TituloCartilha",
        parent=estilos["Title"],
        fontSize=21,
        leading=26,
        alignment=1,
        spaceAfter=16,
        textColor=colors.HexColor("#4527A0"),
    )

    subtitulo = ParagraphStyle(
        "SubtituloCartilha",
        parent=estilos["Normal"],
        fontSize=11,
        leading=16,
        alignment=1,
        spaceAfter=20,
        textColor=colors.HexColor("#6A1B9A"),
    )

    secao = ParagraphStyle(
        "SecaoCartilha",
        parent=estilos["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=14,
        spaceAfter=8,
        textColor=colors.HexColor("#4527A0"),
    )

    texto = ParagraphStyle(
        "TextoCartilha",
        parent=estilos["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=8
    )

    destaque = ParagraphStyle(
        "DestaqueCartilha",
        parent=texto,
        leftIndent=12,
        rightIndent=12,
        spaceBefore=5,
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
        texto
    ))

    conteudo.append(Spacer(1, 2 * cm))
    conteudo.append(Paragraph(
        "<b>Informação é uma forma de proteção.</b>",
        destaque
    ))

    conteudo.append(Paragraph(
        "Material educativo para ajudar pessoas a desenvolver "
        "hábitos mais seguros no ambiente digital.",
        texto
    ))

    conteudo.append(Spacer(1, 2 * cm))
    conteudo.append(Paragraph(
        "Conteúdo educativo e consulta a dados públicos da CISA.",
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
            escape(dica), texto, bulletText="•"
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
            escape(dica), texto, bulletText="•"
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
            escape(dica), texto, bulletText="•"
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
        "6. Vulnerabilidades identificadas pela CISA",
        secao
    ))

    conteudo.append(Paragraph(
        "Uma vulnerabilidade é uma falha em um sistema, programa "
        "ou dispositivo que pode afetar sua segurança. O catálogo "
        "da CISA reúne vulnerabilidades com evidências de exploração. "
        "A presença de um registro não significa que todos os "
        "dispositivos estejam comprometidos.",
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
            f"<b>Fornecedor:</b> {fornecedor}", texto
        ))
        conteudo.append(Paragraph(
            f"<b>Produto:</b> {produto}", texto
        ))
        conteudo.append(Paragraph(
            f"<b>Data de inclusão no catálogo:</b> {data}", texto
        ))
        conteudo.append(Paragraph(
            f"<b>Descrição original:</b> {descricao}", texto
        ))
        conteudo.append(Paragraph(
            f"<b>Ação recomendada original:</b> {acao}", texto
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
