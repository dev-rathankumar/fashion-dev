from newsletters.forms import EmailSubscribeForm


def emailNewsletterCP(request):
    form = EmailSubscribeForm()
    return dict(form=form)