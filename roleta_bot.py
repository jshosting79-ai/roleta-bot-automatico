#!/usr/bin/env python3
"""
Bot de Automação de Apostas - ApostaTudo Roleta
Integra com o script Node.js de análise de sinais
"""

import time
import json
import subprocess
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('roleta_bot.log'),
        logging.StreamHandler()
    ]
)

class RoletaBot:
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha
        self.driver = None
        self.wait = None
        self.historico_numeros = []
        self.ultimo_sinal = None
        self.node_process = None
        
    def iniciar_navegador(self):
        """Inicializa o navegador Chrome com Selenium"""
        logging.info("Iniciando navegador...")
        
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Descomente para modo invisível
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.maximize_window()
        
        logging.info("Navegador iniciado com sucesso")
        
    def fazer_login(self):
        """Realiza login no site ApostaTudo"""
        logging.info("Acessando site ApostaTudo...")
        
        self.driver.get("https://apostatudo.bet.br/games/evolution/xxxtreme-lightning-roulette")
        time.sleep(3)
        
        try:
            # Aceitar cookies se aparecer
            try:
                aceitar_cookies = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceitar todos')]"))
                )
                aceitar_cookies.click()
                time.sleep(1)
            except:
                pass
            
            # Confirmar idade se aparecer
            try:
                btn_sim = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sim')]"))
                )
                btn_sim.click()
                time.sleep(1)
            except:
                pass
            
            # Clicar no botão Entrar
            logging.info("Clicando no botão Entrar...")
            btn_entrar = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entrar')]"))
            )
            btn_entrar.click()
            time.sleep(2)
            
            # Preencher email
            logging.info("Preenchendo credenciais...")
            campo_email = self.wait.until(
                EC.presence_of_element_located((By.ID, "login"))
            )
            campo_email.clear()
            campo_email.send_keys(self.email)
            
            # Preencher senha
            campo_senha = self.driver.find_element(By.ID, "password")
            campo_senha.clear()
            campo_senha.send_keys(self.senha)
            
            # Clicar no botão ENTRAR do formulário
            btn_submit = self.driver.find_element(By.XPATH, "//button[text()='ENTRAR']")
            btn_submit.click()
            
            logging.info("Aguardando login...")
            time.sleep(5)
            
            # Verificar se o login foi bem-sucedido
            if "entrar" not in self.driver.current_url.lower():
                logging.info("Login realizado com sucesso!")
                return True
            else:
                logging.error("Falha no login - verificar credenciais")
                return False
                
        except Exception as e:
            logging.error(f"Erro ao fazer login: {e}")
            return False
    
    def aguardar_iframe_roleta(self):
        """Aguarda o iframe da roleta carregar"""
        logging.info("Aguardando iframe da roleta carregar...")
        
        try:
            # Aguardar iframe da Evolution Gaming
            iframe = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            self.driver.switch_to.frame(iframe)
            logging.info("Iframe da roleta carregado")
            time.sleep(5)
            return True
        except Exception as e:
            logging.error(f"Erro ao carregar iframe: {e}")
            return False
    
    def capturar_numeros_anteriores(self):
        """Captura os números anteriores da roleta"""
        try:
            # Tentar capturar números do histórico visual
            # Isso pode variar dependendo da estrutura do iframe
            numeros = []
            
            # Usar JavaScript para extrair números
            script = """
            var numeros = [];
            var elementos = document.querySelectorAll('[class*="history"], [class*="resultado"], [class*="number"]');
            elementos.forEach(function(el) {
                var texto = el.textContent.trim();
                var num = parseInt(texto);
                if (!isNaN(num) && num >= 0 && num <= 36) {
                    numeros.push(num);
                }
            });
            return numeros;
            """
            
            numeros = self.driver.execute_script(script)
            
            if numeros:
                self.historico_numeros = numeros[-20:]  # Últimos 20 números
                logging.info(f"Números capturados: {self.historico_numeros}")
                return self.historico_numeros
            
        except Exception as e:
            logging.warning(f"Erro ao capturar números: {e}")
        
        return []
    
    def obter_sinal_do_script(self):
        """Executa o script Node.js e captura o sinal de aposta"""
        try:
            # Executar o script Node.js
            result = subprocess.run(
                ['node', 'roleta_matadora.js'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            output = result.stdout
            
            # Extrair informações do sinal
            sinal = {
                'principal': None,
                'reserva': None,
                'confianca_principal': 0,
                'confianca_reserva': 0
            }
            
            # Parsear o output
            if 'APOSTA PRINCIPAL:' in output:
                lines = output.split('\n')
                for i, line in enumerate(lines):
                    if 'APOSTA PRINCIPAL:' in line and i+1 < len(lines):
                        sinal['principal'] = lines[i+1].strip()
                    if 'Confiança:' in line and 'APOSTA PRINCIPAL' in '\n'.join(lines[max(0,i-3):i]):
                        match = re.search(r'(\d+)%', line)
                        if match:
                            sinal['confianca_principal'] = int(match.group(1))
                    if 'RESERVA:' in line and i+1 < len(lines):
                        sinal['reserva'] = lines[i+1].strip()
                    if 'Confiança:' in line and 'RESERVA' in '\n'.join(lines[max(0,i-3):i]):
                        match = re.search(r'(\d+)%', line)
                        if match:
                            sinal['confianca_reserva'] = int(match.group(1))
            
            self.ultimo_sinal = sinal
            logging.info(f"Sinal recebido: {sinal}")
            return sinal
            
        except Exception as e:
            logging.error(f"Erro ao obter sinal: {e}")
            return None
    
    def fazer_aposta(self, tipo_aposta, valor=1.0):
        """Realiza a aposta na roleta"""
        try:
            logging.info(f"Fazendo aposta: {tipo_aposta} - Valor: R$ {valor}")
            
            # Mapeamento de apostas para seletores
            apostas_map = {
                'VERMELHO': 'red',
                'PRETO': 'black',
                '1-18': 'low',
                '19-36': 'high',
                'PAR': 'even',
                'ÍMPAR': 'odd'
            }
            
            # Voltar para o contexto principal se estiver no iframe
            try:
                self.driver.switch_to.default_content()
                iframe = self.driver.find_element(By.TAG_NAME, "iframe")
                self.driver.switch_to.frame(iframe)
            except:
                pass
            
            # Procurar o elemento de aposta
            aposta_class = apostas_map.get(tipo_aposta.upper())
            
            if aposta_class:
                # Tentar diferentes seletores
                seletores = [
                    f"//div[contains(@class, '{aposta_class}')]",
                    f"//button[contains(@class, '{aposta_class}')]",
                    f"//*[contains(text(), '{tipo_aposta}')]"
                ]
                
                for seletor in seletores:
                    try:
                        elemento = self.driver.find_element(By.XPATH, seletor)
                        elemento.click()
                        logging.info(f"Aposta {tipo_aposta} realizada com sucesso!")
                        return True
                    except:
                        continue
            
            # Se não encontrou pelo mapeamento, tentar por texto
            try:
                elemento = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{tipo_aposta}')]")
                elemento.click()
                logging.info(f"Aposta {tipo_aposta} realizada com sucesso!")
                return True
            except:
                pass
            
            logging.warning(f"Não foi possível realizar aposta: {tipo_aposta}")
            return False
            
        except Exception as e:
            logging.error(f"Erro ao fazer aposta: {e}")
            return False
    
    def executar_estrategia(self, sinal):
        """Executa a estratégia de apostas baseada no sinal"""
        if not sinal or not sinal.get('principal'):
            logging.warning("Sinal inválido, pulando aposta")
            return
        
        # Aposta principal
        if sinal['confianca_principal'] >= 70:
            self.fazer_aposta(sinal['principal'], valor=2.0)
        else:
            self.fazer_aposta(sinal['principal'], valor=1.0)
        
        # Aposta reserva se confiança for alta
        if sinal.get('reserva') and sinal['confianca_reserva'] >= 60:
            time.sleep(1)
            self.fazer_aposta(sinal['reserva'], valor=1.0)
    
    def loop_principal(self):
        """Loop principal do bot"""
        logging.info("Iniciando loop principal...")
        
        rodada = 0
        
        while True:
            try:
                rodada += 1
                logging.info(f"\n{'='*50}")
                logging.info(f"RODADA {rodada}")
                logging.info(f"{'='*50}")
                
                # Capturar números anteriores
                numeros = self.capturar_numeros_anteriores()
                
                # Obter sinal do script
                sinal = self.obter_sinal_do_script()
                
                if sinal:
                    # Executar estratégia de apostas
                    self.executar_estrategia(sinal)
                
                # Aguardar próxima rodada (ajustar conforme necessário)
                logging.info("Aguardando próxima rodada...")
                time.sleep(30)  # Aguardar 30 segundos entre rodadas
                
            except KeyboardInterrupt:
                logging.info("Bot interrompido pelo usuário")
                break
            except Exception as e:
                logging.error(f"Erro no loop principal: {e}")
                time.sleep(10)
    
    def iniciar(self):
        """Inicia o bot"""
        try:
            self.iniciar_navegador()
            
            if self.fazer_login():
                if self.aguardar_iframe_roleta():
                    self.loop_principal()
            
        except Exception as e:
            logging.error(f"Erro fatal: {e}")
        finally:
            if self.driver:
                logging.info("Fechando navegador...")
                self.driver.quit()

if __name__ == "__main__":
    # Configurações
    EMAIL = "nsjsjididje@gmail.com"
    SENHA = "mnbvcxz123"
    
    print("="*60)
    print("BOT DE AUTOMAÇÃO DE APOSTAS - APOSTATUDO ROLETA")
    print("="*60)
    print(f"Email: {EMAIL}")
    print("="*60)
    
    bot = RoletaBot(EMAIL, SENHA)
    bot.iniciar()
