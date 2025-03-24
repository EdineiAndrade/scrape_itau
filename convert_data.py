import pandas as pd
import re


def convert_data(df):
    
    # Exemplo de mapeamento
    meses_pt_en = {
        'jan': 'Jan', 'fev': 'Feb', 'mar': 'Mar', 'abr': 'Apr',
        'mai': 'May', 'jun': 'Jun', 'jul': 'Jul', 'ago': 'Aug',
        'set': 'Sep', 'out': 'Oct', 'nov': 'Nov', 'dez': 'Dec'
    }

    # Exemplo de DataFrame
    df = df

    # Substitui os meses PT → EN de forma vetorizada
    def substituir_meses_pt_en(match):
        """Função auxiliar para usar dentro do str.replace com regex."""
        mes_pt = match.group(1).lower()  # ex.: 'abr'
        return meses_pt_en[mes_pt]       # ex.: 'Apr'

    # Aqui usamos .str.replace com regex + lambda
    df['Próximo Vencimento'] = (
        df['Próximo Vencimento']
        .str.replace(
            r'(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)',
            substituir_meses_pt_en,
            case=False,
            regex=True
        )
    )

    # Converte a coluna para datetime
    df['Próximo Vencimento'] = pd.to_datetime(df['Próximo Vencimento'], format='%d %b %Y')


    return df