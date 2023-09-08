self = self.sudo()

tarea = self.env['project.task'].browse(tarea_id)

descripcion = 'Tarea creada por el area ..... y el usuario .... en el dia ...<br/>%s' % descripcion

tarea_creada = self.env['project.task'].create({
    'project_id': proyecto_id,
    'area_id': area_id,
    'categoria_id': categoria_id,
    'x_es_programada': 'Programada',
    'date_start':'%s 03:00:00' % fecha,
    'date_end': '%s 03:00:00' % fecha,
    'x_descripcion_solicitante': descripcion,
})

tarea.write({'child_ids': [(6, 0, list(tarea.child_ids._ids) + [tarea_creada.id])]})