# Databricks notebook source
# dbutils.widgets.text("TABLE_INPUT_SIGNOS_VITALES", "g5_tmd_pacientes_riesgo.silver.signos_vitales")
# dbutils.widgets.text("TABLE_RIESGO_CONSULTAS", "g5_tmd_pacientes_riesgo.silver.riesgo_consultas")

# COMMAND ----------

TABLE_INPUT_SIGNOS_VITALES = dbutils.widgets.get("TABLE_INPUT_SIGNOS_VITALES")
TABLE_RIESGO_CONSULTAS = dbutils.widgets.get("TABLE_RIESGO_CONSULTAS")

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS ${TABLE_RIESGO_CONSULTAS};
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE ${TABLE_RIESGO_CONSULTAS} AS
# MAGIC SELECT 
# MAGIC     id_atencion,
# MAGIC     id_paciente,
# MAGIC     fecha,
# MAGIC     temperatura,
# MAGIC     presion,
# MAGIC     glucosa,
# MAGIC     sintoma,
# MAGIC     enfermedad,
# MAGIC
# MAGIC     -- Clasificación por temperatura
# MAGIC     CASE
# MAGIC         WHEN temperatura >= 37.5 THEN 'fiebre alta'
# MAGIC         WHEN temperatura BETWEEN 37.0 AND 37.4 THEN 'febrícula'
# MAGIC         ELSE 'normal'
# MAGIC     END AS nivel_temperatura,
# MAGIC
# MAGIC     -- Clasificación por presión
# MAGIC     CASE
# MAGIC         WHEN presion < 90 THEN 'hipotensión'
# MAGIC         WHEN presion BETWEEN 90 AND 120 THEN 'normal'
# MAGIC         WHEN presion BETWEEN 121 AND 139 THEN 'prehipertensión'
# MAGIC         ELSE 'hipertensión'
# MAGIC     END AS nivel_presion,
# MAGIC
# MAGIC     -- Clasificación por glucosa
# MAGIC     CASE
# MAGIC         WHEN TRY_CAST(glucosa AS DOUBLE) < 70 THEN 'hipoglucemia'
# MAGIC         WHEN TRY_CAST(glucosa AS DOUBLE) BETWEEN 70 AND 99 THEN 'normal'
# MAGIC         WHEN TRY_CAST(glucosa AS DOUBLE) BETWEEN 100 AND 125 THEN 'prediabetes'
# MAGIC         ELSE 'diabetes'
# MAGIC     END AS nivel_glucosa,
# MAGIC
# MAGIC     -- Clasificación general de riesgo
# MAGIC     CASE
# MAGIC         WHEN temperatura >= 37.5 OR TRY_CAST(glucosa AS DOUBLE) > 125 OR presion >= 140 THEN 'riesgo'
# MAGIC         ELSE 'estable'
# MAGIC     END AS clasificacion_riesgo
# MAGIC
# MAGIC FROM ${TABLE_INPUT_SIGNOS_VITALES};
# MAGIC
# MAGIC

# COMMAND ----------

