from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

class WhatsAppClient:
    def __init__(self):
        """Inicializa o cliente WhatsApp com Selenium"""
        self.driver = None
        self.wait = None
        self.ultima_mensagem = {}

    def iniciar(self):
        """Inicia o navegador e conecta ao WhatsApp Web"""
        print("🔧 Configurando Chrome...")

        # Configurações do Chrome - CORRIGIDAS para evitar erro DevToolsActivePort
        chrome_options = Options()

        # Cria diretório para sessão se não existir
        session_dir = os.path.abspath("./whatsapp_session")
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)

        # Argumentos essenciais para evitar erros
        chrome_options.add_argument(f"--user-data-dir={session_dir}")
        chrome_options.add_argument("--no-sandbox")  # CRÍTICO no Windows
        chrome_options.add_argument("--disable-dev-shm-usage")  # CRÍTICO
        chrome_options.add_argument("--disable-gpu")  # Previne problemas gráficos
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--start-maximized")  # Abre maximizado
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # Remove indicadores de automação
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # User agent real
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

        try:
            # Inicializa o driver
            print("📥 Baixando ChromeDriver (se necessário)...")
            service = Service(ChromeDriverManager().install())

            print("🚀 Iniciando Chrome...")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)

            print("✅ Chrome iniciado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao iniciar Chrome: {e}")
            print("\n💡 POSSÍVEIS SOLUÇÕES:")
            print("1. Certifique-se que o Google Chrome está instalado")
            print("2. Feche todas as janelas do Chrome abertas")
            print("3. Execute como Administrador")
            print("4. Desative antivírus temporariamente")
            raise

        # Acessa WhatsApp Web
        print("🌐 Abrindo WhatsApp Web...")
        self.driver.get("https://web.whatsapp.com")

        print("\n" + "="*60)
        print("📱 ESCANEIE O QR CODE NO NAVEGADOR QUE ABRIU")
        print("="*60)

        # Aguarda login (procura pela barra de pesquisa)
        try:
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            ))
            print("✅ Login realizado com sucesso!")
        except Exception as e:
            print(f"❌ Timeout esperando login: {e}")
            raise

    def normalizar_numero(self, numero):
        """Normaliza o número de telefone para o formato padrão"""
        # Remove caracteres especiais
        numero = ''.join(filter(str.isdigit, numero))

        # Se não começar com código do país, adiciona +55 (Brasil)
        if not numero.startswith('55'):
            numero = '55' + numero

        return numero

    def enviar_mensagem(self, numero, mensagem):
        """Envia mensagem para um número específico ou nome de contato"""
        try:
            print(f"📤 Enviando mensagem para {numero}...")

            # Se for número (só dígitos), usa URL com phone
            if numero.replace('+', '').isdigit():
                numero_normalizado = self.normalizar_numero(numero)
                url = f"https://web.whatsapp.com/send?phone={numero_normalizado}"
                self.driver.get(url)
                time.sleep(3)
            else:
                # Se for nome de contato, procura na lista de conversas
                print(f"🔍 Procurando contato: {numero}")
                # Já está na conversa, só precisa encontrar o input

            # Aguarda a caixa de mensagem aparecer (múltiplos XPaths possíveis)
            input_box = None
            xpaths_possiveis = [
                '//div[@contenteditable="true"][@data-tab="10"]',
                '//div[@contenteditable="true"][@role="textbox"]',
                '//div[@title="Mensagem"]',
                '//footer//div[@contenteditable="true"]'
            ]

            for xpath in xpaths_possiveis:
                try:
                    input_box = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    break
                except:
                    continue

            if not input_box:
                raise Exception("Não foi possível encontrar a caixa de mensagem")

            # Digita a mensagem
            input_box.click()
            input_box.clear()
            input_box.send_keys(mensagem)
            time.sleep(0.5)

            # Clica no botão enviar (múltiplos XPaths possíveis)
            send_button = None
            xpaths_send = [
                '//span[@data-icon="send"]',
                '//button[@aria-label="Enviar"]',
                '//button//span[@data-icon="send"]'
            ]

            for xpath in xpaths_send:
                try:
                    send_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    break
                except:
                    continue

            if send_button:
                send_button.click()
                print(f"✅ Mensagem enviada para {numero}")
            else:
                # Tenta pressionar Enter
                from selenium.webdriver.common.keys import Keys
                input_box.send_keys(Keys.ENTER)
                print(f"✅ Mensagem enviada para {numero} (via Enter)")

            time.sleep(1)

        except Exception as e:
            print(f"❌ Erro ao enviar mensagem para {numero}: {e}")
            import traceback
            traceback.print_exc()
            raise

    def buscar_novas_mensagens(self):
        """Busca por novas mensagens não lidas - VERSÃO MELHORADA"""
        try:
            # Volta para a página inicial do WhatsApp
            if "chat" in self.driver.current_url:
                self.driver.get("https://web.whatsapp.com")
                time.sleep(2)

            print("🔍 Procurando novas mensagens...")

            # XPaths atualizados para interface nova do WhatsApp Web
            conversas_nao_lidas = self.driver.find_elements(
                By.XPATH,
                '//div[@aria-label]//span[@aria-label]'  # Badge de não lidas
            )

            print(f"📊 Encontradas {len(conversas_nao_lidas)} conversas não lidas")

            mensagens_novas = []

            # Pega todas as conversas (não só as não lidas)
            conversas = self.driver.find_elements(
                By.XPATH,
                '//div[@role="listitem"]'
            )

            print(f"📋 Total de conversas: {len(conversas)}")

            for i, conversa in enumerate(conversas[:10]):  # Limita a 10 primeiras
                try:
                    # Clica na conversa
                    conversa.click()
                    time.sleep(1.5)

                    # Pega o nome/número do contato no header
                    try:
                        nome_elemento = self.driver.find_element(
                            By.XPATH,
                            '//header//div[@role="button"]//span[@dir="auto"]'
                        )
                        nome = nome_elemento.text
                    except:
                        nome_elemento = self.driver.find_element(
                            By.XPATH,
                            '//header//span[@dir="auto"]'
                        )
                        nome = nome_elemento.text

                    print(f"💬 Verificando conversa com: {nome}")

                    # Pega as mensagens RECEBIDAS (message-in)
                    msgs = self.driver.find_elements(
                        By.XPATH,
                        '//div[contains(@class, "message-in")]//span[contains(@class, "selectable-text")]'
                    )

                    if msgs:
                        ultima_msg = msgs[-1].text.strip()

                        # Verifica se já processou essa mensagem
                        chave = f"{nome}:{ultima_msg[:50]}"  # Usa primeiros 50 chars como ID

                        if chave not in self.ultima_mensagem:
                            self.ultima_mensagem[chave] = True
                            print(f"✅ Nova mensagem de {nome}: {ultima_msg[:50]}...")

                            mensagens_novas.append({
                                "numero": nome,
                                "mensagem": ultima_msg
                            })
                        else:
                            print(f"⏭️ Mensagem já processada de {nome}")
                    else:
                        print(f"📭 Nenhuma mensagem recebida de {nome}")

                except Exception as e:
                    print(f"⚠️ Erro ao processar conversa {i}: {e}")
                    continue

            if mensagens_novas:
                print(f"🎯 {len(mensagens_novas)} mensagens novas para processar!")
            else:
                print("😴 Nenhuma mensagem nova")

            return mensagens_novas

        except Exception as e:
            print(f"❌ Erro ao buscar mensagens: {e}")
            import traceback
            traceback.print_exc()
            return []

    def processar_mensagens(self, callback):
        """Loop infinito para processar mensagens recebidas"""
        print("👂 Ouvindo mensagens...")

        while True:
            try:
                novas_msgs = self.buscar_novas_mensagens()

                for msg_data in novas_msgs:
                    numero = msg_data["numero"]
                    mensagem = msg_data["mensagem"]

                    # Chama a função callback para processar
                    if callback:
                        callback(numero, mensagem)

                # Aguarda antes de verificar novamente
                time.sleep(5)

            except Exception as e:
                print(f"❌ Erro no loop de mensagens: {e}")
                time.sleep(10)

    def fechar(self):
        """Fecha o navegador"""
        if self.driver:
            self.driver.quit()
            print("🔴 WhatsApp desconectado")
