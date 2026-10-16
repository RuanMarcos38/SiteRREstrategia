"""Deploy explícito FTPS; não remove arquivos, não acessa o sistema financeiro."""
import ftplib
import os
from pathlib import Path
import posixpath
import ssl

ROOT = Path(__file__).resolve().parents[1]

def publish():
    names = ['HOSTINGER_FTP_HOST', 'HOSTINGER_FTP_USER', 'HOSTINGER_FTP_PASSWORD', 'HOSTINGER_FTP_DIR']
    values = {name: os.environ.get(name, '').strip() for name in names}
    missing = [name for name in names if not values[name]]
    if missing:
        raise SystemExit('Configure os Secrets necessários: ' + ', '.join(missing))
    destination = values['HOSTINGER_FTP_DIR'].replace('\\', '/')
    if destination in ('/', '.', '') or '..' in destination.split('/'):
        raise SystemExit('Destino recusado: configure a pasta específica do site institucional.')
    files = [ROOT / 'styles.css', *sorted((ROOT / 'assets').rglob('*')), ROOT / 'index.html']
    files = [file for file in files if file.is_file()]
    if not (ROOT / 'index.html').is_file() or not (ROOT / 'styles.css').is_file():
        raise SystemExit('Arquivos principais ausentes.')
    with ftplib.FTP_TLS(context=ssl.create_default_context(), timeout=60) as ftp:
        ftp.connect(values['HOSTINGER_FTP_HOST'], 21)
        ftp.login(values['HOSTINGER_FTP_USER'], values['HOSTINGER_FTP_PASSWORD'])
        ftp.prot_p()
        ftp.cwd(destination)
        base = ftp.pwd()
        for file in files:
            relative = file.relative_to(ROOT).as_posix()
            ftp.cwd(base)
            for part in relative.split('/')[:-1]:
                try:
                    ftp.cwd(part)
                except ftplib.error_perm as exc:
                    if not str(exc).startswith('550'):
                        raise
                    ftp.mkd(part)
                    ftp.cwd(part)
            name = posixpath.basename(relative)
            with file.open('rb') as stream:
                ftp.storbinary('STOR ' + name, stream)
            print('Publicado: ' + relative)
    print('Transferência FTPS concluída. Confira https://rrestrategiaperformance.com.br/')

if __name__ == '__main__':
    publish()
