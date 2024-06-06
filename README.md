# HuCOVaria

## About
HuCOVaria (Human/COVID-19 Variants Interaction) is a web-tool designed to provide an atlas of Protein-Protein Interaction information between human proteins and SARS-CoV-2 variant proteins. It provides searchable parameters to filter through the 146,146 interactions involving 4,549 human genes across 12 different SARS-CoV-2 strains. It provides a searchable and downloadable table format and a basic network view to visualize the interactions.

## To Populate the DB
1. Decompress the main dataset running `tar -xvf files/master_slim.tar.gz -C files/`. 
2. Comment urlpatterns list in main/urls.py file. Uncomment empty urlpatterns list.
3. Comment out all code after imports in main/views.py file. ( Everything after 'from .models import *' should be commented out.)
4. Run 'python manage.py migrate' to apply migrations.
5. Reverse changes in 1. and 2. (Revert urlpatterns from empty to non-empty list in main/urls.py and uncomment all functions in main/views.py)

## Compile and run with Docker (this will populate the DB automatically)
1. docker build -t hucovaria-app .
2. docker run -p 9018:9018 hucovaria-app 
