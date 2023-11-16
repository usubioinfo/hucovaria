from django.db import models


class Result(models.Model):
    id = models.CharField(max_length=60, primary_key=True)
    time = models.DateTimeField()
    annotation = models.CharField(max_length=60)

    def __str__(self):
        return self.id

class Gene(models.Model):
	symbol = models.CharField(max_length=60, primary_key=True)
	organism = models.CharField(max_length=60)

class Interaction(models.Model):
	virus = models.CharField(max_length=60)
	host = models.CharField(max_length=60)
	interaction = models.CharField(max_length=60)
	strain = models.CharField(max_length=60)
	localization = models.CharField(max_length=60)
	tissue_expression = models.CharField(max_length=60)

	def __str__(self):
		return str(self.virus) + "_" + str(self.host) + "_" + str(self.strain) + "_" + str(self.id)

class KEGG(models.Model):
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
	name = models.CharField(max_length=60)
	description = models.CharField(max_length=100)

class GO(models.Model):
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
	name = models.CharField(max_length=60)
	description = models.CharField(max_length=100)
	type = models.CharField(max_length=10)

class InteractionResult(models.Model):
	result = models.ForeignKey(Result, on_delete=models.CASCADE)
	content = models.CharField(max_length=100)

	def __str__(self):
		return self.content

class VirusResult(models.Model):
	result = models.ForeignKey(Result, on_delete=models.CASCADE)
	content = models.CharField(max_length=100)

	def __str__(self):
		return self.content

class HostResult(models.Model):
	result = models.ForeignKey(Result, on_delete=models.CASCADE)
	content = models.CharField(max_length=100)

	def __str__(self):
		return self.content

class TissueExpressionResult(models.Model):
	result = models.ForeignKey(Result, on_delete=models.CASCADE)
	content = models.CharField(max_length=100)

	def __str__(self):
		return self.content

class GeneOntologyResult(models.Model):
	result = models.ForeignKey(Result, on_delete=models.CASCADE)
	content = models.CharField(max_length=100)

	def __str__(self):
		return self.content

class KeggResult(models.Model):
	result = models.ForeignKey(Result, on_delete=models.CASCADE)
	content = models.CharField(max_length=100)

	def __str__(self):
		return self.content

class LocalizationResult(models.Model):
	result = models.ForeignKey(Result, on_delete=models.CASCADE)
	content = models.CharField(max_length=100)

	def __str__(self):
		return self.content

class StrainResult(models.Model):
	result = models.ForeignKey(Result, on_delete=models.CASCADE)
	content = models.CharField(max_length=100)

	def __str__(self):
		return self.content
