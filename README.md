# 🎰 Bot de Automação de Apostas - ApostaTudo Roleta

Sistema completo de automação de apostas na roleta XXXtreme Lightning Roulette do site ApostaTudo.bet.br

## 📋 Descrição

Este bot integra:
- **Python + Selenium**: Automação do navegador e interface com o site
- **Node.js**: Análise de padrões e geração de sinais de apostas
- **Estratégia inteligente**: Baseada em atraso de padrões e frequência

## 🚀 Funcionalidades

✅ Login automático no site  
✅ Captura de números anteriores da roleta  
✅ Análise inteligente de padrões (VERMELHO, PRETO, 1-18, 19-36)  
✅ Geração de sinais com níveis de confiança  
✅ Apostas automáticas baseadas nos sinais  
✅ Registro de acertos e erros  
✅ Logs detalhados de todas as operações  

## 📦 Requisitos

### Sistema Operacional
- Windows, Linux ou macOS

### Software Necessário
1. **Python 3.8+**
   - Download: https://www.python.org/downloads/

2. **Node.js 14+**
   - Download: https://nodejs.org/

3. **Google Chrome**
   - Download: https://www.google.com/chrome/

4. **ChromeDriver** (compatível com sua versão do Chrome)
   - Download: https://chromedriver.chromium.org/
   - Ou instale automaticamente via webdriver-manager

## 🔧 Instalação

### 1. Instalar dependências Python

```bash
pip install -r requirements.txt
```

Ou manualmente:
```bash
pip install selenium webdriver-manager
```

### 2. Verificar Node.js

```bash
node --version
npm --version
```

### 3. Configurar credenciais

Edite o arquivo `config.json` com suas credenciais:

```json
{
  "credenciais": {
    "email": "seu_email@gmail.com",
    "senha": "sua_senha"
  },
  "apostas": {
    "valor_base": 1.0
  }
}
```

## 🎮 Como Usar

### Modo 1: Bot Completo (Recomendado)

Execute o bot versão 2 que inclui todas as funcionalidades:

```bash
python roleta_bot_v2.py
```

### Modo 2: Apenas Análise

Para apenas ver os sinais sem fazer apostas:

```bash
node roleta_matadora.js analisar
```

### Modo 3: Atualizar Histórico Manualmente

```bash
node roleta_matadora.js atualizar 5 19 32 33 31 16
```

## 📊 Entendendo os Sinais

O sistema analisa 4 padrões principais:

| Padrão | Números |
|--------|---------|
| **VERMELHO** | 1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36 |
| **PRETO** | 2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35 |
| **1-18** | 1 a 18 |
| **19-36** | 19 a 36 |

### Exemplo de Sinal

```
💎 APOSTA PRINCIPAL:
   VERMELHO
   Atraso: 5 rodadas
   Confiança: 90%
   
🛡️  RESERVA:
   19-36
   Atraso: 3 rodadas
   Confiança: 70%
   
📊 ACERTOS: 170 | ERROS: 50 | EFICIÊNCIA: 77.3%
```

## ⚙️ Configurações Avançadas

### config.json

```json
{
  "apostas": {
    "valor_base": 1.0,                    // Valor base de aposta em R$
    "multiplicador_alta_confianca": 2.0,  // Multiplica valor se confiança >= 80%
    "confianca_minima_principal": 60,     // Confiança mínima para apostar
    "confianca_minima_reserva": 50        // Confiança mínima para aposta reserva
  },
  "navegador": {
    "headless": false,                    // true = navegador invisível
    "timeout": 20,                        // Timeout para carregar elementos
    "aguardar_resultado": 60              // Tempo máximo para aguardar resultado
  },
  "estrategia": {
    "historico_minimo": 10                // Mínimo de números para análise
  }
}
```

## 📁 Estrutura de Arquivos

```
roleta_bot/
├── roleta_bot_v2.py          # Bot principal (Python)
├── roleta_matadora.js        # Análise de sinais (Node.js)
├── config.json               # Configurações
├── requirements.txt          # Dependências Python
├── package.json              # Configuração Node.js
├── README.md                 # Esta documentação
├── historico_matadora.json   # Histórico de números (gerado)
├── sinal_atual.json          # Último sinal (gerado)
└── roleta_bot.log            # Logs (gerado)
```

## 🔍 Logs e Debug

### Visualizar Logs em Tempo Real

```bash
tail -f roleta_bot.log
```

### Screenshots de Erro

O bot salva screenshots automaticamente quando encontra erros:
- `erro_login.png` - Erro no login
- `debug_aposta_*.png` - Erro ao fazer aposta
- `erro_*.png` - Outros erros

## ⚠️ Avisos Importantes

1. **Responsabilidade**: Este bot é apenas para fins educacionais. Apostas envolvem riscos financeiros.

2. **Credenciais**: Mantenha suas credenciais seguras. Nunca compartilhe o arquivo `config.json`.

3. **Detecção**: Sites podem detectar automação. Use com moderação.

4. **Saldo**: Certifique-se de ter saldo suficiente na conta antes de iniciar.

5. **Conexão**: Mantenha uma conexão estável com a internet.

## 🐛 Solução de Problemas

### Erro: "ChromeDriver não encontrado"

**Solução**: Instale o webdriver-manager
```bash
pip install webdriver-manager
```

### Erro: "Login falhou"

**Soluções**:
1. Verifique suas credenciais no `config.json`
2. Tente fazer login manualmente primeiro
3. Verifique se não há CAPTCHA

### Erro: "Não foi possível capturar números"

**Soluções**:
1. Aguarde o jogo carregar completamente
2. Verifique sua conexão com a internet
3. O iframe pode ter mudado - aguarde atualização do script

### Bot não faz apostas

**Soluções**:
1. Verifique se há saldo suficiente
2. Aumente o tempo de espera nas configurações
3. Verifique os logs para detalhes

## 📈 Estratégia de Apostas

### Lógica de Atraso

O sistema identifica padrões que não aparecem há várias rodadas:
- **Atraso 2-4**: Confiança baixa (50-60%)
- **Atraso 5-7**: Confiança média (70-80%)
- **Atraso 8+**: Confiança alta (90%)

### Gestão de Banca

**Recomendações**:
- Valor base: 1% do saldo total
- Nunca aposte mais de 5% do saldo em uma rodada
- Defina um limite de perda diário

### Exemplo de Configuração Conservadora

```json
{
  "apostas": {
    "valor_base": 1.0,
    "confianca_minima_principal": 70,
    "confianca_minima_reserva": 60
  }
}
```

### Exemplo de Configuração Agressiva

```json
{
  "apostas": {
    "valor_base": 2.0,
    "multiplicador_alta_confianca": 3.0,
    "confianca_minima_principal": 50,
    "confianca_minima_reserva": 40
  }
}
```

## 🔄 Atualizações Futuras

Recursos planejados:
- [ ] Interface gráfica (GUI)
- [ ] Suporte a múltiplas estratégias
- [ ] Sistema de Martingale
- [ ] Notificações por Telegram
- [ ] Dashboard web de estatísticas
- [ ] Suporte a outros jogos

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs em `roleta_bot.log`
2. Consulte a seção de Solução de Problemas
3. Revise as configurações em `config.json`

## 📄 Licença

Este projeto é fornecido "como está", sem garantias de qualquer tipo.

---

**⚠️ AVISO LEGAL**: Apostas envolvem riscos. Jogue com responsabilidade. Este software é apenas para fins educacionais.
