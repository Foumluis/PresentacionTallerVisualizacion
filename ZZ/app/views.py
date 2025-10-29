from django.shortcuts import render

# Create your views here.

# Análisis Univariado
def distribucion_clientes_genero(request):
    return render(request, 'analisis/univariado/distribucion_genero.html')

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
