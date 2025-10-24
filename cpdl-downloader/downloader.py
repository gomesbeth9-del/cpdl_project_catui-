import requests
import json
import os
import re

# Diretório para salvar as músicas
DOWNLOAD_DIR = 'musicas'

def get_page_titles():
    """Busca os títulos das páginas na categoria da API da MediaWiki."""
    print("Buscando lista de músicas...")
    api_url = "https://www.cpdl.org/wiki/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": "Category:Catuí_Côrte-Real_Suarez_editions",
        "format": "json",
        "cmlimit": 500
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'error' in data:
            print(f"Erro na API: {data['error']['info']}")
            return []

        pages = data.get('query', {}).get('categorymembers', [])
        titles = [page['title'] for page in pages]
        print(f"Encontradas {len(titles)} páginas de música.")
        return titles
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")
        return []

def get_file_urls_from_page(title):
    """Busca o conteúdo de uma página e extrai os links dos arquivos de música."""
    print(f"\nProcessando página: {title}")
    api_url = "https://www.cpdl.org/wiki/api.php"
    params = {
        "action": "parse",
        "page": title,
        "prop": "text",
        "format": "json"
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            print(f"  Erro ao buscar página: {data['error']['info']}")
            return []

        html_content = data.get('parse', {}).get('text', {}).get('*', '')
        # Regex para encontrar apenas links de arquivos PDF
        file_urls = re.findall(r'href="(/wiki/images/[^"]+\.pdf)"', html_content)
        
        # Constrói a URL completa
        full_urls = [f"https://www.cpdl.org{url}" for url in file_urls]
        print(f"  Encontrados {len(full_urls)} arquivos.")
        return full_urls
    except requests.exceptions.RequestException as e:
        print(f"  Erro ao fazer a requisição para a página: {e}")
        return []

def download_file(url, folder):
    """Baixa um arquivo de uma URL para uma pasta específica."""
    try:
        filename = os.path.join(folder, url.split('/')[-1])
        
        # Evita baixar novamente se o arquivo já existir
        if os.path.exists(filename):
            print(f"  Arquivo já existe, pulando: {filename}")
            return

        print(f"  Baixando {url}...")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"  Salvo como {filename}")
    except requests.exceptions.RequestException as e:
        print(f"  Erro ao baixar {url}: {e}")

if __name__ == "__main__":
    # Cria o diretório de download se não existir
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        
    titles = get_page_titles()
    if titles:
        for title in titles:
            file_urls = get_file_urls_from_page(title)
            if file_urls:
                # Cria um subdiretório para cada obra para manter a organização
                work_dir = os.path.join(DOWNLOAD_DIR, re.sub(r'[\\/*?:"<>|]', "", title))
                if not os.path.exists(work_dir):
                    os.makedirs(work_dir)
                
                for url in file_urls:
                    download_file(url, work_dir)
        print("\nDownload de todas as obras concluído!")
