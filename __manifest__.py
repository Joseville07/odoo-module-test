{
    'name': 'Module Test',
    'version': '18.0.1.0',
    'summary': 'Module test to odoo',
    'author': 'Diamond',
    'license': 'LGPL-3',
    'category': 'Other',
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_tags_views.xml",
        "views/real_estate_menus.xml"
    ],
    
    'depends': [ 'base' ],
    'application': True
}