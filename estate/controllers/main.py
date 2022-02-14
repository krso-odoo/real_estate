from odoo import http
from odoo.http import request



class EstateProperty(http.Controller):

	@http.route('/hello',auth="public")
	def hello(self,**kw):
		return "Hello world!"

	@http.route('/hello_user',auth="user")
	def hello(self, **kw):
		return "Hello %s" %(request.env.user.name)

	@http.route('/hello_template')
	def hello_template(self, **kw):
		return request.render('estate.hello_world')

	@http.route('/hello_template_user')
	def hello_template_user(self, **kw):
		est = request.env['estate.property'].search([('status', '=', 'new')])
		print ("property ::: ", est)
		return request.render('estate.hello_user', { 'user': request.env.user, 'est': est })

	@http.route(['/estate', '/estate/static/<string:is_static>'], auth="public", website=True)
	def estate(self, is_static=False, **kw):
		if is_static:
			return request.render('estate.static', {'est2': request.env['estate.property'].sudo().search([], limit=8)})
		return request.render('estate.Myweb_site', {'est2': request.env['estate.property'].sudo().search([], limit=8)})


	@http.route(['/property/<model("estate.property"):property>'], auth="public", website=True)
	def property(self, property=False, **kw):
		if property :
			return request.render('estate.property_details',{
				'pr' :property
				})