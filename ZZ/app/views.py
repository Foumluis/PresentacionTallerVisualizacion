from django.shortcuts import render
from django.conf import settings
import pandas as pd
import numpy as np
import json
# Create your views here.

csv_path = f"{settings.BASE_DIR}/app/static/excel.csv"
tarea = pd.read_csv(csv_path)
tarea = tarea.set_index("Customer ID")
#------------------------------------------------------------------------------------------

#Value_counts de los valores categoricos
categorias = []
for i in ['Gender', 'Item Purchased', 'Category','Location', 'Size', 'Color', 'Season','Subscription Status', 'Shipping Type', 'Discount Applied','Promo Code Used', 'Payment Method','Frequency of Purchases']:
    categorias.append(tarea[i].value_counts())
#------------------------------------------------------------------------------------------

#Viendo los nulos por columna
nulos = tarea.isnull().sum()
#------------------------------------------------------------------------------------------

# funcion que traforma los yes en 0 y los no en 1
#------------------------------------------------------------------------------------------

tarea['Gender']=np.where(tarea['Gender'] == 'Male', 'Hombre',tarea['Gender'])
tarea['Gender']=np.where(tarea['Gender'] == 'Female', 'Mujer',tarea['Gender'])



# Traducción manual de valores categóricos
# Item Purchased
tarea['Item Purchased'] = tarea['Item Purchased'].replace({
    'Shirt': 'Camisa',
    'Pants': 'Pantalón',
    'Shoes': 'Zapatos',
    'Dress': 'Vestido',
    'Hat': 'Sombrero',
    'Jacket': 'Chaqueta',
    'Skirt': 'Falda',
    'Shorts': 'Shorts',
    'Sweater': 'Suéter',
    'Socks': 'Calcetines',
    'Sandals': 'Sandalias',
    'Boots': 'Botas'
})



# Category
tarea['Category'] = tarea['Category'].replace({
    'Clothing': 'Ropa',
    'Footwear': 'Calzado',
    'Accessories': 'Accesorios'
})

# Color
tarea['Color'] = tarea['Color'].replace({
    'Red': 'Rojo',
    'Blue': 'Azul',
    'Green': 'Verde',
    'Black': 'Negro',
    'White': 'Blanco',
    'Yellow': 'Amarillo',
    'Pink': 'Rosa',
    'Purple': 'Morado',
    'Brown': 'Marrón',
    'Orange': 'Naranja'
})
# Season
tarea['Season'] = tarea['Season'].replace({
    'Spring': 'Primavera',
    'Summer': 'Verano',
    'Fall': 'Otoño',
    'Winter': 'Invierno'
})
# Payment Method
tarea['Payment Method'] = tarea['Payment Method'].replace({
    'Credit Card': 'Tarjeta de Crédito',
    'Debit Card': 'Tarjeta de Débito',
    'Cash': 'Efectivo',
    'Bank Transfer': 'Transferencia Bancaria'
})
# Frequency of Purchases
tarea['Frequency of Purchases'] = tarea['Frequency of Purchases'].replace({
    'Weekly': 'Semanal',
    'Monthly': 'Mensual',
    'Bi-Weekly': 'Cada dos semanas',
    'Fortnightly': 'Quincenal',
    'Every 3 Months': 'Cada 3 Meses',
    'Quarterly': 'Trimestral',
    'Annually': 'Anual'
})


# Análisis Univariado
def distribucion_clientes_genero(request):
    x = tarea['Gender'].value_counts().index.tolist()
    y = tarea["Gender"].value_counts().tolist()
    return render(request, 'analisis/univariado/distribucion_genero.html', {'x': x, 'y': y})

# Análisis Bivariado
def comparacion_compras_generos(request):
    # Get purchase amounts by gender
    male_purchases = tarea[tarea['Gender'] == 'Hombre']['Purchase Amount (USD)'].tolist()
    female_purchases = tarea[tarea['Gender'] == 'Mujer']['Purchase Amount (USD)'].tolist()
    
    context = {
        'male_purchases': male_purchases,
        'female_purchases': female_purchases
    }
    return render(request, 'analisis/bivariado/comparacion_generos.html', context)

def relacion_categoria_monto(request):
    # Calculate total purchase amount by category
    category_totals = tarea.groupby('Category')['Purchase Amount (USD)'].sum().to_dict()
    
    # Get category names and values
    categories = list(category_totals.keys())
    values = list(category_totals.values())
    
    # Calculate percentages
    total = sum(values)
    percentages = [(v/total)*100 for v in values]
    
    context = {
        'categories': categories,
        'values': values,
        'percentages': percentages,
        'total': total
    }
    return render(request, 'analisis/bivariado/categoria_monto.html', context)

def cantidad_ventas_categoria(request):
    y=tarea['Category'].value_counts()
    x =  y.index.tolist()
    y = y.values.tolist()

    return render(request, 'analisis/bivariado/ventas_categoria.html', {'y': y, 'x': x})

# --------------Bato-----------------------------------------

# Diccionario para mapear nombres de estados a códigos (para Plotly)
STATE_CODE_MAP = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# Análisis de Ubicación
def relacion_ubicacion_monto(request):
    # Agrupar por ubicación y calcular el total de ventas
    ventas_por_estado = tarea.groupby('Location')['Purchase Amount (USD)'].sum().reset_index()
    ventas_por_estado.columns = ['Estado', 'Total_Ventas']
    
    # Mapear nombres de estados a códigos
    ventas_por_estado['Codigo'] = ventas_por_estado['Estado'].map(STATE_CODE_MAP)
    
    # Ordenar por total de ventas descendente
    ventas_por_estado = ventas_por_estado.sort_values('Total_Ventas', ascending=False)
    
    # Preparar datos para el template
    estados = ventas_por_estado['Estado'].tolist()
    codigos = ventas_por_estado['Codigo'].tolist()
    totales = [int(x) for x in ventas_por_estado['Total_Ventas'].tolist()]
    
    # Top 10 estados
    top_10_estados = estados[:10]
    top_10_totales = totales[:10]
    
    context = {
        'estados': json.dumps(estados),
        'codigos': json.dumps(codigos),
        'totales': json.dumps(totales),
        'top_10_estados': json.dumps(top_10_estados),
        'top_10_totales': json.dumps(top_10_totales)
    }
    
    return render(request, 'analisis/ubicacion/ubicacion_monto.html', context)

def presencia_geografica(request):
    # Calcular cantidad de ventas por estado
    ventas_por_estado = tarea.groupby('Location').size().reset_index(name='Cantidad_Ventas')
    ventas_por_estado.columns = ['Estado', 'Cantidad_Ventas']
    
    # Mapear nombres de estados a códigos
    ventas_por_estado['Codigo'] = ventas_por_estado['Estado'].map(STATE_CODE_MAP)
    
    # Crear copia ordenada para la tabla (bottom 10)
    ventas_ordenadas = ventas_por_estado.sort_values('Cantidad_Ventas', ascending=True)
    estados_baja_presencia = ventas_ordenadas.head(10)
    
    # Bottom 10 para la tabla - crear lista de diccionarios
    bottom_10_data = [
        {'estado': estado, 'cantidad': int(cantidad)}
        for estado, cantidad in zip(
            estados_baja_presencia['Estado'].tolist(),
            estados_baja_presencia['Cantidad_Ventas'].tolist()
        )
    ]
    
    # Preparar datos para el mapa (todos los estados)
    todos_estados = ventas_por_estado['Estado'].tolist()
    todos_codigos = ventas_por_estado['Codigo'].tolist()
    todas_cantidades = [int(x) for x in ventas_por_estado['Cantidad_Ventas'].tolist()]
    
    context = {
        'todos_estados': json.dumps(todos_estados),
        'todos_codigos': json.dumps(todos_codigos),
        'todas_cantidades': json.dumps(todas_cantidades),
        'bottom_10_data': bottom_10_data
    }
    
    return render(request, 'analisis/ubicacion/presencia_geografica.html', context)

# --------------Bato-----------------------------------------


# Análisis Multivariado
def compras_categoria_talla(request):
    # Create a cross-tabulation of Category and Size
    category_size_counts = pd.crosstab(tarea['Category'], tarea['Size'])
    
    # Get the data for the stacked bar chart
    categories = category_size_counts.index.tolist()
    sizes = category_size_counts.columns.tolist()
    
    # Create data for each size (stacked bars)
    size_data = {}
    for size in sizes:
        size_data[size] = category_size_counts[size].tolist()
    
    context = {
        'categories': categories,
        'sizes': sizes,
        'size_data': size_data
    }
    return render(request, 'analisis/multivariado/categoria_talla.html', context)

# Problemas
def problemas(request):
    return render(request, 'problemas/base_problemas.html')

def problema1(request):
    return render(request, 'problemas/problema1.html')

def problema2(request):
    return render(request, 'problemas/problema2.html')

def problema3(request):
    return render(request, 'problemas/problema3.html')

# Alcance
def alcance(request):
    return render(request, 'alcance.html')

def home(request):
    return render(request, 'home.html')

