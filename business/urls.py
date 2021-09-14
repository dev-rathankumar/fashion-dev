from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='biz_dashboard'),
    path('login/', views.login, name='biz_login'),
    path('logout/', views.logout, name='biz_logout'),

    path('forgotPassword/', views.forgotPassword, name='biz_forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='biz_resetForgotPassword_validate'),
    path('resetPassword/', views.biz_resetPassword, name='biz_resetForgotPassword'),

    path('profile/', views.biz_profile, name='biz_profile'),
    path('changePassword/', views.biz_changePassword, name='biz_changePassword'),

    # Edit profile
    path('editProfile/<int:pk>/', views.editProfile, name='editProfile'),

    # Payment settings
    path('paymentSettings/<int:pk>/', views.paymentSettings, name='paymentSettings'),

    # Categories
    path('categories/', views.allCategories, name='allCategories'),
    path('categories/addCategory/', views.addCategory, name='addCategory'),
    path('categories/editCategory/<int:pk>/', views.editCategory, name='editCategory'),
    path('categories/deleteCategory/<int:pk>/', views.deleteCategory, name='deleteCategory'),

    # Products
    path('products/', views.allProducts, name='allProducts'),
    path('products/editProduct/<int:pk>/', views.editProduct, name='editProduct'),
    path('products/editProduct/<int:pk>/editGallery/', views.editGallery, name='editGallery'),
    path('products/editProduct/<int:pk>/editVariants/', views.editVariants, name='editVariants'),
    path('products/addProduct/', views.addProduct, name='addProduct'),
    path('products/deleteProduct/<int:pk>/', views.deleteProduct, name='deleteProduct'),
    path('products/productEnableToggle/', views.productEnableToggle, name='productEnableToggle'),

    # Manage Orders
    path('orders/', views.allOrders, name='allOrders'),
    path('orders/orderDetail/<int:pk>/', views.bizOrderDetail, name='bizOrderDetail'),
    path('orders/editOrder/<int:pk>/', views.editOrder, name='editOrder'),
    path('orders/deleteOrder/<int:pk>/', views.deleteOrder, name='deleteOrder'),

    # Site settings
    path('site_settings/', include('sitesettings.urls')),

    # Plans
    path('plans/', views.plans, name='plans'),
    path('planPurchaseHistory/', views.planPurchaseHistory, name='planPurchaseHistory'),
    path('planHistoryDetail/<int:pk>/', views.planHistoryDetail, name='planHistoryDetail'),
    path('purchasePlan/', views.purchasePlan, name='purchasePlan'),
    path('planPayment/', views.planPayment, name='planPayment'),
    path('planOrder/', views.planOrder, name='planOrder'),
    path('plan_order_complete/', views.plan_order_complete, name='plan_order_complete'),

    # Customers
    path('customers/', views.allCustomers, name='allCustomers'),
    path('customers/CustomerViewProfile/<int:pk>/', views.CustomerViewProfile, name='CustomerViewProfile'),

    path('setTax/<int:business_id>/', views.setTax, name='setTax'),

    # Emails
    path('emails/', include('emails.urls')),

    # Inquiries
    path('inquiries/', views.allInquiries, name='allInquiries'),
    path('inquiries/viewInquiry/<int:pk>/', views.viewInquiry, name='viewInquiry'),
    path('inquiries/deleteInquiry/<int:pk>/', views.deleteInquiry, name='deleteInquiry'),

    # Reviews
    path('review-ratings/', views.allReviewRatings, name='allReviewRatings'),
    path('review-ratings/toggleApproval/<int:pk>/', views.toggleApproval, name='toggleApproval'),

    # Manage Variants
    path('colors/', views.allColors, name='allColors'),
    path('sizes/', views.allSizes, name='allSizes'),
    path('colors/addColor/', views.addColor, name='addColor'),
    path('sizes/addSize/', views.addSize, name='addSize'),
    path('colors/editColor/<int:pk>/', views.editColor, name='editColor'),
    path('sizes/editSize/<int:pk>/', views.editSize, name='editSize'),
    path('colors/deleteColor/<int:pk>/', views.deleteColor, name='deleteColor'),
    path('sizes/deleteSize/<int:pk>/', views.deleteSize, name='deleteSize'),

    #Blogs
    path('blogs/', views.allBlogs, name='allBlogs'),
    path('blogs/addBlog/', views.addBlog, name='addBlog'),
    path('blogs/deleteBlog/<int:pk>/', views.deleteBlog, name='deleteBlog'),
    path('blogs/editBlog/<int:pk>/', views.editBlog, name='editBlog'),

    #blogCategories
    path('blogs/categories/', views.allBlogsCategories, name='allBlogsCategories'),
    path('blogs/addcategory/', views.addBlogCategories, name='addBlogCategories'),
    path('blogs/deletecategory/<int:pk>/', views.deleteBlogCategory, name='deleteBlogCategory'),
    path('blogs/editcategory/<int:pk>/', views.editBlogCategory, name='editBlogCategory'),

    #blog_commentspath('review-ratings/', views.allReviewRatings, name='allReviewRatings'),
    path('blogs/comments/', views.allComments, name='allComments'),
    path('blogs/comments/commentApproval/<int:pk>/', views.commentApproval, name='commentApproval'),
    path('blogs/comments/commentReplies/<int:pk>/', views.commentReplies, name='commentReplies'),
    path('blogs/blogEnableToggle/', views.blogEnableToggle, name='blogEnableToggle'),

    # Inquiries
    path('contactInqs/', views.allContacts, name='allContacts'),
    path('contactInqs/viewContact/<int:pk>/', views.viewContact, name='viewContact'),
    path('contactInqs/deleteContact/<int:pk>/', views.deleteContact, name='deleteContact'),

    # Services
    path('allServices/', views.allServices, name='allServices'),
    path('addService/', views.addService, name='addService'),
    path('editService/<int:pk>/', views.editService, name='editService'),
    path('deleteService/<int:pk>/', views.deleteService, name='deleteService'),
    path('serviceEnableToggle/', views.serviceEnableToggle, name='serviceEnableToggle'),

    # Portfolio
    path('allPortfolio/', views.allPortfolio, name='allPortfolio'),
    path('portfolioEnableToggle/', views.portfolioEnableToggle, name='portfolioEnableToggle'),
    path('editPortfolio/<int:pk>/', views.editPortfolio, name='editPortfolio'),
    path('addPortfolio/', views.addPortfolio, name='addPortfolio'),
    path('deletePortfolio/<int:pk>/', views.deletePortfolio, name='deletePortfolio'),
    path('editPortfolio/<int:pk>/editPortfolioGallery/', views.editPortfolioGallery, name='editPortfolioGallery'),
    
    path('customVariants/', views.customVariants, name='customVariants'),
    path('customVariants/addVariant/', views.addVariant, name='addVariant'),
    path('customVariants/editVariant/<int:pk>/', views.editVariant, name='editVariant'),
    path('customVariants/deleteVariant/<int:pk>/', views.deleteVariant, name='deleteVariant'),

    path('customVariants/addVariantValue/', views.addVariantValue, name='addVariantValue'),
    path('customVariants/editVariantValue/<int:pk>/', views.editVariantValue, name='editVariantValue'),
    path('customVariants/deleteVariantValue/<int:pk>/', views.deleteVariantValue, name='deleteVariantValue'),

]
