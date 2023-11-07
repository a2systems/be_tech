#!/usr/bin/python3

# import xmlrpc and openpyxl modules
from xmlrpc import client
import openpyxl
from datetime import datetime, date

url = 'http://localhost:8069'
common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
res = common.version()

dbname = 'cordoba-v1'
user = 'admin'
pwd = 'admin'
uid = common.authenticate(dbname, user, pwd, {})

# prints Odoo version and UID to make sure we are connected
print(res)
print(uid)

models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Define la variable para leer el workbook
workbook = openpyxl.load_workbook("productos.xlsx")

# Define variable para la planilla activa
worksheet = workbook.active

# Itera las filas para leer los contenidos de cada celda
rows = worksheet.rows
default_code = ''
prod_tmpl_id = None
dict_attrs = {}
for x,row in enumerate(rows):
    # Saltea la primer fila porque tiene el nombre de las columnas
    if x == 0:
        continue
    # Lee cada una de las celdas en la fila
    vals = {}
    field_name = ''
    field_value = None
    skip_row = False
    print(x)
    for i,cell in enumerate(row):
        if i == 0:
            if cell.value:
                if dict_attrs and prod_tmpl_id:
                    print(dict_attrs)
                    print('es aca')
                    for key, values in dict_attrs.items():
                        vals_attribute_line = {
                            'product_tmpl_id':prod_tmpl_id[0],
                            'attribute_id': key,
                            'value_ids':[(6,False,values)]}
                        attribute_line = models.execute_kw(dbname, uid, pwd, 'product.template.attribute.line', 'create',[vals_attribute_line])
                    import pdb;pdb.set_trace()
                dict_attrs = {}
                name = cell.value
                prod_tmpl_id = models.execute_kw(dbname,uid,pwd,'product.template','search',[[['name','=',name]]])
                #if not prod_tmpl_id:
                #    import pdb;pdb.set_trace()
                #else:
                #    print(prod_tmpl_id)
        if i == 24 and prod_tmpl_id:
            if cell.value:
                values = cell.value.split(':')
                # Atrtibuto
                attr_name = values[0]
                attr_id = models.execute_kw(dbname,uid,pwd,'product.attribute','search',[[['name','=',attr_name]]])
                if not attr_id:
                    import pdb;pdb.set_trace()
                attr_value = values[1]
                value_id = models.execute_kw(dbname,uid,pwd,'product.attribute.value','search',[[['attribute_id','=',attr_id],['name','=', attr_value]]])
                if not value_id:
                    import pdb;pdb.set_trace()
                else:
                    #import pdb;pdb.set_trace()
                    if attr_id[0] not in dict_attrs:
                        dict_attrs[attr_id[0]] = []
                    if value_id[0] not in dict_attrs[attr_id[0]]:
                        dict_attrs[attr_id[0]].append(value_id[0])

                    #vals_attribute_line = {
                    #    'product_tmpl_id':prod_tmpl_id[0],
                    #    'attribute_id':attr_id[0],
                    #    'value_ids':[(6,False,[value_id[0]])]}
                    #domain = [[['product_tmpl_id','=',prod_tmpl_id[0]],['attribute_id','=',attr_id[0]]]]]
                    #line_id = models.execute_kw(dbname,uid,pwd,'product.template.attribute.line','search',domain)
                    #attribute_line = models.execute_kw(dbname, uid, pwd, 'product.template.attribute.line', 'create',[vals_attribute_line])
                    #print('********* %s '%(attribute_line))



print(x)
workbook.close()
