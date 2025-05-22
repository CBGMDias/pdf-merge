import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
from ctypes import windll

def selecionar_pdfs():
    # Define o ícone da janela do tkinter para 'icon.ico'
    icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
    root = tk.Tk()
    try:
        root.iconbitmap(icon_path)
    except Exception:
        pass
    root.withdraw()
    # Ajusta o DPI da janela para melhor compatibilidade com telas de alta resolução
    try:
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    root = tk.Tk()
    root.withdraw()
    arquivos = filedialog.askopenfilenames(
        title="Selecione os PDFs para mesclar",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    return list(arquivos)

def copiar_para_pasta(arquivos, pasta_destino):
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    arquivos_copiados = []
    for arquivo in arquivos:
        destino = os.path.join(pasta_destino, os.path.basename(arquivo))
        shutil.copy2(arquivo, destino)
        arquivos_copiados.append(destino)
    return arquivos_copiados

def esvaziar_pasta(pasta):
    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho_arquivo):
            os.remove(caminho_arquivo)

def main():
    pasta = "pdfs"
    arquivos = selecionar_pdfs()
    if not arquivos:
        messagebox.showinfo("Aviso", "Nenhum PDF selecionado.")
        return

    copiar_para_pasta(arquivos, pasta)

    merger = PdfMerger()
    pdfs = [f for f in os.listdir(pasta) if f.endswith(".pdf")]
    pdfs.sort()

    for pdf in pdfs:
        merger.append(os.path.join(pasta, pdf))

    try:
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        output_path = os.path.join(desktop_path, "pdf-mesclado.pdf")
        merger.write(output_path)
        merger.close()
        esvaziar_pasta(pasta)
        messagebox.showinfo("Sucesso", f"PDF mesclado salvo na área de trabalho:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()