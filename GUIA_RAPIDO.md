# 🚀 Guia Rápido - Bot Roleta ApostaTudo

## ⚡ Início Rápido (5 minutos)

### 1️⃣ Instalar Dependências

**Windows:**
```cmd
instalar.bat
```

**Linux/Mac:**
```bash
chmod +x instalar.sh
./instalar.sh
```

### 2️⃣ Configurar Credenciais

Edite `config.json`:
```json
{
  "credenciais": {
    "email": "seu_email@gmail.com",
    "senha": "sua_senha"
  }
}
```

### 3️⃣ Executar o Bot

```bash
python roleta_bot_v2.py
```

## 📊 O que o Bot Faz?

1. ✅ Faz login automaticamente
2. ✅ Captura números anteriores da roleta
3. ✅ Analisa padrões (VERMELHO, PRETO, 1-18, 19-36)
4. ✅ Gera sinais com níveis de confiança
5. ✅ Faz apostas automaticamente
6. ✅ Registra resultados e estatísticas

## 🎯 Entendendo os Sinais

```
💎 APOSTA PRINCIPAL: VERMELHO
   Confiança: 90% → Aposta 2x o valor base
   
🛡️  RESERVA: 19-36
   Confiança: 70% → Aposta 1x o valor base
```

### Níveis de Confiança

| Confiança | Ação |
|-----------|------|
| 90%+ | ⭐⭐⭐ Aposta forte (2x) |
| 70-89% | ⭐⭐ Aposta normal (1.5x) |
| 60-69% | ⭐ Aposta conservadora (1x) |
| <60% | ⚠️ Não aposta |

## ⚙️ Configurações Rápidas

### Conservador (Baixo Risco)
```json
{
  "apostas": {
    "valor_base": 1.0,
    "confianca_minima_principal": 70
  }
}
```

### Moderado (Risco Médio)
```json
{
  "apostas": {
    "valor_base": 2.0,
    "confianca_minima_principal": 60
  }
}
```

### Agressivo (Alto Risco)
```json
{
  "apostas": {
    "valor_base": 5.0,
    "confianca_minima_principal": 50
  }
}
```

## 🔍 Comandos Úteis

### Apenas Analisar (Sem Apostar)
```bash
node roleta_matadora.js analisar
```

### Ver Logs em Tempo Real
```bash
tail -f roleta_bot.log
```

### Limpar Histórico
```bash
rm historico_matadora.json
```

## ⚠️ Checklist Antes de Iniciar

- [ ] Python 3.8+ instalado
- [ ] Node.js 14+ instalado
- [ ] Google Chrome instalado
- [ ] Credenciais configuradas em `config.json`
- [ ] Saldo suficiente na conta ApostaTudo
- [ ] Conexão estável com internet

## 🐛 Problemas Comuns

### "Erro ao fazer login"
→ Verifique email e senha no `config.json`

### "ChromeDriver não encontrado"
→ Execute: `pip install webdriver-manager`

### "Não capturou números"
→ Aguarde o jogo carregar completamente (30-60 segundos)

### Bot não faz apostas
→ Verifique se há saldo na conta

## 📈 Dicas de Uso

1. **Comece com valor baixo** (R$ 1,00) para testar
2. **Monitore as primeiras 10 rodadas** antes de aumentar valores
3. **Defina um limite de perda diário** (ex: R$ 50,00)
4. **Pare quando atingir meta de lucro** (ex: +20%)
5. **Não deixe rodando sem supervisão** nas primeiras vezes

## 🎮 Fluxo de Operação

```
Iniciar Bot
    ↓
Fazer Login
    ↓
Carregar Roleta
    ↓
Capturar Números ←─────┐
    ↓                  │
Analisar Padrões       │
    ↓                  │
Gerar Sinal            │
    ↓                  │
Fazer Apostas          │
    ↓                  │
Aguardar Resultado     │
    ↓                  │
Registrar Acerto/Erro  │
    ↓                  │
Aguardar Próxima ──────┘
```

## 📞 Precisa de Ajuda?

1. Leia o `README.md` completo
2. Verifique os logs em `roleta_bot.log`
3. Consulte screenshots de erro salvos automaticamente

## ⚡ Atalhos de Teclado

- `Ctrl+C` - Parar o bot
- `Ctrl+Z` - Pausar (Linux/Mac)

## 🎯 Meta de Eficiência

**Objetivo**: Manter eficiência acima de 60%

```
📊 ACERTOS: 170 | ERROS: 50 | EFICIÊNCIA: 77.3%
                                          ↑
                                    Muito bom!
```

- **75%+** = Excelente ⭐⭐⭐
- **65-74%** = Bom ⭐⭐
- **55-64%** = Aceitável ⭐
- **<55%** = Revisar estratégia ⚠️

## 🔄 Atualizar Histórico Manualmente

Se o bot não capturar números automaticamente:

```bash
node roleta_matadora.js atualizar 5 19 32 33 31 16 8 10 36 1
```

## 💡 Lembre-se

- ⚠️ **Apostas envolvem riscos financeiros**
- 🎓 **Use para aprendizado e diversão**
- 💰 **Nunca aposte mais do que pode perder**
- 🛑 **Pare se estiver perdendo muito**
- 📊 **Acompanhe suas estatísticas**

---

**Pronto para começar? Execute:**
```bash
python roleta_bot_v2.py
```

**Boa sorte! 🍀**
