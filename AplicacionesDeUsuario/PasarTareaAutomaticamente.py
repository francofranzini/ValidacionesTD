tareas = self.env['project.task'].search([('x_contador_etapas', '=', 2)])
for tarea in tareas:
    proxima_etapa = pe = False
    for etapa in tarea.etapa_ids:
        if pe:
            proxima_etapa = etapa
            break
        if etapa == tarea.stage_id:
            pe = True
    try:
        if proxima_etapa:
            tarea.stage_id = proxima_etapa
    except:
        continue
        

#Modelo: Project.task
#Grupos de ejec: RRHH/Emple
#Planificaciones: 1 vez al dia, hora