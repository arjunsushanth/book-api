from django.contrib import admin
from django.urls import path
from book import views
from  rest_framework.routers import  DefaultRouter
router=DefaultRouter()
router.register('api/book',views.Bookviewset,basename='books')
router.register('user',views.Userview,basename='user')
router.register('carts',views.CartView,basename='carts')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookview/',views.Bookview.as_view()),
    path('bookview/<int:id>',views.Bookdetails.as_view()),
    path('reviews/<int:pk>', views.ReviewDeleteView.as_view()),

]+router.urls
