#!/usr/bin/env python3
"""Gera index.html a partir dos dados de dados.json (somente biblioteca padrão)."""

import html
import json
from pathlib import Path
from urllib.parse import urlparse

PASTA = Path(__file__).resolve().parent
ARQUIVO_DADOS = PASTA / "dados.json"
ARQUIVO_HTML = PASTA / "index.html"


def texto(valor):
    """Converte um valor em texto HTML seguro."""
    return html.escape(str(valor or "").strip())


def link_seguro(url):
    """Aceita somente links HTTP(S), evitando esquemas executáveis."""
    url = str(url or "").strip()
    if not url:
        return ""
    esquema = urlparse(url).scheme.lower()
    return html.escape(url, quote=True) if esquema in {"http", "https"} else ""


def renderizar_projetos(projetos):
    if not projetos:
        return '<p class="vazio">Adicione seus projetos no arquivo dados.json.</p>'

    itens = []
    for projeto in projetos:
        tecnologias = "".join(
            f'<span class="tag">{texto(tecnologia)}</span>'
            for tecnologia in projeto.get("tecnologias", [])
        )
        url = link_seguro(projeto.get("link"))
        acao = (
            f'<a class="project-link" href="{url}" target="_blank" '
            f'rel="noopener noreferrer">Ver projeto ↗</a>'
            if url else ""
        )
        itens.append(
            f"""<article class="project">
              <div class="project-heading">
                <h3>{texto(projeto.get('nome'))}</h3>
                {acao}
              </div>
              <p>{texto(projeto.get('descricao'))}</p>
              <div class="tags">{tecnologias}</div>
            </article>"""
        )
    return "\n".join(itens)


def renderizar_formacao(formacao):
    if not formacao:
        return '<p class="vazio">Adicione sua formação no arquivo dados.json.</p>'

    itens = []
    for item in formacao:
        detalhe = (
            f'<p class="item-detail">{texto(item.get("detalhe"))}</p>'
            if item.get("detalhe") else ""
        )
        itens.append(
            f"""<article class="timeline-item">
              <div class="item-topline">
                <h3>{texto(item.get('curso'))}</h3>
                <span class="periodo">{texto(item.get('periodo'))}</span>
              </div>
              <p class="muted">{texto(item.get('instituicao'))}</p>
              {detalhe}
            </article>"""
        )
    return "\n".join(itens)


def renderizar_cursos(cursos):
    if not cursos:
        return '<p class="vazio">Adicione seus cursos no arquivo dados.json.</p>'

    itens = []
    for curso in cursos:
        itens.append(
            f"""<li>
              <span class="course-name">{texto(curso.get('nome'))}</span>
              <span class="course-meta">{texto(curso.get('instituicao'))} · {texto(curso.get('ano'))}</span>
            </li>"""
        )
    return "\n".join(itens)


def gerar_html(dados):
    perfil = dados.get("perfil", {})
    nome = texto(perfil.get("nome", "Seu Nome"))
    titulo = texto(perfil.get("titulo", "Profissional"))
    localizacao = texto(perfil.get("localizacao"))
    email_original = str(perfil.get("email", "")).strip()
    email = texto(email_original)
    email_href = html.escape(email_original, quote=True)
    telefone = texto(perfil.get("telefone"))
    resumo = texto(perfil.get("resumo"))

    contatos = []
    if email:
        contatos.append(f'<a href="mailto:{email_href}">{email}</a>')
    if telefone:
        contatos.append(f'<span>{telefone}</span>')
    if localizacao:
        contatos.append(f'<span>{localizacao}</span>')

    for campo, rotulo in (("linkedin", "LinkedIn"), ("github", "GitHub")):
        url = link_seguro(perfil.get(campo))
        if url:
            contatos.append(
                f'<a href="{url}" target="_blank" rel="noopener noreferrer">{rotulo} ↗</a>'
            )

    habilidades = "".join(
        f'<span class="skill">{texto(habilidade)}</span>'
        for habilidade in dados.get("habilidades", [])
    )

    # O CSS fica em uma string separada para manter as chaves legíveis.
    css = """
      :root {
        --ink: #17243a;
        --muted: #617087;
        --accent: #0e8f87;
        --line: #e2e8ef;
        --paper: #ffffff;
        --wash: #f3f7f8;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        padding: 38px 18px;
        background: #eaf0f3;
        color: var(--ink);
        font-family: Inter, "Segoe UI", Arial, sans-serif;
        font-size: 14px;
        line-height: 1.55;
      }
      .resume {
        width: min(100%, 960px);
        margin: 0 auto;
        overflow: hidden;
        background: var(--paper);
        border-radius: 18px;
        box-shadow: 0 18px 55px rgba(28, 48, 68, .12);
      }
      .hero {
        position: relative;
        padding: 42px 48px 34px;
        background: #172b43;
        color: #fff;
      }
      .hero::after {
        content: "";
        position: absolute;
        right: 48px;
        top: 38px;
        width: 58px;
        height: 5px;
        border-radius: 10px;
        background: #42c2b5;
      }
      .eyebrow {
        margin: 0 0 8px;
        color: #8fe0d6;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: .16em;
        text-transform: uppercase;
      }
      h1 {
        margin: 0;
        font-size: clamp(32px, 5vw, 45px);
        line-height: 1.08;
        letter-spacing: -.04em;
      }
      .role { margin: 10px 0 0; color: #d4e0eb; font-size: 17px; }
      .contacts {
        display: flex;
        flex-wrap: wrap;
        gap: 8px 18px;
        margin-top: 24px;
        color: #d4e0eb;
        font-size: 12px;
      }
      a { color: inherit; text-decoration: none; }
      .contacts a { color: #9ce5dc; }
      .contacts a:hover, .project-link:hover { text-decoration: underline; }
      .content {
        display: grid;
        grid-template-columns: minmax(0, 1.55fr) minmax(230px, .85fr);
        gap: 38px;
        padding: 36px 48px 42px;
      }
      section { margin: 0 0 29px; }
      section:last-child { margin-bottom: 0; }
      h2 {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 0 0 15px;
        color: var(--ink);
        font-size: 12px;
        font-weight: 800;
        letter-spacing: .13em;
        text-transform: uppercase;
      }
      h2::before {
        content: "";
        display: inline-block;
        width: 18px;
        height: 3px;
        border-radius: 3px;
        background: var(--accent);
      }
      .summary { margin: 0; color: #46566c; font-size: 14px; }
      .project, .timeline-item { padding: 0 0 17px; margin: 0 0 17px; border-bottom: 1px solid var(--line); }
      .project:last-child, .timeline-item:last-child { margin-bottom: 0; padding-bottom: 0; border-bottom: 0; }
      .project-heading, .item-topline { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; }
      h3 { margin: 0; color: var(--ink); font-size: 15px; line-height: 1.35; }
      .project p, .item-detail { margin: 7px 0 10px; color: #53647a; font-size: 12.5px; }
      .project-link { flex: 0 0 auto; color: var(--accent); font-size: 11px; font-weight: 700; }
      .tags, .skills { display: flex; flex-wrap: wrap; gap: 6px; }
      .tag, .skill {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 5px;
        background: #eaf6f4;
        color: #147b75;
        font-size: 10px;
        font-weight: 700;
      }
      .muted, .periodo, .course-meta { color: var(--muted); font-size: 11px; }
      .muted { margin: 5px 0 0; }
      .periodo { white-space: nowrap; }
      .sidebar section { padding: 17px; border: 1px solid var(--line); border-radius: 11px; background: #fbfcfd; }
      .sidebar h2 { margin-bottom: 13px; }
      .skills { gap: 7px; }
      .skill { padding: 5px 9px; background: #eef2f7; color: #3f5066; font-size: 10.5px; }
      .courses { margin: 0; padding: 0; list-style: none; }
      .courses li { margin: 0 0 13px; }
      .courses li:last-child { margin-bottom: 0; }
      .course-name { display: block; font-size: 12px; font-weight: 700; }
      .course-meta { display: block; margin-top: 2px; }
      .vazio { color: var(--muted); font-size: 12px; }
      .footer { padding: 0 48px 24px; color: #8793a3; font-size: 10px; text-align: right; }

      @media (max-width: 680px) {
        body { padding: 0; background: var(--paper); }
        .resume { border-radius: 0; box-shadow: none; }
        .hero { padding: 34px 25px 28px; }
        .hero::after { right: 25px; top: 30px; width: 36px; }
        .contacts { gap: 8px 13px; }
        .content { grid-template-columns: 1fr; gap: 10px; padding: 28px 25px 32px; }
        .sidebar { display: grid; grid-template-columns: 1fr 1fr; align-items: start; gap: 12px; }
        .sidebar section { padding: 14px; }
        .footer { padding: 0 25px 20px; }
      }

      @page { size: A4; margin: 9mm; }
      @media print {
        html, body { width: 100%; min-height: 0; margin: 0; padding: 0; background: #fff; }
        body { font-size: 9.5pt; line-height: 1.38; print-color-adjust: exact; -webkit-print-color-adjust: exact; }
        .resume { width: 100%; max-width: none; margin: 0; overflow: visible; border-radius: 0; box-shadow: none; }
        .hero { padding: 8mm 9mm 6mm; }
        .hero::after { top: 8mm; right: 9mm; }
        h1 { font-size: 27pt; }
        .role { margin-top: 2mm; font-size: 11pt; }
        .contacts { gap: 2mm 5mm; margin-top: 4mm; font-size: 8pt; }
        .content { grid-template-columns: minmax(0, 1.55fr) minmax(0, .85fr); gap: 7mm; padding: 7mm 9mm 5mm; }
        section { margin-bottom: 5mm; }
        h2 { margin-bottom: 2.5mm; font-size: 8pt; }
        .summary { font-size: 9pt; }
        h3 { font-size: 9.5pt; }
        .project, .timeline-item { margin-bottom: 3mm; padding-bottom: 3mm; }
        .project p, .item-detail { margin: 1mm 0 1.5mm; font-size: 8pt; }
        .project-link { font-size: 7.5pt; }
        .tag, .skill { padding: 1mm 2mm; font-size: 7pt; }
        .sidebar section { padding: 3mm; border-radius: 2mm; }
        .sidebar h2 { margin-bottom: 2mm; }
        .courses li { margin-bottom: 2.5mm; }
        .course-name { font-size: 8pt; }
        .course-meta, .muted, .periodo { font-size: 7pt; }
        .footer { padding: 0 9mm; font-size: 7pt; }
        a { color: inherit; }
        .project, .timeline-item, .sidebar section { break-inside: avoid; }
      }
    """

    # HTML montado com f-strings: cada seção é preenchida com os dados do JSON.
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Currículo e portfólio de {nome}.">
  <title>{nome} | Currículo e portfólio</title>
  <style>{css}</style>
</head>
<body>
  <main class="resume">
    <header class="hero">
      <p class="eyebrow">Currículo · Portfólio</p>
      <h1>{nome}</h1>
      <p class="role">{titulo}</p>
      <div class="contacts">{' · '.join(contatos)}</div>
    </header>

    <div class="content">
      <div class="main-column">
        <section aria-labelledby="sobre-titulo">
          <h2 id="sobre-titulo">Sobre mim</h2>
          <p class="summary">{resumo}</p>
        </section>

        <section aria-labelledby="projetos-titulo">
          <h2 id="projetos-titulo">Projetos em destaque</h2>
          {renderizar_projetos(dados.get('projetos', []))}
        </section>

        <section aria-labelledby="formacao-titulo">
          <h2 id="formacao-titulo">Formação</h2>
          {renderizar_formacao(dados.get('formacao', []))}
        </section>
      </div>

      <aside class="sidebar">
        <section aria-labelledby="habilidades-titulo">
          <h2 id="habilidades-titulo">Habilidades</h2>
          <div class="skills">{habilidades}</div>
        </section>

        <section aria-labelledby="cursos-titulo">
          <h2 id="cursos-titulo">Cursos e certificados</h2>
          <ul class="courses">{renderizar_cursos(dados.get('cursos', []))}</ul>
        </section>
      </aside>
    </div>
    <footer class="footer">Currículo atualizado · {localizacao}</footer>
  </main>
</body>
</html>
"""


def main():
    try:
        with ARQUIVO_DADOS.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        raise SystemExit("Erro: não encontrei o arquivo dados.json.")
    except json.JSONDecodeError as erro:
        raise SystemExit(f"Erro no JSON (linha {erro.lineno}, coluna {erro.colno}): {erro.msg}")

    html_gerado = gerar_html(dados)
    ARQUIVO_HTML.write_text(html_gerado, encoding="utf-8")
    print(f"Página gerada com sucesso: {ARQUIVO_HTML}")


if __name__ == "__main__":
    main()
