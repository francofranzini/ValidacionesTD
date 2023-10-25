
self = self.sudo()

tarea = self.env['project.task'].browse(tarea_id)
##area desde la que se solicita la tarea
area = self.env['project.area'].search([('id','=',tarea.area_id.id)])['name']
#usuario que solicita la tarea
usuario = self.env['res.users'].search([('id','=',usuario_id)])
nombre_usuario = usuario['name'] #Administrador
mail_solicitante = usuario.email

fecha = tarea.date_start

proyecto = self.env['project.project'].search([('num_numero_completo', '=', codigo_proyecto)])
if not proyecto:
    raise Warning("No se encontro ningun proyecto con el código %s" % codigo_proyecto)
#if tarea.project_id.subcompania_id == proyecto.subcompania_id:
    #raise Warning("Si la tarea es de la empresa actual debe realizarlo desde el boton solicitar tarea")



# raise Warning(self.env.user.name)


descripcion = u'Tarea creada por el área %s y el usuario %s en el día ...<br/>' % (area, nombre_usuario)



tarea_creada = self.env['project.task'].create({
    #'project_id': proyecto_id,
    'project_id': proyecto.id,
    'area_id': area_id,
    'categoria_id': categoria_id,
    'x_es_programada': 'Programada',
    'date_start': fecha,
    'date_end': fecha,
    'x_mail_solicitante2': mail_solicitante,
    'x_es_solicitada': True,
    'x_descripcion_solicitante': descripcion,
    #######
    'subcompania_id': proyecto.subcompania_id.id,
    'sucursal_id':proyecto.subcompania_id.sucursal_ids[0].id,
    'num_punto_venta_id': self.env['res.punto_venta'].search([('subcompania_id', '=', proyecto.subcompania_id.id)], limit=1).id,
})

tarea.write({'child_ids': [(6, 0, list(tarea.child_ids._ids) + [tarea_creada.id])]})

self.env['mail.template'].browse(50).send_mail(tarea_creada.id, force_send=False)

###variables:
# proyecto_id: RelA1, proj.proj,req
# area_id: RelA1, proj.area, req, vista filtrodearea
# categoria_id: RelA1, proj.category, req,
# descripcion: text, req
# usuario_id: RelA1, res.users, res.users.search, valDefecto: usuario_act.id
# codigo_proyecto: char, req
# tarea_id: RelA1, proj.task, req
# 
#Grupo EJEC: RRHH
# Botones:
# variable: tarea_id
# vista: proj.task.form
# contexto: {'default_categoria_id': categoria_id}
# invisible: ['|',('x_tipo_mano_obra', '!=', 'Contratada'), ('x_contador_etapas', '=', 1 )]###