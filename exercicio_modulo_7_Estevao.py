import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde

pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

df = pd.read_csv('D:/Cursos/Programação/ecommerce_estatistica.csv')

print(df.head())


df['Qtd_Vendidos'] = (
    df['Qtd_Vendidos']
    .astype(str)
    .str.extract(r'(\d+)')[0]  # extrai apenas os dígitos
)
df['Qtd_Vendidos'] = pd.to_numeric(df['Qtd_Vendidos'], errors='coerce')
df = df.dropna(subset=['Qtd_Vendidos'])

top_marcas = df.groupby('Marca')['Qtd_Vendidos'].sum().sort_values(ascending=False).head(5)
df_top = df[df['Marca'].isin(top_marcas.index)].copy()

# ---------------------- GRÁFICO DE BARRA ----------------------
plt.figure(figsize=(8, 5))
top_marcas_df = top_marcas.reset_index()
top_marcas_df.columns = ['Marca', 'Qtd_Vendidos']
sns.barplot(data=top_marcas_df, x='Marca', y='Qtd_Vendidos', hue='Marca', palette='pastel', legend=False)
plt.title('Top 5 Marcas Mais Vendidas')
plt.xlabel('Marca')
plt.ylabel('Quantidade Vendida')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# ---------------------- GRÁFICO DE PIZZA ----------------------
plt.figure(figsize=(6, 6))
plt.pie(top_marcas.values, labels=top_marcas.index, autopct='%.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Participação das Top 5 Marcas')
plt.tight_layout()
plt.show()

# ---------------------- GRÁFICO DE DENSIDADE ----------------------
qtd_vendidos = df_top['Qtd_Vendidos']
density = gaussian_kde(qtd_vendidos)
x_vals = np.linspace(qtd_vendidos.min(), qtd_vendidos.max(), 500)
y_vals = density(x_vals)

plt.figure(figsize=(8, 5))
plt.plot(x_vals, y_vals, color='mediumslateblue', linewidth=2)
plt.fill_between(x_vals, y_vals, color='mediumslateblue', alpha=0.3)
plt.title('Densidade - Qtd Vendida (Top 5 Marcas)')
plt.xlabel('Quantidade Vendida')
plt.ylabel('Densidade')
plt.tight_layout()
plt.show()

# ---------------------- GRÁFICO DE REGRESSÃO ----------------------
if 'Desconto' in df.columns:
    df['Desconto'] = pd.to_numeric(df['Desconto'], errors='coerce')
    df_top = df_top.dropna(subset=['Desconto'])

    plt.figure(figsize=(8, 5))
    sns.regplot(x='Qtd_Vendidos', y='Desconto', data=df_top,
                scatter_kws={'alpha': 0.5, 'color': '#34c289'},
                line_kws={'color': '#278f65'})
    plt.title('Regressão: Qtd Vendida x Desconto (Top 5 Marcas)')
    plt.xlabel('Quantidade Vendida')
    plt.ylabel('Desconto')
    plt.tight_layout()
    plt.show()

# ---------------------- GRÁFICO DE HISTOGRAMA ----------------------
plt.figure(figsize=(8, 5))
sns.histplot(data=df_top, x='Qtd_Vendidos', bins=10, kde=False, color='skyblue')
plt.title('Histograma - Quantidade Vendida (Top 5 Marcas)')
plt.xlabel('Quantidade Vendida')
plt.ylabel('Frequência')
plt.tight_layout()
plt.show()

# ---------------------- GRÁFICO DE DISPERSÃO ----------------------
if 'Desconto' in df.columns:
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df_top, x='Qtd_Vendidos', y='Desconto', hue='Marca', palette='pastel')
    plt.title('Dispersão: Qtd Vendida vs Preço (Top 5 Marcas)')
    plt.xlabel('Quantidade Vendida')
    plt.ylabel('Desconto')
    plt.tight_layout()
    plt.show()

# ---------------------- MAPA DE CALOR (correlação) ----------------------
# Selecionar apenas colunas numéricas relevantes
df_corr = df_top[['Qtd_Vendidos']]
if 'Desconto' in df_top.columns:
    df_corr = df_top[['Qtd_Vendidos', 'Desconto']].copy()
    corr = df_corr.corr()
    plt.figure(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Mapa de Calor - Correlação')
    plt.tight_layout()
    plt.show()