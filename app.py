
import requests
from flask import Flask, send_file, render_template
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from io import BytesIO

app = Flask(__name__)

URL_CISA = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"


def consultar_cisa():
    resposta = requests.get(URL_CISA, timeout=20)
    resposta.raise_for_status()

    dados = resposta.json()
    return dados["vulnerabilities"]


def gerar_pdf(vulnerabilidades):
    arquivo = BytesIO()

    pdf = canvas.Canvas(arquivo, pagesize=A4)
    largura, altura = A4

    pdf.setTitle("Relatório CiberPerifa")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, altura - 50, "CiberPerifa - Relatório de Vulnerabilidades")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, altura - 75, "Fonte: CISA - Catálogo de Vulnerabilidades Exploradas")

    data_consulta = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.drawString(50, altura - 92, f"Data da consulta: {data_consulta}")

    y = altura - 130

    for vulnerabilidade in vulnerabilidades[:5]:
        if y < 100:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = altura - 50

        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(
            50, y,
            f"CVE: {vulnerabilidade.get('cveID', 'Não informado')}"
        )
        y -= 18

        pdf.setFont("Helvetica", 10)
        pdf.drawString(
            50, y,
            f"Produto: {vulnerabilidade.get('product', 'Não informado')}"
        )
        y -= 16

        pdf.drawString(
            50, y,
            f"Data de inclusão: {vulnerabilidade.get('dateAdded', 'Não informada')}"
        )
        y -= 28

    pdf.save()
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
