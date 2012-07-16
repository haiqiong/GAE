from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from google.appengine.api import users
import hfwwgDB 

"""use your model to create a sighting form that inherits from the
django.ModelForm class"""

class SightingForm(djangoforms.ModelForm):
		class Meta:
				model = hfwwgDB.Sighting
				#exclue = ['which_user']

class SightingInputPage(webapp.RequestHandler):
		#respond to GET web request
		def get(self):
				user = users.get_current_user()
				if user:

						html = template.render('templates/header.html', {'title': 'Report a Possible Sighting'})
				
						html = html + template.render('templates/form_start.html', {})
						html = html + str(SightingForm(auto_id=False))
						html = html + template.render('templates/form_end.html', {'sub_title': 'Submit Sighting'})
						html = html + template.render('templates/footer.html', {'links': ''})
						self.response.out.write(html)
				else:
						self.redirect(users.create_login_url(self.request.uri))

		def post(self):
				new_sighting = hfwwgDB.Sighting()

				new_sighting.name = self.request.get('name')
				new_sighting.email = self.request.get('email')
				new_sighting.date = self.request.get('date')
				new_sighting.time = self.request.get('time')
				new_sighting.location = self.request.get('location')
				new_sighting.fin_type = self.request.get('fin_type')
				new_sighting.whale_type = self.request.get('whale_type')
				new_sighting.blow_type = self.request.get('blow_type')
				new_sighting.wave_type = self.request.get('wave_type')

				new_sighting.put()

				html = template.render('templates/header.html', {'title': 'Thank you!'})
				html = html + '<p> Thank you for proving your sighting data.</p>'
				html = html + template.render('templates/footer.html', {'links': 'Enter <a href="/">another sighting</a>.'})

				self.response.out.write(html)
				"""
						#arguments() returns a list of the field names used in the form.
						for field in self.request.arguments():
								self.response.out.write(field)
								self.response.out.write(': ')
								#get() returns the value associated with the provided field name.
								self.response.out.write(self.request.get(field))
								self.response.out.write('<br />')
				"""
app = webapp.WSGIApplication([('/.*', SightingInputPage)], debug=True)

def main():
		run_wsgi_app(app)

if __name__ == '__main__':
		main()
