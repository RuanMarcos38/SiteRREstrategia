# RR Estratégia & Performance

Site institucional estático de assessoria de cobrança e recuperação de crédito.

- Site: https://rrestrategiaperformance.com.br/
- Área do cliente: https://financeiro.rrestrategiaperformance.com.br/
- Arquivos publicados: `index.html`, `styles.css` e `assets/`.
- Sem banco de dados, dependências de build ou credenciais no código.
- Diagnóstico local: gera briefing para download; não envia informações ao servidor.

## Ativar publicação automática na Hostinger

O fluxo está preparado e fica desativado até a configuração abaixo.

1. No hPanel, consulte os dados de acesso FTP/FTPS do domínio institucional. Confirme a pasta de publicação: normalmente `/public_html/` ou `/domains/rrestrategiaperformance.com.br/public_html/`, conforme o diretório inicial da conta. Não use a pasta do subdomínio financeiro. Preferir conta FTP limitada à pasta do site.
2. No GitHub, abra Settings → Secrets and variables → Actions → Secrets e cadastre:
   - `HOSTINGER_FTP_HOST`: hostname FTPS compatível com o certificado TLS.
   - `HOSTINGER_FTP_USER`: usuário FTP.
   - `HOSTINGER_FTP_PASSWORD`: senha FTP.
   - `HOSTINGER_FTP_DIR`: caminho confirmado da pasta do site. O fluxo recusa a raiz `/` por proteção.
3. Na aba Variables, crie `HOSTINGER_DEPLOY_ENABLED` com valor `true`.
4. Em Actions → Publicar site na Hostinger → Run workflow, execute o primeiro deploy e confira o resultado. Depois, cada alteração nos arquivos publicados na branch `main` dispara uma nova publicação.

O fluxo exige FTPS explícito com TLS válido na porta 21; não rebaixa a conexão para FTP sem criptografia. Ele transfere apenas os arquivos do site, não apaga arquivos remotos e não envia documentação ou scripts à hospedagem. `index.html` é enviado por último. O upload não é atômico; mantenha backup antes da primeira publicação. Nenhuma senha deve ser adicionada a commits, issues ou mensagens.

Se uma página inicial antiga tiver prioridade sobre index.html, faça backup e ajuste somente esse arquivo no hPanel. Não altere o sistema financeiro.

## Verificação local

```sh
python3 -m http.server 8000
```

Abra http://localhost:8000. O sistema externo de clientes mantém sua autenticação existente.
