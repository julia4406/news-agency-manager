# news-agency-manager
News agency manager. Django project.

If the publication date is within 2 days, the publication date in the 
Publications table will be highlighted in red.

All pages except index.html protected with LoginRequiredMixin. User should be authenticated for 
further actions.

for adding test data use python manage.py loaddata data.json