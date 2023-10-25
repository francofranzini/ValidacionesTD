tarea = self.env['project.task'].browse(tarea_id)
proxima_etapa = pe = False
for etapa in tarea.etapa_ids:
    if pe:
        proxima_etapa = etapa
        break
    if etapa == tarea.stage_id:
        pe = True
if proxima_etapa:
    tarea.stage_id = proxima_etapa

#variables: tarea_id, relacionAUno(int), modeloRelacionado:project.task, mod, req
#boton: Confirmar, vista: project.taks.form, variable: tarea_id
#grupo ejec rrhh