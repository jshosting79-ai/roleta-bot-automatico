#!/bin/bash

echo "=========================================="
echo "🚀 CONFIGURANDO AMBIENTE DO BOT"
echo "=========================================="

# Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt-get update -qq

# Instalar Chrome
echo "📦 Instalando Google Chrome..."
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update -qq
sudo apt-get install -y google-chrome-stable

# Instalar ChromeDriver
echo "📦 Instalando ChromeDriver..."
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -q https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip
unzip -q chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
rm chromedriver_linux64.zip

# Instalar dependências Python
echo "📦 Instalando dependências Python..."
pip install --quiet selenium==4.15.2

# Instalar dependências Node.js
echo "📦 Instalando dependências Node.js..."
npm install --silent

# Dar permissões
chmod +x *.py
chmod +x *.sh

echo ""
echo "=========================================="
echo "✅ AMBIENTE CONFIGURADO COM SUCESSO!"
echo "=========================================="
echo ""
echo "Para iniciar o bot, execute:"
echo "  python3 roleta_bot_final.py"
echo ""
echo "=========================================="
