from django.db import models

class Business(models.Model):
	name = models.CharField(max_length=200)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.name


class Branch(models.Model):
	business = models.ForeignKey(Business, related_name='business_branch', on_delete=models.CASCADE)
	location = models.CharField(max_length=150)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '{0} ({1})'.format(self.location, self.business.name)


class Department(models.Model):
	name = 	models.CharField(max_length=150,unique=True)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)	


	def __str__(self):
		return self.name 


class Bank(models.Model):
	name = 	models.CharField(max_length=150)
	branch = models.CharField(max_length=200,unique=True)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)	


	def __str__(self):
		return self.branch 


class Account(models.Model):
	bank = models.ForeignKey(Bank, related_name='bank_accounts', on_delete=models.CASCADE)
	account_name = 	models.CharField(max_length=200)
	account_no = models.CharField(max_length=20)		
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)			   

	def __str__(self):
		return self.account_no 	