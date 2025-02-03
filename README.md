# news-agency-manager
News agency manager. Django project.



All pages except index.html protected with LoginRequiredMixin. User should be authenticated for 
further actions.

Publications are sorted by publication_date. Nearest shown first.
If the publication date is within 2 days, the publication date in the 
Publications table will be highlighted in red.

for adding test data use python manage.py loaddata data.json