"""GroundSegment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, re_path
from django.contrib import admin
from API.views import TlmyRawDataList

from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import SimpleRouter
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from Telemetry.models.TlmyVarType import TlmyVarType
#from aptsources.distinfo import Template
from Telemetry.models.TlmyVarType import TlmyVarType
from Telemetry import urls



import GroundSegment
#from DistUpgrade.DistUpgradeViewGtk3 import view
from django.views.generic import TemplateView
from GroundSegment.settings import MAPBOX_KEY
import Telemetry
#import debug_toolbar


# Text to put at the end of each page's <title>.
admin.site.site_title = 'MDIAE Ground Segment'

# Text to put in each page's <h1>.
admin.site.site_header = 'MDIAE Ground Segment'
  

# Text to put at the top of the admin index page.
admin.site.index_title = 'Control Panel'

router = SimpleRouter()

#router.register(r'TlmyApi', TlmyRawDataList)


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    
    #url('__debug__/', include(debug_toolbar.urls)),
    re_path(r'^API/', include('API.urls')),
    re_path(r'^telemetry/', include('Telemetry.urls')),
    #re_path(r'^admin/statuscheck/', include('celerybeat_status.urls')),
    re_path(r'^TlmyRawData/$', TlmyRawDataList.as_view(), name='TlmyRawData-APIPost'),
    
    
    ]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    
