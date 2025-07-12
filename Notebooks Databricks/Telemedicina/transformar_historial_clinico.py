# Databricks notebook source
# dbutils.widgets.text("TABLE_INPUT_BD_MEDICA", "g5_tmd_pacientes_riesgo.bronze.bd_medica_input")
# dbutils.widgets.text("TABLE_HISTORIAL_CLINICO", "g5_tmd_pacientes_riesgo.silver.historial_clinico")

# COMMAND ----------

TABLE_INPUT_PACIENTES = dbutils.widgets.get("TABLE_INPUT_BD_MEDICA")
TABLE_TRANSFORM_PACIENTES = dbutils.widgets.get("TABLE_HISTORIAL_CLINICO")

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS ${TABLE_HISTORIAL_CLINICO}

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Crea la tabla mv_historial_clinico
# MAGIC CREATE TABLE ${TABLE_HISTORIAL_CLINICO} AS
# MAGIC SELECT
# MAGIC     id_paciente,
# MAGIC     enfermedad,
# MAGIC     COUNT(*) AS veces_reportado,
# MAGIC     MAX(fecha) AS ultima_fecha
# MAGIC FROM ${TABLE_INPUT_BD_MEDICA}
# MAGIC GROUP BY id_paciente, enfermedad;
# MAGIC

# COMMAND ----------

