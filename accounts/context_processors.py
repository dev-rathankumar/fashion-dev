from portfolio.models import PortfolioActivation
from products.models import ProductActivation
from blogs.models import BlogActivation
from accounts.models import Business, User, DashboardImage
from urllib.parse import urlparse
from sitesettings.models import Header, Homepage, Footer, ServiceActivation, Topbar
from django.http import HttpResponse
from datetime import date, datetime


def get_business(request):
    url = request.build_absolute_uri()
    domain = urlparse(url).netloc
    try:
        business = Business.objects.get(user__is_business=True, is_account_verified=True)
        get_exp_date = business.account_expiry_date
        exp_date = datetime.strptime(str(get_exp_date), '%Y-%m-%d')
        get_today = date.today()
        today = datetime.strptime(str(get_today), '%Y-%m-%d')
        if today > exp_date:
            account_expiry = True
        else:
            account_expiry = False
        return dict(business=business, domain=domain, account_expiry=account_expiry)
    except:
        business = None
    return dict(domain=domain)


def get_sitesettings(request):
    try:
        business = Business.objects.get(user__is_business=True, is_account_verified=True)
        if business:
            company_name = business.company_name
            
            try:
                header = Header.objects.get(business=business)
                footer = Footer.objects.get(business=business)
                topbar = Topbar.objects.get(business=business)
                blog_activation = BlogActivation.objects.get(business=business)
                product_activation = ProductActivation.objects.get(business=business)
                service_activation = ServiceActivation.objects.get(business=business)
                portfolio_activation = PortfolioActivation.objects.get(business=business)
            except:
                header = None
                footer = None
                topbar = None
                blog_activation = None
                product_activation = None
                service_activation = None
                portfolio_activation = None
    except:
        header = None
        footer = None
        topbar = None
        company_name = None
        blog_activation = None
        product_activation = None
        service_activation = None
        portfolio_activation = None
    return dict(portfolio_activation=portfolio_activation, service_activation=service_activation, product_activation=product_activation, header=header, company_name=company_name, footer=footer, topbar=topbar, blog_activation=blog_activation)


def get_dashboardImage(request):
    try:
        business = Business.objects.get(user__is_business=True, is_account_verified=True)
        dashboardimage = DashboardImage.objects.get(business=business)
    except:
        business = None
        dashboardimage = None
    return dict(dashboardimage=dashboardimage)
    