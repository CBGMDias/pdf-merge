from PDFManager import PDFManager

def main():
    pdf = PDFManager()
    while True:
        print("\n--- MENU PDF ---")
        print("1 - Mesclar PDFs")
        print("2 - Separar PDF por página")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            pdf.merge_pdfs()
        elif escolha == "2":
            pdf.split_pdf()
        elif escolha == "0":
            print("Falou, chefia!")
            break
        else:
            print("Opção inválida. Tente de novo.")

if __name__ == "__main__":
    main()