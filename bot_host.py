#!/usr/bin/env python3
"""
Bot de Roleta - Versão Simplificada para Host
Sem Selenium - Apenas análise e sinais
"""

import time
import json
import subprocess
import os
from datetime import datetime
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

class RoletaBotHost:
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha
        self.VALOR_APOSTA = 1.0
        self.LUCRO_ALVO = 5.0
        self.PERDA_MAXIMA = 25.0
        
        self.sinal_atual = None
        self.aguardando_acerto = False
        
        # Controle de banca
        self.saldo_inicial = 0.0
        self.saldo_atual = 0.0
        self.lucro_prejuizo = 0.0
        self.rodada = 0
        
    def ler_historico_json(self):
        """Lê números do historico_roleta.json"""
        try:
            if os.path.exists('historico_roleta.json'):
                with open('historico_roleta.json', 'r') as f:
                    dados = json.load(f)
                    
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
                    return numeros[-100:]
            
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
            result = subprocess.run(
                ['node', 'roleta_matadora_v3.js', 'analisar'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return None
            
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
    
    def simular_apostas(self):
        """Simula apostas (sem Selenium)"""
        if not self.sinal_atual or self.aguardando_acerto:
            logging.info("⏸️  AGUARDANDO SINAL ACERTAR - PULANDO APOSTAS")
            return False
        
        apostas_feitas = 0
        
        principal = self.sinal_atual['principal']
        if principal['confianca'] >= 60:
            logging.info(f"🎲 APOSTA PRINCIPAL: {principal['tipo']} - R$ {self.VALOR_APOSTA:.2f}")
            apostas_feitas += 1
            self.saldo_atual -= self.VALOR_APOSTA
        
        reserva = self.sinal_atual['reserva']
        if reserva['confianca'] >= 50:
            logging.info(f"🎲 APOSTA RESERVA: {reserva['tipo']} - R$ {self.VALOR_APOSTA:.2f}")
            apostas_feitas += 1
            self.saldo_atual -= self.VALOR_APOSTA
        
        if apostas_feitas > 0:
            total_apostado = apostas_feitas * self.VALOR_APOSTA
            logging.info(f"✅ {apostas_feitas} aposta(s) - Total: R$ {total_apostado:.2f}")
            self.atualizar_banca()
            return True
        
        return False
    
    def atualizar_banca(self):
        """Atualiza e exibe banca"""
        self.lucro_prejuizo = self.saldo_atual - self.saldo_inicial
        
        logging.info("\n" + "="*60)
        logging.info("💰 BANCA")
        logging.info(f"   Inicial: R$ {self.saldo_inicial:.2f}")
        logging.info(f"   Atual: R$ {self.saldo_atual:.2f}")
        
        if self.lucro_prejuizo > 0:
            logging.info(f"   Lucro: +R$ {self.lucro_prejuizo:.2f} 📈")
        elif self.lucro_prejuizo < 0:
            logging.info(f"   Prejuízo: R$ {self.lucro_prejuizo:.2f} 📉")
        else:
            logging.info(f"   Neutro: R$ 0.00 ➖")
        
        logging.info("="*60 + "\n")
    
    def verificar_limites(self):
        """Verifica se atingiu limites"""
        if self.lucro_prejuizo >= self.LUCRO_ALVO:
            logging.info("\n" + "🎉"*20)
            logging.info(f"🎉 META ATINGIDA! Lucro de R$ {self.lucro_prejuizo:.2f}")
            logging.info("🛑 PARANDO BOT")
            logging.info("🎉"*20 + "\n")
            return True
        
        if abs(self.lucro_prejuizo) >= self.PERDA_MAXIMA:
            logging.info("\n" + "⚠️ "*20)
            logging.info(f"⚠️  LIMITE DE PERDA! Prejuízo de R$ {abs(self.lucro_prejuizo):.2f}")
            logging.info("🛑 PARANDO BOT")
            logging.info("⚠️ "*20 + "\n")
            return True
        
        return False
    
    def loop_principal(self):
        """Loop principal do bot"""
        logging.info("\n💰 Digite seu saldo inicial (ex: 50): ", end='')
        try:
            self.saldo_inicial = float(input("R$ "))
            self.saldo_atual = self.saldo_inicial
        except:
            logging.error("Valor inválido!")
            return
        
        logging.info(f"\n✅ Saldo inicial: R$ {self.saldo_inicial:.2f}")
        logging.info("🚀 Iniciando bot...\n")
        
        while True:
            try:
                self.rodada += 1
                
                logging.info("\n" + "="*60)
                logging.info(f"🎰 RODADA {self.rodada} - {datetime.now().strftime('%H:%M:%S')}")
                logging.info("="*60)
                
                # Ler histórico
                numeros = self.ler_historico_json()
                if not numeros or len(numeros) < 10:
                    logging.warning("⚠️  Histórico insuficiente. Aguardando...")
                    time.sleep(30)
                    continue
                
                # Atualizar Node.js
                self.atualizar_historico_nodejs(numeros)
                
                # Obter sinal
                sinal = self.obter_sinal()
                if not sinal:
                    logging.warning("⚠️  Sem sinal. Aguardando...")
                    time.sleep(30)
                    continue
                
                # Simular apostas
                self.simular_apostas()
                
                # Verificar limites
                if self.verificar_limites():
                    break
                
                # Aguardar próxima rodada
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
        print("🎰 BOT DE ROLETA - VERSÃO HOST (SEM SELENIUM)")
        print("="*60)
        print(f"📧 Email: {self.email}")
        print(f"💰 Aposta fixa: R$ {self.VALOR_APOSTA:.2f}")
        print(f"🎯 Para em: +R$ {self.LUCRO_ALVO:.2f} ou -R$ {self.PERDA_MAXIMA:.2f}")
        print(f"⏸️  Aguarda acerto após perda")
        print("="*60 + "\n")
        print("⚠️  ATENÇÃO: Esta versão apenas analisa e exibe sinais.")
        print("   Você precisa fazer as apostas manualmente no site.")
        print("="*60 + "\n")
        
        try:
            self.loop_principal()
        except Exception as e:
            logging.error(f"❌ Erro fatal: {e}")

if __name__ == "__main__":
    EMAIL = "ejeujdjdbdbdhd@gmail.com"
    SENHA = "2mBdDe@9@Pw7DSc"
    
    bot = RoletaBotHost(EMAIL, SENHA)
    bot.iniciar()
