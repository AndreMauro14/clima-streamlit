import dotenv
import os
import requests
import streamlit as st

def fazer_request(url, params=None):
    resposta = requests.get(url, params=params)
    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        st.error(f"Erro ao fazer a requisição: {e}")
        resultado = None
    else:
        resultado = resposta.json()
        return resultado

def pegar_local(local):

    dotenv.load_dotenv()
    token = os.environ['CHAVE_API_OPENWEATHER']

    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'appid' : token,
        'q': local,
        'units':'metric',
        'lang':'pt_br',
    }

    dados_tempo = fazer_request(url=url, params=params)
    return dados_tempo

def main():
    st.title('TA CALOR!')
    st.write("Dados do OpenWeather")
    cidade = st.text_input("Busque uma cidade")
    if not cidade:
        st.stop()

    dados_tempo = pegar_local(local = cidade)
    if not dados_tempo:
        st.warning(f"Dados não encontrados para a cidade {cidade}")
        st.stop()
    clima = dados_tempo['weather'][0]['description']
    temperatura = dados_tempo['main']['temp']
    sensacao = dados_tempo['main']['feels_like']
    umidade = dados_tempo['main']['humidity']
    nuvens = dados_tempo['clouds']['all']

    st.metric(label='Clima atual',value=clima)

    col1,col2 = st.columns(2)

    with col1:
        st.metric(label='Temperatura',value=f'{temperatura}C')
        st.metric(label='Sensação Térmica', value=f'{sensacao}C')
    with col2:
        st.metric(label='Umidade', value=f'{umidade}%')
        st.metric(label='Cobertura de nuvens', value=f'{nuvens}%')

if __name__ == '__main__':
    main()