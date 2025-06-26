from botcity.maestro import *
from botcity.plugins.csv import BotCSVPlugin

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

def main():
    # Autenticação via Runner
    maestro = BotMaestroSDK.from_sys_args()
    # Retorna detalhes de uma terefa
    execution = maestro.get_execution()
    # Retorna o parâmetro da tarefa
    nome_arquivo = execution.parameters.get("nome_arquivo")

    # Uso do plugin CSV para leitura do arquivo
    bot_csv = BotCSVPlugin()
    caminho = fr"C:\Users\...\...\...\arquivo\{nome_arquivo}"
    dados = bot_csv.read(caminho).as_dict()

    # Inicio da contagem de itens
    total = len(dados)
    sucesso = 0
    falha = 0

    # Percorre a planilha lida
    for candidato in dados:
        try:
            # Cria um objeto Datapool
            new_item = DataPoolEntry(
                values={
                    "full_name": candidato['full_name'],
                    "vacancy": candidato['vacancy'],
                    "email": candidato['email'],
                    "contact_number": candidato['contact_number'],
                    "keywords": candidato['keywords']
                }
            )

            # Obtendo a referência do Datapool e cria entrada
            datapool = maestro.get_datapool(label="label_datapool")
            datapool.create_entry(new_item)


            # Log + contagem de sucesso
            maestro.new_log_entry(
                activity_label="acompanha_dados",
                values={
                    "nome": candidato['full_name'],
                    "status": "Sucesso",
                    "email": candidato['email']
                }
            )
            sucesso += 1

        except Exception as error:
            maestro.error(task_id=execution.task_id, exception=error)

            # Log + contagem de falha
            maestro.new_log_entry(
                activity_label="acompanha_dados",
                values={
                    "nome": candidato['full_name'],
                    "status": "Falha",
                    "email": candidato['email']
                }
            )
            falha += 1
    
    if sucesso == total:
        status=AutomationTaskFinishStatus.SUCCESS
        message="Tafera finalizada com sucesso."
        create_task(maestro)
        create_task(maestro)
    elif falha == total:
        status=AutomationTaskFinishStatus.FAILED
        message="Tarefa falhou."
    else:
        status=AutomationTaskFinishStatus.PARTIALLY_COMPLETED
        message="Alguns itens falharam, verifique o log."
        create_task(maestro)
        create_task(maestro)
    

    maestro.post_artifact(
        task_id=execution.task_id,
        artifact_name=f"arquivo_{execution.task_id}.csv",
        filepath=caminho
    )

    maestro.finish_task(
        task_id=execution.task_id,
        status=status,
        message=message,
        total_items=total,
        processed_items=sucesso,
        failed_items=falha
    )

def create_task(maestro):
    maestro.create_task(
        activity_label="label_segundo_bot",
        parameters={},
        test=True
)


if __name__ == '__main__':
    main()