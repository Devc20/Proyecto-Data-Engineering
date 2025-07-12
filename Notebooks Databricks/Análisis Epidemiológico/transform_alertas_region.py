# Databricks notebook source
# dbutils.widgets.text("TABLE_INPUT_CONSULTAS_VIRTUALES", "g5_tmd_pacientes_riesgo.bronze.consultas_virtuales_input")
# dbutils.widgets.text("TABLE_INPUT_PACIENTES", "g5_tmd_pacientes_riesgo.bronze.pacientes_input")
# dbutils.widgets.text("TABLE_TRANSFORM_ALERTAS", "g5_epi_analitica_enfermedades.silver.alertas_region")

# COMMAND ----------

TABLE_INPUT_CONSULTAS_VIRTUALES = dbutils.widgets.get("TABLE_INPUT_CONSULTAS_VIRTUALES")
TABLE_INPUT_PACIENTES = dbutils.widgets.get("TABLE_INPUT_PACIENTES")
TABLE_TRANSFORM_ALERTAS = dbutils.widgets.get("TABLE_TRANSFORM_ALERTAS")

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS ${TABLE_TRANSFORM_ALERTAS}
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE ${TABLE_TRANSFORM_ALERTAS} AS
# MAGIC SELECT 
# MAGIC     p.direccion AS direccion,
# MAGIC     COUNT(*) AS total_consultas,
# MAGIC
# MAGIC     -- Total enfermedades respiratorias
# MAGIC     SUM(
# MAGIC         CASE 
# MAGIC             WHEN c.enfermedad IN ('COVID-19', 'Gripe') THEN 1 
# MAGIC             ELSE 0 
# MAGIC         END
# MAGIC     ) AS total_respiratorias,
# MAGIC
# MAGIC     -- Porcentaje de enfermedades respiratorias
# MAGIC     ROUND(
# MAGIC         100.0 * 
# MAGIC         SUM(CASE WHEN c.enfermedad IN ('COVID-19', 'Gripe') THEN 1 ELSE 0 END) 
# MAGIC         / COUNT(*), 
# MAGIC         2
# MAGIC     ) AS porcentaje_respiratorias,
# MAGIC
# MAGIC     -- Nivel de alerta respiratoria
# MAGIC     CASE
# MAGIC         WHEN 100.0 * SUM(CASE WHEN c.enfermedad IN ('COVID-19', 'Gripe') THEN 1 ELSE 0 END) / COUNT(*) >= 40 THEN 'ALTO'
# MAGIC         WHEN 100.0 * SUM(CASE WHEN c.enfermedad IN ('COVID-19', 'Gripe') THEN 1 ELSE 0 END) / COUNT(*) BETWEEN 20 AND 39.99 THEN 'MODERADO'
# MAGIC         ELSE 'BAJO'
# MAGIC     END AS nivel_alerta_respiratoria
# MAGIC
# MAGIC FROM ${TABLE_INPUT_CONSULTAS_VIRTUALES} c
# MAGIC JOIN ${TABLE_INPUT_PACIENTES} p ON c.id_paciente = p.id_paciente
# MAGIC GROUP BY p.direccion;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from ${TABLE_TRANSFORM_ALERTAS}

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

