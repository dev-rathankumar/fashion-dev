import json
from urllib.parse import urlparse
from pages.views import about, services
from django.core.mail import message
from products.models import ReviewRating, SalesPopup, SalesPopupSetting
from django.shortcuts import render, get_object_or_404, redirect
from .models import AboutContent, CashOnDelivery, DirectDepositEmail, Header, Homepage, BannerImage, PaypalConfig, StoreFeature, ParallaxBackground, ContactPage, Footer, SocialMediaLink, AboutPage, Policy, TermsAndCondition, Topbar
from .forms import AboutContentForm, DirectDepositEmailForm, HeaderForm, BannerImageForm, PaypalConfigForm, SalesPopupForm, SalesPopupSettingForm, StoreFeatureForm, ParallaxBackgroundForm, ContactPageForm, FooterForm, SocialMediaLinkForm, AboutPageForm, PolicyForm, StoreLocationForm, TermsAndConditionForm, TopbarForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from accounts.models import Business
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from business.views import business_required

from django.core.files.storage import FileSystemStorage
from business.views import is_account_expired
from orders.models import StoreLocation


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
def header(request):
    current_user = request.user
    try:
        header = Header.objects.get(business=current_user.id)
        return redirect('headerEdit', header.id)
    except Header.DoesNotExist:
        return redirect('headerAdd')


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def headerEdit(request, pk=None):
    header = get_object_or_404(Header, pk=pk)
    if request.method == 'POST':
        form = HeaderForm(request.POST, request.FILES, instance=header)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings applied successfully.')
            return redirect('header')
    else:
        form = HeaderForm(instance=header)
    context = {
        'form': form,
        'header': header,
    }
    return render(request, 'business/sitesettings/headerEdit.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def headerAdd(request):
    if request.method == 'POST':
        form = HeaderForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            header = form.save(commit=False)
            business_name = Business.objects.get(user=current_user)
            header.business = business_name
            form.save()
            messages.success(request, 'Settings applied successfully.')
            return redirect('headerEdit', header.id)

    else:
        form = HeaderForm()
    context = {
        'form': form,
    }
    return render(request, 'business/sitesettings/headerAdd.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def banners(request):
    try:
        business = Business.objects.get(user=request.user)
        homepage = Homepage.objects.get(business=business)
    except:
        pass
    banners = BannerImage.objects.filter(homepage=homepage)
    context = {
        'banners': banners,
    }
    return render(request, 'business/sitesettings/banners.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def addBanner(request):
    if request.method == 'POST':
        form = BannerImageForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            banner = form.save(commit=False)
            business_name = Business.objects.get(user=current_user)

            homepage = Homepage.objects.get(business=business_name)
            banner.homepage = homepage
            form.save()
            messages.success(request, 'Banner saved successfully.')
            return redirect('banners')
    else:
        form = BannerImageForm()
    context = {
        'form':form,
    }
    return render(request, 'business/sitesettings/addBanner.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editBanner(request, pk=None):
    banner = get_object_or_404(BannerImage, pk=pk)
    if request.method == 'POST':
        form = BannerImageForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banner updated successfully.')
            return redirect('banners')
    else:
        form = BannerImageForm(instance=banner)
    context = {
        'form': form,
        'banner': banner,
    }
    return render(request, 'business/sitesettings/editBanner.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deleteBanner(request, pk=None):
    banner = get_object_or_404(BannerImage, pk=pk)
    banner.delete()
    messages.success(request, 'Banner has been deleted.')
    return redirect('banners')


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def store_features(request):
    try:
        business = Business.objects.get(user=request.user)
        homepage = Homepage.objects.get(business=business)
    except:
        pass
    store_features = StoreFeature.objects.filter(homepage=homepage)
    features_count = store_features.count()
    context = {
        'store_features': store_features,
        'features_count': features_count,
    }
    return render(request, 'business/sitesettings/store_features.html', context)

@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def addFeature(request):
    homepage = Homepage.objects.get(business__user=request.user)
    store_features = StoreFeature.objects.filter(homepage=homepage)
    features_count = store_features.count()
    if features_count >= 4:
        messages.warning(request, 'Only 4 store features allowed!')
        return redirect('store_features')
    else:
        form = StoreFeatureForm(request.POST, request.FILES)
        if request.method == 'POST':
            if form.is_valid():
                current_user = request.user
                feature = form.save(commit=False)
                business_name = Business.objects.get(user=current_user)

                homepage = Homepage.objects.get(business=business_name)
                feature.homepage = homepage
                form.save()
                messages.success(request, 'Feature saved successfully.')
                return redirect('store_features')
        else:
            form = StoreFeatureForm()
    context = {
        'form': form,
    }
    return render(request, 'business/sitesettings/addStoreFeature.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editFeature(request, pk=None):
    feature = get_object_or_404(StoreFeature, pk=pk)
    if request.method == 'POST':
        form = StoreFeatureForm(request.POST, request.FILES, instance=feature)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feature updated successfully.')
            return redirect('store_features')
    else:
        form = StoreFeatureForm(instance=feature)
    context = {
        'form': form,
        'feature': feature,
    }
    return render(request, 'business/sitesettings/editStoreFeature.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deleteFeature(request, pk=None):
    feature = get_object_or_404(StoreFeature, pk=pk)
    feature.delete()
    messages.success(request, 'Feature has been deleted.')
    return redirect('store_features')


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def homepage_background(request):
    homepage = Homepage.objects.get(business__user=request.user)
    background = get_object_or_404(ParallaxBackground, homepage=homepage)
    if request.method == "POST":
        form = ParallaxBackgroundForm(request.POST, request.FILES, instance=background)
        form.save()
        messages.success(request, 'Background Image updated successfully.')
        return redirect('homepage_background')
    else:
        form = ParallaxBackgroundForm(instance=background)
    context = {
        'form': form,
        'background': background,
    }
    return render(request, 'business/sitesettings/homepage_background.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def aboutUs(request):
    business = Business.objects.get(user=request.user)
    about_page = get_object_or_404(AboutPage, business=business)
    AboutContentFormSet = inlineformset_factory(AboutPage, AboutContent, form=AboutContentForm, extra=1)
    if request.method == 'POST':
        form = AboutPageForm(request.POST, instance=about_page)
        if form.is_valid():
            about = form.save(commit=False)
            about.business = business
            form.save()
            messages.success(request, 'Settings saved successfully')
            return redirect('aboutContent')
        else:
            print(form.errors)
    else:
        form = AboutPageForm(instance=about_page)
        aboutContent_form = AboutContentForm()
        formset = AboutContentFormSet()
    context = {
        'form': form,
        'about_page': about_page,
        'aboutContent_form': aboutContent_form,
        'formset': formset,
    }
    return render(request, 'business/sitesettings/aboutUs.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def aboutContent(request):
    business = Business.objects.get(user=request.user)
    aboutus = get_object_or_404(AboutPage, business=business)
    about_form = AboutPageForm(instance=aboutus)
    AboutContentFormSet = inlineformset_factory(AboutPage, AboutContent, form=AboutContentForm, extra=1)
    if request.method == 'POST':
        add_another = request.POST['add_another']
        formset = AboutContentFormSet(request.POST, request.FILES, instance=aboutus)
        if formset.is_valid():
            # aboutContent = formset.save(commit=False)
            # aboutContent.about_id = aboutus.id
            formset.save()
            return redirect('aboutContent')
        else:
            print(formset.errors)
            return redirect('aboutContent')

    else:
        formset = AboutContentFormSet(instance=aboutus)
        about_form = AboutPageForm(instance=aboutus)

    context = {
        'aboutus': aboutus,
        'formset': formset,
        'about_form': about_form,
    }
    return render(request, 'business/sitesettings/aboutUs.html', context)




@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def contactUs(request):
    business = Business.objects.get(user=request.user)
    contact_page = get_object_or_404(ContactPage, business=business)
    if request.method == 'POST':
        form = ContactPageForm(request.POST, instance=contact_page)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.business = business
            form.save()
            messages.success(request, 'Settings saved successfully')
            return redirect('contactUs')
    else:
        form = ContactPageForm(instance=contact_page)
    context = {
        'form': form,
    }
    return render(request, 'business/sitesettings/contactUs.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def footerEdit(request):
    business = Business.objects.get(user=request.user)
    footer = get_object_or_404(Footer, business=business)

    if request.method == 'POST':
        form = FooterForm(request.POST, instance=footer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Footer Copyright updated successfully')
            return redirect('footerEdit')
    else:
        form = FooterForm(instance=footer)
    context = {
        'form': form,
        'footer': footer,
    }
    return render(request, 'business/sitesettings/footerEdit.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def topbarEdit(request):
    business = Business.objects.get(user=request.user)
    # try:
    #     checkTopbar = Topbar.objects.get(business=business, is_enabled=True)
    # except:
    #     checkTopbar = None
    topbar = get_object_or_404(Topbar, business=business)

    if request.method == 'POST':
        form = TopbarForm(request.POST, instance=topbar)
        if form.is_valid():
            form.save()
            messages.success(request, 'Topbar updated successfully')
            return redirect('topbarEdit')
    else:
        form = TopbarForm(instance=topbar)
    context = {
        'form': form,
        'topbar': topbar,
    }
    return render(request, 'business/sitesettings/topbarEdit.html', context)


def topbarToggleEnable(request):
    event = request.GET.get('event')
    business = Business.objects.get(user=request.user)
    topbar = get_object_or_404(Topbar, business=business)
    if event == 'true':
        topbar.is_enabled = True
        topbar.save()
        result = 'enabled'
    else:
        topbar.is_enabled = False
        topbar.save()
        result = 'disabled'
    return HttpResponse(result)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def socialIcons(request):
    business = Business.objects.get(user=request.user)
    social_icons = SocialMediaLink.objects.filter(business=business).order_by('created_date')
    context = {
        'social_icons': social_icons,
    }
    return render(request, 'business/sitesettings/socialIcons.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def addIcon(request):
    business = Business.objects.get(user=request.user)
    social_icons = SocialMediaLink.objects.filter(business=business)
    form = SocialMediaLinkForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            socialicon = form.save(commit=False)
            socialicon.business = business
            form.save()
            messages.success(request, 'Social icon saved successfully.')
            return redirect('socialIcons')
    else:
        form = SocialMediaLinkForm()
    context = {
        'form': form,
    }
    return render(request, 'business/sitesettings/addIcon.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editIcon(request, pk=None):
    social_icons = get_object_or_404(SocialMediaLink, pk=pk)

    if request.method == 'POST':
        form = SocialMediaLinkForm(request.POST, instance=social_icons)
        if form.is_valid():
            form.save()
            messages.success(request, 'Social Icon updated successfully.')
            return redirect('socialIcons')
    else:
        form = SocialMediaLinkForm(instance=social_icons)
    context = {
        'form': form,
        'social_icons': social_icons,
    }
    return render(request, 'business/sitesettings/editIcon.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deleteIcon(request, pk=None):
    social_icon = get_object_or_404(SocialMediaLink, pk=pk)
    social_icon.delete()
    messages.success(request, 'Social Icon has been deleted.')
    return redirect('socialIcons')


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editPolicy(request):
    business = Business.objects.get(user=request.user)
    policy = get_object_or_404(Policy, business=business)
    if request.method == 'POST':
        form = PolicyForm(request.POST, instance=policy)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.business = business
            form.save()
            messages.success(request, 'Policy saved successfully')
            return redirect('editPolicy')
        else:
            print(form.errors)
    else:
        form = PolicyForm(instance=policy)
    context = {
        'form': form,
    }
    return render(request, 'business/sitesettings/editPolicy.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editTermsConditions(request):
    business = Business.objects.get(user=request.user)
    terms = get_object_or_404(TermsAndCondition, business=business)
    if request.method == 'POST':
        form = TermsAndConditionForm(request.POST, instance=terms)
        if form.is_valid():
            terms = form.save(commit=False)
            terms.business = business
            form.save()
            messages.success(request, 'Terms & Conditions saved successfully')
            return redirect('editTermsConditions')
        else:
            print(form.errors)
    else:
        form = TermsAndConditionForm(instance=terms)
    context = {
        'form': form,
    }
    return render(request, 'business/sitesettings/editTermsConditions.html', context)



@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def paymentGateways(request):
    business = Business.objects.get(user=request.user)
    dd = get_object_or_404(DirectDepositEmail, business=business)
    pp = get_object_or_404(PaypalConfig, business=business)
    cod = get_object_or_404(CashOnDelivery, business=business)
   

    if request.method == 'POST':
        gateway = request.POST['gateway']
        if gateway == 'paypal':
            ppform = PaypalConfigForm(request.POST, instance=pp)
            if ppform.is_valid():
                ppform.save()
                messages.success(request, 'Your paypal client id is updated.')
                return redirect('paymentGateways')
        else:
            ddform = DirectDepositEmailForm(request.POST, instance=dd)
            if ddform.is_valid():
                ddform.save()
                messages.success(request, 'Email address for your Direct Deposit payment gateway is updated.')
                return redirect('paymentGateways')
    else:
        ddform = DirectDepositEmailForm(instance=dd)
        ppform = PaypalConfigForm(instance=pp)
        ppform = PaypalConfigForm(instance=pp)
    context = {
        'ddform': ddform,
        'dd': dd,
        'ppform': ppform,
        'pp': pp,
        'cod': cod,
    }
    return render(request, 'business/sitesettings/paymentGateways.html', context)


def ddToggleEnable(request):
    event = request.GET.get('event')
    business = Business.objects.get(user=request.user)
    dd = get_object_or_404(DirectDepositEmail, business=business)
    if event == 'true':
        dd.is_enabled = True
        dd.save()
        result = 'enabled'
    else:
        dd.is_enabled = False
        dd.save()
        result = 'disabled'
    return HttpResponse(result)


def ppToggleEnable(request):
    event = request.GET.get('event')
    business = Business.objects.get(user=request.user)
    pp = get_object_or_404(PaypalConfig, business=business)
    if event == 'true':
        pp.is_enabled = True
        pp.save()
        result = 'enabled'
    else:
        pp.is_enabled = False
        pp.save()
        result = 'disabled'
    return HttpResponse(result)


def codToggleEnable(request):
    event = request.GET.get('event')
    business = Business.objects.get(user=request.user)
    cod = get_object_or_404(CashOnDelivery, business=business)
    if event == 'true':
        cod.is_enabled = True
        cod.save()
        result = 'enabled'
    else:
        cod.is_enabled = False
        cod.save()
        result = 'disabled'
    return HttpResponse(result)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def store_locations(request):
    store_locations = StoreLocation.objects.all().order_by('created_at')
    context = {
        'store_locations': store_locations,
    }
    return render(request, 'business/sitesettings/store_locations.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def addLocation(request):
    form = StoreLocationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            current_user = request.user
            location = form.save(commit=False)
            business = Business.objects.get(user=current_user)
            location.business = business
            location.save()
            messages.success(request, 'Location added successfully.')
            return redirect('store_locations')
    else:
        form = StoreLocationForm()
    context = {
        'form': form,
    }
    return render(request, 'business/sitesettings/addStoreLocation.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editLocation(request, pk=None):
    location = get_object_or_404(StoreLocation, pk=pk)
    if request.method == 'POST':
        form = StoreLocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location updated successfully.')
            return redirect('store_locations')
    else:
        form = StoreLocationForm(instance=location)
    context = {
        'form': form,
        'location': location,
    }
    return render(request, 'business/sitesettings/editStoreLocation.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deleteLocation(request, pk=None):
    location = get_object_or_404(StoreLocation, pk=pk)
    location.delete()
    messages.success(request, 'Store location has been deleted.')
    return redirect('store_locations')


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def salesPopup(request):
    sales_popups = SalesPopup.objects.all().order_by('-created_on')
    context = {
        'sales_popups': sales_popups,
    }
    return render(request, 'business/sitesettings/salesPopup.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def addPopup(request):
    form = SalesPopupForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            current_user = request.user
            popup = form.save(commit=False)
            business = Business.objects.get(user=current_user)
            popup.business = business
            popup.save()
            messages.success(request, 'Sales popup created successfully.')
            return redirect('salesPopup')
    else:
        form = SalesPopupForm()
    context = {
        'form': form,
    }
    return render(request, 'business/sitesettings/addPopup.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def editPopup(request, pk=None):
    popup = get_object_or_404(SalesPopup, pk=pk)
    if request.method == 'POST':
        form = SalesPopupForm(request.POST, instance=popup)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sales popup updated successfully.')
            return redirect('salesPopup')
    else:
        form = SalesPopupForm(instance=popup)
    context = {
        'form': form,
        'popup': popup,
    }
    return render(request, 'business/sitesettings/editPopup.html', context)


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def deletePopup(request, pk=None):
    popup = get_object_or_404(SalesPopup, pk=pk)
    popup.delete()
    messages.success(request, 'Sales popup has been deleted.')
    return redirect('salesPopup')


@login_required(login_url = 'userLogin')
@business_required(login_url="userLogin")
@is_account_expired
def salesPopupSettings(request):
    business = Business.objects.get(user=request.user)
    settings = get_object_or_404(SalesPopupSetting, business=business)

    if request.method == 'POST':
        form = SalesPopupSettingForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully')
            return redirect('salesPopupSettings')
    else:
        form = SalesPopupSettingForm(instance=settings)
    context = {
        'form': form,
        'settings': settings,
    }
    return render(request, 'business/sitesettings/salesPopupSettings.html', context)