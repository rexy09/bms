from weasyprint import HTML
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from administration.models import *
from .models import *
from decimal import Decimal
from django.contrib.auth.decorators import login_required


@login_required
def purchase_order_export_pdf(request, **kwargs):
	id = kwargs.get('id')
	purchase_order = PurchaseOrder.objects.filter(id=id).first() 
	html_string = render_to_string('purchase_order_pdf.html', {'purchase_order':purchase_order,})
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	html.write_pdf(target='/tmp/purchase_order.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('purchase_order.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		return response


@login_required
def local_purchase_order_export_pdf(request, **kwargs):
	id = kwargs.get('id')
	local_purchase_order = LocalPurchaseOrder.objects.filter(id=id).first()
	html_string = render_to_string('local_purchase_order_pdf.html', {'purchase_order':local_purchase_order,})
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	html.write_pdf(target='/tmp/local_purchase_order.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('local_purchase_order.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		return response


@login_required
def sales_report_export_pdf(request, **kwargs):
	context = {
		'business':kwargs.get('business'),
		'sales':kwargs.get('sales'),
		'summary':kwargs.get('summary'),
		'products':kwargs.get('products'),
	}
	html_string = render_to_string('sales_report_pdf.html', context)
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	html.write_pdf(target='/tmp/sales_report.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('sales_report.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		return response


@login_required
def inventory_report_export_pdf(request, **kwargs):
	context = {
		'business':kwargs.get('business'),
		'inventories':kwargs.get('inventories'),
		'summary':kwargs.get('summary'),
		'products':kwargs.get('products'),
	}
	html_string = render_to_string('inventory_report_pdf.html', context)
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	html.write_pdf(target='/tmp/inventory_report.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('inventory_report.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		return response


@login_required
def procurement_report_export_pdf(request, **kwargs):
	context = {
		'business':kwargs.get('business'),
		'local_purchases':kwargs.get('local_purchases'),
		'purchases':kwargs.get('purchases'),
		'summary':kwargs.get('summary'),
	}
	html_string = render_to_string('procurement_report_pdf.html', context)
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	html.write_pdf(target='/tmp/procurement_report.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('procurement_report.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		return response


@login_required
def opex_report_export_pdf(request, **kwargs):
	context = {
		'business':kwargs.get('business'),
		'expenses':kwargs.get('expense_objects'),
		'cost':kwargs.get('total_cost'),
		'expenses_total':kwargs.get('expenses_total'),
		'exps':kwargs.get('exps'),
	}
	html_string = render_to_string('opex-report-pdf.html', context)
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	html.write_pdf(target='/tmp/opex_report.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('opex_report.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		return response


@login_required
def customer_report_export_pdf(request, **kwargs):
	context = {
		'business':kwargs.get('business'),
		'customers':kwargs.get('customers'),
		'normal':kwargs.get('normal'),
		'loyal':kwargs.get('loyal'),
		'other':kwargs.get('other'),
	}
	html_string = render_to_string('customer-report-pdf.html', context)
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	html.write_pdf(target='/tmp/customer_report.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('customer_report.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		return response	


@login_required
def payroll_report_export_pdf(request, **kwargs):
	context = {
		'business':kwargs.get('business'),
		'takehome_total':kwargs.get('takehome_total'),
		'takehome':kwargs.get('takehome'),
		'wcf':kwargs.get('wcf'),
		'nssf':kwargs.get('nssf'),
		'loan_board':kwargs.get('loan_board'),
		'paye':kwargs.get('paye'),
		'bonus':kwargs.get('bonus'),
		'overtime':kwargs.get('overtime'),
		'salaries_total':kwargs.get('salaries_total'),
		'total_expenses':kwargs.get('total_expenses'),
		'employees':kwargs.get('employees'),
		'deduction':kwargs.get('deduction'),
		'sdl': kwargs.get('sdl')
	}
	html_string = render_to_string('payroll-report-pdf.html', context)
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	html.write_pdf(target='/tmp/payroll_report.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('payroll_report.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		return response				



def trial_balance_export_pdf(request, *args, **kwargs):
	id = kwargs.get('id')
	business = Business.objects.filter(id=id).first()
	fr = request.GET.get('fr')
	to = request.GET.get('to')	
	business = Business.objects.filter(id=id).first()
	nssf_funds = Payroll.objects.filter(nssf=True, created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('nssf_amount'))['nssf_amount__sum']
	loan_board_funds = Payroll.objects.filter(heslb=True, created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('heslb_amount'))['heslb_amount__sum']
	paye_total = Payroll.objects.filter(paye=True, created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('paye_amount'))['paye_amount__sum']	
	takehome_total = Takehome.objects.all().aggregate(Sum('salary'))['salary__sum']
	sdl = Payroll.objects.filter( created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('sdl_amount'))['sdl_amount__sum']   		
	taxes = Tax.objects.filter( created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('remain'))['remain__sum']
	interest_remaining = Interest.objects.filter( created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('remaining'))['remaining__sum']
	interest_repayment = Interest.objects.filter( created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('repayment'))['repayment__sum']
	sales = Sale.objects.filter(status='Completed', created_at__date__gte=fr, created_at__date__lte=to).all().aggregate(total_paid=Sum('amount_paid'))
	inventory_qs = Inventory.objects.filter( created_at__date__gte=fr, created_at__date__lte=to).annotate(available=F('remain')-F('damage'))			
	inventories = inventory_qs.filter(available__gt=0).order_by('-pk')
	expenses = Expense.objects.filter( created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('cost'))['cost__sum']
	liabilities = Liability.objects.filter( created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('cost'))['cost__sum']
	fixed_assets = AccountsFixedAsset.objects.filter( created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('value'))['value__sum']
	current_assets = AccountsCurrentAsset.objects.filter( created_at__date__gte=fr, created_at__date__lte=to).aggregate(Sum('cost'))['cost__sum']

	sales = sales['total_paid']

	# Start COGS
	purchases = Inventory.objects.filter(created_at__date__gte=fr, created_at__date__lte=to,).aggregate(total_cost=Sum(F('quantity')*F('product_cost'),output_field=FloatField()))['total_cost']		
	opening = Stock.objects.filter(stock_date__gte=fr, stock_date__lte=to, stock_type='Opening Stock').aggregate(Sum('cost'))['cost__sum']
	closing = Stock.objects.filter(stock_date__gte=fr, stock_date__lte=to, stock_type='Closing Stock').aggregate(Sum('cost'))['cost__sum']
	if purchases is None:
		purchases = 0
	if opening is None:
		opening = 0
	if closing is None:
		closing = 0		
	cogs = opening + Decimal(purchases) - closing
	# End COGS	


	if cogs is None:
		cogs = 0

	if fixed_assets is None:
		fixed_assets = 0
	if current_assets is None:
		current_assets = 0
	if interest_remaining is None:
		interest_remaining = 0	
	if interest_repayment is None:
		interest_repayment = 0		
	
	interests = interest_repayment - interest_remaining		

	assets = fixed_assets + current_assets		       



	if takehome_total is None:
		takehome_total = 0
	if sdl is None:
		sdl = 0	
	if taxes is None:
		taxes = 0
	if interests is None:
		interests = 0					
	if liabilities is None:
		liabilities = 0
	if assets is None:
		assets = 0
	if cogs is None:
		cogs = 0
	if paye_total is None:
		paye_total = 0	
	if expenses is None:
		expenses = 0
	if sales is None:
		sales = 0
	if nssf_funds is None:
		nssf_funds = 0
	if loan_board_funds is None:
		loan_board_funds = 0
	if paye_total is None:
		paye_total = 0	


	total_debit = int(nssf_funds) + int(paye_total) + int(loan_board_funds) + int(takehome_total) + int(sdl) + int(interests) + int(taxes) + int(expenses) + int(cogs) + int(assets)
	total_credit = int(sales) + int(liabilities)


	context = {
		'business' : business,
		'nssf': int(nssf_funds),
		'heslb': int(loan_board_funds),
		'sdl': int(sdl),
		'salaries': int(takehome_total),
		'paye': int(paye_total),
		'sales': sales,
		'taxes': taxes,
		'interests': interests,
		'expenses': expenses,
		'cogs': int(cogs),
		'liabilities': liabilities,
		'assets': assets,
		'credit': total_credit,
		'debit': total_debit,

	}
	html_string = render_to_string('trial-balance-pdf.html', context)
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	html.write_pdf(target='/tmp/trial_balance_report.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('trial_balance_report.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		return response	


def balance_sheet_export_pdf(request, *args, **kwargs):
	context = {
		'business':kwargs.get('business'),
		'assets_total': kwargs.get('assets_total'),
		'liabilities_total': kwargs.get('liabilities_total'),
		'equity_total': kwargs.get('equity_total'),
		'liabilities': kwargs.get('liabilities'),
		'fixed_assets': kwargs.get('fixed_assets'),
		'equities': kwargs.get('equities'),
		'liability_equity': kwargs.get('liability_equity'),
		'current_assets': kwargs.get('current_assets'),
	}
	html_string = render_to_string('balance_sheet_pdf.html', context)
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	html.write_pdf(target='/tmp/balance_sheet_report.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('balance_sheet_report.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		return response    	



def income_statement_export_pdf(request, *args, **kwargs):
	context = {
		'business': kwargs.get('business'),
		'summary': kwargs.get('summary'),
	}
	html_string = render_to_string('income-statement-pdf.html', context)
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	html.write_pdf(target='/tmp/income_statement_report.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('income_statement_report.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		return response  


def cashbook_export_pdf(request, *args, **kwargs):
	context = {
		'business':kwargs.get('business'),
		'cashflow': kwargs.get('cashflow')
	}
	html_string = render_to_string('cashbook-pdf.html', context)
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	html.write_pdf(target='/tmp/cashbook_report.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('cashbook_report.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		return response  


@login_required
def stock_report_export_pdf(request, **kwargs):
	context = {
		'business':kwargs.get('business'),
		'stocks':kwargs.get('stocks'),
	}
	html_string = render_to_string('stock_report_pdf.html', context)
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	html.write_pdf(target='/tmp/stock_report.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('stock_report.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		return response


@login_required
def grn_report_export_pdf(request, **kwargs):
	context = {
		'business':kwargs.get('business'),
		'grns':kwargs.get('grns'),
		'summary':kwargs.get('summary'),
	}
	html_string = render_to_string('grn_report_pdf.html', context)
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	html.write_pdf(target='/tmp/grn_report.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('grn_report.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		return response


@login_required
def supplier_report_export_pdf(request, **kwargs):
	context = {
		'business':kwargs.get('business'),
		'purchases':kwargs.get('purchases'),
		'summary':kwargs.get('summary'),
	}
	html_string = render_to_string('supplier_report_pdf.html', context)
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	html.write_pdf(target='/tmp/supplier_report.pdf');

	fs = FileSystemStorage('/tmp')
	with fs.open('supplier_report.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		return response