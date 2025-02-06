import re
from decimal import Decimal, InvalidOperation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from ofertas.models import Produto

def clean_price(price_str):
    
    price_str = price_str.replace("R$", "").replace("\n", "").strip()
    
    if ',' in price_str:
        price_str = price_str.replace('.', '').replace(',', '.')
    else:
        price_str = price_str.replace('.', '')
    try:
        return Decimal(price_str)
    except InvalidOperation:
        return None

def clean_percent(percent_str):

    percent_str = percent_str.replace('%', '').replace('OFF', '').strip()
    try:
        return Decimal(percent_str)
    except InvalidOperation:
        return None

def truncate_text(text, max_length=200):
    if text and len(text) > max_length:
        return text[:max_length]
    return text

def scrape_mercado_livre():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.mercadolivre.com.br")
    
    driver.implicitly_wait(10)
    
    search_box = driver.find_element(By.NAME, "as_word")
    search_box.send_keys("Computador Gamer i7 16gb ssd 1tb")
    search_box.submit()
    
    driver.implicitly_wait(10)
    
    produtos = driver.find_elements(By.CSS_SELECTOR, "li.ui-search-layout__item")
    
    for produto in produtos:
        try:
            titulo_elem = produto.find_element(By.CSS_SELECTOR, ".poly-component__title-wrapper a")
            nome = titulo_elem.text
            link = titulo_elem.get_attribute("href")
            nome = truncate_text(nome, 200)
            link = truncate_text(link, 200)
            
            preco_elem = produto.find_element(By.CSS_SELECTOR, ".poly-price__current span.andes-money-amount__fraction")
            preco_str = preco_elem.text  
            preco = clean_price(preco_str)
            if preco is None:
                raise ValueError(f"Preço inválido: {preco_str}")
            
            imagem_elem = produto.find_element(By.CSS_SELECTOR, ".poly-card__portada > img.poly-component__picture")
            imagem = imagem_elem.get_attribute("src")
            imagem = truncate_text(imagem, 500) 
            
            parcelamento = produto.find_element(By.CSS_SELECTOR, ".poly-price__installments").text
            parcelamento = truncate_text(parcelamento, 200)
            
            try:
                preco_sem_desconto_elem = produto.find_element(By.CSS_SELECTOR, "s.andes-money-amount--previous")
                preco_sem_desconto_str = preco_sem_desconto_elem.text
                preco_sem_desconto = clean_price(preco_sem_desconto_str)
            except Exception:
                preco_sem_desconto = None
            
            try:
                percentual_desconto_elem = produto.find_element(By.CSS_SELECTOR, ".andes-money-amount__discount")
                percentual_desconto_str = percentual_desconto_elem.text
                percentual_desconto = clean_percent(percentual_desconto_str)
            except Exception:
                percentual_desconto = None
            
            try:
                shipping_elem = produto.find_element(By.CSS_SELECTOR, ".poly-component__shipping")
                shipping_texto = shipping_elem.text.lower()
                frete_gratis = "grátis" in shipping_texto
                tipo_entrega = "Full" if "full" in shipping_texto else "Normal"
            except Exception:
                frete_gratis = False
                tipo_entrega = "Normal"
            
            Produto.objects.create(
                nome=nome,
                preco=preco,
                parcelamento=parcelamento,
                link=link,
                imagem=imagem,
                preco_sem_desconto=preco_sem_desconto,
                percentual_desconto=percentual_desconto,
                tipo_entrega=tipo_entrega,
                frete_gratis=frete_gratis
            )
        except Exception as e:
            print(f"Erro ao processar produto: {e}")
    
    driver.quit()

if __name__ == "__main__":
    scrape_mercado_livre()
