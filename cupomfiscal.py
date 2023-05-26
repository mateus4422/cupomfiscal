import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests


def main():
    chave_acesso = st.text_input("Digite a chave de acesso:")
    if st.button("Visualizar"):
        abrir_site(chave_acesso)


def abrir_site(chave_acesso):
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignorar erros de certificado
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-chrome")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://satsp.fazenda.sp.gov.br/COMSAT/Public/ConsultaPublica/ConsultaPublicaCfe.aspx")

    campo_chave = driver.find_element(By.ID, "conteudo_txtChaveAcesso")
    campo_chave.clear()
    campo_chave.send_keys(chave_acesso)

    # Clicar no elemento do captcha
    captcha_checkbox = driver.find_element(By.ID, "recaptcha-anchor")
    captcha_checkbox.click()

    # Resolver o captcha usando a API Buster
    captcha_img = driver.find_element(By.ID, "conteudo_imgCaptcha")
    captcha_base64 = captcha_img.get_attribute("src").split(",")[-1]
    captcha_text = resolver_captcha_buster(captcha_base64)

    # Preencher o campo do captcha com o texto resolvido
    campo_captcha = driver.find_element(By.ID, "conteudo_txtTexto_captcha_serpro_gov_br")
    campo_captcha.clear()
    campo_captcha.send_keys(captcha_text)

    # Outras ações necessárias, como clicar em botões ou submeter o formulário
    # ...

    # Encerrar o driver
    driver.quit()


def resolver_captcha_buster(captcha_base64):
    # Substitua <API_KEY> pela sua chave de API Buster
    api_key = "4AAFJXPVVNYCCMA4MCN66NOEPGEQYCZT"
    url = f"http://api.busterapp.com/in.php?key={api_key}&method=base64&json=1&body={captcha_base64}"

    response = requests.get(url)
    response_json = response.json()

    if response_json["status"] == 1:
        captcha_id = response_json["request"]
        fetch_url = f"http://api.busterapp.com/res.php?key={api_key}&json=1&action=get&id={captcha_id}"

        while True:
            response = requests.get(fetch_url)
            response_json = response.json()

            if response_json["status"] == 1:
                return response_json["text"]

            if response_json["status"] == 2:
                break

    return ""


if __name__ == "__main__":
    main()
