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
for x,row in enumerate(rows):
    # Saltea la primer fila porque tiene el nombre de las columnas
    if x == 0:
        continue
    # Lee cada una de las celdas en la fila
    vals = {}
    for i,cell in enumerate(row):
        if i == 24:
            print(i,cell.value)
            if cell.value:
                values = cell.value.split(':')
                # Atrtibuto
                attr_name = values[0]
                attr_id = models.execute_kw(dbname,uid,pwd,'product.attribute','search',[[['name','=',attr_name]]])
                if not attr_id:
                    vals_attr = {
                        'name': attr_name,
                        #'create_variant': 'no_variant',
                        }
                    attr_id = models.execute_kw(dbname,uid,pwd,'product.attribute','create',[vals_attr])
                    print(attr_id)
                else:
                    attr_id = attr_id[0]
                # Valor del atributo
                attr_value = values[1]
                value_id = models.execute_kw(dbname,uid,pwd,'product.attribute.value','search',[[['attribute_id','=',attr_id],['name','=', attr_value]]])
                if not value_id:
                    vals_value = {
                            'name': attr_value,
                            'attribute_id': attr_id,
                            }
                    value_id = models.execute_kw(dbname,uid,pwd,'product.attribute.value','create',[vals_value])
                    print(value_id)

print(x)
workbook.close()
