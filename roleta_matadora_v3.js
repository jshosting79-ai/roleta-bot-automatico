// roleta_matadora_v3.js - Versão atualizada com historico_roleta.json
const fs = require('fs');

class RoletaMATADORA {
    constructor() {
        this.historico = [];
        this.acertos = 0;
        this.erros = 0;
        this.arquivoHistoricoUsuario = 'historico_roleta.json';  // Seu arquivo JSON
        this.arquivoHistoricoInterno = 'historico_matadora.json';
        this.arquivoSinal = 'sinal_atual.json';
        this.ultimoSinalAcertou = null;
        
        this.carregarHistorico();
    }

    carregarHistorico() {
        try {
            // Prioriza o arquivo do usuário (historico_roleta.json)
            if (fs.existsSync(this.arquivoHistoricoUsuario)) {
                const dados = JSON.parse(fs.readFileSync(this.arquivoHistoricoUsuario, 'utf8'));
                
                // Suporta diferentes formatos
                if (Array.isArray(dados)) {
                    this.historico = dados;
                } else if (dados.historico && Array.isArray(dados.historico)) {
                    this.historico = dados.historico;
                } else if (dados.numeros && Array.isArray(dados.numeros)) {
                    this.historico = dados.numeros;
                }
                
                console.log(`✅ Histórico carregado de ${this.arquivoHistoricoUsuario}: ${this.historico.length} números`);
            }
            
            // Carrega estatísticas do arquivo interno
            if (fs.existsSync(this.arquivoHistoricoInterno)) {
                const dados = JSON.parse(fs.readFileSync(this.arquivoHistoricoInterno, 'utf8'));
                this.acertos = dados.acertos || 0;
                this.erros = dados.erros || 0;
                this.ultimoSinalAcertou = dados.ultimoSinalAcertou;
            }
        } catch (e) {
            console.error('Erro ao carregar histórico:', e);
        }
    }

    salvarHistorico() {
        try {
            const dados = {
                historico: this.historico,
                acertos: this.acertos,
                erros: this.erros,
                ultimoSinalAcertou: this.ultimoSinalAcertou,
                timestamp: new Date().toISOString()
            };
            fs.writeFileSync(this.arquivoHistoricoInterno, JSON.stringify(dados, null, 2));
        } catch (e) {
            console.error('Erro ao salvar histórico:', e);
        }
    }

    atualizarHistorico(numeros) {
        if (Array.isArray(numeros) && numeros.length > 0) {
            this.historico = numeros.slice(-100); // Mantém últimos 100
            this.salvarHistorico();
        }
    }

    // ANÁLISE MATADORA
    analiseMATADORA() {
        if (this.historico.length < 10) {
            console.log('⚠️  Histórico insuficiente. Mínimo: 10 números');
            return null;
        }

        const ultimos10 = this.historico.slice(-10);
        
        // 4 PADRÕES PRINCIPAIS
        const padroes = {
            'VERMELHO': [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36],
            'PRETO': [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35],
            '1-18': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18],
            '19-36': [19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
        };

        let melhor = null;
        let melhorAtraso = -1;

        // PEGA O PADRÃO COM MAIOR ATRASO
        for (const [nome, numeros] of Object.entries(padroes)) {
            let atraso = 0;
            
            for (let i = this.historico.length - 1; i >= 0; i--) {
                if (numeros.includes(this.historico[i])) {
                    break;
                }
                atraso++;
            }
            
            if (atraso >= 2 && atraso <= 10) {
                if (atraso > melhorAtraso) {
                    melhorAtraso = atraso;
                    melhor = { nome, numeros, atraso };
                }
            }
        }

        // SE NÃO ENCONTROU, USA FREQUÊNCIA BAIXA
        if (!melhor) {
            let menorFrequencia = 999;
            for (const [nome, numeros] of Object.entries(padroes)) {
                const freq10 = ultimos10.filter(n => numeros.includes(n)).length;
                if (freq10 < menorFrequencia) {
                    menorFrequencia = freq10;
                    melhor = { nome, numeros, atraso: 0, motivo: 'baixa_freq' };
                }
            }
        }

        // RESERVA
        let reserva = null;
        let reservaAtraso = -1;

        for (const [nome, numeros] of Object.entries(padroes)) {
            if (nome === melhor.nome) continue;
            
            let atraso = 0;
            for (let i = this.historico.length - 1; i >= 0; i--) {
                if (numeros.includes(this.historico[i])) break;
                atraso++;
            }
            
            if (atraso > reservaAtraso) {
                reservaAtraso = atraso;
                reserva = { nome, numeros, atraso };
            }
        }

        return {
            melhor: {
                ...melhor,
                confianca: melhor.atraso >= 5 ? 90 : melhor.atraso >= 3 ? 70 : 60
            },
            reserva: {
                ...reserva,
                confianca: reservaAtraso >= 4 ? 80 : reservaAtraso >= 2 ? 60 : 50
            }
        };
    }

    salvarSinal(analise) {
        try {
            const sinal = {
                timestamp: new Date().toISOString(),
                principal: {
                    tipo: analise.melhor.nome,
                    atraso: analise.melhor.atraso,
                    confianca: analise.melhor.confianca,
                    numeros: analise.melhor.numeros
                },
                reserva: {
                    tipo: analise.reserva.nome,
                    atraso: analise.reserva.atraso,
                    confianca: analise.reserva.confianca,
                    numeros: analise.reserva.numeros
                },
                estatisticas: {
                    acertos: this.acertos,
                    erros: this.erros,
                    eficiencia: this.acertos + this.erros > 0 
                        ? ((this.acertos / (this.acertos + this.erros)) * 100).toFixed(1)
                        : 0
                },
                ultimoSinalAcertou: this.ultimoSinalAcertou,
                podeApostar: this.ultimoSinalAcertou !== false  // false = esperando acerto
            };
            
            fs.writeFileSync(this.arquivoSinal, JSON.stringify(sinal, null, 2));
            return sinal;
        } catch (e) {
            console.error('Erro ao salvar sinal:', e);
            return null;
        }
    }

    mostrarPlacar() {
        const total = this.acertos + this.erros;
        const percentual = total > 0 ? ((this.acertos / total) * 100).toFixed(1) : 0;
        
        console.log(`📊 ACERTOS: ${this.acertos} | ERROS: ${this.erros} | EFICIÊNCIA: ${percentual}%`);
    }

    executarAnalise() {
        console.log('\n🔍 ANALISANDO...');
        
        const analise = this.analiseMATADORA();
        
        if (!analise) {
            return null;
        }
        
        const { melhor, reserva } = analise;
        
        console.log('💎 APOSTA PRINCIPAL:');
        console.log(`   ${melhor.nome}`);
        console.log(`   Atraso: ${melhor.atraso} rodadas`);
        console.log(`   Confiança: ${melhor.confianca}%`);
        console.log(`   Números: ${melhor.numeros.length}`);
        
        console.log('🛡️  RESERVA:');
        console.log(`   ${reserva.nome}`);
        console.log(`   Atraso: ${reserva.atraso} rodadas`);
        console.log(`   Confiança: ${reserva.confianca}%`);
        
        this.mostrarPlacar();
        
        // Verificar se pode apostar
        if (this.ultimoSinalAcertou === false) {
            console.log('⏸️  AGUARDANDO SINAL ACERTAR ANTES DE APOSTAR NOVAMENTE');
        } else {
            console.log('⏳ Aguardando próximo número...');
        }
        
        return this.salvarSinal(analise);
    }

    registrarResultado(numero, acertou) {
        if (acertou) {
            this.acertos++;
            console.log('🎉 ✅ ACERTOU!');
            this.ultimoSinalAcertou = true;
        } else {
            this.erros++;
            console.log('❌ ERROU');
            this.ultimoSinalAcertou = false;
        }
        
        if (numero !== null && numero !== undefined) {
            this.historico.push(numero);
            if (this.historico.length > 100) {
                this.historico.shift();
            }
        }
        
        this.salvarHistorico();
        this.mostrarPlacar();
    }

    verificarAcerto(numero) {
        // Verifica se o último sinal acertou (para modo observação)
        try {
            if (fs.existsSync(this.arquivoSinal)) {
                const sinal = JSON.parse(fs.readFileSync(this.arquivoSinal, 'utf8'));
                
                const acertouPrincipal = sinal.principal.numeros.includes(numero);
                const acertouReserva = sinal.reserva.numeros.includes(numero);
                
                if (acertouPrincipal || acertouReserva) {
                    console.log('🎉 ✅ ACERTOU!');
                    if (acertouPrincipal) {
                        console.log(`   PRINCIPAL: ${sinal.principal.tipo}`);
                    }
                    if (acertouReserva) {
                        console.log(`   RESERVA: ${sinal.reserva.tipo}`);
                    }
                    this.ultimoSinalAcertou = true;
                    this.acertos++;
                } else {
                    console.log('❌ ERROU');
                    this.ultimoSinalAcertou = false;
                    this.erros++;
                }
                
                this.salvarHistorico();
                this.mostrarPlacar();
            }
        } catch (e) {
            console.error('Erro ao verificar acerto:', e);
        }
    }

    resetarStatus() {
        // Reseta o status de espera
        this.ultimoSinalAcertou = null;
        this.salvarHistorico();
        console.log('✅ Status resetado - pode apostar novamente');
    }
}

// Modo de operação
const args = process.argv.slice(2);
const comando = args[0];

const roleta = new RoletaMATADORA();

switch(comando) {
    case 'analisar':
        roleta.executarAnalise();
        break;
        
    case 'atualizar':
        const numeros = args.slice(1).map(n => parseInt(n)).filter(n => !isNaN(n));
        if (numeros.length > 0) {
            roleta.atualizarHistorico(numeros);
            console.log(`✅ Histórico atualizado com ${numeros.length} números`);
        }
        break;
        
    case 'resultado':
        const numero = parseInt(args[1]);
        const acertou = args[2] === 'true';
        roleta.registrarResultado(numero, acertou);
        break;
        
    case 'verificar':
        // Verifica se o último sinal acertou (modo observação)
        const num = parseInt(args[1]);
        if (!isNaN(num)) {
            roleta.verificarAcerto(num);
        }
        break;
        
    case 'resetar':
        // Reseta o status de espera
        roleta.resetarStatus();
        break;
        
    default:
        roleta.executarAnalise();
}
