 
{
   'name': 'Real Estate Extended',
   'version': '1.0',
   'summary': 'Real estate Advertisement App',
   'description': "",
   'author':"Pravin nayee",
   'depends': ['base','estate'],
   'data' : [
       'security/ir.model.access.csv',
       'views/extended_view.xml',
       #'views/res_users_views.xml',
   ],

   
 
   'installable': True,
   'auto_install': False,
   'application': True,
   'license': 'LGPL-3',
}