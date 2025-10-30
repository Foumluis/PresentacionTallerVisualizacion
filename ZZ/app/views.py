from django.shortcuts import render
from django.conf import settings
import pandas as pd
import numpy as np
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
    return render(request, 'analisis/bivariado/comparacion_generos.html')

def relacion_categoria_monto(request):
    return render(request, 'analisis/bivariado/categoria_monto.html')

def cantidad_ventas_categoria(request):
    return render(request, 'analisis/bivariado/ventas_categoria.html')

# Análisis de Ubicación
def relacion_ubicacion_monto(request):
    return render(request, 'analisis/ubicacion/ubicacion_monto.html')

def presencia_geografica(request):
    return render(request, 'analisis/ubicacion/presencia_geografica.html')

# Análisis Multivariado
def compras_categoria_talla(request):
    return render(request, 'analisis/multivariado/categoria_talla.html')

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

