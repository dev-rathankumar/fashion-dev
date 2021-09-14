from modeltranslation.translator import translator, TranslationOptions
from .models import Blog

class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'blog_body')

translator.register(Blog, BlogTranslationOptions)