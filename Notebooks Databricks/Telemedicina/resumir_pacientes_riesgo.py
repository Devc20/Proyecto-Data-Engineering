# Databricks notebook source
# dbutils.widgets.text("TABLE_TRANSFORM_PACIENTES", "g5_tmd_pacientes_riesgo.silver.riesgo_consultas")
# dbutils.widgets.text("TABLE_SUMMARY_PACIENTES", "g5_tmd_pacientes_riesgo.gold.pacientes_summary")

# COMMAND ----------

TABLE_TRANSFORM_PACIENTES = dbutils.widgets.get("TABLE_TRANSFORM_PACIENTES")
TABLE_SUMMARY_PACIENTES = dbutils.widgets.get("TABLE_SUMMARY_PACIENTES")

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS ${TABLE_SUMMARY_PACIENTES}

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Crear resumen por clasificación de riesgo
# MAGIC CREATE TABLE ${TABLE_SUMMARY_PACIENTES} AS
# MAGIC SELECT
# MAGIC   clasificacion_riesgo,
# MAGIC   COUNT(*) AS total_por_riesgo
# MAGIC FROM ${TABLE_TRANSFORM_PACIENTES}
# MAGIC GROUP BY clasificacion_riesgo;
# MAGIC
# MAGIC