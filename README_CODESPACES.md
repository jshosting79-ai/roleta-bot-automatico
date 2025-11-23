# 🎰 Bot de Roleta - GitHub Codespaces

Bot automatizado para apostas em roleta com análise de padrões e sinais inteligentes.

## 🚀 Como Usar no GitHub Codespaces

### 1️⃣ Criar Codespace

1. Faça fork ou clone este repositório no GitHub
2. Clique no botão **Code** → **Codespaces** → **Create codespace on main**
3. Aguarde o ambiente ser configurado automaticamente (2-3 minutos)

### 2️⃣ Configurar Credenciais

Edite o arquivo `roleta_bot_final.py` e atualize suas credenciais:

```python
EMAIL = "seu_email@gmail.com"
SENHA = "sua_senha"
```

Ou edite o arquivo `config.json`:

```json
{
  "credenciais": {
    "email": "seu_email@gmail.com",
    "senha": "sua_senha"
  }
}
```

### 3️⃣ Preparar Histórico

Crie ou edite o arquivo `historico_roleta.json` com os últimos números da roleta:

```json
[5, 19, 32, 33, 31, 16, 8, 10, 36, 1, 33, 25, 14, 7, 22]
```

💡 **Dica**: Coloque pelo menos 10-20 números recentes.

### 4️⃣ Executar o Bot

No terminal do Codespace, execute:

```bash
python3 roleta_bot_final.py
```

O bot irá:
- ✅ Fazer login automaticamente
- ✅ Analisar padrões da roleta
- ✅ Fazer apostas de R$ 1,00
- ✅ Parar em +R$ 5,00 de lucro ou -R$ 25,00 de perda
- ✅ Aguardar acerto após cada perda

## 📊 Monitoramento

### Ver logs em tempo real

```bash
tail -f roleta_bot.log
```

### Ver sinais atuais

```bash
cat sinal_atual.json
```

### Análise manual (sem apostar)

```bash
node roleta_matadora_v3.js analisar
```

## ⚙️ Personalizar

Edite `roleta_bot_final.py` (linhas 40-42):

```python
self.VALOR_APOSTA = 1.0    # Valor por aposta
self.LUCRO_ALVO = 5.0      # Parar ao atingir este lucro
self.PERDA_MAXIMA = 25.0   # Parar ao atingir esta perda
```

## 🔧 Comandos Úteis

### Atualizar histórico via Node.js

```bash
node roleta_matadora_v3.js atualizar 5 19 32 33 31
```

### Verificar se sinal acertou

```bash
node roleta_matadora_v3.js verificar 32
```

### Resetar status de espera

```bash
node roleta_matadora_v3.js resetar
```

## 🛑 Parar o Bot

Pressione `Ctrl+C` no terminal.

## 📝 Arquivos Importantes

- `roleta_bot_final.py` - Bot principal com Selenium
- `roleta_matadora_v3.js` - Análise de padrões em Node.js
- `historico_roleta.json` - Números da roleta
- `config.json` - Configurações
- `sinal_atual.json` - Último sinal gerado
- `roleta_bot.log` - Logs de execução

## ⚠️ Importante

- O bot roda em modo **headless** (sem interface gráfica)
- Mantenha o Codespace ativo enquanto o bot estiver rodando
- Codespaces gratuitos têm limite de 60 horas/mês
- Faça backup do `historico_roleta.json` regularmente

## 🆘 Problemas Comuns

### "ChromeDriver não encontrado"

Execute:
```bash
bash .devcontainer/setup.sh
```

### "Login falhou"

Verifique suas credenciais no arquivo `roleta_bot_final.py`

### "Histórico insuficiente"

Adicione mais números no `historico_roleta.json` (mínimo 10)

## 📚 Documentação Completa

- `COMO_USAR.md` - Guia detalhado de uso
- `GUIA_RAPIDO.md` - Início rápido
- `MODIFICACOES.md` - Histórico de mudanças
- `RESUMO_EXECUTIVO.md` - Visão geral do sistema

## 🎯 Estratégia

O bot usa análise de padrões para identificar:
- **Cores**: VERMELHO vs PRETO
- **Faixas**: 1-18 vs 19-36
- **Atrasos**: Quantas rodadas sem aparecer
- **Confiança**: Probabilidade baseada em histórico

Após cada perda, aguarda um acerto do sinal antes de voltar a apostar.

## 💰 Gestão de Banca

- Aposta fixa de R$ 1,00
- Para automaticamente nos limites configurados
- Exibe saldo e lucro/prejuízo em tempo real

---

**Desenvolvido para GitHub Codespaces** ☁️

Para suporte, consulte a documentação ou abra uma issue.
