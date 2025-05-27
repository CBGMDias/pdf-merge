import os
import shutil
from tkinter import filedialog, messagebox, Tk
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from ctypes import windll

class PDFManager:
    def __init__(self):
        self.pasta = "pdfs"
        if not os.path.exists(self.pasta):
            os.makedirs(self.pasta)

    def selecionar_arquivos(self, titulo="Selecione os PDFs", tipo_arquivo=[("Arquivos PDF", "*.pdf")]):
        self._ajustar_dpi_e_janela()
        arquivos = filedialog.askopenfilenames(title=titulo, filetypes=tipo_arquivo)
        return list(arquivos)

    def _ajustar_dpi_e_janela(self):
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
        root = Tk()
        root.withdraw()

    def copiar_para_pasta(self, arquivos):
        arquivos_copiados = []
        for arquivo in arquivos:
            destino = os.path.join(self.pasta, os.path.basename(arquivo))
            shutil.copy2(arquivo, destino)
            arquivos_copiados.append(destino)
        return arquivos_copiados

    def esvaziar_pasta(self):
        for arquivo in os.listdir(self.pasta):
            caminho = os.path.join(self.pasta, arquivo)
            if os.path.isfile(caminho):
                os.remove(caminho)

    def merge_pdfs(self):
        arquivos = self.selecionar_arquivos("Selecione os PDFs para mesclar")
        if not arquivos:
            messagebox.showinfo("Aviso", "Nenhum PDF selecionado.")
            return

        self.copiar_para_pasta(arquivos)
        merger = PdfMerger()
        pdfs = sorted(f for f in os.listdir(self.pasta) if f.endswith(".pdf"))

        for pdf in pdfs:
            merger.append(os.path.join(self.pasta, pdf))

        try:
            output_path = os.path.join(os.path.expanduser("~"), "Desktop", "pdf-mesclado.pdf")
            merger.write(output_path)
            merger.close()
            self.esvaziar_pasta()
            messagebox.showinfo("Sucesso", f"PDF mesclado salvo em:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar PDF: {e}")

    def split_pdf(self):
        arquivos = self.selecionar_arquivos("Selecione o PDF para dividir")
        if not arquivos:
            messagebox.showinfo("Aviso", "Nenhum PDF selecionado.")
            return

        pdf_path = arquivos[0]
        nome_base = os.path.splitext(os.path.basename(pdf_path))[0]
        output_dir = os.path.join(os.path.expanduser("~"), "Desktop", f"{nome_base}_paginas")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            reader = PdfReader(pdf_path)
            for i, pagina in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(pagina)
                with open(os.path.join(output_dir, f"{nome_base}_pagina_{i+1}.pdf"), "wb") as f:
                    writer.write(f)
            messagebox.showinfo("Sucesso", f"PDF separado por página em:\n{output_dir}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao separar PDF: {e}")
