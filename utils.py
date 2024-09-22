import re

def extrair_valor(string: str) -> float:
        padrao = r'[\d.,]+'  # Captura apenas a parte numérica
        valor = re.search(padrao, string).group()
        return float(valor.replace(',', ''))