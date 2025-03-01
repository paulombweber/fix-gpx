# Script de Correção de Pausas em Arquivos GPX

Este script processa um arquivo GPX, identifica uma seção de pausa durante uma atividade e ajusta os dados do GPX para contabilizar a pausa. Ele cria um novo arquivo GPX com os dados corrigidos.

## Requisitos

Para usar este script, você precisa:

1. **Python Instalado**: Certifique-se de que o Python 3.8 ou superior está instalado no seu computador. Você pode baixá-lo no [site oficial do Python](https://www.python.org/downloads/).
2. **Conhecimento Básico de Linha de Comando**: O script é executado a partir da linha de comando (Terminal no macOS/Linux ou Prompt de Comando/PowerShell no Windows).

## Instalação

1. **Baixe o Script**:

   - Salve o arquivo `run.py` em uma pasta no seu computador.

2. **Instale as Bibliotecas Necessárias**:
   - Abra o terminal ou prompt de comando.
   - Execute o seguinte comando para atualizar o gerenciador de pacotes:
     ```bash
     pip install --upgrade pip
     ```
   - Não são necessárias bibliotecas adicionais, pois o script utiliza módulos embutidos do Python.

## Como Usar

Siga os passos abaixo para executar o script:

### 1. Abra o Terminal ou Prompt de Comando

- No **Windows**:
  - Pressione `Win + R`, digite `cmd` e pressione Enter.
- No **macOS** ou **Linux**:
  - Abra o aplicativo Terminal.

### 2. Navegue até a Pasta que Contém o Script

Use o comando `cd` para navegar até a pasta onde você salvou o arquivo `run.py`. Por exemplo:

```bash
cd caminho/para/sua/pasta
```

Substitua `caminho/para/sua/pasta` pelo caminho real da pasta.

### 3. Execute o Script

Execute o script utilizando o seguinte comando:

```bash
python run.py <gpx_file_path> <momento_ida> <momento_pausa> <momento_continuacao> <output_path>
```

#### Explicação dos Argumentos:

1. `<gpx_file_path>`: Caminho para o arquivo GPX que você deseja processar (ex: `schmidt.gpx`).
2. `<momento_ida>`: O horário em que o trajeto foi percorrido antes da pausa, mas no mesmo local onde a atividade foi retomada. **Todos os pontos entre este momento e o momento da pausa serão replicados**. Certifique-se de que este ponto esteja no mesmo local do ponto de continuação.
3. `<momento_pausa>`: O horário do último ponto antes de a atividade ser pausada. Você pode identificar este ponto usando ferramentas como [GPX Studio](https://gpx.studio/).
4. `<momento_continuacao>`: O horário do primeiro ponto imediatamente após a atividade ser retomada, ou seja, o momento em que a pausa terminou.
5. `<output_path>`: O caminho onde o arquivo GPX corrigido será salvo (ex: `novo_schmidt.gpx`).

#### Exemplo de Comando:

```bash
python run.py schmidt.gpx 2025-02-22T10:05:15+00:00 2025-02-22T10:56:30+00:00 2025-02-22T11:27:42+00:00 novo_schmidt.gpx
```

### 4. Localize o Arquivo GPX Corrigido

Após executar o script, o arquivo GPX corrigido será salvo no local especificado por `<output_path>`.

## Limitações Importantes

Este script **só funciona em situações específicas**:

1. O trajeto percorrido entre o momento da pausa e o momento de continuação **deve ter sido percorrido anteriormente** (antes da pausa).
2. O ponto definido como `<momento_ida>` deve estar na **mesma localização** do ponto de `<momento_continuacao>`.

Se essas condições não forem atendidas, o script não funcionará corretamente.

## Como Identificar os Momentos

- **Momento Pausa (`<momento_pausa>`)**:

  - Este é o último ponto registrado antes de a atividade ser pausada.
  - Você pode usar ferramentas como [GPX Studio](https://gpx.studio/) para visualizar o arquivo GPX e identificar este ponto.

- **Momento Continuação (`<momento_continuacao>`)**:

  - Este é o primeiro ponto registrado imediatamente após a atividade ser retomada.

- **Momento Ida (`<momento_ida>`)**:
  - Este é um ponto no trajeto anterior à pausa, que está no mesmo local do ponto de continuação.
  - Todos os pontos entre este momento e o momento da pausa serão replicados para preencher o intervalo entre a pausa e a continuação.

## Solução de Problemas

- **Python Não Encontrado**:

  - Se você vir um erro como `python is not recognized as an internal or external command`, significa que o Python não está instalado ou não foi adicionado ao PATH do sistema. Consulte [este guia](https://www.python.org/downloads/) para instalar o Python e configurá-lo corretamente.

- **Arquivo GPX Inválido**:

  - Certifique-se de que o arquivo GPX de entrada é válido e segue o formato padrão GPX.

- **Formato de Hora Incorreto**:
  - Os horários (`momento_ida`, `momento_pausa`, `momento_continuacao`) devem estar no formato ISO 8601 (ex: `2025-02-22T10:05:15+00:00`). Verifique novamente suas entradas.

## Notas

- Este script assume que o arquivo GPX utiliza o esquema padrão GPX e inclui timestamps no elemento `<time>`.
- O script não sobrescreverá o arquivo GPX de entrada. O arquivo corrigido será salvo no caminho especificado em `<output_path>`.

## Feedback

Se você encontrar algum problema ou tiver sugestões de melhoria, sinta-se à vontade para entrar em contato!
