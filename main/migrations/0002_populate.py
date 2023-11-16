# Generated by Django 4.0 on 2022-04-02 23:17

from django.db import migrations
import pandas as pd

def populate_db(apps, schema_editor):
    Interaction = apps.get_model('main', 'Interaction')
    Gene = apps.get_model('main', 'Gene')
    GO = apps.get_model('main', 'GO')
    KEGG = apps.get_model('main', 'KEGG')

    #interactions
    df = pd.read_csv('files/master_slim.csv')
    df_dict = df.to_dict('records')
    toAdd = []
    for row in df_dict:
        newInteraction = Interaction(
            virus=row['virus'],
            host=row['host'],
            interaction=row['interaction'],
            strain=row['strain'],
            localization=row['localization'],
            tissue_expression=row['tissue_expression'],
        )
        toAdd.append(newInteraction)
    interactions = Interaction.objects.bulk_create(toAdd)

    #host gene
    gene_list = df['host'].drop_duplicates().tolist()
    toAdd = []
    for gene in gene_list:
        newGene = Gene(symbol=gene, organism='Homo sapiens')
        toAdd.append(newGene)
    genes = Gene.objects.bulk_create(toAdd)

    geneDict = {}
    for gene in genes:
        geneDict[gene.symbol] = gene

    #gene ontologies
    df = pd.read_csv('files/go_slim.csv')
    df_dict = df.to_dict('records')
    toAdd = []
    for row in df_dict:
        newGO = GO(
            gene=geneDict[row['gene']],
            name=row['name'],
            description=row['description'],
            type=row['type'],
        )
        toAdd.append(newGO)
    gos = GO.objects.bulk_create(toAdd)

    #kegg
    df = pd.read_csv('files/kegg_slim.csv')
    df_dict = df.to_dict('records')
    toAdd = []
    for row in df_dict:
        newKEGG = KEGG(
            gene=geneDict[row['gene']],
            name=row['name'],
            description=row['description']
        )
        toAdd.append(newKEGG)
    keggs = KEGG.objects.bulk_create(toAdd)

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_db)
    ]
