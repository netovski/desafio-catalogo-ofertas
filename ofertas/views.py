from django.core.paginator import Paginator
from django.shortcuts import render
from ofertas.models import Produto
from ofertas.scrapy import scrape_mercado_livre

# Create your views here.

def lista_produtos(request):
    # scrape_mercado_livre()
    produtos = Produto.objects.all()
    
    # Filtros
    filtro_frete_gratis = request.GET.get('frete_gratis')
    filtro_full = request.GET.get('full')
    
    if filtro_frete_gratis:
        produtos = produtos.filter(frete_gratis=True)
    if filtro_full:
        produtos = produtos.filter(tipo_entrega='Full')
        
    paginator = Paginator(produtos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Cálculos extras
    maior_preco = produtos.order_by('-preco').first()
    menor_preco = produtos.order_by('preco').first()
    maior_desconto = produtos.order_by('-percentual_desconto').first()
    
    # Contexto para o template
    context = {
        'produtos': produtos,
        'maior_preco': maior_preco,
        'menor_preco': menor_preco,
        'maior_desconto': maior_desconto,
    }
    
    return render(request, 'ofertas/lista_produtos.html', context)