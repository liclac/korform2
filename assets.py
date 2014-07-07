from flask.ext.assets import Environment, Bundle

assets = Environment()

vendor_js = Bundle(
	'../bower_components/jquery/dist/jquery.js',
	'../bower_components/bootstrap/dist/js/bootstrap.js'
)
coffee = Bundle(
	'script.coffee',
	filters='coffeescript'
)
assets.register('js_all', vendor_js, coffee, output='gen/script.js')

less = Bundle(
	'style.less',
	filters='less'
)
assets.register('css_all', less, output='gen/style.css')
