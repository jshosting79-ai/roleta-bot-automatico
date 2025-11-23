#!/usr/bin/env python3
"""
Bot de Automação de Apostas - Versão para Host
Com Chrome local instalado
"""

import time
import json
import subprocess
import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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

class RoletaBotAuto:
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha
        self.VALOR_APOSTA = 1.0
        self.LUCRO_ALVO = 5.0
        self.PERDA_MAXIMA = 25.0
        
        self.driver = None
        self.wait = None
        self.sinal_atual = None
        self.em_jogo = False
        self.aguardando_acerto = False
        
        self.saldo_inicial = 50.0  # Padrão
        self.saldo_atual = 50.0
        self.lucro_prejuizo = 0.0
        self.rodada = 0
        
    def iniciar_navegador(self):
        """Inicializa o navegador Chrome local"""
        logging.info("Iniciando navegador...")
        
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        
        # Caminho para Chrome e ChromeDriver locais
        chrome_local_path = '/home/container/chrome_local/opt/google/chrome/chrome'
        chromedriver_path = '/home/container/chrome_local/chromedriver'
        
        if os.path.exists(chrome_local_path):
            chrome_options.binary_location = chrome_local_path
            logging.info(f"Usando Chrome local: {chrome_local_path}")
        
        if os.path.exists(chromedriver_path):
            service = Service(executable_path=chromedriver_path)
            logging.info(f"Usando ChromeDriver local: {chromedriver_path}")
        else:
            service = Service()
            logging.warning("ChromeDriver local não encontrado, usando padrão")
        
        try:
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            self.driver.maximize_window()
            
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
            })
            
            logging.info("✅ Navegador iniciado")
            return True
        except Exception as e:
            logging.error(f"❌ Erro ao iniciar navegador: {e}")
            return False
        
    def fazer_login(self):
        """Realiza login no site"""
        logging.info("Acessando site...")
        
        try:
            self.driver.get("https://apostatudo.bet.br/games/evolution/xxxtreme-lightning-roulette")
            time.sleep(5)
            
            # Aceitar cookies
            try:
                btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceitar')]"))
                )
                btn.click()
                time.sleep(2)
            except:
                pass
            
            # Confirmar idade
            try:
                btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sim')]"))
                )
                btn.click()
                time.sleep(2)
            except:
                pass
            
            # Botão Entrar
            btn_entrar = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entrar') and not(contains(text(), 'Google'))]"))
            )
            btn_entrar.click()
            time.sleep(3)
            
            # Preencher credenciais
            campo_email = self.wait.until(EC.presence_of_element_located((By.ID, "login")))
            campo_email.clear()
            campo_email.send_keys(self.email)
            time.sleep(1)
            
            campo_senha = self.driver.find_element(By.ID, "password")
            campo_senha.clear()
            campo_senha.send_keys(self.senha)
            time.sleep(1)
            
            # Submit
            btn_submit = self.driver.find_element(By.XPATH, "//button[text()='ENTRAR']")
            btn_submit.click()
            
            logging.info("Aguardando login...")
            time.sleep(8)
            
            # Verificar login
            try:
                self.driver.find_element(By.ID, "login")
                logging.error("❌ Login falhou")
                return False
            except:
                logging.info("✅ Login realizado!")
                return True
                
        except Exception as e:
            logging.error(f"Erro no login: {e}")
            return False
    
    def aguardar_iframe_roleta(self):
        """Aguarda iframe da roleta"""
        logging.info("Aguardando roleta...")
        
        try:
            iframe = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            self.driver.switch_to.frame(iframe)
            logging.info("✅ Roleta carregada")
            time.sleep(8)
            return True
        except Exception as e:
            logging.error(f"Erro ao carregar roleta: {e}")
            return False
    
    def loop_principal(self):
        """Loop principal do bot"""
        logging.info(f"\n✅ Saldo inicial: R$ {self.saldo_inicial:.2f}")
        logging.info("🚀 Iniciando bot...\n")
        
        while True:
            try:
                self.rodada += 1
                
                logging.info("\n" + "="*60)
                logging.info(f"🎰 RODADA {self.rodada} - {datetime.now().strftime('%H:%M:%S')}")
                logging.info("="*60)
                
                # Aqui você implementaria a lógica de apostas
                # Por enquanto, apenas mantém rodando
                
                logging.info("⏳ Aguardando próxima rodada (60s)...")
                time.sleep(60)
                
            except KeyboardInterrupt:
                logging.info("\n\n⚠️  Bot interrompido pelo usuário")
                break
            except Exception as e:
                logging.error(f"❌ Erro: {e}")
                time.sleep(30)
    
    def iniciar(self):
        """Inicia o bot"""
        print("\n" + "="*60)
        print("🎰 BOT DE AUTOMAÇÃO - APOSTATUDO ROLETA")
        print("="*60)
        print(f"📧 Email: {self.email}")
        print(f"💰 Aposta fixa: R$ {self.VALOR_APOSTA:.2f}")
        print(f"🎯 Para em: +R$ {self.LUCRO_ALVO:.2f} ou -R$ {self.PERDA_MAXIMA:.2f}")
        print("="*60 + "\n")
        
        try:
            if not self.iniciar_navegador():
                logging.error("Falha ao iniciar navegador")
                return
            
            if self.fazer_login():
                if self.aguardar_iframe_roleta():
                    time.sleep(5)
                    self.loop_principal()
            
        except Exception as e:
            logging.error(f"❌ Erro fatal: {e}")
        finally:
            if self.driver:
                logging.info("🔚 Fechando...")
                self.driver.quit()

if __name__ == "__main__":
    EMAIL = "ejeujdjdbdbdhd@gmail.com"
    SENHA = "2mBdDe@9@Pw7DSc"
    
    bot = RoletaBotAuto(EMAIL, SENHA)
    bot.iniciar()
