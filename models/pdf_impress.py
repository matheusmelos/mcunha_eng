import fitz 
import pandas as pd
import shutil
import os
import zipfile
import rarfile

class PDF_Printer:
    
    def __init__(self, zip_folder):

        self.folder = zip_folder
        self.data = None
        self.pdfs = []
        self.extraction_folder = "Extração"
        
        self.descompact_folder = self.extract_folder()
        self.found_pdfs()
        self.print_data()
        self.processed_zip = self.zip_file_process()
    
    def extract_folder(self): 
                
                # Remove a pasta de extração se ela já existir
                if os.path.exists(self.extraction_folder):
                    shutil.rmtree(self.extraction_folder)
                
                # Cria a pasta de extração
                os.makedirs(self.extraction_folder)

                # Verifica o tipo de arquivo e realiza a extração
                if self.folder.lower().endswith('.zip'):
                    with zipfile.ZipFile(self.folder, 'r') as archive:
                        archive.extractall(self.extraction_folder)
                        
                elif self.folder.lower().endswith('.rar'):
                    with rarfile.RarFile(self.folder, 'r') as archive:
                        archive.extractall(self.extraction_folder)
                        
                # Chama a função para extrair subarquivos
                sub = self.extraction_folder
                extrair = self.extract_subfiles(sub)
                return extrair
  
    def print_data(self):
      

        # Abrir a planilha usando pandas
        df = pd.read_excel(self.data)

        # Colunas específicas a serem incluídas na tabela
        colunas_especificas = ["NOME DO PDF", "ORDEM DE COMPRA", "CÓD. PEÇA", "QTD", "DATA"]

        # Verifique se as colunas existem na planilha
        df = df[colunas_especificas]

        # Corrigir a coluna "ORDEM DE COMPRA" para evitar valores como "100234.0"
        if "ORDEM DE COMPRA" in df.columns:
            df["ORDEM DE COMPRA"] = df["ORDEM DE COMPRA"].fillna("").apply(
                lambda x: str(int(x)) if pd.notnull(x) and x != "" else "Informação não disponível"
            )

        # Formatar a coluna "DATA" no padrão brasileiro e remover a hora
        if "DATA" in df.columns:
            def formatar_data(data):
                try:
                    return pd.to_datetime(data).strftime("%d/%m/%Y")
                except Exception:
                    return "Data inválida"

            df["DATA"] = df["DATA"].apply(formatar_data)

        # Preencher valores nulos e converter todos os dados para string
        df = df.fillna("Informação não disponível").astype(str)

        # Iterar sobre a lista de PDFs
        for pdf in self.pdfs:
            # Filtrar apenas as linhas onde "NOME DO PDF" é igual ao nome do PDF atual
            nome_do_pdf_atual = pdf.split("/")[-1]  # Obtem apenas o nome do arquivo (sem o caminho)
            dados_pdf = df[df["NOME DO PDF"] == nome_do_pdf_atual]

            # Se não houver correspondência, não faz nada
            if dados_pdf.empty:
                print(f"Nenhuma entrada correspondente ao PDF '{nome_do_pdf_atual}' na planilha.")
            else:
                # Abrir o PDF existente
                doc = fitz.open(pdf)

                # Dimensões da página em paisagem
                largura = 842
                altura = 595

                # Criar uma nova página em paisagem
                nova_pagina = doc.new_page(width=largura, height=altura)

                # Adicionar o título
                titulo = f"Informações para: {nome_do_pdf_atual}"
                nova_pagina.insert_text((50, 20), titulo, fontsize=14, color=(0, 0, 0))

                # Configurar a tabela
                x_inicial, y_inicial = 50, 50
                largura_celula, altura_celula = 180, 30  # Ajustar altura para remover espaço extra

                # Cabeçalhos da tabela
                cabecalhos = list(dados_pdf.columns[1:])  # Ignorar "NOME DO PDF"
                for j, texto in enumerate(cabecalhos):
                    x1 = x_inicial + j * largura_celula
                    y1 = y_inicial
                    x2 = x1 + largura_celula
                    y2 = y1 + altura_celula
                    nova_pagina.draw_rect(fitz.Rect(x1, y1, x2, y2), color=(0, 0, 0), width=0.5)
                    nova_pagina.insert_textbox(
                        fitz.Rect(x1, y1, x2, y2), texto, fontsize=10, align=1
                    )

                # Adicionar os dados filtrados sem espaços entre as linhas
                for i, linha in enumerate(dados_pdf.itertuples(index=False)):
                    for j, valor in enumerate(linha[1:]):  # Ignorar "NOME DO PDF"
                        x1 = x_inicial + j * largura_celula
                        y1 = y_inicial + (i + 1) * altura_celula
                        x2 = x1 + largura_celula
                        y2 = y1 + altura_celula
                        nova_pagina.draw_rect(fitz.Rect(x1, y1, x2, y2), color=(0, 0, 0), width=0.5)
                        nova_pagina.insert_textbox(
                            fitz.Rect(x1, y1, x2, y2), str(valor), fontsize=10, align=1
                        )

                # Gerar o caminho do PDF final na mesma pasta do PDF original
                pasta_pdf = os.path.dirname(pdf)  # Obtem o diretório do PDF original
                nome_pdf_final = os.path.splitext(nome_do_pdf_atual)[0] + "_editado.pdf"  # Adiciona o sufixo "_editado"
                pdf_final = os.path.join(pasta_pdf, nome_pdf_final)
                
                os.remove(pdf)
              
              
              
                doc.save(pdf_final)
                print(f"PDF editado salvo como: {pdf_final}")
        
    def found_pdfs(self):
        
        for root, dirs, files in os.walk(self.descompact_folder):
            # Ignora pastas que contêm outras subpastas
            if dirs:
                continue

            for file in files:
                file_path = os.path.join(root, file)

                # Processa arquivos compactados
                if file.lower().endswith('.zip') or file.lower().endswith('.rar'):
                    sub_destino = os.path.join(root, os.path.splitext(file)[0])
                    os.makedirs(sub_destino, exist_ok=True)
                    try:
                        if file.lower().endswith('.zip'):
                            with zipfile.ZipFile(file_path, 'r') as sub_archive:
                                sub_archive.extractall(sub_destino)
                        elif file.lower().endswith('.rar'):
                            with rarfile.RarFile(file_path, 'r') as sub_archive:
                                sub_archive.extractall(sub_destino)
                        os.remove(file_path)
                    except Exception as e:
                        self.registrar_erro(file_path, e)

                # Cria objetos específicos para os arquivos e os adiciona ao grupo
                elif file.upper().endswith(".PDF"):
                    pdf_obj = file_path
                    self.pdfs.append(pdf_obj)
                    
                    
                elif file.upper().endswith(".XLSX"):
                    self.data = file_path
                
    def extract_subfiles(self, root_folder):
            
            processed_files = set()
            stack = [root_folder]

            while stack:
                current_folder = stack.pop()

                for root, dirs, files in os.walk(current_folder):
                    for file in files:
                        file_path = os.path.join(root, file)

                        if file_path in processed_files:
                            continue

                        processed_files.add(file_path)

                        # Tratamento de erro para arquivos ZIP
                        if file.upper().endswith(".XLSX"):
                            self.data = file_path
                        
                        elif file.lower().endswith('.zip'):
                            sub_destino = os.path.join(root, os.path.splitext(file)[0])
                            os.makedirs(sub_destino, exist_ok=True)
                            try:
                                with zipfile.ZipFile(file_path, 'r') as sub_archive:
                                    sub_archive.extractall(sub_destino)
                                os.remove(file_path)
                                stack.append(sub_destino)
                            except zipfile.BadZipFile as e:
                                with open("relatorio.txt", "a") as f:
                                    f.write(f"O arquivo {file_path} não é um ZIP válido ou está corrompido.\n")
                                    f.write(f"Erro ao processar o arquivo {file_path}:\n")
                                    f.write(f"{str(e)}\n")

                        # Tratamento de erro para arquivos RAR
                        elif file.lower().endswith('.rar'):
                            sub_destino = os.path.join(root, os.path.splitext(file)[0])
                            os.makedirs(sub_destino, exist_ok=True)
                            try:
                                with rarfile.RarFile(file_path, 'r') as sub_archive:
                                    sub_archive.extractall(sub_destino)
                                os.remove(file_path)
                                stack.append(sub_destino)
                            except rarfile.Error as e:
                                with open("relatorio.txt", "a") as f:
                                    f.write(f"O arquivo {file_path} não é um RAR válido ou está corrompido.\n")
                                    f.write(f"Erro ao processar o arquivo {file_path}:\n")
                                    f.write(f"{str(e)}\n")

            return root_folder

    def zip_file_process(self):
        
        data_dashboard = "data dashboard"
        
        if os.path.exists(data_dashboard):
            shutil.rmtree(data_dashboard)
                
        os.makedirs(data_dashboard)
        
        shutil.move(self.data, data_dashboard)
        
        
        folder_zip = "PDFs IMPRESSÃO.zip"
        relatorio = "relatorio.txt"
        
    
        def zip_folder (base_file, zip_file):
      
            with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for root, dirs, files in os.walk(base_file):
                            for file in files:
                                caminho = os.path.join(root, file)
                                zipf.write(caminho, os.path.relpath(caminho, base_file))
                
            return zip_file
        
        
        if os.path.exists(relatorio):
            shutil.move(relatorio, self.folder)
            
        zip_file_processed = zip_folder(self.descompact_folder, folder_zip)
        
        destino_path = os.path.join("uploads", zip_file_processed)
        
        if os.path.exists(destino_path):
            shutil.rmtree(destino_path)
        shutil.move(zip_file_processed, "uploads")
        
        return zip_file_processed

# Apaga pastas criadas durante o processo    
    def clean_all(self):
        
        if os.path.exists(self.extraction_folder):
            shutil.rmtree(self.extraction_folder)
        if os.path.exists(self.folder):
            os.remove(self.folder)    
