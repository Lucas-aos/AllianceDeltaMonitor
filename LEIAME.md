# Alliance Delta Monitor

![Python](https://img.shields.io/badge/python-3.x-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

Ferramenta de monitoramento de pressão baseada em **OCR** para instrumentos **Waters Alliance HPLC**.

Este programa lê o **valor de pressão exibido no software do instrumento** utilizando OCR e calcula variações de pressão (delta) ao longo de **30 e 60 segundos (PSI)** para auxiliar na detecção de instabilidades de pressão durante a operação.

O programa funciona como uma **janela transparente leve**, que pode ser posicionada sobre a interface do software do instrumento.

---

# Funcionalidades

- Leitura de pressão em tempo real via **OCR**
- Cálculo de **delta de pressão em 30 e 60 segundos**
- Janela transparente sobreposta
- Temporizador de execução com opção de **reset**
- Interface gráfica leve construída com **Tkinter**
- Executável standalone para Windows
- Funciona **inteiramente offline**

---

# Como usar

### 1. Abrir a janela Instrument Status

No software Empower 3, abra o painel **Instrument Status**.

Essa janela normalmente pode ser acessada através de um dos seguintes caminhos:

**Opção 1**

View → Instrument Status / Control Panel

**Opção 2**

Instrument → Tools → Diagnostics → Instrument Status

---

### 2. Iniciar o monitor

Execute:

```
AllianceDeltaMonitor.exe
```

Uma pequena **janela transparente** aparecerá na tela.

---

### 3. Alinhar a área de leitura

Mova a janela do monitor para que a área de captura fique posicionada sobre o valor de **Pressure (psi)** exibido na janela Instrument Status.

Diretrizes para alinhamento:

- O valor monitorado é **Pressure (psi)**.
- Alinhe a área de captura com o **valor numérico da pressão**.
- Se necessário, priorize capturar **os números**, mesmo que o texto *"Pressure (psi)"* fique parcialmente fora da área.
- Certifique-se de que os números estejam **claramente visíveis e sem obstruções**.

Depois de alinhado corretamente, o programa começará automaticamente a ler a pressão e calcular os deltas.

---

# Botão Reset

O botão **Reset** executa duas ações:

1. **Reinicia o temporizador de execução**
2. **Limpa o histórico de pressão usado para os cálculos de delta**

Após pressionar Reset, o programa inicia **um novo ciclo de monitoramento**, recalculando os deltas de pressão de **30 e 60 segundos** a partir das novas leituras.

---

# Screenshot

Exemplo da interface:

![Interface](docs/interface.png)

---

# Aviso de Segurança

Este aplicativo captura **apenas uma pequena região da tela** para realizar OCR sobre o valor de pressão exibido pelo software do instrumento.

- Nenhuma captura de tela é armazenada
- Nenhum dado é registrado
- Nenhuma informação é transmitida externamente
- O programa opera **inteiramente de forma local**

---

# Executando a versão Python

Instale as dependências:

```
pip install -r requirements.txt
```

Execute o programa:

```
python delta_pressure.py
```

---

# Executável Standalone

Um executável para Windows já compilado está disponível na seção **Releases**.

Download:

```
AllianceDeltaMonitor.exe
```

Nenhuma instalação de Python é necessária.

---

# Gerar o Executável

Para gerar manualmente o executável usando PyInstaller:

```
pyinstaller --noconfirm --windowed \
--name AllianceDeltaMonitor \
--icon=delta.ico \
--version-file build_tools/version.txt \
--add-data "tesseract;tesseract" \
--add-data "delta.ico;." \
delta_pressure.py
```

---

# Solução de Problemas

### OCR não está lendo corretamente a pressão

Tente o seguinte:

- Verifique se os **números da pressão estão claramente visíveis**
- Evite janelas sobrepostas
- Alinhe a área de captura mais próxima do **valor numérico**
- Garanta **bom contraste visual**

A precisão do OCR depende da clareza e visibilidade dos números na tela.

---

# Autor

Lucas Albuquerque

---

# Licença

Este projeto está licenciado sob a **MIT License**.
