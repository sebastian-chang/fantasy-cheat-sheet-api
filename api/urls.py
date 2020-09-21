from django.urls import path
# from .views.mango_views import Mangos, MangoDetail
from .views.player_views import Players, PlayerDetail
from .views.sheet_views import Sheets, SheetDetail
from .views.player_stat_views import QBStats, QBStatDetails
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    # path('mangos/', Mangos.as_view(), name='mangos'),
    # path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),
    path('players/', Players.as_view(), name='players'),
    path('players/<int:pk>/', PlayerDetail.as_view(), name='pla yer_detail'),
    path('sheets/', Sheets.as_view(), name='sheets'),
    path('sheets/<int:pk>/', SheetDetail.as_view(), name='sheet_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw'),

    # Player views for data from 3rd party API
    path('qb-stat/<int:pk>', QBStatDetails.as_view(), name='qb-stat'),
    path('qb-stat/', QBStats.as_view(), name='qb-stats')
]
