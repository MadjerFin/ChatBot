# Instruções: WhatsApp Bot com Selenium

## O que foi corrigido

O erro `DevToolsActivePort file doesn't exist` acontece quando o Chrome não consegue iniciar corretamente. As seguintes correções foram aplicadas:

### Configurações adicionadas no `whatsapp_client.py`:
- `--no-sandbox` - CRÍTICO no Windows, permite Chrome rodar sem sandbox
- `--disable-dev-shm-usage` - CRÍTICO, evita problemas de memória compartilhada
- `--disable-gpu` - Desabilita aceleração GPU que pode causar conflitos
- `--disable-software-rasterizer` - Evita problemas de renderização
- `--start-maximized` - Abre a janela maximizada
- Criação automática do diretório de sessão
- User-Agent real do Chrome para evitar detecção

## Como usar

### 1. Feche TODAS as janelas do Chrome abertas
```bash
# No Windows, pressione Ctrl+Shift+Esc e feche todos os processos "Google Chrome"
```

### 2. Execute como Administrador (IMPORTANTE!)
- Clique com botão direito no terminal/CMD
- Selecione "Executar como administrador"

### 3. Execute o bot
```bash
python main.py
```

### 4. O que vai acontecer:
1. Uma janela do Chrome vai abrir automaticamente
2. O WhatsApp Web vai carregar
3. Aparecerá um QR Code na tela
4. **ESCANEIE O QR CODE** com seu WhatsApp (celular)
   - Abra WhatsApp no celular
   - Vá em "Dispositivos conectados" ou "WhatsApp Web"
   - Escaneie o código
5. Após conectar, o bot ficará ouvindo mensagens
6. **NÃO FECHE A JANELA DO CHROME** - ela precisa ficar aberta

### 5. Como funciona:
- O bot monitora mensagens novas a cada 5 segundos
- Quando alguém envia mensagem, o bot responde automaticamente usando a IA
- A sessão fica salva na pasta `whatsapp_session/`
- Na próxima vez que rodar, não precisará escanear QR Code novamente

## Endpoints disponíveis

### GET /status
Verifica se WhatsApp está conectado
```bash
curl http://localhost:5000/status
```

### POST /chat
Chat via frontend (funciona sem WhatsApp conectado)
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"msg": "Olá!"}'
```

### POST /enviar
Envia mensagem manual via WhatsApp (requer WhatsApp conectado)
```bash
curl -X POST http://localhost:5000/enviar \
  -H "Content-Type: application/json" \
  -d '{"numero": "5511999999999", "mensagem": "Teste"}'
```

## Problemas comuns

### 1. Erro "session not created" persiste
**Solução:**
- Feche TODAS as janelas do Chrome (incluindo em segundo plano)
- Execute o terminal como **Administrador**
- Desative temporariamente o antivírus
- Delete a pasta `whatsapp_session/` e tente novamente

### 2. Chrome não abre
**Solução:**
- Verifique se Google Chrome está instalado
- Reinstale o Chrome se necessário
- Tente executar: `pip install --upgrade selenium webdriver-manager`

### 3. WhatsApp não conecta (QR Code não aparece)
**Solução:**
- Limpe cache do navegador
- Delete a pasta `whatsapp_session/`
- Tente usar navegador em modo anônimo primeiro

### 4. Bot não responde mensagens
**Solução:**
- Verifique se a janela do Chrome está aberta
- Veja os logs no terminal
- Teste enviar mensagem para o número do WhatsApp conectado
- Verifique se `.env` tem a chave `ANTHROPIC_API_KEY` configurada

### 5. "WhatsApp não conectado" no /enviar
**Solução:**
- Aguarde alguns segundos após iniciar
- Verifique `/status` para ver se está conectado
- Escaneie o QR Code se aparecer novamente

## Estrutura do projeto

```
ChatBot/
├── main.py                    # Servidor Flask principal
├── whatsapp_client.py         # Cliente WhatsApp com Selenium
├── duvidas.py                 # Lógica da IA
├── prompts.py                 # Prompts do bot
├── requirements.txt           # Dependências
├── .env                       # Chaves API (não commitar!)
└── whatsapp_session/          # Sessão do WhatsApp (auto-criada)
```

## Arquitetura

```
┌─────────────────┐
│   WhatsApp      │
│   (celular)     │
└────────┬────────┘
         │ QR Code
         ↓
┌─────────────────┐
│  WhatsApp Web   │◄── Selenium controla
│  (Chrome)       │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ whatsapp_client │
│     .py         │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│    main.py      │◄── Flask Server
│   (Flask API)   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   duvidas.py    │◄── Anthropic Claude API
│   (IA Bot)      │
└─────────────────┘
```

## Importante

⚠️ **Avisos:**
- O WhatsApp pode banir contas que usam automação não oficial
- Use em conta de testes, não em conta pessoal importante
- Mantenha a janela do Chrome aberta enquanto o bot estiver rodando
- Não execute múltiplas instâncias simultaneamente
- A sessão expira após ~2 semanas de inatividade

## Alternativa: Voltar para Twilio

Se preferir estabilidade, você pode voltar para Twilio (recomendado para produção):

1. Configure conta no Twilio
2. Configure WhatsApp Business API
3. Reverta para versão anterior do código
4. Use webhooks ao invés de automação de navegador

**Vantagens do Twilio:**
- Mais estável e confiável
- Não viola termos de serviço
- Não requer navegador rodando
- Escalável para produção

**Desvantagens do Twilio:**
- Requer aprovação do WhatsApp Business
- Pode ter custos associados
- Configuração mais complexa inicialmente
