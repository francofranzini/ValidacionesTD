tarea = self.env['project.task'].browse(tarea_id)
esperando_ejecucion = self.env['project.task.type'].search([('name', '=', 'Esperando Ejecucion')])

for etapa in tarea.etapa_ids:
    if etapa == tarea.etapa_inicial_id:
        tarea.stage_id = etapa
