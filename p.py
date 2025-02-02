import re

string = "DESENHOS PDFs\\01.33.00019\\aa_0746_08\\AA_0746_08.PDF"

# Expressão para capturar um trecho no formato "XX.XX.XXXXX"
padrao = r"\b\d{2}\.\d{2}\.\d{5}\b"

match = re.search(padrao, string)

if match:
    print(match.group())  # Saída: 01.33.00017
else:
    print("Código não encontrado")
