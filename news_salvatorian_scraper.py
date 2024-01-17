### SCRAPER DIARIOS NACIONALES EL SALVADOR ###

#importing libraries
import streamlit as st
import pandas as pd
from PIL import Image
import requests
from bs4 import BeautifulSoup
import base64 

def get_download_link(data, filename, text):
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'


# Función para realizar el scrape según el diario seleccionado
def scrape_data(diario, url):
    #### CONTRA PUNTO####
    if diario == "Contra Punto":
        # Código de scraping para Contra Punto
        url_contra_punto= url
         # Realizar la solicitud HTTP a la página de noticias
        response = requests.get(url_contra_punto)
        soup = BeautifulSoup(response.text, 'html.parser')

        #scraping the front page 
        main_section= soup.find('body')
        news_container= main_section.find('div', class_= 'td_block_inner tdb-block-inner td-fix-index')
        news_box= news_container.find_all('div', class_= 'tdb_module_loop td_module_wrap td-animation-stack')

        title_article= []
        link_article= []
        date_article= []
        article_summary= []

        for box in news_box:
            date_section= box.find_all('time')
            summary_sections= box.find_all('div', class_= 'td-excerpt')
            title_sections= box.find_all('h3')
                        
            for date in date_section:
                date_news= date['datetime']
                date_article.append(date_news)

            for summary in summary_sections:
                new_summary= summary.text
                article_summary.append(new_summary)

            for title in title_sections:
                title_element= title.find('a')
                if title_element:
                    title= title_element.text
                    title_article.append(title)
                    link= title_element['href']
                    link_article.append(link)
        
        #Adding the type of news
        main_section= soup.find('body')
        news_classification= main_section.find('div', class_= 'td_block_wrap tdb_title tdi_71 tdb-category-title td-pb-border-top td_block_template_1')
        news_type= news_classification.find('h1', class_= 'tdb-title-text').text

        #making the dataframe
        data= pd.DataFrame({'title': title_article, 'url': link_article, 'publication_date': date_article, 'summary': article_summary})
        data['source_id']= 'Diario Digital Contra Punto'
        data['source_type']= 'Web Page'
        data['category_id']= news_type

        return data
    
    #### LA HUELLA####
    elif diario == "La Huella":
        # Código de scraping para Contra Punto
        url_la_huella= url
        # Realizar la solicitud HTTP a la página de noticias
        response = requests.get(url_la_huella)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #scraping the front page 
        main_section= soup.find('div', class_= 'site-outer')
        news_container= main_section.find('div', class_= 'grid-container')
        news_box= news_container.find_all('div', class_= 'p-wrap p-list p-list-1')

        title_article= []
        link_article= []
        date_article= []
        author= []

        for box in news_box:
            date_section= box.find_all('time')
            title_sections= box.find_all('h3')
            author_sections= box.find_all('span', class_= 'meta-el meta-author')
                        
            for date in date_section:
                date_news= date['datetime']
                date_article.append(date_news)

            for author_id in author_sections:
                author_element= author_id.find('a')
                if author_element:
                    author_name= author_element.text
                    author.append(author_name) 

            for title in title_sections:
                title_element= title.find('a')
                if title_element:
                    title= title_element.text
                    title_article.append(title)
                    link= title_element['href']
                    link_article.append(link)
            
        main_section= soup.find('div', class_= 'site-outer')
        news_classification= main_section.find('div', class_= 'archive-inner')
        news_type= news_classification.find('h1', class_= 'archive-title').text

        # Iterar sobre cada enlace para obtener los resumenes
        summary_data = []
        for url in link_article:
            try:
                # Realizar la solicitud HTTP
                response = requests.get(url)
                response.raise_for_status()  # Verificar si la solicitud fue exitosa
            except requests.exceptions.HTTPError as errh:
                print(f"Error HTTP: {errh}")
                continue
            except requests.exceptions.ConnectionError as errc:
                print(f"Error de conexión: {errc}")
                continue
            except requests.exceptions.RequestException as err:
                print(f"Error: {err}")
                continue

            # Parsear el contenido HTML de la página
            soup = BeautifulSoup(response.text, 'html.parser')

            # Encontrar y extraer la parte específica del artículo (ajusta según tus necesidades)
            main= soup.find('div', class_= 'site-outer')
            header_section= main.find('header', class_= 'single-header')
            summary_section= header_section.find('h2', class_='s-tagline fw-tagline')  # Cambia 'div' y 'class_' según la estructura de la página

            # Almacenar el enlace y la parte específica en las listas
            summary_data.append(summary_section.get_text() if summary_section else None)

        #creando el dataframe
        data= pd.DataFrame({'title': title_article, 'url': link_article, 'publication_date': date_article, 'author_id': author, 'summary': summary_data})
        data['source_id']= 'Diario La Huella'
        data['source_type']= 'Web Page'
        data['category_id']= news_type

        return data
    
    ####PRENSA GRAFICA####
    elif diario == "La Prensa Gráfica":
        url_la_prensa_grafica= url
        # Realizar la solicitud HTTP a la página de noticias
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url_la_prensa_grafica, headers= headers)

        if response.status_code == 200:
            content = response.text
            # Crea el objeto BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
        else:
            print(f'Error al hacer la solicitud. Código de estado: {response.status_code}')
        
        #scraping the front page 
        main_section= soup.find('section', class_= 'jsx-3343590874')
        news_box= main_section.find_all('article', class_= 'jsx-1067927586 box summary')

        title_article= []
        link_article= []
        date_article= []
        news_classification= []
        author= []

        for box in news_box:
            date_section= box.find_all('time')
            article_sections= box.find_all('h2')
            type_sections= box.find_all('div')
            author_sections= box.find_all('div', class_= 'jsx-4208424821 info')
        
            for date in date_section:
                date_news= date['datetime']
                date_article.append(date_news)

            for type in type_sections:
                type_element= type.find('a', class_= 'jsx-513040738 section')
                
                if type_element:
                    type_article= type_element['title']
                    news_classification.append(type_article)
                    
            for author_id in author_sections:
                author_element= author_id.text
                author.append(author_element)

            for article in article_sections:
                a_element= article.find('a')
                if a_element:
                    title= a_element.text
                    title_article.append(title)
                    link= a_element['href']
                    link_article.append(link)
            
        #LINK DE LOS ARTICULOS
        link_prensa_grafica= 'https://www.laprensagrafica.com/seccion' 
        link= [link_prensa_grafica + i for i in link_article]
        link

        #LIMPIANDO LA LISTA DE LOS AUTORES
        author_id = [chain.split('\xa0·\xa0')[0] for chain in author]

        #RESUMEN
        summary_list= []

        #iterando sobre los enlaces de los articulos
        for url in link:
            try:
                # Realizar la solicitud HTTP
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                response = requests.get(url, headers= headers)
                response.raise_for_status()  # Verificar si la solicitud fue exitosa
            except requests.exceptions.HTTPError as errh:
                print(f"Error HTTP: {errh}")
                continue
            except requests.exceptions.ConnectionError as errc:
                print(f"Error de conexión: {errc}")
                continue
            except requests.exceptions.RequestException as err:
                print(f"Error: {err}")
                continue

            # Parsear el contenido HTML de la página
            soup = BeautifulSoup(response.text, 'html.parser')

            ##scraping the page article
            main_section= soup.find('div', class_= 'jsx-336959476')
            article_box= main_section.find('article', class_= 'jsx-336959476')
            summary_section= article_box.find('div', class_= 'jsx-652497729')

            summary_element= summary_section.find('p')
            summary_data= summary_element.text
            summary_list.append(summary_data)  
        
        #LIMPIANDO LA LISTA DE RESUMENES
        summary_final= [i.rstrip('\xa0') for i in summary_list]

        #making the dataframe
        data= pd.DataFrame({'title': title_article, 'url': link, 'publication_date': date_article, 'category_id': news_classification, 'author_id': author_id, 'summary': summary_final})
        
        #OTRAS COLUMNAS PARA EL DATAFRAME
        data['source_id']= 'La Prensa Gráfica'
        data['source_type']= 'Web Page'         

        return data

### CREATING THE APP ###
#image in the sidebar
image = Image.open('Omdena-San-Salvador-Logo.jpeg')
st.sidebar.image(image, caption='Omdena El Salvador Local Chapter')

#title of the app
st.sidebar.title(':blue[Opciones]')

#titulo app

st.title(':blue[_Herramienta para Scraping de Diarios de El Salvador_] "📰"')

st.info("Bienvenido: Esta app fue diseñada para realiza Web Scraping de diarios locales de El Salvador. Sigue estas intrucciones para continuar:")

# Lista de instrucciones
st.info(" 1. Selecciona un diario de la barra lateral.")
st.info("2. Escoge la categoría de noticias.")
st.info("3. Presiona el botón *Realizar scraping*.")
st.info("4. Puedes descargar 2 archivos: Dataset completa y Dataset para análisis de sentimiento. El último solo contiene dos columnas: Título y Resumen")

#select the news paper
option_1 = st.sidebar.selectbox('Selecciona el diario:', ('Contra Punto', 'La Huella', 'La Prensa Gráfica'))


#select the category
# Definir las opciones para la segunda selectbox
if option_1 == 'Contra Punto':
    option_2_select = ['Internacionales', 'Opinión', 'Política', 'Sociedad', 'Economía', 'Cultura', 'Deportes']
elif option_1 == 'La Huella':
    option_2_select = ['Nacionales', 'Política', 'Internacionales', 'Deportes', 'Opinión', 'Trends']
elif option_1 == 'La Prensa Gráfica':
    option_2_select = ['Deportes', 'Tendencias', 'Internacionales', 'Salvadoreñisimo']

option_2= st.sidebar.selectbox('Selecciona la categoría:', option_2_select)

# Mapeo de diarios a URLs
diarios_urls = {
    "Contra Punto": 'https://www.contrapunto.com.sv',
    "La Huella": 'https://diariolahuella.com/category',
    "La Prensa Gráfica": 'https://www.laprensagrafica.com/seccion'
}

# Obtener la URL correspondiente al diario seleccionado
url_diario = diarios_urls.get(option_1, '') 

# Mapeo de tópicos a rutas específicas en el sitio web
topicos_rutas = {
    'Política': '/politica',
    'Deportes': '/deportes',
    'Internacionales': '/internacionales',
    'Opinión': '/opinion',
    'Sociedad': '/sociedad',
    'Economía': '/economia',
    'Cultura': '/cultura',
    'Salvadoreñisimo': '/salvadorenisimo',
    'Tendencias': '/tendencias',
    'Trends': '/trends',
    'Nacionales': '/nacionales'
}

# Obtener la ruta específica para el tópico seleccionado
ruta_topico = topicos_rutas.get(option_2, "")

# Construir la URL final para el scraping
url_scrape = url_diario + ruta_topico

# Mostrar la URL resultante
st.write(f"URL para el scraping: {url_scrape}")

# Botón para iniciar el scraping
if st.button("Realizar Scraping", type= 'primary'):
    # Llamar a la función de scraping con la URL
    datos_scrapeados = scrape_data(option_1, url_scrape)
    
    # Mostrar los resultados (puedes usar st.write, st.dataframe, etc.)
    st.write('Resultados del scraping:')
    st.dataframe(datos_scrapeados)
    data_shape= datos_scrapeados.shape
    st.write(f'El dataframe tiene una dimensión de: {data_shape}')

    
        # Convertir el DataFrame a formato CSV
    csv_data = datos_scrapeados.to_csv(index=False).encode('utf-8')
    csv_sent_analysis= datos_scrapeados[['title', 'summary']].to_csv(index=False).encode('utf-8')

    st.markdown(get_download_link(csv_data, 'dataset_completo.csv', 'Descargar CSV Completo'), unsafe_allow_html=True)
    st.markdown(get_download_link(csv_sent_analysis, 'dataset_analisis_sentimiento.csv', 'Descargar CSV para Análisis de Sentimiento'), unsafe_allow_html=True)








#####SCRAPING THE NEWS#####










st.sidebar.write('Omdena El Salvador Local Chapter')
