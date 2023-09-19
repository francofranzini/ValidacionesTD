
#CATEGORIAS sobre las que se valida que hayan materiales cargados
categorias_alcanzadas_por_deposito = ['v202204_TA', 'v202204_TS', 'v202204_EMPAL', 'v202204_ITFO', 'v202204_CC0', 'v202204_OE', 'v202204_ME', 'v202204_MSCE', 'v202204_IEC0', 'v202204_MSI', 
'v202204_ZM', 'v202204_CCI', 'v202204_EMCP', 'v202204_EXM', 'v202204_TTT', 'v202204_TTD', 'v202204_POST', 'v202204_SUBD', 'v202204_COM']


def isAdmin(user):
    return user['categoria_usuario_id']['name'] == 'Administracion'

def aplicaProgramacion(obj):
    return obj.categoria_id.x_aplica_programacion

def alcanzadoPorDeposito(obj):
    return obj.categoria_id.codigo in categorias_alcanzadas_por_deposito

def excepcionServicioTecnico(obj):
    return obj.categoria_id.codigo == 'v202204_IEC0' and obj.area_id.codigo == 'SETE'

def hayMaterialesCargados(obj):
    if obj.x_x_materiales_ids:
        return True
    return False

def manoObraPropia(obj):
    return obj.x_tipo_mano_obra == 'Propia'
def manoObraContratada(obj):
    return obj.x_tipo_mano_obra == 'Contratada'

def hayPersonalContratado(obj):
    return obj.x_contratado_ids

def hayPersonalPropio(obj):
    return obj.x_empleado_ids

def esNoProgramada(obj):
    return obj.x_es_programada == 'Noprogramada'
def esProgramada(obj):
    return obj.x_es_programada == 'Programada'

def tieneFechasCargadas(obj):
    return obj.date_start or obj.date_end

def fechaBienProgramada(obj):
    return obj.date_start[:10] >= hoy(dias=+3)

def hayPersonalCruzado(obj):
    if manoObraPropia(obj):
        if hayPersonalContratado(obj):
            return True
    if manoObraContratada(obj):
        if hayPersonalPropio(obj):
            return True
    return False

def responsablesEnPersonal(obj):
    return len(obj.env['x_tarea_personal'].search([('x_tarea_id', '=', obj.id), ('x_responsable', '=', True)]))
def horasTotalesEnPersonal(obj):
    return obj.env['x_tarea_personal'].search([('x_tarea_id', '=', obj.id), ('x_hs_totales', '>', 0)])
def fechasEnContratados(obj):
    return obj.env['x_tarea_contratados'].search([('x_tarea_id', '=', obj.id), ('x_fecha_desde', '!=', None)]) or obj.env['x_tarea_contratados'].search([('x_tarea_id', '=', obj.id), ('x_fecha_hasta', '!=', None)])
def sinAmbasFechasEnContratados(obj):
    return obj.env['x_tarea_contratados'].search([('x_tarea_id', '=', obj.id), ('x_fecha_desde', '=', None)]) or obj.env['x_tarea_contratados'].search([('x_tarea_id', '=', obj.id), ('x_fecha_hasta', '=', None)])
def importesEnContratados(obj):
    return obj.env['x_tarea_contratados'].search([('x_tarea_id', '=', obj.id), ('x_importe', '!=', 0)])
def horasPropiasEjecutadas(obj):
    return obj.x_hs_totales_ejec_mo_propia
def horasContratadasEjecutadas(obj):
    return obj.x_hs_totales_ejec_mo_contratada
for obj in self:

    #Costo de Area:
    #
    if isAdmin(usuario):
        validacion = False
        continue
    
    validacion = False
    mensaje = ''
    
    # Sale de Pendiente
    if obj.stage_id.codigo == 'PROG' and aplicaProgramacion(obj):
        
        if alcanzadoPorDeposito(obj):
            #si es civil cota 0 y serv. tecnico saltea validacion
            if(not(excepcionServicioTecnico(obj))):
                if not hayMaterialesCargados(obj):
                    mensaje += "Debe estar cargada al menos un material \n"
                    validacion = True
        
        #lo comento pq no puedo cargar las lineas, pero valida bien :)
        #if not obj.x_presupuesto_lineas_ids:
            #mensaje += "Debe estar cargada al menos una linea de Computo de Obra \n"
            #validacion = True
        if esNoProgramada(obj) and tieneFechasCargadas(obj):
                mensaje += 'Si la Tarea no es Programada la Fecha de Inicio y Fin debe estar vacias\n'
                validacion = True
        if esProgramada(obj):
            if not (fechaBienProgramada(obj)):
                mensaje += 'Programable a partir del dia: ' + hoy(dias=+3) + '\n'
                mensaje += 'No se puede programar una tarea menor a 3 dias desde hoy \n'
                validacion = True

        if hayPersonalCruzado(obj):
            validacion = True
            mensaje += 'No debe haber personal contratado \n' if manoObraPropia(obj) else 'No debe haber personal propio \n'
        
        
        
        if manoObraPropia(obj):
            if not hayPersonalPropio(obj):
                mensaje += 'Debe ingresar el Personal Asociado\n'
                validacion = True
            if esProgramada(obj):
                if not tieneFechasCargadas(obj) or obj.date_start == '' or obj.date_end == '':
                    mensaje += 'Debe ingresar la Fecha de Inicio y Fin\n'
                    validacion = True
                else:
                    tz = usuario.tz
                    fecha_start_date = datetime.datetime.strptime(str(obj.date_start), "%Y-%m-%d %H:%M:%S")
                    fecha_start = pytz.timezone('UTC').localize((fecha_start_date), is_dst=None).astimezone(pytz.timezone(tz)).strftime("%Y-%m-%d %H:%M:%S")
                    fecha_end_date = datetime.datetime.strptime(str(obj.date_end), "%Y-%m-%d %H:%M:%S")
                    fecha_end = pytz.timezone('UTC').localize(fecha_end_date, is_dst=None).astimezone(pytz.timezone(tz)).strftime("%Y-%m-%d %H:%M:%S")
                    if obj.date_start and obj.date_end and fecha_start[:10] != fecha_end[:10]:
                        mensaje += 'La fecha de inicio y fin deben ser del mismo dia\n'
                        validacion = True
            
            if responsablesEnPersonal(obj) != 1:
                mensaje += 'Debe haber un solo empleado responsable del gasto en el Personal\n'
                validacion = True
            #Horas vacias en personal propio:
            if horasTotalesEnPersonal(obj):
                mensaje += 'El personal no debe tener horas cargadas'
                validacion = True
            
            
            
        if manoObraContratada(obj):
            if esProgramada(obj):
                if not tieneFechasCargadas(obj):
                    mensaje += 'Debe ingresar la Fecha de Inicio y Fin\n'
                    validacion = True
            if esNoProgramada(obj) and tieneFechasCargadas(obj):
                mensaje += 'Si la Tarea no es Programada la Fecha de Inicio y Fin debe estar vacias\n'
                validacion = True
            if not hayPersonalContratado(obj):
                mensaje += 'Debe ingresar el Personal Contratado\n'
                validacion = True
        #Fechas desde/hasta vacias en personal Contratado:
            if fechasEnContratados(obj):
                mensaje += 'El personal contratado no debe tener fechas cargadas'
                validacion = True
            if importesEnContratados(obj):
                mensaje += 'El personal contratado no debe tener importes cargados'
                validacion = True
    #Entra a Esperando Ejecucion (PROG)
    if obj.stage_id.codigo == 'EJEC':
        if esProgramada(obj) and hoy() != obj.date_start[:10]:
            validacion = True
            mensaje += 'Debe esperar al dia de ejecucion\n'
        
        if esNoProgramada(obj) and hoy() != obj.x_fecha_ejecucion[:10]:
            validacion = True
            mensaje += 'Debe esperar al dia de ejecucion\n'
    # Entra a Finalizada
    #
    #
    #
    #
    if obj.stage_id.codigo == 'FIN' and obj.categoria_id.x_aplica_programacion:
        if hayPersonalCruzado(obj):
           validacion = True
           mensaje += 'No debe haber personal contratado \n' if manoObraPropia(obj) else 'No debe haber personal propio \n'
        if manoObraPropia(obj):
            if not hayPersonalPropio(obj):
                mensaje += 'Debe ingresar el Personal Asociado\n'
                validacion = True
            if responsablesEnPersonal(obj) != 1:
                mensaje += 'Debe haber un solo empleado responsable del gasto en el Personal\n'
                validacion = True
        if manoObraContratada(obj):
            if not hayPersonalContratado(obj):
                mensaje += 'Debe haber personal contratado \n'
                validacion = True
        
        #
        if not obj.x_no_ejecutada:
        # EJECUTADA
        #
            #Si es contratada, que esta cargado Fecha desde/hasta
            # y certificado
            if manoObraContratada(obj):
                if not importesEnContratados(obj):
                    mensaje += 'El personal contratado debe tener al menos un certificado cargado \n'
                    validacion = True
                if sinAmbasFechasEnContratados(obj):
                    mensaje += 'Debe ingresar las fechas desde y hasta en el personal contratado\n'
                    validacion = True
            #
            #verificar que no haya personal contratado en Mano Obra propia y que haya personal asociado
            #verifica que haya horas ejecutadas
            if manoObraPropia(obj):
                if not horasTotalesEnPersonal(obj):
                    validacion = True
                    mensaje += 'Debe ingresar las horas ejecutadas \n'
            #
            #
        #
        # NO EJECUTADA
        #
        else:
            if horasPropiasEjecutadas(obj):
                validacion = True
                mensaje += 'No debe haber horas ejecutadas \n'
            
            if manoObraContratada(obj):
                if horasContratadasEjecutadas(obj) > 0:
                    mensaje += 'Tarea no ejecutada, quitar fechas en personal contratado \n'
                    validacion = True
                if importesEnContratados(obj):
                    mensaje += 'El personal contratado no debe tener certificados cargados \n'
                    validacion = True
                

if validacion:
    raise Warning(mensaje)
        