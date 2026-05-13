import pandas as pd
import json

def procesar_y_generar():
    archivo_csv = 'afluenciamb_simple_03_2026.csv'
    archivo_html = 'index.html'

    try:
        df = pd.read_csv(archivo_csv)
        df = df.dropna(subset=['afluencia'])

        # ── Estadísticas globales ──────────────────────────────────────
        media   = round(df['afluencia'].mean(), 2)
        mediana = int(df['afluencia'].median())
        moda    = int(df['afluencia'].mode()[0])

        print(f"Media:   {media:,.2f}")
        print(f"Mediana: {mediana:,}")
        print(f"Moda:    {moda:,}")

        
        f_abs = df.groupby('linea')['afluencia'].sum().reset_index()
        total = f_abs['afluencia'].sum()
        f_abs = f_abs.sort_values(by='afluencia', ascending=False)
        f_abs['relativa']  = (f_abs['afluencia'] / total * 100).round(2)
        f_abs['acumulada'] = f_abs['afluencia'].cumsum()

       
        barras   = f_abs[['linea', 'afluencia']].rename(columns={'afluencia': 'valor'}).to_dict(orient='records')
        pastel   = f_abs[['linea', 'relativa']].rename(columns={'linea': 'label', 'relativa': 'value'}).to_dict(orient='records')
        poligono = f_abs[['linea', 'acumulada']].to_dict(orient='records')

        def limpiar(obj):
            if isinstance(obj, list):
                return [{k: (int(v) if hasattr(v, 'item') else v) for k, v in d.items()} for d in obj]
            return obj

        barras   = limpiar(barras)
        pastel   = limpiar(pastel)
        poligono = limpiar(poligono)

       
        with open(archivo_html, 'r', encoding='utf-8') as f:
            html = f.read()

        html = html.replace('{{ media }}',    f'{media:,.2f}')
        html = html.replace('{{ mediana }}',  f'{mediana:,}')
        html = html.replace('{{ moda }}',     f'{moda:,}')
        html = html.replace('{{ barras }}',   json.dumps(barras,   ensure_ascii=False))
        html = html.replace('{{ pastel }}',   json.dumps(pastel,   ensure_ascii=False))
        html = html.replace('{{ poligono }}', json.dumps(poligono, ensure_ascii=False))

        with open(archivo_html, 'w', encoding='utf-8') as f:
            f.write(html)

       

    except FileNotFoundError:
        print(f"Error: No se encontró '{archivo_csv}'. Ponlo en la misma carpeta que main.py.")

if __name__ == "__main__":
    procesar_y_generar()