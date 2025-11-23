#!/usr/bin/env python3
"""
Bot de Automação de Apostas - ApostaTudo Roleta V2
Versão melhorada com integração completa com Node.js
"""

import time
import json
import subprocess
import os
from datetime import datetime
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

class RoletaBotV2:
    def __init__(self, email, senha, valor_aposta_base=1.0):
        self.email = email
        self.senha = senha
        self.valor_aposta_base = valor_aposta_base
        self.driver = None
        self.wait = None
        self.historico_numeros = []
        self.ultimo_numero = None
        self.sinal_atual = None
        self.em_jogo = False
        
    def iniciar_navegador(self):
        """Inicializa o navegador Chrome com Selenium"""
        logging.info("Iniciando navegador...")
        
        chrome_options = Options()
        # Descomente a linha abaixo para modo invisível
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--window-size=1920,1080')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.maximize_window()
        
        # Executar script para evitar detecção
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })
        
        logging.info("Navegador iniciado com sucesso")
        
    def fazer_login(self):
        """Realiza login no site ApostaTudo"""
        logging.info("Acessando site ApostaTudo...")
        
        self.driver.get("https://apostatudo.bet.br/games/evolution/xxxtreme-lightning-roulette")
        time.sleep(5)
        
        try:
            # Aceitar cookies se aparecer
            try:
                aceitar_cookies = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceitar todos') or contains(text(), 'Aceitar')]"))
                )
                aceitar_cookies.click()
                logging.info("Cookies aceitos")
                time.sleep(2)
            except:
                logging.info("Popup de cookies não encontrado")
            
            # Confirmar idade se aparecer
            try:
                btn_sim = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sim')]"))
                )
                btn_sim.click()
                logging.info("Idade confirmada")
                time.sleep(2)
            except:
                logging.info("Popup de idade não encontrado")
            
            # Clicar no botão Entrar
            logging.info("Procurando botão Entrar...")
            btn_entrar = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entrar') and not(contains(text(), 'Google')) and not(contains(text(), 'Twitch'))]"))
            )
            btn_entrar.click()
            time.sleep(3)
            
            # Preencher email
            logging.info("Preenchendo credenciais...")
            campo_email = self.wait.until(
                EC.presence_of_element_located((By.ID, "login"))
            )
            campo_email.clear()
            campo_email.send_keys(self.email)
            time.sleep(1)
            
            # Preencher senha
            campo_senha = self.driver.find_element(By.ID, "password")
            campo_senha.clear()
            campo_senha.send_keys(self.senha)
            time.sleep(1)
            
            # Clicar no botão ENTRAR do formulário
            btn_submit = self.driver.find_element(By.XPATH, "//button[text()='ENTRAR']")
            btn_submit.click()
            
            logging.info("Aguardando login...")
            time.sleep(8)
            
            # Verificar se ainda está na tela de login
            try:
                self.driver.find_element(By.ID, "login")
                logging.error("Ainda na tela de login - credenciais podem estar incorretas")
                return False
            except:
                logging.info("✅ Login realizado com sucesso!")
                return True
                
        except Exception as e:
            logging.error(f"Erro ao fazer login: {e}")
            self.driver.save_screenshot('erro_login.png')
            return False
    
    def aguardar_iframe_roleta(self):
        """Aguarda o iframe da roleta carregar e muda o contexto"""
        logging.info("Aguardando iframe da roleta carregar...")
        
        try:
            # Aguardar iframe da Evolution Gaming
            iframe = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            self.driver.switch_to.frame(iframe)
            logging.info("✅ Iframe da roleta carregado")
            time.sleep(8)
            return True
        except Exception as e:
            logging.error(f"Erro ao carregar iframe: {e}")
            return False
    
    def capturar_numeros_anteriores(self):
        """Captura os números anteriores da roleta usando múltiplas estratégias"""
        try:
            # Estratégia 1: Buscar por classes comuns de histórico
            scripts = [
                # Script 1: Buscar por elementos de histórico
                """
                var numeros = [];
                var seletores = [
                    '[class*="history"]',
                    '[class*="History"]',
                    '[class*="resultado"]',
                    '[class*="Resultado"]',
                    '[class*="number"]',
                    '[class*="Number"]',
                    '[class*="previous"]',
                    '[class*="past"]'
                ];
                
                seletores.forEach(function(sel) {
                    var elementos = document.querySelectorAll(sel);
                    elementos.forEach(function(el) {
                        var texto = el.textContent || el.innerText;
                        var matches = texto.match(/\\b([0-9]|[1-2][0-9]|3[0-6])\\b/g);
                        if (matches) {
                            matches.forEach(function(m) {
                                var num = parseInt(m);
                                if (!isNaN(num) && num >= 0 && num <= 36) {
                                    numeros.push(num);
                                }
                            });
                        }
                    });
                });
                
                return [...new Set(numeros)].slice(0, 50);
                """,
                
                # Script 2: Buscar em todo o DOM
                """
                var numeros = [];
                var allText = document.body.innerText;
                var matches = allText.match(/\\b([0-9]|[1-2][0-9]|3[0-6])\\b/g);
                if (matches) {
                    matches.forEach(function(m) {
                        var num = parseInt(m);
                        if (!isNaN(num) && num >= 0 && num <= 36) {
                            numeros.push(num);
                        }
                    });
                }
                return numeros.slice(0, 30);
                """
            ]
            
            for i, script in enumerate(scripts):
                try:
                    numeros = self.driver.execute_script(script)
                    if numeros and len(numeros) >= 5:
                        # Remover duplicatas mantendo ordem
                        numeros_unicos = []
                        for n in numeros:
                            if n not in numeros_unicos:
                                numeros_unicos.append(n)
                        
                        self.historico_numeros = numeros_unicos[-30:]  # Últimos 30
                        logging.info(f"✅ {len(self.historico_numeros)} números capturados (Script {i+1})")
                        logging.info(f"Números: {self.historico_numeros[-10:]}")  # Mostrar últimos 10
                        return self.historico_numeros
                except Exception as e:
                    logging.debug(f"Script {i+1} falhou: {e}")
                    continue
            
            logging.warning("⚠️  Não foi possível capturar números automaticamente")
            
        except Exception as e:
            logging.error(f"Erro ao capturar números: {e}")
        
        return self.historico_numeros
    
    def atualizar_historico_nodejs(self):
        """Atualiza o histórico no script Node.js"""
        if not self.historico_numeros:
            logging.warning("Histórico vazio, não é possível atualizar")
            return False
        
        try:
            # Atualizar histórico no Node.js
            cmd = ['node', 'roleta_matadora.js', 'atualizar'] + [str(n) for n in self.historico_numeros]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                logging.info("✅ Histórico atualizado no Node.js")
                return True
            else:
                logging.error(f"Erro ao atualizar histórico: {result.stderr}")
                return False
                
        except Exception as e:
            logging.error(f"Erro ao atualizar histórico: {e}")
            return False
    
    def obter_sinal(self):
        """Obtém sinal de aposta do script Node.js"""
        try:
            # Executar análise
            result = subprocess.run(
                ['node', 'roleta_matadora.js', 'analisar'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                logging.error(f"Erro ao executar análise: {result.stderr}")
                return None
            
            # Ler arquivo de sinal
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
                    logging.info("="*60)
                    
                    return sinal
            
            return None
            
        except Exception as e:
            logging.error(f"Erro ao obter sinal: {e}")
            return None
    
    def localizar_botao_aposta(self, tipo_aposta):
        """Localiza o botão de aposta na interface"""
        # Mapeamento de tipos de aposta
        mapeamentos = {
            'VERMELHO': ['red', 'vermelho', 'rouge'],
            'PRETO': ['black', 'preto', 'noir'],
            '1-18': ['1-18', 'low', 'baixo', 'manque'],
            '19-36': ['19-36', 'high', 'alto', 'passe'],
        }
        
        termos = mapeamentos.get(tipo_aposta, [tipo_aposta.lower()])
        
        # Tentar diferentes estratégias
        for termo in termos:
            try:
                # Estratégia 1: Por classe
                elemento = self.driver.find_element(By.XPATH, f"//*[contains(@class, '{termo}')]")
                return elemento
            except:
                pass
            
            try:
                # Estratégia 2: Por texto
                elemento = self.driver.find_element(By.XPATH, f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{termo}')]")
                return elemento
            except:
                pass
        
        return None
    
    def fazer_aposta(self, tipo_aposta, valor=None):
        """Realiza a aposta na roleta"""
        if valor is None:
            valor = self.valor_aposta_base
        
        try:
            logging.info(f"🎲 Tentando apostar: {tipo_aposta} - Valor: R$ {valor:.2f}")
            
            # Localizar botão de aposta
            botao = self.localizar_botao_aposta(tipo_aposta)
            
            if botao:
                # Clicar no botão
                botao.click()
                logging.info(f"✅ Aposta {tipo_aposta} realizada!")
                time.sleep(1)
                return True
            else:
                logging.warning(f"⚠️  Botão de aposta {tipo_aposta} não encontrado")
                
                # Salvar screenshot para debug
                self.driver.save_screenshot(f'debug_aposta_{tipo_aposta}_{int(time.time())}.png')
                return False
                
        except Exception as e:
            logging.error(f"❌ Erro ao fazer aposta {tipo_aposta}: {e}")
            return False
    
    def executar_estrategia(self):
        """Executa a estratégia de apostas baseada no sinal"""
        if not self.sinal_atual:
            logging.warning("Sem sinal disponível")
            return False
        
        sinal = self.sinal_atual
        apostas_realizadas = 0
        
        # Aposta principal
        principal = sinal['principal']
        if principal['confianca'] >= 60:
            valor = self.valor_aposta_base * (2 if principal['confianca'] >= 80 else 1)
            if self.fazer_aposta(principal['tipo'], valor):
                apostas_realizadas += 1
        
        # Aposta reserva
        reserva = sinal['reserva']
        if reserva['confianca'] >= 50:
            valor = self.valor_aposta_base
            time.sleep(1)
            if self.fazer_aposta(reserva['tipo'], valor):
                apostas_realizadas += 1
        
        if apostas_realizadas > 0:
            self.em_jogo = True
            logging.info(f"✅ {apostas_realizadas} aposta(s) realizada(s)")
            return True
        else:
            logging.warning("⚠️  Nenhuma aposta foi realizada")
            return False
    
    def aguardar_resultado(self, timeout=60):
        """Aguarda o resultado da rodada"""
        logging.info("⏳ Aguardando resultado da rodada...")
        
        inicio = time.time()
        numero_anterior = self.ultimo_numero
        
        while time.time() - inicio < timeout:
            try:
                # Tentar capturar novo número
                numeros = self.capturar_numeros_anteriores()
                
                if numeros and len(numeros) > 0:
                    numero_atual = numeros[-1]
                    
                    if numero_atual != numero_anterior:
                        self.ultimo_numero = numero_atual
                        logging.info(f"🎯 RESULTADO: {numero_atual}")
                        
                        # Verificar se acertou
                        if self.sinal_atual:
                            acertou = self.verificar_acerto(numero_atual)
                            self.registrar_resultado(numero_atual, acertou)
                        
                        return numero_atual
                
                time.sleep(2)
                
            except Exception as e:
                logging.debug(f"Erro ao aguardar resultado: {e}")
                time.sleep(2)
        
        logging.warning("⏰ Timeout ao aguardar resultado")
        return None
    
    def verificar_acerto(self, numero):
        """Verifica se a aposta acertou"""
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
            if acertou_reserva:
                logging.info(f"   🛡️  RESERVA: {reserva['tipo']}")
            return True
        else:
            logging.info("❌ ERROU")
            return False
    
    def registrar_resultado(self, numero, acertou):
        """Registra o resultado no Node.js"""
        try:
            cmd = ['node', 'roleta_matadora.js', 'resultado', str(numero), str(acertou).lower()]
            subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        except Exception as e:
            logging.error(f"Erro ao registrar resultado: {e}")
    
    def loop_principal(self):
        """Loop principal do bot"""
        logging.info("🚀 Iniciando loop principal...")
        
        rodada = 0
        
        while True:
            try:
                rodada += 1
                logging.info(f"\n{'='*60}")
                logging.info(f"🎰 RODADA {rodada} - {datetime.now().strftime('%H:%M:%S')}")
                logging.info(f"{'='*60}")
                
                # 1. Capturar números anteriores
                numeros = self.capturar_numeros_anteriores()
                
                if len(numeros) >= 10:
                    # 2. Atualizar histórico no Node.js
                    self.atualizar_historico_nodejs()
                    
                    # 3. Obter sinal
                    sinal = self.obter_sinal()
                    
                    if sinal:
                        # 4. Executar apostas
                        if self.executar_estrategia():
                            # 5. Aguardar resultado
                            self.aguardar_resultado()
                            self.em_jogo = False
                        
                        # Aguardar próxima rodada
                        logging.info("⏸️  Aguardando próxima rodada...")
                        time.sleep(20)
                    else:
                        logging.warning("⚠️  Não foi possível obter sinal")
                        time.sleep(10)
                else:
                    logging.warning(f"⚠️  Histórico insuficiente ({len(numeros)} números). Aguardando...")
                    time.sleep(15)
                
            except KeyboardInterrupt:
                logging.info("\n🛑 Bot interrompido pelo usuário")
                break
            except Exception as e:
                logging.error(f"❌ Erro no loop principal: {e}")
                self.driver.save_screenshot(f'erro_{int(time.time())}.png')
                time.sleep(10)
    
    def iniciar(self):
        """Inicia o bot"""
        try:
            print("\n" + "="*60)
            print("🎰 BOT DE AUTOMAÇÃO DE APOSTAS - APOSTATUDO ROLETA V2")
            print("="*60)
            print(f"📧 Email: {self.email}")
            print(f"💰 Valor base de aposta: R$ {self.valor_aposta_base:.2f}")
            print("="*60 + "\n")
            
            self.iniciar_navegador()
            
            if self.fazer_login():
                if self.aguardar_iframe_roleta():
                    # Aguardar um pouco para garantir que tudo carregou
                    time.sleep(5)
                    self.loop_principal()
                else:
                    logging.error("❌ Falha ao carregar iframe da roleta")
            else:
                logging.error("❌ Falha no login")
            
        except Exception as e:
            logging.error(f"❌ Erro fatal: {e}")
        finally:
            if self.driver:
                logging.info("🔚 Fechando navegador...")
                self.driver.quit()

if __name__ == "__main__":
    # Configurações
    EMAIL = "nsjsjididje@gmail.com"
    SENHA = "mnbvcxz123"
    VALOR_APOSTA_BASE = 1.0  # Valor base em reais
    
    bot = RoletaBotV2(EMAIL, SENHA, VALOR_APOSTA_BASE)
    bot.iniciar()
