# Carrega Dados
Automação desenvolvida para fazer leitura de arquivo em uma pasta específica e carrega dados lidos em um Datapool do Orquestrador BotCity através do SDK.

## Pré requisitos
- Python 3.9^
- Conta na BotCity
- Automação para consumo do arquivo pronta na plataforma

## Orquestrador BotCity:
### [Datapool](https://documentation.botcity.dev/pt/maestro/features/datapool/#criando-um-datapool)

- Label:
    - `dados_cadastro`
- Status:
    - `Ativo`
- Política de consumo:
    - `FIFO`
- Gatilho:
    - `Nunca`
- Schema (como está no csv):
    - `full_name` - `string`
    - `vacancy` - `string`
    - `email` - `string`
    - `contact_number` - `string`
    - `keywords` - `string`
- (restante dos campos preenchidos conforme quiser)

### [Log de execução](https://documentation.botcity.dev/pt/maestro/features/logs/#criando-um-log-de-execucao)

- Label:
    - `acompanha_dados`
- Colunas (label - nome):
    - `nome` - `Nome do candidato`
    - `status` - `Status de upload de dados` 
    - `email` - `E-mail do candidato`

### [Build e Deploy](https://documentation.botcity.dev/pt/maestro/features/easy-deploy/)
- Faça o build executando o arquivo `build.xxx` que está na raiz do projeto.
- Faça o deploy na plataforma BotCity.

---

## Para testes locais

### Refatoração
Para rodar localmente, é necessário refatorar o código para que ele possa se comunicar com o Orquestrador BotCity.

### [Método login](https://documentation.botcity.dev/pt/maestro/maestro-sdk/setup/#utilizando-as-informacoes-do-workspace)

Adicionar as seguintes linhas:

```python
    maestro.login(
        server="https://developers.botcity.dev", 
        login="...", 
        key="..."
    )
```

- Login:
    - [`**encontra em Amb. de Desenvolvedor**`](https://developers.botcity.dev/dev)
- Key:
    - [`**encontra em Amb. de Desenvolvedor**`](https://developers.botcity.dev/dev)

### [Criar tarefa](https://documentation.botcity.dev/pt/maestro/features/new-task/)

Adicionar as seguintes linhas:

```python
execution = maestro.get_execution("12345")
execution.task_id = "12345"
```

O número `12345` é referente ao id da tarefa foi criada no Orquestrador BotCity, deve ter o status `Aguardando`.


### Crie e ative um ambiente virtual

   Para garantir que as dependências do projeto sejam isoladas de outros projetos Python, é recomendado usar um ambiente virtual.

   - No macOS/Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - No Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

### Instalação de Dependências

Instale as dependências do projeto com o seguinte comando:

```bash
python -m pip install -r requirements.txt
```

### Execução local

Execute o arquivo bot.py:

```bash
python bot.py
```