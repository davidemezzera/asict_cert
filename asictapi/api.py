from rest_framework.exceptions import PermissionDenied
import logging

from provider.oauth2 import models
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview


def permission_check(request):

		#Check: There is a Token?
        if request.META.get('HTTP_AUTHORIZATION'):
            tkn=request.META.get('HTTP_AUTHORIZATION').replace("Bearer ", "")
            token=models.AccessToken.objects.get(token=tkn)
            user=token.user

        #USER --> Cookie
        else:
            user=request.user

        #Permission Check: only superUser
        if user.is_superuser:
        	return True
        else:
            raise PermissionDenied()


