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

vals_attr_1 = {
        'name': 'Talle',
        #'create_variant': 'no_variant',
        }
attr_1_id = models.execute_kw(dbname,uid,pwd,'product.attribute','create',[vals_attr_1])
print(attr_1_id)

vals_attr_val_1 = {
        'attribute_id': attr_1_id,
        'name': 'Large'
        }
attr_val_1_id = models.execute_kw(dbname,uid,pwd,'product.attribute.value','create',[vals_attr_val_1])
print(attr_val_1_id)

vals_attr_val_2 = {
        'attribute_id': attr_1_id,
        'name': 'Small'
        }
attr_val_2_id = models.execute_kw(dbname,uid,pwd,'product.attribute.value','create',[vals_attr_val_2])
print(attr_val_2_id)

vals_attr_2 = {
        'name': 'Color',
        #'create_variant': 'no_variant',
        }
attr_2_id = models.execute_kw(dbname,uid,pwd,'product.attribute','create',[vals_attr_2])
print(attr_2_id)

vals_attr_2_val_1 = {
        'attribute_id': attr_2_id,
        'name': 'Azul'
        }
attr_2_val_1_id = models.execute_kw(dbname,uid,pwd,'product.attribute.value','create',[vals_attr_2_val_1])
print(attr_2_val_1_id)

vals_attr_2_val_2 = {
        'attribute_id': attr_2_id,
        'name': 'Blanco'
        }
attr_2_val_2_id = models.execute_kw(dbname,uid,pwd,'product.attribute.value','create',[vals_attr_2_val_2])
print(attr_2_val_2_id)


vals_tmpl = {
        'name': 'Remera',
        'sale_ok': True,
        'type': 'product',
        }

product_tmpl_id = models.execute_kw(dbname,uid,pwd,'product.template','create',[vals_tmpl])
print(product_tmpl_id)

vals_attribute_line = {
        'product_tmpl_id':product_tmpl_id,
        'attribute_id':attr_1_id,
        'value_ids':[(6,False,[attr_val_1_id,attr_val_2_id])]}

attribute_line = models.execute_kw(dbname, uid, pwd, 'product.template.attribute.line', 'create',[vals_attribute_line])

vals_attribute_line_2 = {
        'product_tmpl_id':product_tmpl_id,
        'attribute_id':attr_2_id,
        'value_ids':[(6,False,[attr_2_val_1_id,attr_2_val_2_id])]}

attribute_line = models.execute_kw(dbname, uid, pwd, 'product.template.attribute.line', 'create',[vals_attribute_line_2])

print(attribute_line)
