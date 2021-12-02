from django.shortcuts import render, redirect
from administration.models import *
from .models import *
from django.db.models import Avg, CharField, F, FloatField, Q, Sum, Value
from datetime import date, timedelta, datetime
from decimal import Decimal
from .pdfs import *
from .excels import *
from django.contrib.auth.decorators import login_required
from human_resource.decorators import *


@login_required
def reports(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first() 
	context = {
		'business':business,
	}
	return render(request, 'reports.html', context)


# """""""""" PROCUREMENT REPORT """""""""""
@procurement_finance_ceo_required
@login_required
def procurement_time(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first()
	context = {
		'business':business,
	}
	return render(request, 'procurement_time.html', context)

@procurement_finance_ceo_required
@login_required
def procurement_report(request, *args, **kwargs):
	id = kwargs.get('id')
	d = kwargs.get('d')
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')
	fr = request.GET.get('fr')
	to = request.GET.get('to')
	business = Business.objects.filter(id=id).first() 
	if d == 1:
		local_purchases = LocalPurchaseOrder.objects.filter(business=business, created_at__date=date.today(), published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
		purchases = PurchaseOrder.objects.filter(business=business, created_at__date=date.today(), published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')

		p_local_purchases = LocalPurchaseOrder.objects.filter(business=business, created_at__date=date.today(), published=True, authorized=False).all().count()
		p_purchases = PurchaseOrder.objects.filter(business=business, created_at__date=date.today(), published=True, authorized=False).all().count()
		
		summary = LocalPurchaseOrder.objects.filter(business=business, created_at__date=date.today(), published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)

		purchases_qs = PurchaseOrder.objects.filter(business=business, created_at__date=date.today(), published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
		summary['total_purchase'] = purchases_qs.filter(business=business, created_at__date=date.today(), published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']

		if pdf == '1':
			return procurement_report_export_pdf(request,business=business, local_purchases=local_purchases, purchases=purchases, summary=summary,)

		if xl == '2':
			return procurement_report_export_excel(request,business=business, local_purchases=local_purchases, purchases=purchases)	

	elif d == 2:	
		dt = date.today() - timedelta(days=1)

		local_purchases = LocalPurchaseOrder.objects.filter(business=business, created_at__date=dt, published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
		purchases = PurchaseOrder.objects.filter(business=business, created_at__date=dt, published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')

		p_local_purchases = LocalPurchaseOrder.objects.filter(business=business, created_at__date=dt, published=True, authorized=False).all().count()
		p_purchases = PurchaseOrder.objects.filter(business=business, created_at__date=dt, published=True, authorized=False).all().count()
		
		summary = LocalPurchaseOrder.objects.filter(business=business, created_at__date=dt, published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)

		purchases_qs = PurchaseOrder.objects.filter(business=business, created_at__date=dt, published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
		summary['total_purchase'] = purchases_qs.filter(business=business, created_at__date=dt, published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']

		if pdf == '1':
			return procurement_report_export_pdf(request,business=business, local_purchases=local_purchases, purchases=purchases, summary=summary,)

		if xl == '2':
			return procurement_report_export_excel(request,business=business, local_purchases=local_purchases, purchases=purchases)	
		
	elif d == 3:	
		dt = date.today() - timedelta(days=7)

		local_purchases = LocalPurchaseOrder.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today(), published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
		purchases = PurchaseOrder.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')

		p_local_purchases = LocalPurchaseOrder.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, authorized=False).all().count()
		p_purchases = PurchaseOrder.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, authorized=False).all().count()
		
		summary = LocalPurchaseOrder.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)

		purchases_qs = PurchaseOrder.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
		summary['total_purchase'] = purchases_qs.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']

		if pdf == '1':
			return procurement_report_export_pdf(request,business=business, local_purchases=local_purchases, purchases=purchases, summary=summary,)

		if xl == '2':
			return procurement_report_export_excel(request,business=business, local_purchases=local_purchases, purchases=purchases)	

	elif d == 4:	
		dt = date.today() - timedelta(days=30)

		local_purchases = LocalPurchaseOrder.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today(), published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
		purchases = PurchaseOrder.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')
		p_local_purchases = LocalPurchaseOrder.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, authorized=False).all().count()
		p_purchases = PurchaseOrder.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, authorized=False).all().count()
		
		summary = LocalPurchaseOrder.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)

		purchases_qs = PurchaseOrder.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
		summary['total_purchase'] = purchases_qs.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today(), published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']

		if pdf == '1':
			return procurement_report_export_pdf(request,business=business, local_purchases=local_purchases, purchases=purchases, summary=summary,)

		if xl == '2':
			return procurement_report_export_excel(request,business=business, local_purchases=local_purchases, purchases=purchases)		
		
	elif d == 5:	
		dt = date.today()
		local_purchases = LocalPurchaseOrder.objects.filter(business=business, created_at__month=dt.month, created_at__year=dt.year, published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
		purchases = PurchaseOrder.objects.filter(business=business, created_at__month=dt.month, created_at__year=dt.year, published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')
		p_local_purchases = LocalPurchaseOrder.objects.filter(business=business, created_at__month=dt.month, created_at__year=dt.year, published=True, authorized=False).all().count()
		p_purchases = PurchaseOrder.objects.filter(business=business, created_at__month=dt.month, created_at__year=dt.year, published=True, authorized=False).all().count()
		
		summary = LocalPurchaseOrder.objects.filter(business=business, created_at__month=dt.month, created_at__year=dt.year, published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)

		purchases_qs = PurchaseOrder.objects.filter(business=business, created_at__month=dt.month, created_at__year=dt.year, published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
		summary['total_purchase'] = purchases_qs.filter(business=business, created_at__month=dt.month, created_at__year=dt.year, published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']

		if pdf == '1':
			return procurement_report_export_pdf(request,business=business, local_purchases=local_purchases, purchases=purchases, summary=summary,)

		if xl == '2':
			return procurement_report_export_excel(request,business=business, local_purchases=local_purchases, purchases=purchases)	
	
	elif d == 6:	
		dt = date.today()
		month = dt.month - 1
		local_purchases = LocalPurchaseOrder.objects.filter(business=business, created_at__month=month, created_at__year=dt.year, published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
		purchases = PurchaseOrder.objects.filter(business=business, created_at__month=month, created_at__year=dt.year, published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')

		p_local_purchases = LocalPurchaseOrder.objects.filter(business=business, created_at__month=month, created_at__year=dt.year, published=True, authorized=False).all().count()
		p_purchases = PurchaseOrder.objects.filter(business=business, created_at__month=month, created_at__year=dt.year, published=True, authorized=False).all().count()

		summary = LocalPurchaseOrder.objects.filter(business=business, created_at__month=month, created_at__year=dt.year, published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)
		
		purchases_qs = PurchaseOrder.objects.filter(business=business, created_at__month=month, created_at__year=dt.year, published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
		summary['total_purchase'] = purchases_qs.filter(business=business, created_at__month=month, created_at__year=dt.year, published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']

		if pdf == '1':
			return procurement_report_export_pdf(request,business=business, local_purchases=local_purchases, purchases=purchases, summary=summary,)

		if xl == '2':
			return procurement_report_export_excel(request,business=business, local_purchases=local_purchases, purchases=purchases)	

	elif d == 7:	
		local_purchases = LocalPurchaseOrder.objects.filter(business=business, published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
		purchases = PurchaseOrder.objects.filter(business=business, published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')

		p_local_purchases = LocalPurchaseOrder.objects.filter(business=business, published=True, authorized=False).all().count()
		p_purchases = PurchaseOrder.objects.filter(business=business, published=True, authorized=False).all().count()

		summary = LocalPurchaseOrder.objects.filter(business=business, published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)
		purchases_qs = PurchaseOrder.objects.filter(business=business, published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
		summary['total_purchase'] = purchases_qs.filter(business=business, published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']

		if pdf == '1':
			return procurement_report_export_pdf(request,business=business, local_purchases=local_purchases, purchases=purchases, summary=summary,)

		if xl == '2':
			return procurement_report_export_excel(request,business=business, local_purchases=local_purchases, purchases=purchases)	
	
	elif d == 8:
		if request.method == 'GET':	
			local_purchases = LocalPurchaseOrder.objects.filter(business=business, created_at__date__gte=fr, created_at__date__lte=to, published=True,local_purchase_order_authorize__authorized=True).all().order_by('-pk')
			purchases = PurchaseOrder.objects.filter(business=business, created_at__date__gte=fr, created_at__date__lte=to, published=True, purchase_order_authorize__authorized=True).all().order_by('-pk')
			p_local_purchases = LocalPurchaseOrder.objects.filter(business=business, created_at__date__gte=fr, created_at__date__lte=to,  published=True, authorized=False).all().count()
			p_purchases = PurchaseOrder.objects.filter(business=business, created_at__date__gte=fr, created_at__date__lte=to, published=True, authorized=False).all().count()
			
			summary = LocalPurchaseOrder.objects.filter(business=business, created_at__date__gte=fr, created_at__date__lte=to, published=True, local_purchase_order_authorize__authorized=True).all().aggregate(total_local_purchase=Sum('local_purchase_order_list__total'),)

			purchases_qs = PurchaseOrder.objects.filter(business=business, created_at__date__gte=fr, created_at__date__lte=to, published=True, purchase_order_authorize__authorized=True).all().annotate(total_purchase=Sum('purchase_order_list__total'),)
			summary['total_purchase'] = purchases_qs.filter(business=business, created_at__date__gte=fr, created_at__date__lte=to, published=True, purchase_order_authorize__authorized=True).all().aggregate(total_p=Sum(F('total_purchase')+F('shipping')+F('customs')+F('tax')),)['total_p']


			if pdf == '1':
				return procurement_report_export_pdf(request,business=business, local_purchases=local_purchases, purchases=purchases, summary=summary,)

			if xl == '2':
				return procurement_report_export_excel(request,business=business, local_purchases=local_purchases, purchases=purchases)		

	context = {
		'business':business,
		'local_purchases':local_purchases,
		'purchases':purchases,
		'summary':summary,
		'd':d,
		'fr':fr,
		'to':to,
		'p_local_purchases':p_local_purchases,
		'p_purchases':p_purchases,
	}
	return render(request, 'procurement_report.html', context)


# """""""""" SALES REPORT """""""""""
@finance_report_required
@login_required
def sales_time(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first()
	context = {
		'business':business,
	}
	return render(request, 'sale_time.html', context)

@finance_report_required
@login_required
def sales_report(request, *args, **kwargs):
	id = kwargs.get('id')
	day = kwargs.get('d')
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')
	fr = request.GET.get('fr')
	to = request.GET.get('to')
	business = Business.objects.filter(id=id).first() 
	if day == 1:
		sales = Sale.objects.filter(business=business, created_at__date=date.today()).all().order_by('-pk')
		summary = Sale.objects.filter(business=business, created_at__date=date.today()).all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

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

		data = Product.objects.filter(business=business, inventory_product__sale_inventory__created_at__date=date.today()).all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
		products = []
		for d in data:
			dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
			products.append(dic)

		if pdf == '1':
			return sales_report_export_pdf(request,business=business, products=products, summary=summary,sales=sales)

		if xl == '2':
			return sales_report_export_excel(request,business=business,sales=sales)	

	elif day == 2:	
		dt = date.today() - timedelta(days=1)
		sales = Sale.objects.filter(business=business, created_at__date=dt).all().order_by('-pk')	
		summary = Sale.objects.filter(business=business, created_at__date=dt).all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

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

		data = Product.objects.filter(business=business, inventory_product__sale_inventory__created_at__date=dt).all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
		products = []
		for d in data:
			dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
			products.append(dic)

		if pdf == '1':
			return sales_report_export_pdf(request,business=business, products=products, summary=summary,sales=sales)

		if xl == '2':
			return sales_report_export_excel(request,business=business,sales=sales)	

	elif day == 3:	
		dt = date.today() - timedelta(days=7)
		sales = Sale.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today()).all().order_by('-pk')
		summary = Sale.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today()).all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

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

		data = Product.objects.filter(business=business, inventory_product__sale_inventory__created_at__date__gte=dt, inventory_product__sale_inventory__created_at__date__lte=date.today()).all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
		products = []
		for d in data:
			dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
			products.append(dic)

		if pdf == '1':
			return sales_report_export_pdf(request,business=business, products=products, summary=summary,sales=sales)

		if xl == '2':
			return sales_report_export_excel(request,business=business,sales=sales)

	elif day == 4:	
		dt = date.today() - timedelta(days=30)
		sales = Sale.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today()).all().order_by('-pk')	
		summary = Sale.objects.filter(business=business, created_at__date__gte=dt, created_at__date__lte=date.today()).all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

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

		data = Product.objects.filter(business=business, inventory_product__sale_inventory__created_at__date__gte=dt, inventory_product__sale_inventory__created_at__date__lte=date.today()).all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
		products = []
		for d in data:
			dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
			products.append(dic)

		if pdf == '1':
			return sales_report_export_pdf(request,business=business, products=products, summary=summary,sales=sales)	

		if xl == '2':
			return sales_report_export_excel(request,business=business,sales=sales)	

	elif day == 5:	
		dt = date.today()
		sales = Sale.objects.filter(business=business, created_at__month=dt.month, created_at__year=dt.year).all().order_by('-pk')
		summary = Sale.objects.filter(business=business, created_at__month=dt.month, created_at__year=dt.year).all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

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

		data = Product.objects.filter(business=business, inventory_product__sale_inventory__created_at__month=dt.month, inventory_product__sale_inventory__created_at__year=dt.year).all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
		products = []
		for d in data:
			dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
			products.append(dic)

		if pdf == '1':
			return sales_report_export_pdf(request,business=business, products=products, summary=summary,sales=sales)

		if xl == '2':
			return sales_report_export_excel(request,business=business,sales=sales)
				
	elif day == 6:	
		dt = date.today()
		month = dt.month - 1
		sales = Sale.objects.filter(business=business, created_at__month=month, created_at__year=dt.year).all().order_by('-pk')	
		summary = Sale.objects.filter(business=business, created_at__month=month, created_at__year=dt.year).all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

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

		data = Product.objects.filter(business=business, inventory_product__sale_inventory__created_at__month=month, inventory_product__sale_inventory__created_at__year=dt.year).all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
		products = []
		for d in data:
			dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
			products.append(dic)

		if pdf == '1':
			return sales_report_export_pdf(request,business=business, products=products, summary=summary,sales=sales)
		
		if xl == '2':
			return sales_report_export_excel(request,business=business,sales=sales)

	elif day == 7:	
		sales = Sale.objects.filter(business=business).all().order_by('-pk')	
		summary = Sale.objects.filter(business=business).all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

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

		data = Product.objects.filter(business=business).all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
		products = []
		for d in data:
			dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
			products.append(dic)	

		if pdf == '1':
			return sales_report_export_pdf(request,business=business, products=products, summary=summary,sales=sales)

		if xl == '2':
			return sales_report_export_excel(request,business=business,sales=sales)

	elif day == 8:
		if request.method == 'GET':	
			sales = Sale.objects.filter(business=business, created_at__date__gte=fr, created_at__date__lte=to).all().order_by('-pk')	
			summary = Sale.objects.filter(business=business, created_at__date__gte=fr, created_at__date__lte=to).all().aggregate(total_paid=Sum('amount_paid'), total_quantity=Sum('quantity'), total_profit=Sum('profit'))

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
			data = Product.objects.filter(business=business, inventory_product__sale_inventory__created_at__date__gte=fr, inventory_product__sale_inventory__created_at__date__lte=to).all().annotate(quantity_sold=Sum('inventory_product__sale_inventory__quantity'),profit_sold=Sum('inventory_product__sale_inventory__profit'),revenue_sold=Sum('inventory_product__sale_inventory__amount_paid'))
			products = []
			for d in data:
				dic = {'name': d.name, 'quantity_sold': d.quantity_sold, 'profit_sold': d.profit_sold, 'revenue_sold': d.revenue_sold}
				products.append(dic)

			if pdf == '1':
				return sales_report_export_pdf(request,business=business, products=products, summary=summary,sales=sales)

			if xl == '2':
				return sales_report_export_excel(request,business=business,sales=sales)
				
	context = {
		'business':business,
		'sales':sales,
		'summary':summary,
		'products':products,
		'day':day,
		'fr':fr,
		'to':to,
	}
	return render(request, 'sales_report.html', context)


# """""""""" INVENTORY REPORT """""""""""
@store_report_required
@login_required
def inventory_product(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first()
	products = Product.objects.filter(business=business)
	context = {
		'business':business,
		'products':products,
	}
	return render(request, 'inventory_product.html', context)

@store_report_required
@login_required
def inventory_report(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first() 
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')

	if request.method == 'GET':
		p = request.GET['p']

		if p == '0':
			inventory_qs = Inventory.objects.filter(business=business, exist=True).annotate(available=F('remain')-F('damage'))	
			if inventory_qs:
				inventory_qs.filter(available=0).update(exist=False)		
			inventories = Inventory.objects.filter(business=business).order_by('-pk')
			summary = inventory_qs.aggregate(total_cost=Sum(F('available')*F('product_cost'),output_field=FloatField()),total_worth=Sum(F('available')*F('product__sell_price'),output_field=FloatField()))

			data = Product.objects.filter(business=business).all()
			products = []
			for d in data:
				dic = {'name': d.name, 'quantity': d.quantity, 'worth':d.worth}
				products.append(dic)

			if pdf == '1':				
				return inventory_report_export_pdf(request, business=business, inventories=inventories, summary=summary, products=products,)

			if xl == '2':				
				return inventory_report_export_excel(request, business=business, inventories=inventories)

		else:
			inventory_qs = Inventory.objects.filter(business=business, product__id=p, exist=True).annotate(available=F('remain')-F('damage'))	
			if inventory_qs:
				inventory_qs.filter(available=0).update(exist=False)			
			inventories = Inventory.objects.filter(business=business, product__id=p).order_by('-pk')
			summary = inventory_qs.aggregate(total_cost=Sum(F('available')*F('product_cost'),output_field=FloatField()),total_worth=Sum(F('available')*F('product__sell_price'),output_field=FloatField()))

			data = Product.objects.filter(id=p,business=business).all()
			products = []
			for d in data:
				dic = {'name': d.name, 'quantity': d.quantity, 'worth':d.worth}
				products.append(dic)

			if pdf == '1':				
				return inventory_report_export_pdf(request, business=business, inventories=inventories, summary=summary, products=products,)

			if xl == '2':				
				return inventory_report_export_excel(request, business=business, inventories=inventories)	
			
	context = {
		'business':business,
		'inventories':inventories,
		'summary':summary,
		'products':products,
		'p':p,
	}
	return render(request, 'inventory_report.html', context)


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
		takehome = Takehome.objects.filter(created_at__date=date.today(), business=business)
		employees = Payroll.objects.filter(created_at__date=date.today(), business=business).count()           
		deduction = Payroll.objects.filter(created_at__date=date.today(), business=business).aggregate(Sum('deduction'))['deduction__sum']   		
		bonuses = Payroll.objects.filter(created_at__date=date.today(), business=business).aggregate(Sum('bonus'))['bonus__sum']   		
		overtime = Payroll.objects.filter(created_at__date=date.today(), business=business).aggregate(Sum('overtime'))['overtime__sum']    		
		nssf_funds = Payroll.objects.filter(nssf=True, created_at__date=date.today(), business=business).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		# wcf = Payroll.objects.filter(tax_rate__icontains='wcf', created_at__date=date.today(), business=business)
		loan_board_funds = Payroll.objects.filter(heslb=True, created_at__date=date.today(), business=business).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		salaries = Payroll.objects.filter(created_at__date=date.today(), business=business).aggregate(Sum('employee__salary'))['employee__salary__sum']
		paye_total = Payroll.objects.filter(paye=True, created_at__date=date.today(), business=business).aggregate(Sum('paye_amount'))['paye_amount__sum']
		takehome_total = Takehome.objects.filter(created_at__date=date.today(), business=business).aggregate(Sum('salary'))['salary__sum']
		sdl = Payroll.objects.filter(created_at__date=date.today(), business=business).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		

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
			return payroll_report_export_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries, deduction=deduction, sdl=sdl, business=business)
		if xl == '1':
			return payroll_report_export_excel(request, takehome=takehome, business=business, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

	elif day == 2:	
		dt = date.today() - timedelta(days=1)
		takehome = Takehome.objects.filter(created_at__date=dt, business=business)
		employees = Payroll.objects.filter(created_at__date=dt, business=business).count()           
		sdl = Payroll.objects.filter(created_at__date=dt, business=business).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		deduction = Payroll.objects.filter(created_at__date=dt, business=business).aggregate(Sum('deduction'))['deduction__sum']   		
		bonuses = Payroll.objects.filter(created_at__date=dt, business=business).aggregate(Sum('bonus'))['bonus__sum']   		
		overtime = Payroll.objects.filter(created_at__date=dt, business=business).aggregate(Sum('overtime'))['overtime__sum']    		
		nssf_funds = Payroll.objects.filter(nssf=True, created_at__date=dt, business=business).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True, created_at__date=dt, business=business).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		salaries = Payroll.objects.filter(created_at__date=dt, business=business).aggregate(Sum('employee__salary'))['employee__salary__sum']
		paye_total = Payroll.objects.filter(paye=True, created_at__date=dt, business=business).aggregate(Sum('paye_amount'))['paye_amount__sum']
		takehome_total = Takehome.objects.filter(created_at__date=dt, business=business).aggregate(Sum('salary'))['salary__sum']


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
			return payroll_report_export_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries,deduction=deduction, sdl=sdl, business=business)
		if xl == '1':
			return payroll_report_export_excel(request, takehome=takehome, business=business, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

	elif day == 3:	
		dt = date.today() - timedelta(days=7)
		takehome = Takehome.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business)
		employees = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).count()           
		sdl = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		deduction = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('deduction'))['deduction__sum']   		
		bonuses = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('bonus'))['bonus__sum']   		
		overtime = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('overtime'))['overtime__sum']    		
		nssf_funds = Payroll.objects.filter(nssf=True, created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True, created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		salaries = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('employee__salary'))['employee__salary__sum']
		paye_total = Payroll.objects.filter(paye=True, created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('paye_amount'))['paye_amount__sum']
		takehome_total = Takehome.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('salary'))['salary__sum']


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
			return payroll_report_export_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries, deduction=deduction, sdl=sdl, business=business)
		if xl == '1':
			return payroll_report_export_excel(request, takehome=takehome, business=business, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

	elif day == 4:	
		dt = date.today() - timedelta(days=30)
		takehome = Takehome.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business)
		employees = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).count()           
		sdl = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		deduction = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('deduction'))['deduction__sum']   		
		bonuses = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('bonus'))['bonus__sum']   		
		overtime = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('overtime'))['overtime__sum']    		
		nssf_funds = Payroll.objects.filter(nssf=True, created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True, created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		salaries = Payroll.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('employee__salary'))['employee__salary__sum']
		paye_total = Payroll.objects.all().filter(paye=True, created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('paye_amount'))['paye_amount__sum']
		takehome_total = Takehome.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('salary'))['salary__sum']


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
			return payroll_report_export_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries, deduction=deduction, sdl=sdl, business=business)
		if xl == '1':
			return payroll_report_export_excel(request, takehome=takehome, business=business, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

	elif day == 5:	
		dt = date.today()
		takehome = Takehome.objects.filter(created_at__month=dt.month, created_at__year=dt.year, business=business)
		employees = Payroll.objects.filter(created_at__month=dt.month, created_at__year=dt.year, business=business).count()           
		sdl = Payroll.objects.filter(created_at__month=dt.month, created_at__year=dt.year, business=business).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		deduction = Payroll.objects.filter(created_at__month=dt.month, created_at__year=dt.year, business=business).aggregate(Sum('deduction'))['deduction__sum']   		
		bonuses = Payroll.objects.filter(created_at__month=dt.month, created_at__year=dt.year, business=business).aggregate(Sum('bonus'))['bonus__sum']   		
		overtime = Payroll.objects.filter(created_at__month=dt.month, created_at__year=dt.year, business=business).aggregate(Sum('overtime'))['overtime__sum']    		
		nssf_funds = Payroll.objects.filter(nssf=True, created_at__month=dt.month, created_at__year=dt.year, business=business).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True, created_at__month=dt.month, created_at__year=dt.year, business=business).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		salaries = Payroll.objects.filter(created_at__month=dt.month, created_at__year=dt.year, business=business).aggregate(Sum('employee__salary'))['employee__salary__sum']
		paye_total = Payroll.objects.filter(paye=True, created_at__month=dt.month, created_at__year=dt.year, business=business).aggregate(Sum('paye_amount'))['paye_amount__sum']
		takehome_total = Takehome.objects.filter(created_at__month=dt.month, created_at__year=dt.year, business=business).aggregate(Sum('salary'))['salary__sum']


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
			return payroll_report_export_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries, deduction=deduction, sdl=sdl, business=business)
		if xl == '1':
			return payroll_report_export_excel(request, takehome=takehome, business=business, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

	elif day == 6:	
		dt = date.today()
		month = dt.month - 1
		takehome = Takehome.objects.filter(created_at__month=month, created_at__year=dt.year, business=business)
		employees = Payroll.objects.filter(created_at__month=month, created_at__year=dt.year, business=business).count()           
		sdl = Payroll.objects.filter(created_at__month=month, created_at__year=dt.year, business=business).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		deduction = Payroll.objects.filter(created_at__month=month, created_at__year=dt.year, business=business).aggregate(Sum('deduction'))['deduction__sum']   		
		bonuses = Payroll.objects.filter(created_at__month=month, created_at__year=dt.year, business=business).aggregate(Sum('bonus'))['bonus__sum']   		
		overtime = Payroll.objects.filter(created_at__month=month, created_at__year=dt.year, business=business).aggregate(Sum('overtime'))['overtime__sum']    		
		nssf_funds = Payroll.objects.filter(nssf=True, created_at__month=month, created_at__year=dt.year, business=business).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True, created_at__month=month, created_at__year=dt.year, business=business).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		salaries = Payroll.objects.filter(created_at__month=month, created_at__year=dt.year, business=business).aggregate(Sum('employee__salary'))['employee__salary__sum']
		paye_total = Payroll.objects.filter(paye=True, created_at__month=month, created_at__year=dt.year, business=business).aggregate(Sum('paye_amount'))['paye_amount__sum']
		takehome_total = Takehome.objects.filter(created_at__month=month, created_at__year=dt.year, business=business).aggregate(Sum('salary'))['salary__sum']


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
			return payroll_report_export_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries, deduction=deduction, sdl=sdl, business=business)
		if xl == '1':
			return payroll_report_export_excel(request, takehome=takehome, business=business, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

	elif day == 7:	
		takehome = Takehome.objects.filter(business=business)
		employees = Payroll.objects.filter(business=business).count()           
		deduction = Payroll.objects.filter(business=business).aggregate(Sum('deduction'))['deduction__sum']   		
		bonuses = Payroll.objects.filter(business=business).aggregate(Sum('bonus'))['bonus__sum']   		
		overtime = Payroll.objects.filter(business=business).aggregate(Sum('overtime'))['overtime__sum']    		
		nssf_funds = Payroll.objects.filter(nssf=True, business=business).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True, business=business).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		sdl = Payroll.objects.filter(business=business).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		paye_total = Payroll.objects.filter(paye=True, business=business).aggregate(Sum('paye_amount'))['paye_amount__sum']
		salaries = Payroll.objects.filter(business=business).aggregate(Sum('employee__salary'))['employee__salary__sum']
		takehome_total = Takehome.objects.filter(business=business).aggregate(Sum('salary'))['salary__sum']

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
			return payroll_report_export_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries, deduction=deduction, sdl=sdl, business=business)
		if xl == '1':
			return payroll_report_export_excel(request, takehome=takehome, business=business, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

	elif day == 8:
		if request.method == 'GET':	
			takehome = Takehome.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, business=business)
			employees = Payroll.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, business=business).count()           
			sdl = Payroll.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, business=business).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
			deduction = Payroll.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, business=business).aggregate(Sum('deduction'))['deduction__sum']   		
			bonuses = Payroll.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, business=business).aggregate(Sum('bonus'))['bonus__sum']   		
			overtime = Payroll.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, business=business).aggregate(Sum('overtime'))['overtime__sum']    		
			nssf_funds = Payroll.objects.filter(nssf=True, created_at__date__gte=fr, created_at__date__lte=to, business=business).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
			loan_board_funds = Payroll.objects.filter(heslb=True, created_at__date__gte=fr, created_at__date__lte=to, business=business).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
			salaries = Payroll.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, business=business).all().aggregate(Sum('employee__salary'))['employee__salary__sum']
			paye_total = Payroll.objects.filter(paye=True, created_at__date__gte=fr, created_at__date__lte=to, business=business).aggregate(Sum('paye_amount'))['paye_amount__sum']
			takehome_total = Takehome.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, business=business).aggregate(Sum('salary'))['salary__sum']

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
				return payroll_report_export_pdf(request, takehome=takehome, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), employees=employees, bonus=bonuses, overtime=overtime, total_expenses=total, salaries_total=salaries, deduction=deduction, sdl=sdl, business=business)
			if xl == '1':
				return payroll_report_export_excel(request, takehome=takehome, business=business, takehome_total=takehome_total, nssf=int(nssf_funds), loan_board=int(loan_board_funds), paye=int(paye_total), bonus=bonuses, overtime=overtime, salaries_total=salaries, deduction=deduction, sdl=sdl)

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
	template_name = 'payroll-report.html'

	return render(request, template_name, context)


########## Payroll Report - time ##############
@finance_report_required
@login_required
def payroll_time(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first()
	context = {
		'business':business,
	}
	return render(request, 'payroll-time.html', context)


############ OPEX Report ###########  
@finance_report_required  
@login_required
def opex_report(request, *args, **kwargs):

	id = kwargs.get('id')
	day = kwargs.get('d')
	fr = request.GET.get('fr')
	to = request.GET.get('to')	
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')
	business = Business.objects.filter(id=id).first()

	exps_objects = []

	if day == 1:	
		expense_objects = Expense.objects.filter(created_at__date=date.today(), business=business)
		total_cost = Expense.objects.filter(created_at__date=date.today(), business=business).aggregate(Sum('cost'))['cost__sum'] 
		expenses = Expense.objects.filter(created_at__date=date.today(), business=business).count()          
		exps = Expense.objects.filter(created_at__date=date.today(), business=business)

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps, business=business)

		if xl == '2':
			return opex_report_export_excel(request, expense_objects=expense_objects, business=business)	

	elif day == 2:	
		dt = date.today() - timedelta(days=1)
		expense_objects = Expense.objects.filter(created_at__date=dt, business=business)
		total_cost = Expense.objects.filter(created_at__date=dt, business=business).aggregate(Sum('cost'))['cost__sum'] 
		expenses = Expense.objects.filter(created_at__date=dt, business=business).count()          
		exps = Expense.objects.filter(created_at__date=dt, business=business)

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps, business=business)

		if xl == '2':
   			return opex_report_export_excel(request, expense_objects=expense_objects, business=business)	
	

	elif day == 3:	
		dt = date.today() - timedelta(days=7)
		expense_objects = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business)
		total_cost = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('cost'))['cost__sum'] 
		expenses = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).count()          
		exps = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business)

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps, business=business)

		if xl == '2':
   			return opex_report_export_excel(request, expense_objects=expense_objects, business=business)	

	elif day == 4:	
		dt = date.today() - timedelta(days=30)
		expense_objects = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business)
		total_cost = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).aggregate(Sum('cost'))['cost__sum'] 
		expenses = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business).count()          
		exps = Expense.objects.filter(created_at__date__gte=dt, created_at__date__lte=date.today(), business=business)

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps, business=business)

		if xl == '2':
   			return opex_report_export_excel(request, expense_objects=expense_objects, business=business)	

	elif day == 5:	
		dt = date.today()
		expense_objects = Expense.objects.filter(created_at__month=dt.month, created_at__year=dt.year, business=business)
		total_cost = Expense.objects.filter(created_at__month=dt.month, created_at__year=dt.year, business=business).aggregate(Sum('cost'))['cost__sum'] 
		expenses = Expense.objects.filter(created_at__month=dt.month, created_at__year=dt.year, business=business).count()          
		exps = Expense.objects.filter(created_at__month=dt.month, created_at__year=dt.year, business=business)

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps, business=business)

		if xl == '2':
   			return opex_report_export_excel(request, expense_objects=expense_objects, business=business)	

	elif day == 6:	
		dt = date.today()
		month = dt.month - 1
		expense_objects = Expense.objects.filter(created_at__month=month, created_at__year=dt.year, business=business)
		total_cost = Expense.objects.filter(created_at__month=month, created_at__year=dt.year, business=business).aggregate(Sum('cost'))['cost__sum'] 
		expenses = Expense.objects.filter(created_at__month=month, created_at__year=dt.year, business=business).count()          
		exps = Expense.objects.filter(created_at__month=month, created_at__year=dt.year, business=business)

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps, business=business)

		if xl == '2':
			return opex_report_export_excel(request, expense_objects=expense_objects, business=business)	

	elif day == 7:	
		expense_objects = Expense.objects.filter(business=business)
		total_cost = Expense.objects.filter(business=business).aggregate(Sum('cost'))['cost__sum'] 
		expenses = Expense.objects.filter(business=business).count()          
		exps = Expense.objects.filter(business=business)

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps, business=business)

		if xl == '2':
   			return opex_report_export_excel(request, expense_objects=expense_objects, business=business)	

	elif day == 8:
		if request.method == 'GET':	
			expense_objects = Expense.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, business=business)
			total_cost = Expense.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, business=business).aggregate(Sum('cost'))['cost__sum'] 
			expenses = Expense.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, business=business).count()          
			exps = Expense.objects.filter(created_at__date__gte=fr, created_at__date__lte=to, business=business)

		if pdf == '1':
			return opex_report_export_pdf(request, expense_objects=expense_objects, total_cost=total_cost, expenses_total=expenses, exps=exps, business=business)
			
		if xl == '2':
   			return opex_report_export_excel(request, expense_objects=expense_objects, business=business)	

	if total_cost is None:
		total_cost = 0


	for exp in exps:
		exps_objects.append({'name': exp.category, 'cost':exp.cost})

	context = {
		'business' : business,
		'expenses': expense_objects,
		'cost': total_cost,
		'expenses_total': str(expenses),
		'exps' : exps_objects,
		'day': day,
		'fr' : fr,
		'to' : to,
	}
	template_name = 'opex-report.html'

	return render(request, template_name, context)


########## Opex Report - time ##############
@finance_report_required
@login_required
def opex_time(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first()
	context = {
		'business':business,
	}
	return render(request, 'opex-time.html', context)	


@finance_report_required
@login_required
def customer_report(request, *args, **kwargs):

	id = kwargs.get('id')
	pdf = request.GET.get('pdf')
	business = Business.objects.filter(id=id).first()
	customers = Customer.objects.filter(business=business)
	url_parameter = request.GET.get("q")

	for customer in customers:
		customer_sales = Sale.objects.filter(customer=customer, business=business)
		dates = []

		for sale in customer_sales:

			customer_point = {f'{customer.full_name} : {sale.created_at.date()}'}

			if customer_point in dates:
				pass
			else:
				dates.append({f'{customer.full_name} : {sale.created_at.date()}'})

		points = len(dates)

		Customer.objects.filter(id=customer.id, business=business).update(points=points)

		if customer.points == 30:
			Customer.objects.filter(id=customer.id, business=business).update(category='Loyal')



	if url_parameter:
		customers = Customer.objects.filter(business=business).filter(Q(full_name__icontains=url_parameter) | Q(contact__icontains=url_parameter))

	else:
		customers = Customer.objects.filter(business=business)
			

	if request.is_ajax():
		html = render_to_string(
			template_name='customer-results.html',
			context={'customers':customers}
		)

		data_dict = {"html_from_view": html}

		return JsonResponse(data=data_dict, safe=False)

	normal_customers = Customer.objects.filter(category="Normal", business=business).count()	
	loyal_customers = Customer.objects.filter(category="Loyal", business=business).count()	
	other_customers = Sale.objects.filter(customer=None, business=business).count()

	if pdf == '1':
		return customer_report_export_pdf(request, customers=customers, normal=normal_customers, loyal=loyal_customers, other=other_customers,business=business)

	customer_category = [
		{"name": "Loyal customers", "value": loyal_customers},
		{"name": "Normal customers", "value": normal_customers},
		{"name": "Other customers", "value": other_customers},
		]

	context = {
		'business': business,
		'customers': customers,
		'categories': customer_category,
		'normal': normal_customers,
		'loyal': loyal_customers,
		'other': other_customers,
	}
	template_name = 'customer-report.html'
	return render(request, template_name, context)


@finance_report_required
@login_required
def financial_statements(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first()

	context = {
		'business':business,
	}
	return render(request, 'financial_statements.html', context)

@finance_report_required
@login_required
def income_statement_time(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first()

	context = {
		'business':business,
	}
	return render(request, 'income_statement_time.html', context)


@finance_report_required
@login_required
def income_statement(request, *args, **kwargs):
	id = kwargs.get('id')
	d = kwargs.get('d')
	fr = request.GET.get('fr')
	to = request.GET.get('to')
	pdf = request.GET.get('pdf')
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')
	business = Business.objects.filter(id=id).first() 
	if d == 1:
		dt = date.today()
		summary = {}

		# Start COGS
		purchases = Inventory.objects.filter(created_at__month=dt.month).aggregate(total_cost=Sum(F('quantity')*F('product_cost'),output_field=FloatField()))['total_cost']		
		opening = Stock.objects.filter(stock_date__month=dt.month, stock_type='Opening Stock').aggregate(Sum('cost'))['cost__sum']
		closing = Stock.objects.filter(stock_date__month=dt.month, stock_type='Closing Stock').aggregate(Sum('cost'))['cost__sum']
		if purchases is None:
			purchases = 0
		if opening is None:
			opening = 0
		if closing is None:
			closing = 0		
		cogs = opening + Decimal(purchases) - closing
		# End COGS		


		advertising = Expense.objects.filter(category='Advertising', created_at__month=dt.month).aggregate(Sum('cost'))['cost__sum']
		contractors = Expense.objects.filter(category='Contractors', created_at__month=dt.month).aggregate(Sum('cost'))['cost__sum']
		rent = Expense.objects.filter(category='Rent or Lease', created_at__month=dt.month).aggregate(Sum('cost'))['cost__sum']
		travel = Expense.objects.filter(category='Travel', created_at__month=dt.month).aggregate(Sum('cost'))['cost__sum']
		financial_charge = Expense.objects.filter(category='Financial Charge', created_at__month=dt.month).aggregate(Sum('cost'))['cost__sum']
		education = Expense.objects.filter(category='Education and Training', created_at__month=dt.month).aggregate(Sum('cost'))['cost__sum']
		services = Expense.objects.filter(category='Professional Services', created_at__month=dt.month).aggregate(Sum('cost'))['cost__sum']
		utilities = Expense.objects.filter(category='Utilities', created_at__month=dt.month).aggregate(Sum('cost'))['cost__sum']
		other_expenses = Expense.objects.filter(category='Other Expenses', created_at__month=dt.month).aggregate(Sum('cost'))['cost__sum']


		if advertising is None:
			advertising = 0
		if contractors is None:
			contractors = 0
		if rent is None:
			rent = 0
		if travel is None:
			travel = 0
		if financial_charge is None:
			financial_charge = 0
		if education is None:
			education = 0
		if services is None:
			services = 0
		if utilities is None:
			utilities = 0
		if other_expenses is None:
			other_expenses = 0								



		summary['advertising'] = advertising
		summary['contractors'] = contractors
		summary['rent'] = rent
		summary['travel'] = travel
		summary['financial_charge'] = financial_charge
		summary['services'] = services
		summary['utilities'] = utilities
		summary['other_expenses'] = other_expenses
		summary['education'] = education



		sales = Sale.objects.filter(created_at__month=dt.month).all().aggregate(total_paid=Sum('amount_paid'))['total_paid']
		total_expense = Expense.objects.filter(created_at__month=dt.month).aggregate(Sum('cost'))['cost__sum']
		depreciation = AccountsFixedAsset.objects.filter(depreciation_value__gt=0, created_at__month=dt.month).aggregate(Sum('depreciation_value'))['depreciation_value__sum']
		amortization = AccountsFixedAsset.objects.filter(amortization_value__gt=0, created_at__month=dt.month).aggregate(Sum('amortization_value'))['amortization_value__sum'] 
		takehome = Takehome.objects.filter(created_at__month=dt.month, ).aggregate(Sum('salary'))['salary__sum']
		interest_total = Interest.objects.filter(created_at__month=dt.month).aggregate(Sum('remaining'))['remaining__sum']
		tax_total = Tax.objects.filter(created_at__month=dt.month).aggregate(total=Sum('remain'))['total']
		
		if sales is None:
			sales = 0

		summary['total_paid'] = sales
		total_revenue = summary['total_paid']

		if tax_total is None:
			tax_total = 0

		if interest_total is None:
			interest_total = 0		

		if total_revenue is None:
			total_revenue = 0

		if takehome is None:
				takehome = 0
		
		if total_expense is None:
			total_expense = 0

		if depreciation is None:
			depreciation = 0

		if amortization is None:
			amortization = 0	

		nssf_funds = Payroll.objects.filter(nssf=True, created_at__month=dt.month).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True, created_at__month=dt.month).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		sdl = Payroll.objects.filter(created_at__month=dt.month).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		paye_total = Payroll.objects.filter(paye=True, created_at__month=dt.month).aggregate(Sum('paye_amount'))['paye_amount__sum']


		if sdl is None:
			sdl =0 

		if nssf_funds is None:
			nssf_funds = 0

		if loan_board_funds is None:
			loan_board_funds = 0

		if paye_total is None:
			paye_total = 0	

	
		total_social_funds = int(nssf_funds) + int(paye_total) + int(loan_board_funds) + int(sdl)

		tax = tax_total 	
		tax_interest = tax + interest_total

		takehome = takehome - total_social_funds


		##### Calculating OPEX #####
		opex = total_expense + takehome + depreciation + amortization
		opex_da = total_expense + takehome 

		##### Calculating EBITDA #####
		ebitda = total_revenue - (cogs + opex_da)				

		taxes = int(paye_total) + int(sdl)

		gross_profit = total_revenue - cogs
		summary['gross_profit'] = gross_profit


		##### Calculating EBIT #####
		ebit = gross_profit - opex


		####### Net Income ########
		net_income = ebit - tax_interest


		expenses = Expense.objects.filter(created_at__month=dt.month)
		summary['expenses'] = expenses

		summary['net_income'] = round(net_income,2)
		summary['social_funds'] = round(total_social_funds,2)
		summary['opex'] = round(opex,2)
		summary['ebit'] = round(ebit,2)
		summary['ebitda'] = round(ebitda,2)
		summary['tax_interest'] = round(tax_interest,2)
		summary['cogs'] = cogs
		summary['salaries'] = takehome
		summary['da'] = depreciation + amortization


		if pdf == '1':
			return income_statement_export_pdf(request, summary=summary)
		if xl == '1':
			return income_statement_export_excel(request, summary=summary)

	elif d == 2:	
		dt = date.today() 
		month = dt.month - 1
		summary = {}

		# Start COGS
		purchases = Inventory.objects.filter( created_at__month=month).aggregate(total_cost=Sum(F('quantity')*F('product_cost'),output_field=FloatField()))['total_cost']		
		opening = Stock.objects.filter( stock_date__month=month, stock_type='Opening Stock').aggregate(Sum('cost'))['cost__sum']
		closing = Stock.objects.filter( stock_date__month=month, stock_type='Closing Stock').aggregate(Sum('cost'))['cost__sum']
		if purchases is None:
			purchases = 0
		if opening is None:
			opening = 0
		if closing is None:
			closing = 0		
		cogs = opening + Decimal(purchases) - closing
		# End COGS		



		advertising = Expense.objects.filter(category='Advertising', created_at__month=month).aggregate(Sum('cost'))['cost__sum']
		contractors = Expense.objects.filter(category='Contractors', created_at__month=month).aggregate(Sum('cost'))['cost__sum']
		rent = Expense.objects.filter(category='Rent or Lease', created_at__month=month).aggregate(Sum('cost'))['cost__sum']
		travel = Expense.objects.filter(category='Travel', created_at__month=month).aggregate(Sum('cost'))['cost__sum']
		financial_charge = Expense.objects.filter(category='Financial Charge', created_at__month=month).aggregate(Sum('cost'))['cost__sum']
		education = Expense.objects.filter(category='Education and Training', created_at__month=month).aggregate(Sum('cost'))['cost__sum']
		services = Expense.objects.filter(category='Professional Services', created_at__month=month).aggregate(Sum('cost'))['cost__sum']
		utilities = Expense.objects.filter(category='Utilities', created_at__month=month).aggregate(Sum('cost'))['cost__sum']
		other_expenses = Expense.objects.filter(category='Other Expenses', created_at__month=month).aggregate(Sum('cost'))['cost__sum']


		if advertising is None:
			advertising = 0
		if contractors is None:
			contractors = 0
		if rent is None:
			rent = 0
		if travel is None:
			travel = 0
		if financial_charge is None:
			financial_charge = 0
		if education is None:
			education = 0
		if services is None:
			services = 0
		if utilities is None:
			utilities = 0
		if other_expenses is None:
			other_expenses = 0								



		summary['advertising'] = advertising
		summary['contractors'] = contractors
		summary['rent'] = rent
		summary['travel'] = travel
		summary['financial_charge'] = financial_charge
		summary['services'] = services
		summary['utilities'] = utilities
		summary['other_expenses'] = other_expenses
		summary['education'] = education



		sales = Sale.objects.filter( created_at__month=month).all().aggregate(total_paid=Sum('amount_paid'))['total_paid']
		total_expense = Expense.objects.filter(created_at__month=month, ).aggregate(Sum('cost'))['cost__sum']
		depreciation = AccountsFixedAsset.objects.filter(depreciation_value__gt=0, created_at__month=month ).aggregate(Sum('depreciation_value'))['depreciation_value__sum']
		amortization = AccountsFixedAsset.objects.filter(amortization_value__gt=0, created_at__month=month ).aggregate(Sum('amortization_value'))['amortization_value__sum'] 
		takehome = Takehome.objects.filter(created_at__month=month ).aggregate(Sum('salary'))['salary__sum']
		interest_total = Interest.objects.filter( created_at__month=month).aggregate(Sum('remaining'))['remaining__sum']
		tax_total = Tax.objects.filter( created_at__month=month).aggregate(total=Sum('remain'))['total']

		if sales is None:
			sales = 0

		summary['total_paid'] = sales
		total_revenue = summary['total_paid']

		if tax_total is None:
			tax_total = 0

		if interest_total is None:
			interest_total = 0

		if total_revenue is None:
			total_revenue = 0

		if takehome is None:
			takehome = 0
		
		if total_expense is None:
			total_expense = 0

		if depreciation is None:
			depreciation = 0

		if amortization is None:
			amortization = 0		

		nssf_funds = Payroll.objects.filter(nssf=True, created_at__month=month).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True, created_at__month=month).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		sdl = Payroll.objects.filter(created_at__month=month).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		paye_total = Payroll.objects.filter(paye=True, created_at__month=month).aggregate(Sum('paye_amount'))['paye_amount__sum']


		if sdl is None:
			sdl =0 

		if nssf_funds is None:
			nssf_funds = 0

		if loan_board_funds is None:
			loan_board_funds = 0

		if paye_total is None:
			paye_total = 0	

		total_social_funds = int(nssf_funds) + int(paye_total) + int(loan_board_funds) + int(sdl)

		tax = tax_total 	
		tax_interest = tax + interest_total

		takehome = takehome - total_social_funds


		##### Calculating OPEX #####
		opex = total_expense + takehome + depreciation + amortization
		opex_da = total_expense + takehome 

		##### Calculating EBITDA #####
		ebitda = total_revenue - (cogs + opex_da)				

		taxes = int(paye_total) + int(sdl)

		gross_profit = total_revenue - cogs
		summary['gross_profit'] = gross_profit


		##### Calculating EBIT #####
		ebit = gross_profit - opex


		####### Net Income ########
		net_income = ebit - tax_interest

		expenses = Expense.objects.filter(created_at__month=month)
		summary['expenses'] = expenses

		summary['net_income'] = round(net_income,2)
		summary['social_funds'] = round(total_social_funds,2)
		summary['opex'] = round(opex,2)
		summary['ebit'] = round(ebit,2)
		summary['ebitda'] = round(ebitda,2)
		summary['tax_interest'] = round(tax_interest,2)
		summary['cogs'] = cogs
		summary['salaries'] = takehome
		summary['da'] = depreciation + amortization


		if pdf == '1':
			return income_statement_export_pdf(request, summary=summary)
		if xl == '1':
			return income_statement_export_excel(request, summary=summary)			

	elif d == 3:	
		summary = {}

		# Start COGS
		purchases = Inventory.objects.filter().aggregate(total_cost=Sum(F('quantity')*F('product_cost'),output_field=FloatField()))['total_cost']		
		opening = Stock.objects.filter( stock_type='Opening Stock').aggregate(Sum('cost'))['cost__sum']
		closing = Stock.objects.filter( stock_type='Closing Stock').aggregate(Sum('cost'))['cost__sum']
		if purchases is None:
			purchases = 0
		if opening is None:
			opening = 0
		if closing is None:
			closing = 0		
		cogs = opening + Decimal(purchases) - closing
		# End COGS		


		advertising = Expense.objects.filter(category='Advertising').aggregate(Sum('cost'))['cost__sum']
		contractors = Expense.objects.filter(category='Contractors').aggregate(Sum('cost'))['cost__sum']
		rent = Expense.objects.filter(category='Rent or Lease').aggregate(Sum('cost'))['cost__sum']
		travel = Expense.objects.filter(category='Travel').aggregate(Sum('cost'))['cost__sum']
		financial_charge = Expense.objects.filter(category='Financial Charge').aggregate(Sum('cost'))['cost__sum']
		education = Expense.objects.filter(category='Education and Training').aggregate(Sum('cost'))['cost__sum']
		services = Expense.objects.filter(category='Professional Services').aggregate(Sum('cost'))['cost__sum']
		utilities = Expense.objects.filter(category='Utilities').aggregate(Sum('cost'))['cost__sum']
		other_expenses = Expense.objects.filter(category='Other Expenses').aggregate(Sum('cost'))['cost__sum']


		if advertising is None:
			advertising = 0
		if contractors is None:
			contractors = 0
		if rent is None:
			rent = 0
		if travel is None:
			travel = 0
		if financial_charge is None:
			financial_charge = 0
		if education is None:
			education = 0
		if services is None:
			services = 0
		if utilities is None:
			utilities = 0
		if other_expenses is None:
			other_expenses = 0								



		summary['advertising'] = advertising
		summary['contractors'] = contractors
		summary['rent'] = rent
		summary['travel'] = travel
		summary['financial_charge'] = financial_charge
		summary['services'] = services
		summary['utilities'] = utilities
		summary['other_expenses'] = other_expenses
		summary['education'] = education




		sales = Sale.objects.all().aggregate(total_paid=Sum('amount_paid'))['total_paid']
		inventory_qs = Inventory.objects.all().annotate(available=F('remain')-F('damage'))			
		inventories = inventory_qs.filter(available__gt=0).order_by('-pk')
		total_expense = Expense.objects.all().aggregate(Sum('cost'))['cost__sum'] 
		depreciation = AccountsFixedAsset.objects.filter(depreciation_value__gt=0).aggregate(Sum('depreciation_value'))['depreciation_value__sum']
		amortization = AccountsFixedAsset.objects.filter(amortization_value__gt=0).aggregate(Sum('amortization_value'))['amortization_value__sum'] 
		takehome = Takehome.objects.all().aggregate(Sum('salary'))['salary__sum']
		interest_total = Interest.objects.all().aggregate(Sum('remaining'))['remaining__sum']
		tax_total = Tax.objects.all().aggregate(total=Sum('remain'))['total']

		if sales is None:
			sales = 0

		summary['total_paid'] = sales
		total_revenue = summary['total_paid']

		if tax_total is None:
			tax_total = 0

		if interest_total is None:
			interest_total = 0

		if total_revenue is None:
			total_revenue = 0

		if takehome is None:
			takehome = 0
		
		if total_expense is None:
			total_expense = 0

		if depreciation is None:
			depreciation = 0

		if amortization is None:
			amortization = 0

		nssf_funds = Payroll.objects.filter(nssf=True,).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True,).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		sdl = Payroll.objects.all().aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		paye_total = Payroll.objects.filter(paye=True,).aggregate(Sum('paye_amount'))['paye_amount__sum']


		if sdl is None:
			sdl =0 

		if nssf_funds is None:
			nssf_funds = 0

		if loan_board_funds is None:
			loan_board_funds = 0

		if paye_total is None:
			paye_total = 0	



		total_social_funds = int(nssf_funds) + int(paye_total) + int(loan_board_funds) + int(sdl)

		tax = tax_total 	
		tax_interest = tax + interest_total

		takehome = takehome - total_social_funds


		##### Calculating OPEX #####
		opex = total_expense + takehome + depreciation + amortization
		opex_da = total_expense + takehome 

		##### Calculating EBITDA #####
		ebitda = total_revenue - (cogs + opex_da)				

		taxes = int(paye_total) + int(sdl)

		gross_profit = total_revenue - cogs
		summary['gross_profit'] = gross_profit


		##### Calculating EBIT #####
		ebit = gross_profit - opex


		####### Net Income ########
		net_income = ebit - tax_interest

		expenses = Expense.objects.all()
		summary['expenses'] = expenses

		summary['net_income'] = round(net_income,2)
		summary['social_funds'] = round(total_social_funds,2)
		summary['opex'] = round(opex,2)
		summary['ebit'] = round(ebit,2)
		summary['ebitda'] = round(ebitda,2)
		summary['tax_interest'] = round(tax_interest,2)
		summary['cogs'] = cogs
		summary['salaries'] = takehome
		summary['da'] = depreciation + amortization


		if pdf == '1':
			return income_statement_export_pdf(request, summary=summary)
		if xl == '1':
			return income_statement_export_excel(request, summary=summary)			
		
	elif d == 4:	
		summary = {}

		# Start COGS
		purchases = Inventory.objects.filter( created_at__date__gte=fr, created_at__date__lte=to,).aggregate(total_cost=Sum(F('quantity')*F('product_cost'),output_field=FloatField()))['total_cost']		
		opening = Stock.objects.filter( stock_date__gte=fr, stock_date__lte=to, stock_type='Opening Stock').aggregate(Sum('cost'))['cost__sum']
		closing = Stock.objects.filter( stock_date__gte=fr, stock_date__lte=to, stock_type='Closing Stock').aggregate(Sum('cost'))['cost__sum']
		if purchases is None:
			purchases = 0
		if opening is None:
			opening = 0
		if closing is None:
			closing = 0		
		cogs = opening + Decimal(purchases) - closing
		# End COGS		

		advertising = Expense.objects.filter(category='Advertising', created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('cost'))['cost__sum']
		contractors = Expense.objects.filter(category='Contractors', created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('cost'))['cost__sum']
		rent = Expense.objects.filter(category='Rent or Lease', created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('cost'))['cost__sum']
		travel = Expense.objects.filter(category='Travel', created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('cost'))['cost__sum']
		financial_charge = Expense.objects.filter(category='Financial Charge', created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('cost'))['cost__sum']
		education = Expense.objects.filter(category='Education and Training', created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('cost'))['cost__sum']
		services = Expense.objects.filter(category='Professional Services', created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('cost'))['cost__sum']
		utilities = Expense.objects.filter(category='Utilities', created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('cost'))['cost__sum']
		other_expenses = Expense.objects.filter(category='Other Expenses', created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('cost'))['cost__sum']


		if advertising is None:
			advertising = 0
		if contractors is None:
			contractors = 0
		if rent is None:
			rent = 0
		if travel is None:
			travel = 0
		if financial_charge is None:
			financial_charge = 0
		if education is None:
			education = 0
		if services is None:
			services = 0
		if utilities is None:
			utilities = 0
		if other_expenses is None:
			other_expenses = 0								



		summary['advertising'] = advertising
		summary['contractors'] = contractors
		summary['rent'] = rent
		summary['travel'] = travel
		summary['financial_charge'] = financial_charge
		summary['services'] = services
		summary['utilities'] = utilities
		summary['other_expenses'] = other_expenses
		summary['education'] = education


		sales = Sale.objects.filter( created_at__date__gte=fr, created_at__date__lte=to,).all().aggregate(total_paid=Sum('amount_paid'))['total_paid']

		total_expense = Expense.objects.filter(created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('cost'))['cost__sum'] 
		depreciation = AccountsFixedAsset.objects.filter(depreciation_value__gt=0, created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('depreciation_value'))['depreciation_value__sum']
		amortization = AccountsFixedAsset.objects.filter(amortization_value__gt=0, created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('amortization_value'))['amortization_value__sum'] 
		takehome = Takehome.objects.filter(created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('salary'))['salary__sum']
		takehome_objs = Takehome.objects.filter(created_at__date__gte=fr, created_at__date__lte=to)
		interest_total = Interest.objects.filter( created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('remaining'))['remaining__sum']
		tax_total = Tax.objects.filter( created_at__date__gte=fr, created_at__date__lte=to,).aggregate(total=Sum('remain'))['total']

		if sales is None:
			sales = 0

		summary['total_paid'] = sales
		total_revenue = summary['total_paid']

		if tax_total is None:
			tax_total = 0

		if interest_total is None:
			interest_total = 0

		if total_revenue is None:
			total_revenue = 0

		if takehome is None:
			takehome = 0
		
		if total_expense is None:
			total_expense = 0

		if depreciation is None:
			depreciation = 0

		if amortization is None:
			amortization = 0

		nssf_funds = Payroll.objects.filter(nssf=True, created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
		loan_board_funds = Payroll.objects.filter(heslb=True, created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
		sdl = Payroll.objects.filter(created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
		paye_total = Payroll.objects.filter(paye=True, created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('paye_amount'))['paye_amount__sum']


		if sdl is None:
			sdl =0 

		if nssf_funds is None:
			nssf_funds = 0

		if loan_board_funds is None:
			loan_board_funds = 0

		if paye_total is None:
			paye_total = 0	

		total_social_funds = int(nssf_funds) + int(paye_total) + int(loan_board_funds) + int(sdl)

		tax = tax_total 	
		tax_interest = tax + interest_total

		takehome = takehome - total_social_funds


		##### Calculating OPEX #####
		opex = total_expense + takehome + depreciation + amortization
		opex_da = total_expense + takehome 

		##### Calculating EBITDA #####
		ebitda = total_revenue - (cogs + opex_da)				

		taxes = int(paye_total) + int(sdl)

		gross_profit = total_revenue - cogs
		summary['gross_profit'] = gross_profit


		##### Calculating EBIT #####
		ebit = gross_profit - opex


		####### Net Income ########
		net_income = ebit - tax_interest

		expenses = Expense.objects.filter(created_at__date__gte=fr, created_at__date__lte=to)
		summary['expenses'] = expenses

		summary['net_income'] = round(net_income,2)
		summary['social_funds'] = round(total_social_funds,2)
		summary['opex'] = round(opex,2)
		summary['ebit'] = round(ebit,2)
		summary['ebitda'] = round(ebitda,2)
		summary['tax_interest'] = round(tax_interest,2)
		summary['cogs'] = cogs
		summary['salaries'] = takehome
		summary['da'] = depreciation + amortization


		if pdf == '1':
			return income_statement_export_pdf(request, summary=summary)
		if xl == '1':
			return income_statement_export_excel(request, summary=summary)			

			
	context = {
		'business':business,
		'summary':summary,
		'd':d,
		'fr':fr,
		'to':to,
	}
	return render(request, 'income_statement.html', context)


####### Balance Sheet ########
@finance_report_required
@login_required
def balance_sheet(request, *args, **kwargs):
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first()
	interest_total = Interest.objects.all().aggregate(Sum('remaining'))['remaining__sum']
	tax_total = Tax.objects.all().aggregate(total=Sum('remain'))['total']
	liabilities_total = Liability.objects.all().aggregate(Sum('cost'))['cost__sum'] 
	assets_value = AccountsFixedAsset.objects.all().aggregate(Sum('value'))['value__sum']
	current_assets_value = AccountsCurrentAsset.objects.all().aggregate(Sum('cost'))['cost__sum']
	equity_total = Equity.objects.all().aggregate(Sum('value'))['value__sum']
	equities = Equity.objects.all() 
	liabilities = Liability.objects.all() 
	fixed_assets = AccountsFixedAsset.objects.all()
	current_assets = AccountsCurrentAsset.objects.all()


	if tax_total is None:
		tax_total = 0

	if interest_total is None:
		interest_total = 0

	if liabilities_total is None:
		liabilities_total = 0			

	if assets_value is None:
		assets_value = 0

	if current_assets_value is None:
		current_assets_value = 0
	if equity_total is None:
		equity_total = 0				

	liabilities_total = interest_total + tax_total + liabilities_total

	assets_total = assets_value + current_assets_value
	
	liabilities_equity = liabilities_total + equity_total


	if pdf == '1':
			return balance_sheet_export_pdf(request,  assets_total=assets_total, liabilities_total=liabilities_total, equity_total=equity_total, fixed_assets=fixed_assets, current_assets=current_assets, liabilities=liabilities, equities=equities, liability_equity=liabilities_equity)
	if xl == '1':
			return balance_sheet_export_excel(request,  assets_total=assets_total, liabilities_total=liabilities_total, equity_total=equity_total, fixed_assets=fixed_assets, current_assets=current_assets, liabilities=liabilities, equities=equities, liability_equity=liabilities_equity)		

	context = {
		'business':business,
		'liability_equity': liabilities_equity,
		'equities': equities,
		'fixed_assets': fixed_assets,
		'current_assets': current_assets,
		'liabilities': liabilities,
		'assets_total': assets_total,
		'liabilities_total': round(liabilities_total,2),
		'equity_total' : round(equity_total, 2),
	}
	template_name = 'balance_sheet.html'
	return render(request, template_name, context)	


@finance_report_required
@login_required
def cashflow_time(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first()
		
	context = {
		'business':business,
	}
	return render(request, 'cashflow_time.html', context)


@finance_report_required
@login_required
def cashflow(request, *args, **kwargs):
	id = kwargs.get('id')
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')
	fr = request.GET.get('fr')
	to = request.GET.get('to')
	business = Business.objects.filter(id=id).first()

	if request.method == 'GET':	
		cashflow = CheckAccount.objects.filter(created_at__date__gte=fr, created_at__date__lte=to)
	
	if pdf == '1':
			return cashbook_export_pdf(request, cashflow=cashflow)

	if xl == '1':
			return cashbook_export_excel(request, cashflow=cashflow)

	context = {
		'business':business,
		'cashflow':cashflow,	
		'fr':fr,
		'to':to,
	}
	return render(request, 'cashflow.html', context)


@finance_report_required
@login_required
def trial_balance_time(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first()
		
	context = {
		'business':business,
	}
	return render(request, 'trial-balance-time.html', context)


# """""""""" STOCK REPORT """""""""""
@store_report_required	
@login_required
def stock_time(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first()
	context = {
		'business':business,
	}
	return render(request, 'stock_time.html', context)

@store_report_required		
@login_required
def stock_report(request, *args, **kwargs):
	id = kwargs.get('id')
	d = kwargs.get('d')
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')
	fr = request.GET.get('fr')
	to = request.GET.get('to')
	business = Business.objects.filter(id=id).first() 
	if d == 1:
		dt = date.today()
		stocks = Stock.objects.filter(business=business, stock_date__month=dt.month,).all()
		opening = Stock.objects.filter(business=business, stock_date__month=dt.month, stock_type='Opening Stock').aggregate(Sum('cost'))['cost__sum']
		closing = Stock.objects.filter(business=business, stock_date__month=dt.month, stock_type='Closing Stock').aggregate(Sum('cost'))['cost__sum']
	
		if pdf == '1':
			return stock_report_export_pdf(request, business=business, stocks=stocks)

		if xl == '2':
			return stock_report_export_excel(request,business=business, stocks=stocks)	

	elif d == 2:	
		dt = date.today()
		month = dt.month - 1

		stocks = Stock.objects.filter(business=business, stock_date__month=month,).all()
		opening = Stock.objects.filter(business=business, stock_date__month=month, stock_type='Opening Stock').aggregate(Sum('cost'))['cost__sum']
		closing = Stock.objects.filter(business=business, stock_date__month=month, stock_type='Closing Stock').aggregate(Sum('cost'))['cost__sum']

		if pdf == '1':
			return stock_report_export_pdf(request, business=business, stocks=stocks)

		if xl == '2':
			return stock_report_export_excel(request,business=business, stocks=stocks)	
		
	elif d == 3:	
		stocks = Stock.objects.filter(business=business).all()
		opening = Stock.objects.filter(business=business, stock_type='Opening Stock').aggregate(Sum('cost'))['cost__sum']
		closing = Stock.objects.filter(business=business, stock_type='Closing Stock').aggregate(Sum('cost'))['cost__sum']

		if pdf == '1':
			return stock_report_export_pdf(request, business=business, stocks=stocks)

		if xl == '2':
			return stock_report_export_excel(request,business=business, stocks=stocks)	
	
	elif d == 4:
		if request.method == 'GET':	

			stocks = Stock.objects.filter(business=business, stock_date__gte=fr,stock_date__lte=to,).all()
			opening = Stock.objects.filter(business=business, stock_date__gte=fr, stock_date__lte=to, stock_type='Opening Stock').aggregate(Sum('cost'))['cost__sum']
			closing = Stock.objects.filter(business=business, stock_date__gte=fr, stock_date__lte=to, stock_type='Closing Stock').aggregate(Sum('cost'))['cost__sum']

			if pdf == '1':
				return stock_report_export_pdf(request, business=business, stocks=stocks)

			if xl == '2':
				return stock_report_export_excel(request,business=business, stocks=stocks)		

	context = {
		'business':business,
		'stocks':stocks,
		'd':d,
		'fr':fr,
		'to':to,
	}
	return render(request, 'stock_report.html', context)


@store_report_required
@login_required
def supplier_time(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first()
	suppliers = Supplier.objects.filter(business=business)
	context = {
		'business':business,
		'suppliers':suppliers,
	}
	return render(request, 'supplier_time.html', context)

@store_report_required
@login_required
def supplier_report(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first() 
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')

	if request.method == 'GET':
		p = request.GET['p']
		fr = request.GET.get('fr')
		to = request.GET.get('to')

		if p == '0':

			purchases = PurchaseLedger.objects.filter(business=business, created_at__date__gte=fr, created_at__date__lte=to,).all().order_by('-pk')
			summary = PurchaseLedger.objects.filter(business=business, created_at__date__gte=fr, created_at__date__lte=to,).all().order_by('-pk').aggregate(total_purchase=Sum('amount'),)
			if pdf == '1':
				return supplier_report_export_pdf(request, business=business, purchases=purchases, summary=summary)

		else:
			purchases = PurchaseLedger.objects.filter(business=business, supplier=p, created_at__date__gte=fr, created_at__date__lte=to,).all().order_by('-pk')
			summary = PurchaseLedger.objects.filter(business=business, supplier=p, created_at__date__gte=fr, created_at__date__lte=to,).all().order_by('-pk').aggregate(total_purchase=Sum('amount'),)
			if pdf == '1':
				return supplier_report_export_pdf(request, business=business, purchases=purchases, summary=summary)

			
	context = {
		'business':business,
		'purchases':purchases,
		'summary':summary,
		'p':p,
		'fr':fr,
		'to':to,
	}
	return render(request, 'supplier_report.html', context)


@store_report_required
@login_required
def grn_time(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first()
	suppliers = Supplier.objects.filter(business=business)
	context = {
		'business':business,
		'suppliers':suppliers,
	}
	return render(request, 'grn_time.html', context)

@store_report_required
@login_required
def grn_report(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first() 
	pdf = request.GET.get('pdf')
	xl = request.GET.get('xl')

	if request.method == 'GET':
		fr = request.GET.get('fr')
		to = request.GET.get('to')

		grns = GoodsReceivedNote.objects.filter(business=business, published=True, created_at__date__gte=fr, created_at__date__lte=to,).all().order_by('-pk')
		
		summary = GoodsReceivedNote.objects.filter(business=business, published=True, created_at__date__gte=fr, created_at__date__lte=to,).all().aggregate(grn_total=Sum('grn_list__total'),)
		
		if pdf == '1':
			return grn_report_export_pdf(request, business=business, grns=grns, summary=summary)
			
	context = {
		'business':business,
		'grns':grns,
		'summary':summary,
		'fr':fr,
		'to':to,
	}
	return render(request, 'grn_report.html', context)	