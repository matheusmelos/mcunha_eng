import os
from datetime import datetime

# Registra erros em um arquivo de relatório.
def registrar_erro(mensagem):
    
    try:
        log_file = "relatorio.txt"

        # Formatar a mensagem com data e hora
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensagem_formatada = f"[{timestamp}] {mensagem}\n"

        # Gravar a mensagem no arquivo de relatório
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(mensagem_formatada)

    except Exception as e:
        print(f"Erro ao tentar registrar erro no relatório: {e}")
