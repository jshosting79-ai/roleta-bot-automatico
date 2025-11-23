#!/usr/bin/env python3
"""
Bot de Automação de Apostas - ApostaTudo Roleta FINAL
Versão com todas as modificações:
- Lê historico_roleta.json
- Aposta fixa de R$ 1,00
- Espera acerto após perda
- Para em +R$5 ou -R$25
"""

import time
import json
import subprocess
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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

class RoletaBotFinal:
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha
        self.VALOR_APOSTA = 1.0  # FIXO R$ 1,00
        self.LUCRO_ALVO = 5.0    # Para em +R$ 5,00
        self.PERDA_MAXIMA = 25.0 # Para em -R$ 25,00
        
        self.driver = None
        self.wait = None
        self.sinal_atual = None
        self.em_jogo = False
        self.aguardando_acerto = False
        
        # Controle de banca
        self.saldo_inicial = 0.0
        self.saldo_atual = 0.0
        self.lucro_prejuizo = 0.0
        
    def iniciar_navegador(self):
        """Inicializa o navegador Chrome"""
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
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.maximize_window()
        
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })
        
        logging.info("✅ Navegador iniciado")
        
    def fazer_login(self):
        """Realiza login no site"""
        logging.info("Acessando site...")
        
        self.driver.get("https://apostatudo.bet.br/games/evolution/xxxtreme-lightning-roulette")
        time.sleep(5)
        
        try:
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
    
    def ler_historico_json(self):
        """Lê números do historico_roleta.json"""
        try:
            if os.path.exists('historico_roleta.json'):
                with open('historico_roleta.json', 'r') as f:
                    dados = json.load(f)
                    
                # Suporta diferentes formatos
                if isinstance(dados, list):
                    numeros = dados
                elif 'historico' in dados:
                    numeros = dados['historico']
                elif 'numeros' in dados:
                    numeros = dados['numeros']
                else:
                    numeros = []
                
                if numeros:
                    logging.info(f"✅ {len(numeros)} números lidos de historico_roleta.json")
                    return numeros[-100:]  # Últimos 100
            
            logging.warning("⚠️  historico_roleta.json não encontrado")
            return []
            
        except Exception as e:
            logging.error(f"Erro ao ler JSON: {e}")
            return []
    
    def atualizar_historico_nodejs(self, numeros):
        """Atualiza histórico no Node.js"""
        if not numeros:
            return False
        
        try:
            cmd = ['node', 'roleta_matadora_v3.js', 'atualizar'] + [str(n) for n in numeros]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                logging.info("✅ Histórico atualizado no Node.js")
                return True
            return False
                
        except Exception as e:
            logging.error(f"Erro ao atualizar: {e}")
            return False
    
    def obter_sinal(self):
        """Obtém sinal do Node.js"""
        try:
            # Executar análise
            result = subprocess.run(
                ['node', 'roleta_matadora_v3.js', 'analisar'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return None
            
            # Ler sinal
            if os.path.exists('sinal_atual.json'):
                with open('sinal_atual.json', 'r') as f:
                    sinal = json.load(f)
                    self.sinal_atual = sinal
                    
                    logging.info("="*60)
                    logging.info("📡 SINAL RECEBIDO")
                    logging.info("="*60)
                    logging.info(f"💎 PRINCIPAL: {sinal['principal']['tipo']}")
                    logging.info(f"   Atraso: {sinal['principal']['atraso']} | Confiança: {sinal['principal']['confianca']}%")
                    logging.info(f"🛡️  RESERVA: {sinal['reserva']['tipo']}")
                    logging.info(f"   Atraso: {sinal['reserva']['atraso']} | Confiança: {sinal['reserva']['confianca']}%")
                    logging.info(f"📊 Eficiência: {sinal['estatisticas']['eficiencia']}%")
                    
                    # Verificar se pode apostar
                    if sinal.get('podeApostar', True):
                        logging.info("✅ PODE APOSTAR")
                        self.aguardando_acerto = False
                    else:
                        logging.info("⏸️  AGUARDANDO ACERTO - NÃO VAI APOSTAR")
                        self.aguardando_acerto = True
                    
                    logging.info("="*60)
                    
                    return sinal
            
            return None
            
        except Exception as e:
            logging.error(f"Erro ao obter sinal: {e}")
            return None
    
    def localizar_botao_aposta(self, tipo_aposta):
        """Localiza botão de aposta"""
        mapeamentos = {
            'VERMELHO': ['red', 'vermelho', 'rouge'],
            'PRETO': ['black', 'preto', 'noir'],
            '1-18': ['1-18', 'low', 'baixo', 'manque'],
            '19-36': ['19-36', 'high', 'alto', 'passe'],
        }
        
        termos = mapeamentos.get(tipo_aposta, [tipo_aposta.lower()])
        
        for termo in termos:
            try:
                elemento = self.driver.find_element(By.XPATH, f"//*[contains(@class, '{termo}')]")
                return elemento
            except:
                pass
            
            try:
                elemento = self.driver.find_element(By.XPATH, f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{termo}')]")
                return elemento
            except:
                pass
        
        return None
    
    def fazer_aposta(self, tipo_aposta):
        """Faz aposta de R$ 1,00"""
        try:
            logging.info(f"🎲 Apostando: {tipo_aposta} - R$ {self.VALOR_APOSTA:.2f}")
            
            botao = self.localizar_botao_aposta(tipo_aposta)
            
            if botao:
                botao.click()
                logging.info(f"✅ Aposta {tipo_aposta} realizada!")
                time.sleep(1)
                return True
            else:
                logging.warning(f"⚠️  Botão {tipo_aposta} não encontrado")
                self.driver.save_screenshot(f'debug_aposta_{int(time.time())}.png')
                return False
                
        except Exception as e:
            logging.error(f"❌ Erro ao apostar: {e}")
            return False
    
    def executar_apostas(self):
        """Executa apostas baseadas no sinal"""
        if not self.sinal_atual:
            return False
        
        # Verificar se deve aguardar acerto
        if self.aguardando_acerto:
            logging.info("⏸️  AGUARDANDO SINAL ACERTAR - PULANDO APOSTAS")
            return False
        
        apostas_feitas = 0
        
        # Aposta principal - SEMPRE R$ 1,00
        principal = self.sinal_atual['principal']
        if principal['confianca'] >= 60:
            if self.fazer_aposta(principal['tipo']):
                apostas_feitas += 1
                self.saldo_atual -= self.VALOR_APOSTA
        
        # Aposta reserva - SEMPRE R$ 1,00
        reserva = self.sinal_atual['reserva']
        if reserva['confianca'] >= 50:
            time.sleep(1)
            if self.fazer_aposta(reserva['tipo']):
                apostas_feitas += 1
                self.saldo_atual -= self.VALOR_APOSTA
        
        if apostas_feitas > 0:
            self.em_jogo = True
            total_apostado = apostas_feitas * self.VALOR_APOSTA
            logging.info(f"✅ {apostas_feitas} aposta(s) - Total: R$ {total_apostado:.2f}")
            self.atualizar_banca()
            return True
        
        return False
    
    def aguardar_resultado(self, timeout=60):
        """Aguarda resultado"""
        logging.info("⏳ Aguardando resultado...")
        
        inicio = time.time()
        
        while time.time() - inicio < timeout:
            try:
                # Aqui você pode implementar lógica para detectar o número
                # Por ora, vamos simular com tempo
                time.sleep(30)
                
                # Ler o próximo número do JSON
                numeros = self.ler_historico_json()
                if numeros and len(numeros) > 0:
                    numero = numeros[-1]
                    logging.info(f"🎯 RESULTADO: {numero}")
                    
                    # Verificar acerto
                    acertou = self.verificar_acerto(numero)
                    self.registrar_resultado(numero, acertou)
                    
                    return numero
                
                time.sleep(5)
                
            except Exception as e:
                logging.debug(f"Erro ao aguardar: {e}")
                time.sleep(5)
        
        return None
    
    def verificar_acerto(self, numero):
        """Verifica se acertou"""
        if not self.sinal_atual:
            return False
        
        principal = self.sinal_atual['principal']
        reserva = self.sinal_atual['reserva']
        
        acertou_principal = numero in principal['numeros']
        acertou_reserva = numero in reserva['numeros']
        
        if acertou_principal or acertou_reserva:
            logging.info("🎉 ✅ ACERTOU!")
            if acertou_principal:
                logging.info(f"   💎 PRINCIPAL: {principal['tipo']}")
                self.saldo_atual += self.VALOR_APOSTA * 2  # Paga 2x
            if acertou_reserva:
                logging.info(f"   🛡️  RESERVA: {reserva['tipo']}")
                self.saldo_atual += self.VALOR_APOSTA * 2
            
            self.aguardando_acerto = False  # Pode apostar novamente
            return True
        else:
            logging.info("❌ ERROU")
            self.aguardando_acerto = True  # Aguarda próximo acerto
            return False
    
    def registrar_resultado(self, numero, acertou):
        """Registra resultado no Node.js"""
        try:
            cmd = ['node', 'roleta_matadora_v3.js', 'resultado', str(numero), str(acertou).lower()]
            subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        except Exception as e:
            logging.error(f"Erro ao registrar: {e}")
    
    def atualizar_banca(self):
        """Atualiza e exibe banca"""
        self.lucro_prejuizo = self.saldo_atual - self.saldo_inicial
        
        logging.info("="*60)
        logging.info("💰 BANCA")
        logging.info(f"   Inicial: R$ {self.saldo_inicial:.2f}")
        logging.info(f"   Atual: R$ {self.saldo_atual:.2f}")
        
        if self.lucro_prejuizo >= 0:
            logging.info(f"   Lucro: +R$ {self.lucro_prejuizo:.2f} 📈")
        else:
            logging.info(f"   Prejuízo: R$ {self.lucro_prejuizo:.2f} 📉")
        
        logging.info("="*60)
    
    def verificar_limites(self):
        """Verifica se atingiu limites"""
        if self.lucro_prejuizo >= self.LUCRO_ALVO:
            logging.info("="*60)
            logging.info(f"🎉 META ATINGIDA! Lucro de R$ {self.lucro_prejuizo:.2f}")
            logging.info("🛑 PARANDO BOT")
            logging.info("="*60)
            return True
        
        if self.lucro_prejuizo <= -self.PERDA_MAXIMA:
            logging.info("="*60)
            logging.info(f"⚠️  LIMITE DE PERDA! Prejuízo de R$ {abs(self.lucro_prejuizo):.2f}")
            logging.info("🛑 PARANDO BOT")
            logging.info("="*60)
            return True
        
        return False
    
    def loop_principal(self):
        """Loop principal"""
        logging.info("🚀 Iniciando loop...")
        
        # Solicitar saldo inicial
        print("\n" + "="*60)
        saldo_input = input("💰 Digite seu saldo inicial (ex: 50): R$ ")
        try:
            self.saldo_inicial = float(saldo_input)
            self.saldo_atual = self.saldo_inicial
        except:
            logging.error("Valor inválido, usando R$ 50,00")
            self.saldo_inicial = 50.0
            self.saldo_atual = 50.0
        
        logging.info(f"💰 Saldo inicial: R$ {self.saldo_inicial:.2f}")
        logging.info(f"🎯 Meta de lucro: +R$ {self.LUCRO_ALVO:.2f}")
        logging.info(f"⚠️  Limite de perda: -R$ {self.PERDA_MAXIMA:.2f}")
        print("="*60 + "\n")
        
        rodada = 0
        
        while True:
            try:
                rodada += 1
                logging.info(f"\n{'='*60}")
                logging.info(f"🎰 RODADA {rodada} - {datetime.now().strftime('%H:%M:%S')}")
                logging.info(f"{'='*60}")
                
                # 1. Ler histórico do JSON
                numeros = self.ler_historico_json()
                
                if len(numeros) >= 10:
                    # 2. Atualizar Node.js
                    self.atualizar_historico_nodejs(numeros)
                    
                    # 3. Obter sinal
                    sinal = self.obter_sinal()
                    
                    if sinal:
                        # 4. Executar apostas (se não estiver aguardando)
                        if self.executar_apostas():
                            # 5. Aguardar resultado
                            self.aguardar_resultado()
                            self.em_jogo = False
                            
                            # 6. Verificar limites
                            if self.verificar_limites():
                                break
                        
                        # Aguardar próxima rodada
                        logging.info("⏸️  Aguardando próxima rodada...")
                        time.sleep(20)
                    else:
                        time.sleep(10)
                else:
                    logging.warning(f"⚠️  Histórico insuficiente ({len(numeros)})")
                    time.sleep(15)
                
            except KeyboardInterrupt:
                logging.info("\n🛑 Bot interrompido")
                break
            except Exception as e:
                logging.error(f"❌ Erro: {e}")
                time.sleep(10)
    
    def iniciar(self):
        """Inicia o bot"""
        try:
            print("\n" + "="*60)
            print("🎰 BOT DE AUTOMAÇÃO - APOSTATUDO ROLETA FINAL")
            print("="*60)
            print(f"📧 Email: {self.email}")
            print(f"💰 Aposta fixa: R$ {self.VALOR_APOSTA:.2f}")
            print(f"🎯 Para em: +R$ {self.LUCRO_ALVO:.2f} ou -R$ {self.PERDA_MAXIMA:.2f}")
            print(f"⏸️  Aguarda acerto após perda")
            print("="*60 + "\n")
            
            self.iniciar_navegador()
            
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
    
    bot = RoletaBotFinal(EMAIL, SENHA)
    bot.iniciar()
