# 🚀 Como Usar - Versão Atualizada

## ⚡ Início Rápido (3 Passos)

### 1️⃣ Preparar Histórico

Crie o arquivo `historico_roleta.json` com seus números:

```json
[5, 19, 32, 33, 31, 16, 8, 10, 36, 1, 33, 25]
```

💡 **Dica**: Coloque os últimos 20-50 números da roleta.

### 2️⃣ Executar Bot

```bash
python roleta_bot_final.py
```

### 3️⃣ Informar Saldo

```
💰 Digite seu saldo inicial (ex: 50): R$ 50
```

**Pronto!** O bot vai começar a funcionar.

---

## 📋 O Que o Bot Faz

### ✅ Funcionalidades

1. **Lê seus números** do `historico_roleta.json`
2. **Analisa padrões** (VERMELHO, PRETO, 1-18, 19-36)
3. **Aposta R$ 1,00** sempre (fixo)
4. **Se perder**: Aguarda um sinal acertar antes de apostar novamente
5. **Para automaticamente** em:
   - ✅ **+R$ 5,00 de lucro**
   - ❌ **-R$ 25,00 de perda**

---

## 🎮 Exemplo de Uso

### Passo 1: Criar historico_roleta.json

```bash
echo '[5, 19, 32, 33, 31, 16, 8, 10, 36, 1]' > historico_roleta.json
```

### Passo 2: Executar

```bash
python roleta_bot_final.py
```

### Passo 3: Acompanhar

```
🎰 BOT DE AUTOMAÇÃO - APOSTATUDO ROLETA FINAL
====================================
📧 Email: seu_email@gmail.com
💰 Aposta fixa: R$ 1.00
🎯 Para em: +R$ 5.00 ou -R$ 25.00
⏸️  Aguarda acerto após perda
====================================

💰 Digite seu saldo inicial (ex: 50): R$ 50

====================================
🎰 RODADA 1 - 14:30:15
====================================
✅ 10 números lidos de historico_roleta.json
✅ Histórico atualizado no Node.js

====================================
📡 SINAL RECEBIDO
====================================
💎 PRINCIPAL: VERMELHO
   Atraso: 5 | Confiança: 90%
🛡️  RESERVA: 19-36
   Atraso: 3 | Confiança: 70%
📊 Eficiência: 77.3%
✅ PODE APOSTAR
====================================

🎲 Apostando: VERMELHO - R$ 1.00
✅ Aposta VERMELHO realizada!
✅ 1 aposta(s) - Total: R$ 1.00

====================================
💰 BANCA
   Inicial: R$ 50.00
   Atual: R$ 49.00
   Prejuízo: R$ -1.00 📉
====================================

⏳ Aguardando resultado...
🎯 RESULTADO: 32
🎉 ✅ ACERTOU!
   💎 PRINCIPAL: VERMELHO

====================================
💰 BANCA
   Inicial: R$ 50.00
   Atual: R$ 51.00
   Lucro: +R$ 1.00 📈
====================================
```

---

## 🔄 Atualizar Números Durante Execução

### Opção 1: Atualizar JSON Manualmente

Edite `historico_roleta.json` e adicione novos números:

```json
[5, 19, 32, 33, 31, 16, 8, 10, 36, 1, 33, 25, 14, 7]
```

O bot vai ler automaticamente na próxima rodada.

### Opção 2: Usar Comando Node.js

```bash
node roleta_matadora_v3.js atualizar 5 19 32 33 31 16
```

---

## ⏸️ Sistema de Espera Após Perda

### Como Funciona

```
Rodada 1: Aposta VERMELHO → PERDEU ❌
   ↓
Rodada 2: Sinal PRETO → NÃO APOSTA (aguardando)
   ↓
Rodada 3: Sinal 1-18 → NÃO APOSTA (aguardando)
   ↓
Rodada 4: Sinal VERMELHO → ACERTOU ✅ (sem apostar)
   ↓
Rodada 5: Sinal PRETO → APOSTA NOVAMENTE 🎲
```

### Por Que Isso?

- Evita sequências de perdas
- Aguarda o padrão "esquentar"
- Mais seguro para sua banca

---

## 🎯 Limites de Banca

### Para Automaticamente

| Situação | Limite | Ação |
|----------|--------|------|
| **Lucro** | +R$ 5,00 | 🛑 Para e mostra lucro |
| **Perda** | -R$ 25,00 | 🛑 Para e mostra prejuízo |

### Exemplo

```
Saldo inicial: R$ 50,00

Cenário 1 - Atingiu Meta:
R$ 50 → R$ 51 → R$ 52 → R$ 54 → R$ 55
🎉 META ATINGIDA! Lucro de R$ 5.00
🛑 PARANDO BOT

Cenário 2 - Atingiu Limite:
R$ 50 → R$ 48 → R$ 45 → R$ 30 → R$ 25
⚠️  LIMITE DE PERDA! Prejuízo de R$ 25.00
🛑 PARANDO BOT
```

---

## 📊 Monitoramento

### Ver Logs em Tempo Real

```bash
tail -f roleta_bot.log
```

### Ver Histórico de Sinais

```bash
cat sinal_atual.json
```

### Ver Estatísticas

```bash
cat historico_matadora.json
```

---

## 🔧 Comandos Úteis

### Apenas Analisar (Sem Apostar)

```bash
node roleta_matadora_v3.js analisar
```

### Verificar Se Sinal Acertou

```bash
node roleta_matadora_v3.js verificar 32
```

### Resetar Status de Espera

Se o bot ficou travado aguardando:

```bash
node roleta_matadora_v3.js resetar
```

### Atualizar Números

```bash
node roleta_matadora_v3.js atualizar 5 19 32 33 31
```

---

## ⚙️ Personalizar Limites

Edite `roleta_bot_final.py` (linhas 30-32):

```python
self.VALOR_APOSTA = 1.0    # Mude para 2.0, 5.0, etc
self.LUCRO_ALVO = 5.0      # Mude para 10.0, 20.0, etc
self.PERDA_MAXIMA = 25.0   # Mude para 50.0, 100.0, etc
```

**Exemplo**: Para apostar R$ 2,00 e parar em +R$ 10 ou -R$ 50:

```python
self.VALOR_APOSTA = 2.0
self.LUCRO_ALVO = 10.0
self.PERDA_MAXIMA = 50.0
```

---

## 🐛 Solução de Problemas

### "historico_roleta.json não encontrado"

**Solução**: Crie o arquivo:
```bash
echo '[5, 19, 32, 33, 31]' > historico_roleta.json
```

### "Histórico insuficiente"

**Solução**: Adicione mais números (mínimo 10):
```json
[5, 19, 32, 33, 31, 16, 8, 10, 36, 1, 33, 25]
```

### Bot não para de "aguardar acerto"

**Solução**: Resetar status:
```bash
node roleta_matadora_v3.js resetar
```

### Bot não para nos limites

**Solução**: Verificar se está atualizando o saldo corretamente. Veja os logs.

---

## 📝 Formato do historico_roleta.json

### Formato 1: Array Simples (Recomendado)

```json
[5, 19, 32, 33, 31, 16, 8, 10, 36, 1]
```

### Formato 2: Objeto com "historico"

```json
{
  "historico": [5, 19, 32, 33, 31, 16, 8, 10, 36, 1]
}
```

### Formato 3: Objeto com "numeros"

```json
{
  "numeros": [5, 19, 32, 33, 31, 16, 8, 10, 36, 1],
  "timestamp": "2024-11-23T14:30:00Z"
}
```

**Todos funcionam!** O bot detecta automaticamente.

---

## 🎯 Dicas de Uso

1. **Comece com saldo baixo** (R$ 20-50) para testar
2. **Mantenha historico_roleta.json atualizado** com números recentes
3. **Monitore as primeiras rodadas** antes de deixar automático
4. **Respeite os limites** - não mude durante execução
5. **Faça backup** do historico_roleta.json

---

## 📞 Precisa de Ajuda?

1. Leia `MODIFICACOES.md` para entender as mudanças
2. Consulte `README.md` para documentação completa
3. Veja os logs em `roleta_bot.log`
4. Verifique screenshots de erro (se houver)

---

## ✅ Checklist Antes de Iniciar

- [ ] Python 3.8+ instalado
- [ ] Node.js 14+ instalado
- [ ] Arquivo `historico_roleta.json` criado
- [ ] Mínimo 10 números no histórico
- [ ] Credenciais configuradas
- [ ] Saldo suficiente na conta

---

**🎉 Pronto para começar!**

```bash
python roleta_bot_final.py
```

**Boa sorte! 🍀**
