from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#Devuelve una lista paginada de una lista de objetos de un modelo determinada
def getPaginator(request, object_list, num_objects):
    paginator = Paginator(object_list, num_objects) # Muestra num_objects en una pagina
    page = request.GET.get('page', 1)
    try:
        object_list_paginated = paginator.page(page)
    except PageNotAnInteger:
        # Si el parametro page no es un entero manda la primera pagina
        object_list_paginated = paginator.page(1)
    except EmptyPage:
        # Si la pagina esta fuera de rango (e.g. 9999) manda la ultima pagina de los resultados
        object_list_paginated = paginator.page(paginator.num_pages)
    return object_list_paginated

#Devuelve una lista con todas las instancias de un modelo y su primary key correspondiente: [(pk1,reg1), (pk2,reg2), ...]
def getAllObjects(model):
    return [(x.pk, x.title) for x in model.objects.all()]

#Devuelve una lista con todos los campos de un modelo: [(campo1,campo1), (campo2,campo2), ...]
def getAllFields(model):
    return [(x, x) for x in model._meta.get_all_field_names()]

#Devuelve una lista con todos los campos de un modelo y su etiqueta correspondiente: [(campo1,label1), (campo2,label2), ...]
#Los campos relacionales no los coge
def getLabelFields(model):
    fields = []
    for (name1,name2) in getAllFields(model):
        try:
            field=(name1,model._meta.get_field_by_name(name1)[0].verbose_name)
            fields.append(field)
        except AttributeError: #para descartar campos RelatedObject
            continue
    return fields
