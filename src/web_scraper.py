# web_scraper.py
import os
import logging
import requests
from bs4 import BeautifulSoup
from typing import List
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class PDFScraper:
    """Extrai links de PDFs da URL informada, filtrando links que contenham 'Anexo I' ou 'Anexo II'."""
    def extract_pdf_links(self, url: str) -> List[str]:
        pdf_links = []
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=lambda href: href and href.lower().endswith(".pdf"))
            for link in links:
                link_text = link.get_text().strip().lower()
                if "anexo i" in link_text or "anexo ii" in link_text:
                    full_url = requests.compat.urljoin(url, link.get("href"))
                    pdf_links.append(full_url)
            logging.info(f"{len(pdf_links)} links filtrados para Anexo I/II extraídos.")
        except Exception as e:
            logging.error(f"Erro ao extrair links: {e}")
        return pdf_links

class FileDownloader:
    """Realiza o download de arquivos individualmente e de forma concorrente."""
    def download(self, file_url: str, destination: str) -> None:
        try:
            response = requests.get(file_url, stream=True)
            response.raise_for_status()
            with open(destination, "wb") as f_out:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f_out.write(chunk)
            logging.info(f"Baixado: {destination}")
        except Exception as e:
            logging.error(f"Erro ao baixar {file_url}: {e}")

    def download_all(self, file_urls: List[str], dest_folder: str) -> List[str]:
        os.makedirs(dest_folder, exist_ok=True)
        downloaded_files = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(self.download, url, os.path.join(dest_folder, f"anexo{idx}.pdf")): idx 
                       for idx, url in enumerate(file_urls, start=1)}
            for future in as_completed(futures):
                try:
                    future.result()
                    downloaded_files.append(os.path.join(dest_folder, f"anexo{futures[future]}.pdf"))
                except Exception as e:
                    logging.error(f"Erro no download: {e}")
        return downloaded_files

class ZipArchiver:
    """Compacta uma lista de arquivos em um arquivo ZIP."""
    def create_zip(self, file_paths: List[str], zip_file_path: str) -> None:
        try:
            with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip_archive:
                for path in file_paths:
                    zip_archive.write(path, os.path.basename(path))
            logging.info(f"ZIP criado em: {zip_file_path}")
        except Exception as e:
            logging.error(f"Erro na compactação: {e}")

def main():
    SCRAPE_URL = os.getenv("SCRAPE_URL", "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos")
    DEST_FOLDER = "downloads"
    ZIP_OUTPUT = os.getenv("ZIP_OUTPUT", "anexos.zip")

    os.makedirs(DEST_FOLDER, exist_ok=True)

    scraper = PDFScraper()
    downloader = FileDownloader()
    archiver = ZipArchiver()

    pdf_links = scraper.extract_pdf_links(SCRAPE_URL)
    if not pdf_links:
        logging.error("Nenhum link de Anexo I/II encontrado.")
        return

    downloaded_files = downloader.download_all(pdf_links, DEST_FOLDER)
    if not downloaded_files:
        logging.error("Nenhum arquivo foi baixado.")
        return

    archiver.create_zip(downloaded_files, ZIP_OUTPUT)
    logging.info("Processo concluído.")

if __name__ == "__main__":
    main()