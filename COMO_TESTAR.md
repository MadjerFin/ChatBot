# Como Testar o Bot WhatsApp

## ✅ WhatsApp já está logado! Agora vamos fazer o bot responder

### O que foi corrigido:

1. **Busca de mensagens melhorada** - Agora procura em todas as conversas recentes
2. **Logs detalhados** - Você verá exatamente o que o bot está fazendo
3. **Envio de mensagens corrigido** - Funciona com nomes de contatos e números
4. **Múltiplos XPaths** - Compatível com diferentes versões do WhatsApp Web

---

## 🧪 Teste 1: Verificar se está funcionando

### 1. Execute o bot
```bash
python main.py
```

### 2. Aguarde aparecer:
```
✅ WhatsApp conectado e pronto!
👂 Ouvindo mensagens...
🔍 Procurando novas mensagens...
```

### 3. Envie uma mensagem para o WhatsApp logado
- Pegue outro celular ou peça para alguém te mandar uma mensagem
- Ou use o WhatsApp do seu próprio celular para enviar mensagem para você mesmo

### 4. Observe os logs no terminal:
```
📋 Total de conversas: X
💬 Verificando conversa com: Nome do Contato
✅ Nova mensagem de Nome: Olá!
🎯 1 mensagens novas para processar!
📱 Mensagem de Nome: Olá!
📤 Enviando mensagem para Nome...
✅ Mensagem enviada para Nome
✅ Resposta enviada para Nome
```

---

## 🧪 Teste 2: Enviar mensagem manual (via API)

### 1. Bot deve estar rodando (`python main.py`)

### 2. Em outro terminal, teste enviar:

**Via número de telefone:**
```bash
curl -X POST http://localhost:5000/enviar -H "Content-Type: application/json" -d "{\"numero\": \"5511999999999\", \"mensagem\": \"Teste do bot\"}"
```

**Via nome de contato (se já tem conversa aberta):**
```bash
curl -X POST http://localhost:5000/enviar -H "Content-Type: application/json" -d "{\"numero\": \"Nome do Contato\", \"mensagem\": \"Teste do bot\"}"
```

---

## 🧪 Teste 3: Verificar status

```bash
curl http://localhost:5000/status
```

**Resposta esperada:**
```json
{
  "whatsapp_conectado": true,
  "servidor": "online"
}
```

---

## 📊 Entendendo os Logs

### Logs normais (funcionando):
```
🔍 Procurando novas mensagens...
📊 Encontradas X conversas não lidas
📋 Total de conversas: Y
💬 Verificando conversa com: João
✅ Nova mensagem de João: Olá!
📤 Enviando mensagem para João...
✅ Mensagem enviada para João
```

### Logs quando não há mensagens novas:
```
🔍 Procurando novas mensagens...
📊 Encontradas 0 conversas não lidas
📋 Total de conversas: 5
💬 Verificando conversa com: João
⏭️ Mensagem já processada de João
😴 Nenhuma mensagem nova
```

### Logs de erro (algo errado):
```
❌ Erro ao processar conversa 0: Message: ...
⚠️ Erro ao processar conversa: ...
❌ Erro ao buscar mensagens: ...
```

---

## 🐛 Problemas Comuns

### 1. Bot não detecta mensagens novas
**Sintomas:**
- Você envia mensagem mas bot não responde
- Logs mostram "😴 Nenhuma mensagem nova"

**Soluções:**
- Aguarde 5 segundos (tempo do loop)
- Verifique se a conversa aparece na lista do WhatsApp Web
- Envie mensagem de OUTRO número (não o mesmo que está logado)
- Olhe os logs para ver se está detectando as conversas

### 2. Bot detecta mas não envia resposta
**Sintomas:**
- Logs mostram "✅ Nova mensagem de X"
- Mas não mostra "✅ Mensagem enviada"

**Soluções:**
- Verifique se `.env` tem `ANTHROPIC_API_KEY` configurada
- Teste chamar a IA manualmente: `curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d '{"msg":"teste"}'`
- Veja se há erro da API Anthropic nos logs

### 3. XPath não encontrado
**Sintomas:**
- `❌ Não foi possível encontrar a caixa de mensagem`

**Soluções:**
- WhatsApp Web mudou a interface
- Abra o Chrome e inspecione elemento (F12)
- Me avise para atualizar os XPaths

### 4. Bot processa mesma mensagem várias vezes
**Sintomas:**
- Você recebe resposta duplicada

**Soluções:**
- O sistema de cache não está funcionando
- Reinicie o bot (`Ctrl+C` e `python main.py`)

---

## 🎯 Fluxo Completo Esperado

1. **Usuário envia:** "Olá"
2. **Bot detecta (a cada 5s):**
   ```
   🔍 Procurando novas mensagens...
   💬 Verificando conversa com: João
   ✅ Nova mensagem de João: Olá
   ```
3. **Bot processa:**
   ```
   📱 Mensagem de João: Olá
   ```
4. **IA responde:**
   - Chama `bot()` do `duvidas.py`
   - Usa API Anthropic Claude
5. **Bot envia:**
   ```
   📤 Enviando mensagem para João...
   ✅ Mensagem enviada para João
   ✅ Resposta enviada para João
   ```
6. **Usuário recebe resposta no WhatsApp**

---

## 🔧 Debug Avançado

### Ver HTML da página (se XPath não funcionar):
```python
# Adicione no whatsapp_client.py temporariamente:
print(self.driver.page_source)
```

### Tirar screenshot da tela:
```python
# Adicione no whatsapp_client.py:
self.driver.save_screenshot("debug.png")
```

### Testar IA separadamente:
```bash
python -c "from duvidas import bot; print(bot('teste'))"
```

---

## 📝 Checklist de Funcionamento

- [ ] Chrome abre automaticamente
- [ ] WhatsApp Web carrega
- [ ] Login feito (QR Code escaneado)
- [ ] Logs mostram "👂 Ouvindo mensagens..."
- [ ] Logs mostram "🔍 Procurando novas mensagens..." a cada 5s
- [ ] Ao enviar mensagem, logs mostram "✅ Nova mensagem de X"
- [ ] Bot envia resposta automaticamente
- [ ] Resposta aparece no WhatsApp

---

## ✅ Próximos Passos

Se tudo funcionar:
1. Deixe rodando 24/7
2. Configure deploy em servidor (Heroku, AWS, etc)
3. Adicione mais funcionalidades (comandos, mídia, etc)

Se não funcionar:
1. Copie os logs de erro
2. Me envie para analisar
3. Verificaremos os XPaths
