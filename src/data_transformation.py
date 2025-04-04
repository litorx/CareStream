import os
import re
import csv
import zipfile
import logging
import pdfplumber
from time import time
from concurrent.futures import ProcessPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def read_legend(pdf_path: str) -> dict:
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = pdf.pages[-1].extract_text() or ""
    except Exception as e:
        logging.error(f"Erro ao abrir PDF para legenda: {e}")
        return {}
    pattern = r"([A-Z]{2,})\s*:\s*([^:]+?)(?=\s+[A-Z]{2,}\s*:|$)"
    matches = re.findall(pattern, text)
    legend = {key.strip(): desc.strip() for key, desc in matches}
    logging.info("Legenda lida com sucesso.")
    return legend

def process_page(pdf_path: str, page_index: int) -> tuple:
    start = time()
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[page_index]
            tables = page.extract_tables() or []
        elapsed = time() - start
        return (page_index, elapsed, tables)
    except Exception as e:
        logging.error(f"Erro na página {page_index+1}: {e}")
        return (page_index, 0, [])

def extract_tables_concurrent(pdf_path: str) -> list:
    combined = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
    except Exception as e:
        logging.error(f"Erro ao abrir PDF para contagem de páginas: {e}")
        return combined
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_page, pdf_path, i) for i in range(total_pages)]
        for future in as_completed(futures):
            page_index, elapsed, tables = future.result()
            logging.info(f"Página {page_index+1} processada em {elapsed:.2f}s, {len(tables)} tabela(s) extraída(s).")
            for tbl in tables:
                if not tbl or not tbl[0]:
                    continue
                header = [cell.strip() for cell in tbl[0] if cell]
                if "OD" in header or "AMB" in header:
                    if not combined:
                        combined = tbl
                        logging.info(f"Página {page_index+1}: Tabela iniciada com cabeçalho: {header}")
                    elif tbl[0] == combined[0]:
                        combined.extend(tbl[1:])
                        logging.info(f"Página {page_index+1}: Tabela combinada.")
    return combined

def replace_in_table(table: list, legend: dict) -> list:
    if not table:
        return table
    new_table = [table[0]]
    for row in table[1:]:
        new_row = []
        for cell in row:
            txt = cell.strip() if cell else ""
            if txt == "OD":
                new_row.append(legend.get("OD", txt))
            elif txt == "AMB":
                new_row.append(legend.get("AMB", txt))
            else:
                new_row.append(txt)
        new_table.append(new_row)
    return new_table

def write_csv(csv_path: str, data: list) -> None:
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(data)
        logging.info(f"CSV salvo: {csv_path}")
    except Exception as e:
        logging.error(f"Erro ao escrever CSV: {e}")

def zip_files(zip_path: str, files: list) -> None:
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for f in files:
                z.write(f, os.path.basename(f))
        logging.info(f"ZIP criado em: {zip_path}")
    except Exception as e:
        logging.error(f"Erro na compactação: {e}")

def main():
    pdf_input = os.getenv("PDF_INPUT", "downloads/anexo1.pdf")
    csv_output = os.getenv("CSV_OUTPUT", "dados.csv")
    zip_output = os.getenv("ZIP_OUTPUT", "Teste_Vitor.zip")

    legend = read_legend(pdf_input)
    logging.info(f"Legenda lida: {legend}")
    if "OD" not in legend or "AMB" not in legend:
        logging.error("Legenda para OD ou AMB não encontrada.")
        return

    combined_table = extract_tables_concurrent(pdf_input)
    if not combined_table:
        logging.error("Nenhuma tabela encontrada.")
        return

    final_table = replace_in_table(combined_table, legend)
    write_csv(csv_output, final_table)
    zip_files(zip_output, [csv_output])
    logging.info("Processo concluído.")

if __name__ == "__main__":
    main()
