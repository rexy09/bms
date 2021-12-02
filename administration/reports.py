from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .excels import *
from business.models import *
from business.pdfs import *
from .pdfs import *
from django.db.models import Avg, CharField, F, FloatField, Q, Sum, Value
from datetime import date, timedelta, datetime
from decimal import Decimal
from human_resource.decorators import *



@login_required
def general_reports(request, *args, **kwargs):
	template_name = 'general_reports.html'	
	return render(request, template_name, {})	


# """""""""" SALES REPORT """""""""""
@finance_report_required
@login_required
def sales_time(request, *args, **kwargs):
	return render(request, 'g_sale_time.html', {})

@finance_report_required
@login_required
def sales_report(request, *args, **kwargs):
	day = kwargs.get('d')
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')
	fr = request.GET.get('fr')
	to = request.GET.get('to')
	if day == 1:
		sales = Sale.objects.filter(created_at__date=date.today()).all().order_by('-pk')
		summary = Sale.objects.filter(created_at__date=date.today()).all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

		discount = 0
		tax = 0
		for sale in sales:
			if sale.discount_unit == 'flat':
				discount = discount + sale.discount
			elif sale.discount_unit == '%':
				disc = (Decimal(sale.discount)/100) * Decimal(sale.total)
				discount = discount + disc

			if sale.tax_unit == '%':
				t = ( Decimal(sale.tax)/100) * Decimal(sale.total)
				tax = tax + t
						
		summary['total_discount'] = discount
		summary['total_tax'] = tax

		data = Product.objects.filter(inventory_product__sale_inventory__created_at__date=date.today()).all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
		products = []
		for d in data:
			dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
			products.append(dic)

		if pdf == '1':
			return sales_report_export_pdf(request, products=products, summary=summary, sales=sales)

		if xl == '2':
			return sales_report_export_excel(request, sales=sales)	

	elif day == 2:	
		dt = date.today() - timedelta(days=1)
		sales = Sale.objects.filter(created_at__date=dt).all().order_by('-pk')	
		summary = Sale.objects.filter(created_at__date=dt).all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

		discount = 0
		tax = 0
		for sale in sales:
			if sale.discount_unit == 'flat':
				discount = discount + sale.discount
			elif sale.discount_unit == '%':
				disc = (Decimal(sale.discount)/100) * Decimal(sale.total)
				discount = discount + disc

			if sale.tax_unit == '%':
				t = ( Decimal(sale.tax)/100) * Decimal(sale.total)
				tax = tax + t				

		summary['total_discount'] = discount
		summary['total_tax'] = tax

		data = Product.objects.filter(inventory_product__sale_inventory__created_at__date=dt).all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
		products = []
		for d in data:
			dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
			products.append(dic)

		if pdf == '1':
			return sales_report_export_pdf(request, products=products, summary=summary, sales=sales)

		if xl == '2':
			return sales_report_export_excel(request, sales=sales)	

	elif day == 3:	
		dt = date.today() - timedelta(days=7)
		sales = Sale.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).all().order_by('-pk')
		summary = Sale.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

		discount = 0
		tax = 0
		for sale in sales:
			if sale.discount_unit == 'flat':
				discount = discount + sale.discount
			elif sale.discount_unit == '%':
				disc = (Decimal(sale.discount)/100) * Decimal(sale.total)
				discount = discount + disc

			if sale.tax_unit == '%':
				t = ( Decimal(sale.tax)/100) * Decimal(sale.total)
				tax = tax + t				

		summary['total_discount'] = discount
		summary['total_tax'] = tax

		data = Product.objects.filter(inventory_product__sale_inventory__created_at__date__gte=dt, inventory_product__sale_inventory__created_at__date__lte=date.today()).all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
		products = []
		for d in data:
			dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
			products.append(dic)

		if pdf == '1':
			return sales_report_export_pdf(request, products=products, summary=summary, sales=sales)

		if xl == '2':
			return sales_report_export_excel(request, sales=sales)

	elif day == 4:	
		dt = date.today() - timedelta(days=30)
		sales = Sale.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).all().order_by('-pk')	
		summary = Sale.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

		discount = 0
		tax = 0
		for sale in sales:
			if sale.discount_unit == 'flat':
				discount = discount + sale.discount
			elif sale.discount_unit == '%':
				disc = (Decimal(sale.discount)/100) * Decimal(sale.total)
				discount = discount + disc

			if sale.tax_unit == '%':
				t = ( Decimal(sale.tax)/100) * Decimal(sale.total)
				tax = tax + t				

		summary['total_discount'] = discount
		summary['total_tax'] = tax	

		data = Product.objects.filter(inventory_product__sale_inventory__created_at__date__gte=dt, inventory_product__sale_inventory__created_at__date__lte=date.today()).all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
		products = []
		for d in data:
			dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
			products.append(dic)

		if pdf == '1':
			return sales_report_export_pdf(request, products=products, summary=summary, sales=sales)	

		if xl == '2':
			return sales_report_export_excel(request, sales=sales)	

	elif day == 5:	
		dt = date.today()
		sales = Sale.objects.filter(created_at__month=dt.month, created_at__year=dt.year).all().order_by('-pk')
		summary = Sale.objects.filter(created_at__month=dt.month, created_at__year=dt.year).all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

		discount = 0
		tax = 0
		for sale in sales:
			if sale.discount_unit == 'flat':
				discount = discount + sale.discount
			elif sale.discount_unit == '%':
				disc = (Decimal(sale.discount)/100) * Decimal(sale.total)
				discount = discount + disc

			if sale.tax_unit == '%':
				t = ( Decimal(sale.tax)/100) * Decimal(sale.total)
				tax = tax + t				

		summary['total_discount'] = discount
		summary['total_tax'] = tax	

		data = Product.objects.filter(inventory_product__sale_inventory__created_at__month=dt.month, inventory_product__sale_inventory__created_at__year=dt.year).all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
		products = []
		for d in data:
			dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
			products.append(dic)

		if pdf == '1':
			return sales_report_export_pdf(request, products=products, summary=summary, sales=sales)

		if xl == '2':
			return sales_report_export_excel(request, sales=sales)
				
	elif day == 6:	
		dt = date.today()
		month = dt.month - 1
		sales = Sale.objects.filter(created_at__month=month, created_at__year=dt.year).all().order_by('-pk')	
		summary = Sale.objects.filter(created_at__month=month, created_at__year=dt.year).all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

		discount = 0
		tax = 0
		for sale in sales:
			if sale.discount_unit == 'flat':
				discount = discount + sale.discount
			elif sale.discount_unit == '%':
				disc = (Decimal(sale.discount)/100) * Decimal(sale.total)
				discount = discount + disc

			if sale.tax_unit == '%':
				t = ( Decimal(sale.tax)/100) * Decimal(sale.total)
				tax = tax + t				

		summary['total_discount'] = discount
		summary['total_tax'] = tax	

		data = Product.objects.filter(inventory_product__sale_inventory__created_at__month=month, inventory_product__sale_inventory__created_at__year=dt.year).all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
		products = []
		for d in data:
			dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
			products.append(dic)

		if pdf == '1':
			return sales_report_export_pdf(request,products=products, summary=summary, sales=sales)
		
		if xl == '2':
			return sales_report_export_excel(request,sales=sales)

	elif day == 7:	
		sales = Sale.objects.all().order_by('-pk')	
		summary = Sale.objects.all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

		discount = 0
		tax = 0
		for sale in sales:
			if sale.discount_unit == 'flat':
				discount = discount + sale.discount
			elif sale.discount_unit == '%':
				disc = (Decimal(sale.discount)/100) * Decimal(sale.total)
				discount = discount + disc

			if sale.tax_unit == '%':
				t = ( Decimal(sale.tax)/100) * Decimal(sale.total)
				tax = tax + t				

		summary['total_discount'] = discount
		summary['total_tax'] = tax	

		data = Product.objects.all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
		products = []
		for d in data:
			dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
			products.append(dic)	

		if pdf == '1':
			return sales_report_export_pdf(request, products=products, summary=summary, sales=sales)

		if xl == '2':
			return sales_report_export_excel(request, sales=sales)

	elif day == 8:
		if request.method == 'GET':	
			sales = Sale.objects.filter(created_at__date__gte=fr, created_at__date__lte=to).all().order_by('-pk')	
			summary = Sale.objects.filter(created_at__date__gte=fr, created_at__date__lte=to).all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

			discount = 0
			tax = 0
			for sale in sales:
				if sale.discount_unit == 'flat':
					discount = discount + sale.discount
				elif sale.discount_unit == '%':
					disc = (Decimal(sale.discount)/100) * Decimal(sale.total)
					discount = discount + disc

				if sale.tax_unit == '%':
					t = ( Decimal(sale.tax)/100) * Decimal(sale.total)
					tax = tax + t				

			summary['total_discount'] = discount
			summary['total_tax'] = tax	
			data = Product.objects.filter(inventory_product__sale_inventory__created_at__date__gte=fr, inventory_product__sale_inventory__created_at__date__lte=to).all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
			products = []
			for d in data:
				dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
				products.append(dic)

			if pdf == '1':
				return sales_report_export_pdf(request, products=products, summary=summary, sales=sales)

			if xl == '2':
				return sales_report_export_excel(request, sales=sales)
				
	context = {
		'sales':sales,
		'summary':summary,
		'products':products,
		'day':day,
		'fr':fr,
		'to':to,
	}
	return render(request, 'g_sales_report.html', context)



# """""""""" INVENTORY REPORT """""""""""
@store_report_required
@login_required
def inventory_product(request, *args, **kwargs):
	products = Product.objects.all()
	context = {
		'products':products,
	}
	return render(request, 'g_inventory_product.html', context)

@store_report_required
@login_required
def inventory_report(request, *args, **kwargs):
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')

	if request.method == 'GET':
		p = request.GET['p']

		if p == '0':
			inventory_qs = Inventory.objects.filter(exist=True).annotate(available=F('remain')-F('damage'))	
			if inventory_qs:
				inventory_qs.filter(available=0).update(exist=False)		
			inventories = Inventory.objects.all().order_by('-pk')
			summary = inventory_qs.aggregate(total_cost=Sum(F('available')*F('product_cost'),output_field=FloatField()),total_worth=Sum(F('available')*F('product__sell_price'),output_field=FloatField()))

			data = Product.objects.all()
			products = []
			for d in data:
				dic = {'name': d.name, 'quantity': d.quantity, 'worth':d.worth}
				products.append(dic)

			if pdf == '1':				
				return inventory_report_export_pdf(request, inventories=inventories, summary=summary, products=products,)

			if xl == '2':				
				return inventory_report_export_excel(request, inventories=inventories)

		else:
			inventory_qs = Inventory.objects.filter(product__id=p, exist=True).annotate(available=F('remain')-F('damage'))	
			if inventory_qs:
				inventory_qs.filter(available=0).update(exist=False)			
			inventories = Inventory.objects.filter(product__id=p).order_by('-pk')
			summary = inventory_qs.aggregate(total_cost=Sum(F('available')*F('product_cost'),output_field=FloatField()),total_worth=Sum(F('available')*F('product__sell_price'),output_field=FloatField()))

			data = Product.objects.filter(id=p).all()
			products = []
			for d in data:
				dic = {'name': d.name, 'quantity': d.quantity, 'worth':d.worth}
				products.append(dic)

			if pdf == '1':				
				return inventory_report_export_pdf(request, inventories=inventories, summary=summary, products=products,)

			if xl == '2':				
				return inventory_report_export_excel(request, inventories=inventories)	
			
	context = {
		'inventories':inventories,
		'summary':summary,
		'products':products,
		'p':p,
	}
	return render(request, 'g_inventory_report.html', context)


# """""""""" PROCUREMENT REPORT """""""""""
@procurement_finance_ceo_required
@login_required
def procurement_time(request, *args, **kwargs):
	return render(request, 'g_procurement_time.html', {})

@procurement_finance_ceo_required
@login_required
def procurement_report(request, *args, **kwargs):
	d = kwargs.get('d')
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')
	fr = request.GET.get('fr')
	to = request.GET.get('to')
	if d == 1:
		local_purchases = LocalPurchaseOrder.objects.filter(created_at__date=date.today(), published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
		purchases = PurchaseOrder.objects.filter(created_at__date=date.today(), published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')

		p_local_purchases = LocalPurchaseOrder.objects.filter(created_at__date=date.today(), published=True, authorized=False).all().count()
		p_purchases = PurchaseOrder.objects.filter(created_at__date=date.today(), published=True, authorized=False).all().count()

		summary = LocalPurchaseOrder.objects.filter(created_at__date=date.today(), published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)

		purchases_qs = PurchaseOrder.objects.filter(created_at__date=date.today(), published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
		summary['total_purchase'] = purchases_qs.filter(created_at__date=date.today(), published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']

		if pdf == '1':
			return procurement_report_export_pdf(request,local_purchases=local_purchases, purchases=purchases, summary=summary,)

		if xl == '2':
			return procurement_report_export_excel(request,local_purchases=local_purchases, purchases=purchases)	

	elif d == 2:	
		dt = date.today() - timedelta(days=1)

		local_purchases = LocalPurchaseOrder.objects.filter(created_at__date=dt, published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
		purchases = PurchaseOrder.objects.filter(created_at__date=dt, published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')
		p_local_purchases = LocalPurchaseOrder.objects.filter(created_at__date=dt, published=True, authorized=False).all().count()
		p_purchases = PurchaseOrder.objects.filter(created_at__date=dt, published=True, authorized=False).all().count()
		
		summary = LocalPurchaseOrder.objects.filter(created_at__date=dt, published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)

		purchases_qs = PurchaseOrder.objects.filter(created_at__date=dt, published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
		summary['total_purchase'] = purchases_qs.filter(created_at__date=dt, published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']


		if pdf == '1':
			return procurement_report_export_pdf(request, local_purchases=local_purchases, purchases=purchases, summary=summary,)

		if xl == '2':
			return procurement_report_export_excel(request, local_purchases=local_purchases, purchases=purchases)	
		
	elif d == 3:	
		dt = date.today() - timedelta(days=7)

		local_purchases = LocalPurchaseOrder.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
		purchases = PurchaseOrder.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')

		p_local_purchases = LocalPurchaseOrder.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, authorized=False).all().count()
		p_purchases = PurchaseOrder.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, authorized=False).all().count()
		
		
		summary = LocalPurchaseOrder.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)

		purchases_qs = PurchaseOrder.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
		summary['total_purchase'] = purchases_qs.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']

		if pdf == '1':
			return procurement_report_export_pdf(request,local_purchases=local_purchases, purchases=purchases, summary=summary,)

		if xl == '2':
			return procurement_report_export_excel(request,local_purchases=local_purchases, purchases=purchases)	

	elif d == 4:	
		dt = date.today() - timedelta(days=30)

		local_purchases = LocalPurchaseOrder.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
		purchases = PurchaseOrder.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')

		p_local_purchases = LocalPurchaseOrder.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, authorized=False).all().count()
		p_purchases = PurchaseOrder.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, authorized=False).all().count()
		
		summary = LocalPurchaseOrder.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)

		purchases_qs = PurchaseOrder.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
		summary['total_purchase'] = purchases_qs.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']

		if pdf == '1':
			return procurement_report_export_pdf(request,local_purchases=local_purchases, purchases=purchases, summary=summary,)

		if xl == '2':
			return procurement_report_export_excel(request,local_purchases=local_purchases, purchases=purchases)		
		
	elif d == 5:	
		dt = date.today()
		local_purchases = LocalPurchaseOrder.objects.filter(created_at__month=dt.month, created_at__year=dt.year, published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
		purchases = PurchaseOrder.objects.filter(created_at__month=dt.month, created_at__year=dt.year, published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')

		p_local_purchases = LocalPurchaseOrder.objects.filter(created_at__month=dt.month, created_at__year=dt.year, published=True, authorized=False).all().count()
		p_purchases = PurchaseOrder.objects.filter(created_at__month=dt.month, created_at__year=dt.year, published=True, authorized=False).all().count()
		
		summary = LocalPurchaseOrder.objects.filter(created_at__month=dt.month, created_at__year=dt.year, published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)

		purchases_qs = PurchaseOrder.objects.filter(created_at__month=dt.month, created_at__year=dt.year, published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
		summary['total_purchase'] = purchases_qs.filter(created_at__month=dt.month, created_at__year=dt.year, published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']

		if pdf == '1':
			return procurement_report_export_pdf(request,local_purchases=local_purchases, purchases=purchases, summary=summary,)

		if xl == '2':
			return procurement_report_export_excel(request,local_purchases=local_purchases, purchases=purchases)	
	
	elif d == 6:	
		dt = date.today()
		month = dt.month - 1
		local_purchases = LocalPurchaseOrder.objects.filter(created_at__month=month, created_at__year=dt.year, published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
		purchases = PurchaseOrder.objects.filter(created_at__month=month, created_at__year=dt.year, published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')

		p_local_purchases = LocalPurchaseOrder.objects.filter(created_at__month=month, created_at__year=dt.year, published=True, authorized=False).all().count()
		p_purchases = PurchaseOrder.objects.filter(created_at__month=month, created_at__year=dt.year, published=True, authorized=False).all().count()
		
		summary = LocalPurchaseOrder.objects.filter(created_at__month=month, created_at__year=dt.year, published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)

		purchases_qs = PurchaseOrder.objects.filter(created_at__month=month, created_at__year=dt.year, published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
		summary['total_purchase'] = purchases_qs.filter(created_at__month=month, created_at__year=dt.year, published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']

		if pdf == '1':
			return procurement_report_export_pdf(request,local_purchases=local_purchases, purchases=purchases, summary=summary,)

		if xl == '2':
			return procurement_report_export_excel(request,local_purchases=local_purchases, purchases=purchases)	

	elif d == 7:	
		local_purchases = LocalPurchaseOrder.objects.filter(published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
		purchases = PurchaseOrder.objects.filter(published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')

		p_local_purchases = LocalPurchaseOrder.objects.filter(published=True, authorized=False).all().count()
		p_purchases = PurchaseOrder.objects.filter(published=True, authorized=False).all().count()
		
		summary = LocalPurchaseOrder.objects.filter(published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)
		purchases_qs = PurchaseOrder.objects.filter(published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
		summary['total_purchase'] = purchases_qs.filter(published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']

		if pdf == '1':
			return procurement_report_export_pdf(request,local_purchases=local_purchases, purchases=purchases, summary=summary,)

		if xl == '2':
			return procurement_report_export_excel(request,local_purchases=local_purchases, purchases=purchases)	
	
	elif d == 8:
		if request.method == 'GET':	
			local_purchases = LocalPurchaseOrder.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
			purchases = PurchaseOrder.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')

			p_local_purchases = LocalPurchaseOrder.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, published=True, authorized=False).all().count()
			p_purchases = PurchaseOrder.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, published=True, authorized=False).all().count()
			
			summary = LocalPurchaseOrder.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)
			
			purchases_qs = PurchaseOrder.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
			summary['total_purchase'] = purchases_qs.filter(created_at__date__gte=fr, created_at__date__lte=to, published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']


			if pdf == '1':
				return procurement_report_export_pdf(request,local_purchases=local_purchases, purchases=purchases, summary=summary,)

			if xl == '2':
				return procurement_report_export_excel(request,local_purchases=local_purchases, purchases=purchases)		

	context = {
		'local_purchases':local_purchases,
		'purchases':purchases,
		'summary':summary,
		'd':d,
		'fr':fr,
		'to':to,
		'p_local_purchases':p_local_purchases,
		'p_purchases':p_purchases,
	}
	return render(request, 'g_procurement_report.html', context)



############ OPEX Report ###########    
@finance_report_required
@login_required
def opex_report(request, *args, **kwargs):

	day = kwargs.get('d')
	fr = request.GET.get('fr')
	to = request.GET.get('to')	
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')


	exps_objects = []

	if day == 1:	
		expense_objects = Expense.objects.filter(created_at__date=date.today())
		total_cost = Expense.objects.filter(created_at__date=date.today()).aggregate(Sum('cost'))['cost__sum'] 
		expenses = Expense.objects.filter(created_at__date=date.today()).count()          
		exps = Expense.objects.filter(created_at__date=date.today())

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps)

		if xl == '2':
			return opex_report_export_excel(request, expense_objects=expense_objects)	

	elif day == 2:	
		dt = date.today() - timedelta(days=1)
		expense_objects = Expense.objects.filter(created_at__date=dt)
		total_cost = Expense.objects.filter(created_at__date=dt).aggregate(Sum('cost'))['cost__sum'] 
		expenses = Expense.objects.filter(created_at__date=dt).count()          
		exps = Expense.objects.filter(created_at__date=dt)

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps)

		if xl == '2':
   			return opex_report_export_excel(request, expense_objects=expense_objects)	
	

	elif day == 3:	
		dt = date.today() - timedelta(days=7)
		expense_objects = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today())
		total_cost = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('cost'))['cost__sum'] 
		expenses = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).count()          
		exps = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today())

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps)

		if xl == '2':
   			return opex_report_export_excel(request, expense_objects=expense_objects)	

	elif day == 4:	
		dt = date.today() - timedelta(days=30)
		expense_objects = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today())
		total_cost = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('cost'))['cost__sum'] 
		expenses = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).count()          
		exps = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today())

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps)

		if xl == '2':
   			return opex_report_export_excel(request, expense_objects=expense_objects)	

	elif day == 5:	
		dt = date.today()
		expense_objects = Expense.objects.filter(created_at__month=dt.month, created_at__year=dt.year)
		total_cost = Expense.objects.filter(created_at__month=dt.month, created_at__year=dt.year).aggregate(Sum('cost'))['cost__sum'] 
		expenses = Expense.objects.filter(created_at__month=dt.month, created_at__year=dt.year).count()          
		exps = Expense.objects.filter(created_at__month=dt.month, created_at__year=dt.year)

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps)

		if xl == '2':
   			return opex_report_export_excel(request, expense_objects=expense_objects)	

	elif day == 6:	
		dt = date.today()
		month = dt.month - 1
		expense_objects = Expense.objects.filter(created_at__month=month, created_at__year=dt.year)
		total_cost = Expense.objects.filter(created_at__month=month, created_at__year=dt.year).aggregate(Sum('cost'))['cost__sum'] 
		expenses = Expense.objects.filter(created_at__month=month, created_at__year=dt.year).count()          
		exps = Expense.objects.filter(created_at__month=month, created_at__year=dt.year)

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps)

		if xl == '2':
			return opex_report_export_excel(request, expense_objects=expense_objects)	

	elif day == 7:	
		expense_objects = Expense.objects.all()
		total_cost = Expense.objects.aggregate(Sum('cost'))['cost__sum'] 
		expenses = Expense.objects.all().count()          
		exps = Expense.objects.all()

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps)

		if xl == '2':
   			return opex_report_export_excel(request, expense_objects=expense_objects)	

	elif day == 8:
		if request.method == 'GET':	
			expense_objects = Expense.objects.filter(created_at__date__gte=fr, created_at__date__lte=to)
			total_cost = Expense.objects.filter(created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('cost'))['cost__sum'] 
			expenses = Expense.objects.filter(created_at__date__gte=fr, created_at__date__lte=to).count()          
			exps = Expense.objects.filter(created_at__date__gte=fr, created_at__date__lte=to)

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps)
			
		if xl == '2':
   			return opex_report_export_excel(request, expense_objects=expense_objects)	

	if total_cost is None:
		total_cost = 0


	for exp in exps:
		exps_objects.append({'name': exp.category, 'cost':exp.cost})

	context = {
		'expenses': expense_objects,
		'cost': total_cost,
		'expenses_total': str(expenses),
		'exps' : exps_objects,
		'day': day,
		'fr' : fr,
		'to' : to,
	}
	template_name = 'g-opex-report.html'

	return render(request, template_name, context)


########## Opex Report - time ##############
@finance_report_required
@login_required
def opex_time(request, *args, **kwargs):
	context = {
	}
	return render(request, 'g-opex-time.html', context)	

@finance_report_required
@login_required
def customer_report(request, *args, **kwargs):
	pdf = request.GET.get('pdf')
	customers = Customer.objects.all()
	url_parameter = request.GET.get("q")

	for customer in customers:
		customer_sales = Sale.objects.filter(customer=customer)
		dates = []

		for sale in customer_sales:

			customer_point = {f'{customer.full_name} : {sale.created_at.date()}'}

			if customer_point in dates:
				pass
			else:
				dates.append({f'{customer.full_name} : {sale.created_at.date()}'})

		points = len(dates)

		Customer.objects.filter(id=customer.id,).update(points=points)

		if customer.points == 30:
			Customer.objects.filter(id=customer.id,).update(category='Loyal')



	if url_parameter:
		customers = Customer.objects.filter(Q(full_name__icontains=url_parameter) | Q(contact__icontains=url_parameter))

	else:
		customers = Customer.objects.all()
			

	if request.is_ajax():
		html = render_to_string(
			template_name='customer-results.html',
			context={'customers':customers}
		)

		data_dict = {"html_from_view": html}

		return JsonResponse(data=data_dict, safe=False)

	normal_customers = Customer.objects.filter(category="Normal", ).count()	
	loyal_customers = Customer.objects.filter(category="Loyal", ).count()	
	other_customers = Sale.objects.filter(customer=None,).count()

	if pdf == '1':
		return customer_report_export_pdf(request, customers=customers, normal=normal_customers, loyal=loyal_customers, other=other_customers)

	customer_category = [
		{"name": "Loyal customers", "value": loyal_customers},
		{"name": "Normal customers", "value": normal_customers},
		{"name": "Other customers", "value": other_customers},
		]

	context = {
		'customers': customers,
		'categories': customer_category,
		'normal': normal_customers,
		'loyal': loyal_customers,
		'other': other_customers,
	}
	template_name = 'g-customer-report.html'
	return render(request, template_name, context)


############ Payroll Report ###########    
@finance_report_required
@login_required
def payroll_report(request, *args, **kwargs):

	id = kwargs.get('id')
	day = kwargs.get('d')
	fr = request.GET.get('fr')
	to = request.GET.get('to')
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')

	business = Business.objects.filter(id=id).first()

	if day == 1:
		takehome = Takehome.objects.filter(created_at__date=date.today())
		employees = Payroll.objects.filter(created_at__date=date.today()).count()           
		deduction = Payroll.objects.filter(created_at__date=date.today()).aggregate(Sum('deduction'))['deduction__sum']   		
		bonuses = Payroll.objects.filter(created_at__date=date.today()).aggregate(Sum('bonus'))['bonus__sum']   		
		overtime = Payroll.objects.filter(created_at__date=date.today()).aggregate(Sum('overtime'))['overtime__sum']    		
		nssf_funds = Payroll.objects.filter(nssf=True, created_at__date=date.today()).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		# wcf = Payroll.objects.filter(tax_rate__icontains='wcf', created_at__date=date.today())
		loan_board_funds = Payroll.objects.filter(heslb=True, created_at__date=date.today()).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		salaries = Payroll.objects.filter(created_at__date=date.today()).aggregate(Sum('employee__salary'))['employee__salary__sum']
		paye_total = Payroll.objects.filter(paye=True, created_at__date=date.today()).aggregate(Sum('paye_amount'))['paye_amount__sum']
		takehome_total = Takehome.objects.filter(created_at__date=date.today()).aggregate(Sum('salary'))['salary__sum']
		sdl = Payroll.objects.filter(created_at__date=date.today()).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		

		if paye_total is None:
			paye_total = 0

		if nssf_funds is None:
			nssf_funds = 0

		if loan_board_funds is None:
			loan_board_funds = 0		

		if bonuses is None:
			bonuses = 0
		if overtime is None:
			overtime = 0
		if takehome_total is None:
			takehome_total = 0
		if deduction is None:
			deduction = 0
		if sdl is None:
			sdl = 0				

		total = int(nssf_funds) + int(paye_total) + int(loan_board_funds) + takehome_total + int(sdl)

		if pdf == '1':
			return payroll_report_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries, deduction=deduction, sdl=sdl)
		if xl == '1':
			return payroll_report_export_excel(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

	elif day == 2:	
		dt = date.today() - timedelta(days=1)
		takehome = Takehome.objects.filter(created_at__date=dt)
		employees = Payroll.objects.filter(created_at__date=dt).count()           
		sdl = Payroll.objects.filter(created_at__date=dt).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		deduction = Payroll.objects.filter(created_at__date=dt).aggregate(Sum('deduction'))['deduction__sum']   		
		bonuses = Payroll.objects.filter(created_at__date=dt).aggregate(Sum('bonus'))['bonus__sum']   		
		overtime = Payroll.objects.filter(created_at__date=dt).aggregate(Sum('overtime'))['overtime__sum']    		
		nssf_funds = Payroll.objects.filter(nssf=True, created_at__date=dt).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True, created_at__date=dt).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		salaries = Payroll.objects.filter(created_at__date=dt).aggregate(Sum('employee__salary'))['employee__salary__sum']
		paye_total = Payroll.objects.filter(paye=True, created_at__date=dt).aggregate(Sum('paye_amount'))['paye_amount__sum']
		takehome_total = Takehome.objects.filter(created_at__date=dt).aggregate(Sum('salary'))['salary__sum']


		if paye_total is None:
			paye_total = 0

		if nssf_funds is None:
			nssf_funds = 0

		if loan_board_funds is None:
			loan_board_funds = 0	

		if bonuses is None:
			bonuses = 0
		if overtime is None:
			overtime = 0
		if takehome_total is None:
			takehome_total = 0		
		if deduction is None:
			deduction = 0
		if sdl is None:
			sdl = 0	

		total = int(nssf_funds) + int(paye_total) + int(loan_board_funds) + takehome_total + int(sdl)

		if pdf == '1':
			return payroll_report_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries,deduction=deduction, sdl=sdl)
		if xl == '1':
			return payroll_report_export_excel(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

	elif day == 3:	
		dt = date.today() - timedelta(days=7)
		takehome = Takehome.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today())
		employees = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).count()           
		sdl = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		deduction = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('deduction'))['deduction__sum']   		
		bonuses = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('bonus'))['bonus__sum']   		
		overtime = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('overtime'))['overtime__sum']    		
		nssf_funds = Payroll.objects.filter(nssf=True, created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True, created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		salaries = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('employee__salary'))['employee__salary__sum']
		paye_total = Payroll.objects.filter(paye=True, created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('paye_amount'))['paye_amount__sum']
		takehome_total = Takehome.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('salary'))['salary__sum']


		if paye_total is None:
			paye_total = 0

		if nssf_funds is None:
			nssf_funds = 0

		if loan_board_funds is None:
			loan_board_funds = 0	

		if bonuses is None:
			bonuses = 0
		if overtime is None:
			overtime = 0
		if takehome_total is None:
			takehome_total = 0	
		if deduction is None:
			deduction = 0
		if sdl is None:
			sdl = 0			

		total = int(nssf_funds) + int(paye_total) + int(loan_board_funds) + takehome_total + int(sdl)

		if pdf == '1':
			return payroll_report_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries, deduction=deduction, sdl=sdl)
		if xl == '1':
			return payroll_report_export_excel(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

	elif day == 4:	
		dt = date.today() - timedelta(days=30)
		takehome = Takehome.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today())
		employees = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).count()           
		sdl = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		deduction = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('deduction'))['deduction__sum']   		
		bonuses = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('bonus'))['bonus__sum']   		
		overtime = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('overtime'))['overtime__sum']    		
		nssf_funds = Payroll.objects.filter(nssf=True, created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True, created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		salaries = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('employee__salary'))['employee__salary__sum']
		paye_total = Payroll.objects.all().filter(paye=True, created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('paye_amount'))['paye_amount__sum']
		takehome_total = Takehome.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today()).aggregate(Sum('salary'))['salary__sum']


		if paye_total is None:
			paye_total = 0

		if nssf_funds is None:
			nssf_funds = 0

		if loan_board_funds is None:
			loan_board_funds = 0	

		if bonuses is None:
			bonuses = 0
		if overtime is None:
			overtime = 0
		if takehome_total is None:
			takehome_total = 0		
		if deduction is None:
			deduction = 0
		if sdl is None:
			sdl = 0	
 
		total = int(nssf_funds) + int(paye_total) + int(loan_board_funds) + takehome_total + int(sdl)

		if pdf == '1':
			return payroll_report_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries, deduction=deduction, sdl=sdl)
		if xl == '1':
			return payroll_report_export_excel(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

	elif day == 5:	
		dt = date.today()
		takehome = Takehome.objects.filter(created_at__month=dt.month, created_at__year=dt.year)
		employees = Payroll.objects.filter(created_at__month=dt.month, created_at__year=dt.year).count()           
		sdl = Payroll.objects.filter(created_at__month=dt.month, created_at__year=dt.year).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		deduction = Payroll.objects.filter(created_at__month=dt.month, created_at__year=dt.year).aggregate(Sum('deduction'))['deduction__sum']   		
		bonuses = Payroll.objects.filter(created_at__month=dt.month, created_at__year=dt.year).aggregate(Sum('bonus'))['bonus__sum']   		
		overtime = Payroll.objects.filter(created_at__month=dt.month, created_at__year=dt.year).aggregate(Sum('overtime'))['overtime__sum']    		
		nssf_funds = Payroll.objects.filter(nssf=True, created_at__month=dt.month, created_at__year=dt.year).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True, created_at__month=dt.month, created_at__year=dt.year).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		salaries = Payroll.objects.filter(created_at__month=dt.month, created_at__year=dt.year).aggregate(Sum('employee__salary'))['employee__salary__sum']
		paye_total = Payroll.objects.filter(paye=True, created_at__month=dt.month, created_at__year=dt.year).aggregate(Sum('paye_amount'))['paye_amount__sum']
		takehome_total = Takehome.objects.filter(created_at__month=dt.month, created_at__year=dt.year).aggregate(Sum('salary'))['salary__sum']


		if paye_total is None:
			paye_total = 0

		if nssf_funds is None:
			nssf_funds = 0

		if loan_board_funds is None:
			loan_board_funds = 0	


		if bonuses is None:
			bonuses = 0
		if overtime is None:
			overtime = 0
		if takehome_total is None:
			takehome_total = 0	
		if deduction is None:
			deduction = 0
		if sdl is None:
			sdl = 0			

		total = int(nssf_funds) + int(paye_total) + int(loan_board_funds) + takehome_total + int(sdl)

		if pdf == '1':
			return payroll_report_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries, deduction=deduction, sdl=sdl)
		if xl == '1':
			return payroll_report_export_excel(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

	elif day == 6:	
		dt = date.today()
		month = dt.month - 1
		takehome = Takehome.objects.filter(created_at__month=month, created_at__year=dt.year)
		employees = Payroll.objects.filter(created_at__month=month, created_at__year=dt.year).count()           
		sdl = Payroll.objects.filter(created_at__month=month, created_at__year=dt.year).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		deduction = Payroll.objects.filter(created_at__month=month, created_at__year=dt.year).aggregate(Sum('deduction'))['deduction__sum']   		
		bonuses = Payroll.objects.filter(created_at__month=month, created_at__year=dt.year).aggregate(Sum('bonus'))['bonus__sum']   		
		overtime = Payroll.objects.filter(created_at__month=month, created_at__year=dt.year).aggregate(Sum('overtime'))['overtime__sum']    		
		nssf_funds = Payroll.objects.filter(nssf=True, created_at__month=month, created_at__year=dt.year).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True, created_at__month=month, created_at__year=dt.year).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		salaries = Payroll.objects.filter(created_at__month=month, created_at__year=dt.year).aggregate(Sum('employee__salary'))['employee__salary__sum']
		paye_total = Payroll.objects.filter(paye=True, created_at__month=month, created_at__year=dt.year).aggregate(Sum('paye_amount'))['paye_amount__sum']
		takehome_total = Takehome.objects.filter(created_at__month=month, created_at__year=dt.year).aggregate(Sum('salary'))['salary__sum']


		if paye_total is None:
			paye_total = 0

		if nssf_funds is None:
			nssf_funds = 0

		if loan_board_funds is None:
			loan_board_funds = 0	


		if bonuses is None:
			bonuses = 0
		if overtime is None:
			overtime = 0
		if takehome_total is None:
			takehome_total = 0	
		if deduction is None:
			deduction = 0	
		if sdl is None:
			sdl = 0		

		total = int(nssf_funds) + int(paye_total) + int(loan_board_funds) + takehome_total + int(sdl)

		if pdf == '1':
			return payroll_report_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries, deduction=deduction, sdl=sdl)
		if xl == '1':
			return payroll_report_export_excel(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

	elif day == 7:	
		takehome = Takehome.objects.all()
		employees = Payroll.objects.all().count()           
		sdl = Payroll.objects.all().aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		deduction = Payroll.objects.all().aggregate(Sum('deduction'))['deduction__sum']   		
		bonuses = Payroll.objects.all().aggregate(Sum('bonus'))['bonus__sum']   		
		overtime = Payroll.objects.all().aggregate(Sum('overtime'))['overtime__sum']    		
		nssf_funds = Payroll.objects.filter(nssf=True).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		salaries = Payroll.objects.all().aggregate(Sum('employee__salary'))['employee__salary__sum']
		paye_total = Payroll.objects.filter(paye=True).aggregate(Sum('paye_amount'))['paye_amount__sum']
		takehome_total = Takehome.objects.all().aggregate(Sum('salary'))['salary__sum']

		if paye_total is None:
			paye_total = 0

		if nssf_funds is None:
			nssf_funds = 0

		if loan_board_funds is None:
			loan_board_funds = 0	

		if bonuses is None:
			bonuses = 0
		if overtime is None:
			overtime = 0
		if takehome_total is None:
			takehome_total = 0
		if deduction is None:
			deduction = 0
		if sdl is None:
			sdl = 0				

		total = int(nssf_funds) + int(paye_total) + int(loan_board_funds) + takehome_total + int(sdl)

		if pdf == '1':
			return payroll_report_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries, deduction=deduction, sdl=sdl)
		if xl == '1':
			return payroll_report_export_excel(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

	elif day == 8:
		if request.method == 'GET':	
			takehome = Takehome.objects.filter(created_at__date__gte=fr, created_at__date__lte=to)
			employees = Payroll.objects.filter(created_at__date__gte=fr, created_at__date__lte=to).count()           
			sdl = Payroll.objects.filter(created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
			deduction = Payroll.objects.filter(created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('deduction'))['deduction__sum']   		
			bonuses = Payroll.objects.filter(created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('bonus'))['bonus__sum']   		
			overtime = Payroll.objects.filter(created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('overtime'))['overtime__sum']    		
			nssf_funds = Payroll.objects.filter(nssf=True, created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
			loan_board_funds = Payroll.objects.filter(heslb=True, created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
			salaries = Payroll.objects.filter(created_at__date__gte=fr, created_at__date__lte=to).all().aggregate(Sum('employee__salary'))['employee__salary__sum']
			paye_total = Payroll.objects.filter(paye=True, created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('paye_amount'))['paye_amount__sum']
			takehome_total = Takehome.objects.filter(created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('salary'))['salary__sum']

			if paye_total is None:
				paye_total = 0

			if nssf_funds is None:
				nssf_funds = 0

			if loan_board_funds is None:
				loan_board_funds = 0	

			if bonuses is None:
				bonuses = 0
			if overtime is None:
				overtime = 0
			if takehome_total is None:
				takehome_total = 0
			if deduction is None:
				deduction = 0
			if sdl is None:
				sdl = 0				

			total = int(nssf_funds) + int(paye_total) + int(loan_board_funds) + takehome_total + int(sdl)

			if pdf == '1':
				return payroll_report_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries, deduction=deduction, sdl=sdl)
			if xl == '1':
				return payroll_report_export_excel(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

	if bonuses is None:
		bonuses = 0
	if overtime is None:
		overtime = 0
	if takehome_total is None:
		takehome_total = 0		

	### Total payroll expenses
	total_expenses = int(nssf_funds) + int(paye_total) + int(loan_board_funds) + takehome_total + int(sdl)

	funds = [
		{ 'name': 'Paye', 'cost': int(paye_total) },
		{ 'name': 'Helsb', 'cost': int(loan_board_funds) },
		{ 'name': 'Nssf', 'cost': int(nssf_funds) },
	]	

	extras = [

		{ 'name': 'Takehome', 'cost': takehome_total },
		{ 'name': 'Overtime', 'cost': overtime },
		{ 'name': 'Bonus', 'cost': bonuses },

	]

	context = {
		'business' : business,
		# 'payroll' : payroll_objects,
		'takehome': takehome,
		'takehome_total': takehome_total,
		'nssf': int(nssf_funds),
		'loan_board': int(loan_board_funds),
		'deduction': deduction,
		'bonus': bonuses,
		'sdl': sdl,
		'salaries_total': salaries,
		'overtime': overtime,
		'paye': int(paye_total),
		'employees': employees,
		'funds': funds,
		'extras': extras,
		'total_expenses': total_expenses,
		'day': day,
		'fr': fr,
		'to': to,
	}
	template_name = 'g-payroll-report.html'

	return render(request, template_name, context)


########## Payroll Report - time ##############
@finance_report_required
@login_required
def payroll_time(request, *args, **kwargs):
	context = {
	}
	return render(request, 'g-payroll-time.html', context)



# """""""""" STOCK REPORT """""""""""
@login_required
def stock_time(request, *args, **kwargs):
	context = {
	}
	return render(request, 'g_stock_time.html', context)

		
@login_required
def stock_report(request, *args, **kwargs):
	d = kwargs.get('d')
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')
	fr = request.GET.get('fr')
	to = request.GET.get('to')
	if d == 1:
		dt = date.today()
		stocks = Stock.objects.filter(stock_date__month=dt.month,).all()
		opening = Stock.objects.filter(stock_date__month=dt.month, stock_type='Opening Stock').aggregate(Sum('cost'))['cost__sum']
		closing = Stock.objects.filter(stock_date__month=dt.month, stock_type='Closing Stock').aggregate(Sum('cost'))['cost__sum']
	
		if pdf == '1':
			return stock_report_export_pdf(request, stocks=stocks)

		if xl == '2':
			return stock_report_export_excel(request, stocks=stocks)	

	elif d == 2:	
		dt = date.today()
		month = dt.month - 1

		stocks = Stock.objects.filter(stock_date__month=month,).all()
		opening = Stock.objects.filter(stock_date__month=month, stock_type='Opening Stock').aggregate(Sum('cost'))['cost__sum']
		closing = Stock.objects.filter(stock_date__month=month, stock_type='Closing Stock').aggregate(Sum('cost'))['cost__sum']

		if pdf == '1':
			return stock_report_export_pdf(request, stocks=stocks)

		if xl == '2':
			return stock_report_export_excel(request,stocks=stocks)	
		
	elif d == 3:	
		stocks = Stock.objects.all()
		opening = Stock.objects.filter(stock_type='Opening Stock').aggregate(Sum('cost'))['cost__sum']
		closing = Stock.objects.filter(stock_type='Closing Stock').aggregate(Sum('cost'))['cost__sum']

		if pdf == '1':
			return stock_report_export_pdf(request, stocks=stocks)

		if xl == '2':
			return stock_report_export_excel(request,stocks=stocks)	
	
	elif d == 4:
		if request.method == 'GET':	

			stocks = Stock.objects.filter(stock_date__gte=fr,stock_date__lte=to,).all()
			opening = Stock.objects.filter(stock_date__gte=fr, stock_date__lte=to, stock_type='Opening Stock').aggregate(Sum('cost'))['cost__sum']
			closing = Stock.objects.filter(stock_date__gte=fr, stock_date__lte=to, stock_type='Closing Stock').aggregate(Sum('cost'))['cost__sum']

			if pdf == '1':
				return stock_report_export_pdf(request, stocks=stocks)

			if xl == '2':
				return stock_report_export_excel(request,stocks=stocks)		

	context = {
		'stocks':stocks,
		'd':d,
		'fr':fr,
		'to':to,
	}
	return render(request, 'g_stock_report.html', context)
