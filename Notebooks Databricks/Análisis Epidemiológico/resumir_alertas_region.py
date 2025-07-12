# Databricks notebook source
# dbutils.widgets.text("TABLE_TRANSFORM_ALERTAS_REGION", "g5_epi_analitica_enfermedades.silver.alertas_region")
# dbutils.widgets.text("TABLE_SUMMARY_ALERTAS_REGION", "g5_epi_analitica_enfermedades.gold.alertas_region_summary")

# COMMAND ----------

TABLE_TRANSFORM_ALERTAS_REGION = dbutils.widgets.get("TABLE_TRANSFORM_ALERTAS_REGION")
TABLE_SUMMARY_ALERTAS_REGION = dbutils.widgets.get("TABLE_SUMMARY_ALERTAS_REGION")

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS ${TABLE_SUMMARY_ALERTAS_REGION}

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE ${TABLE_SUMMARY_ALERTAS_REGION} AS
# MAGIC SELECT
# MAGIC     nivel_alerta_respiratoria,
# MAGIC     COUNT(*) AS total_registros,
# MAGIC     
# MAGIC     ROUND(AVG(total_consultas), 1) AS promedio_consultas,
# MAGIC     ROUND(AVG(total_respiratorias), 1) AS promedio_respiratorias,
# MAGIC     ROUND(AVG(porcentaje_respiratorias), 1) AS porcentaje_resp_prom,
# MAGIC     
# MAGIC     MAX(porcentaje_respiratorias) AS max_porcentaje,
# MAGIC     MIN(porcentaje_respiratorias) AS min_porcentaje
# MAGIC
# MAGIC FROM ${TABLE_TRANSFORM_ALERTAS_REGION}
# MAGIC GROUP BY nivel_alerta_respiratoria;
# MAGIC