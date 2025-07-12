# PROYECTO DATA ENGINEERING
Este proyecto implementa una arquitectura moderna de datos basada en principios de Data Mesh y el enfoque Medallion Architecture (Bronze, Silver, Gold), con el objetivo de generar productos de datos valiosos a partir de datos de telemedicina, gestión hospitalaria y análisis epidemiológico.

Utilizamos Apache Airflow para la orquestación de pipelines y Azure Data Lake Storage (ADLS) como repositorio principal de datos. La transformación y análisis de los datos se realizan mediante notebooks de Databricks, organizados por dominio.

## Arquitectura General
- Orquestación: Apache Airflow (DAGs funcionales)
- Almacenamiento: Azure Data Lake Storage (ADLS)
- Procesamiento: Databricks Notebooks
- Modelo de Datos: Data Mesh dividido por Dominios
- Enfoque: Medallion Architecture (Bronze, Silver, Gold)

## Dominios y Data Products

### Telemedicina
- Data Product: tmd_pacientes_riesgo
- Notebooks: Extracción y transformación de signos vitales, historial clínico y riesgo de consultas.
- Output: Lista de pacientes en riesgo por signos críticos o enfermedades.

### Gestión Hospitalaria
- Data Product: ghs_cobertura_hospitalaria
- Notebooks: Mapeo de hospitales y zonas sin cobertura.
- Output: Mapa de cobertura hospitalaria y zonas críticas.

### Análisis Epidemiológico
- Data Product: epi_analitica_enfermedades
- Notebooks: Tendencia y distribución de enfermedades por zona.
- Output: Alertas epidemiológicas y análisis temporal.


# APACHE AIRFLOW WITH DOCKER
- Airflow official documentation
Steps: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
- Donwload yaml file indicated in Airflow official documentation
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.0.0/docker-compose.yaml'
- Create folders for the volumes:
mkdir ./dags ./logs ./config ./plugings
- Setting airflow user
    - For Linux - MAC
    echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
    - For Windows, ignore the warning, or manually we can create an .env file with value:
    AIRFLOW_UID=50000
- Initialize Database (It will create the first user account)
docker compose up airflow-init
(At the end we should see Messages like: User "airflow" created with role "Admin" \n 3.0.0 \n airflow-init_1 exited with code 0)
- Run Airflow
docker compose up
- In a second terminal we can check all the conditions of the containers, by running
docker ps
- To interact with one of the container, just use the docker exec [CONTAINER ID] [Comand Line Interface]
docker exec 0c04f0e03aa8 airflow version

- Adding requirements file to docker airflow
    - Comment the image and add: "build: ." bellow it
    #image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:3.0.0}
    build: .
    - Create "Dockerfile" in the same folder your docker-compose.yaml file is with content similar to:
    FROM apache/airflow:3.0.0
    ADD requirements.txt .
    RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
    - Create a requirements.txt file in the same folder of the docker-compose.yaml
    - Now we can restart and build:
    docker compose down && docker compose up --build -d

- Adding data volume to the yaml
    - Go to the docker-compose.yaml
    - Locate the volumns part and add the volume
    "- ${AIRFLOW_PROJ_DIR:-.}/data:/opt/airflow/data"
    - Create the data folder (at the same level of dags):
    mkdir ./data
    - restart the volume (No need to use build here)
    docker compose down && docker compose up -d

- Note, each task executes acctions (Behind the scenes, each DAG is an operator):
    - Python Function: pythonoperator
    - Bash Command: bashoperator
    - Inser data into a DB: postgresoperator
(Depending in the action we want to trigger from our dag, we will use the corresponding operator)
Operator: It is an object encapsulating the job we want to run in our dag
(Each time we are adding an operator in our dag, we are adding a dag)

Examples:
1. Create my_dag.py inside ./dags
2. You will automatically see the DAG in Airflow UI: http://localhost:8080

# Connecting to Azure Blob Storage
Tutorial: https://www.astronomer.io/docs/learn/connections/azure-blob-storage?tab=shared-access-key#azure-blob-storage
Get Account Keys: https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal#view-account-access-keys

0. Add connection to Azure in Airflow
1. In Airflow, go to admin
2. Go to connection
3. Click in Add conneciton
4. Define a connection_id: azure_blob_storage
5. Connection Type: wasb
6. In Extra files JSON, copy the Blob Storage Connection String (IT is located below Key1)
{"connection_string": <copy_the_connection_string>}
(Make sure there are no other connections from Azure or it would generate warnings)

# Isolating python scripts in Airflow Dags
1. Add Python Path to Airflow in the yaml (To be able to import scripts)
    environment:
        PYTHONPATH: '/opt/airflow'

# Avoid loading samples in Airflow
1. Change in yaml:
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'

# Docker compose codes
- docker compose up airflow-init: Initial load for airflow
- docker compose up: To turn on airflow
- docker compose up -d: To turn on airflow and run it in background (Recommended)
- docker compose down && docker compose up -d: Normal Restart
- docker compose down && docker compose up --build -d: Restart forcing to build docker file (Only when dockerfile is updated)
