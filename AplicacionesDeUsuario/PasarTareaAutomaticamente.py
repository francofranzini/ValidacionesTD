tareas = self.env['project.task'].search([('x_contador_etapas', '=', 2), ('date_start', '<=', '%s 23:00:00' % hoy())])
for tarea in tareas:
    proxima_etapa = pe = False
    for etapa in tarea.etapa_ids:
        if pe:
            proxima_etapa = etapa
            break
        if etapa == tarea.stage_id:
            pe = True
    if proxima_etapa:
        tarea.stage_id = proxima_etapa