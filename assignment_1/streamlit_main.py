#------------CODIGO DEL DASHBOARD------------------------------------------------------------------
# instala las librerias necesarias desde la consola bash
# Para instalar cualquier libreria en visual code hay que hacer lo siguiente. 

# 1. ACTIVAR ENTORNO VISUAL. 
# En windows tienes que meterte a la ruta del proyecto. cd ruta/del/proyecto / <-------- esas lineas (/) al reves
# EN consola tipo BASH ESCRIBIR LA SIGUIENTE LINEA: python -m venv venv
# 2. Activar el entorno virtual
# En windows; .\venv\Scripts\activate
# En Mac; source venv/bin/activate
# pip install streamlit yfinance
# Reiniciar Visual code y listo! correr el codigo completo


# Importamos librerias
import streamlit as st
import yfinance as yf
import pandas as pd
import importlib.util
import time


import os
import sys
# print("Directorio actual:", os.getcwd())
# sys.path.insert(1, '../functions')
# print("Python Path:", sys.path)

# from sidebar import create_sidebar

def show():
    # show_stock_ticker_bar(stocks)
    st.markdown(f"{Introduccion}", unsafe_allow_html=True)





# def get_stock_prices(stocks):
#     prices = []
#     for stock in stocks:
#         try:
#             # Descargar datos del último día de negociación
#             data = yf.download(stock, period="1d")
#             # Obtener el último precio de cierre disponible
#             price = data['Close'].iloc[-1] if not data.empty else "No Disponible"
#             prices.append(f"{stock}: ${price:.2f}")
#         except Exception as e:
#             prices.append(f"{stock}: Error al obtener datos")
#     return " | ".join(prices)



# def show_stock_ticker_bar(stocks):
#     st.markdown("""
#     <style>
#     .ticker-wrap {
#         width: 100%;
#         overflow: hidden;
#         position: fixed;
#         top: 0;
#         background-color: #4CAF50;
#         padding: 10px;
#         z-index: 999;
#     }
#     .ticker {
#         display: inline-block;
#         white-space: nowrap;
#         padding-left: 100%;
#         animation: ticker 30s linear infinite;
#     }
#     .ticker__item {
#         display: inline-block;
#         padding: 0 2rem;
#     }
#     @keyframes ticker {
#         0% { transform: translate3d(0, 0, 0); }
#         100% { transform: translate3d(-100%, 0, 0); }
#     }
#     </style>
#     <div class="ticker-wrap">
#         <div class="ticker">
#             <div class="ticker__item">""" + get_stock_prices(stocks) + """</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)



def create_sidebar():   #  NAVEGACION 1
    st.sidebar.title('Navegación')
    pages = [file.replace('.py', '') for file in os.listdir('page') if file.endswith('.py')]
    selected_page = st.sidebar.selectbox("Seleccione una página", pages)
    return selected_page

def create_sidebar():   #  NAVEGACION 1
    st.sidebar.title('Navegación')
    # Obtener los nombres de los archivos sin la extensión .py y excluir el archivo main.py
    pages = [file.replace('.py', '') for file in os.listdir('page') if file.endswith('.py') ]
    # Usar radio buttons en lugar de un selectbox para la selección de la página
    selected_page = st.sidebar.radio("Seleccione una página", pages)
    return selected_page



def load_page(page_name):
    # Construye el path al archivo .py en la carpeta page
    page_path = os.path.join('page', f'{page_name}.py')
    # Importa el módulo correspondiente al nombre de la página
    spec = importlib.util.spec_from_file_location(page_name, page_path)
    page_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(page_module)
    # Ejecuta la función show() del módulo importado
    page_module.show()


# Esto debe estar al final de tu main.py
if __name__ == "__main__":
    selected_page = create_sidebar()
    load_page(selected_page)



# Aqui pondremos definiciones, no importa que este abajo de lo de "__main__"

# Lista de símbolos de acciones para mostrar
stocks = ["AAPL", "GOOGL", "MSFT", "AMZN", "META"]


Introduccion = """
<div style="text-align: justify;">

# Proyecto de Backtesting de Estrategias de Asset Allocation

En el dinámico mundo de las inversiones, la capacidad para tomar decisiones informadas y efectivas es fundamental. Esto se vuelve aún más crítico cuando se trata de la asignación de activos, una piedra angular en la gestión de carteras de inversión. El proyecto que se propone abordar aquí se centra en la investigación, documentación, implementación y backtesting de diversas estrategias de quantitative asset allocation. La relevancia de este proyecto radica en su potencial para revolucionar la forma en que los inversores y gestores de carteras abordan la asignación de activos.

## Importancia del Proyecto

La asignación de activos es un proceso esencial en la gestión de inversiones, determinando en gran medida los resultados de las carteras. Una asignación efectiva de activos puede significar la diferencia entre el éxito y el fracaso de una estrategia de inversión. Este proyecto propone no solo explorar, sino también implementar y probar rigurosamente una serie de estrategias de asignación de activos, cada una con sus propios objetivos y métodos. Al hacerlo, este proyecto busca ofrecer:

1. **Evaluación Detallada de Riesgo-Rendimiento:** Mediante la implementación de estrategias como Mínima Varianza y Máximo Sharpe, los inversores pueden evaluar y elegir estrategias que se alineen mejor con sus perfiles de riesgo y objetivos de rendimiento.
2. **Innovación en la Selección de Estrategias:** La diversidad de las estrategias, incluyendo enfoques como Martingala, HRP y Black-Litterman, ofrece una amplia gama de opciones para abordar diferentes necesidades y condiciones del mercado.
3. **Desarrollo de Herramientas de Backtesting Dinámicas:** La realización de backtesting de estas estrategias proporciona una comprensión profunda de su rendimiento histórico y potencial futuro bajo diversas condiciones del mercado.

## Metodología y Desarrollo del Proyecto

El proyecto se desarrollará en varias fases clave:

1. **Investigación y Documentación:** Se realizará una exhaustiva investigación de cada estrategia de asset allocation. Esto incluirá una revisión de la teoría subyacente, los casos de uso históricos, y las ventajas y limitaciones de cada enfoque.
2. **Implementación Utilizando POO:** La programación orientada a objetos (POO) se utilizará para implementar estas estrategias. Este enfoque asegura un código estructurado, modular y escalable. La restricción de no utilizar librerías externas para la implementación desafía al equipo a desarrollar soluciones más profundas y personalizadas.
3. **Backtesting:** Cada estrategia será sometida a un riguroso proceso de backtesting. Esto implica probar las estrategias con datos históricos para evaluar su efectividad y fiabilidad en diferentes escenarios de mercado.
4. **Herramienta Visual para la Selección de Estrategias:** El objetivo final es crear una herramienta visual que permita a los usuarios seleccionar y backtestear estrategias de inversión de forma dinámica y con base en criterios personalizados.

## Aplicaciones y Beneficios

Los resultados de este proyecto tendrán aplicaciones prácticas significativas en el mundo de las inversiones:

- **Toma de Decisiones Informada para Inversores y Gestores de Cartera:** Con una herramienta que permite comparar y contrastar el rendimiento de diversas estrategias de asset allocation, los usuarios pueden tomar decisiones más informadas y adaptadas a sus necesidades.
- **Educación y Transparencia en la Gestión de Inversiones:** Al documentar y compartir los resultados y metodologías, el proyecto contribuye al conocimiento y la transparencia en el campo de la gestión de inversiones.
- **Adaptabilidad a Cambios en el Mercado:** La capacidad de realizar backtesting dinámico permite a los usuarios adaptar sus estrategias a los cambios en el mercado, un aspecto crucial para la gestión exitosa de inversiones en un entorno económico en constante evolución.

En resumen, este proyecto representa una oportunidad emocionante para avanzar en el campo de la asignación de activos, proporcionando herramientas y conocimientos valiosos para una amplia gama de usuarios, desde inversores individuales hasta grandes gestores de carteras.
</div>
                """