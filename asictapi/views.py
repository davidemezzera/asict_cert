# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from django.http import JsonResponse
from django.db import connection
from rest_framework.exceptions import PermissionDenied
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from provider.oauth2 import models

from lms.djangoapps.courseware.courses import get_courses
from lms.djangoapps.course_api.api import course_detail, list_courses
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from opaque_keys.edx.keys import CourseKey




class HeartRESTView(APIView):

    def get(self, request, *args, **kw):

        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        risposta = {
            "alive_at": now
        }

        response = Response(risposta, status=status.HTTP_200_OK)
        return response

class HistoricalCertsRESTView(APIView):

    def get(self, request, start_date, end_date):

        #Check: There is a Token?
        if request.META.get('HTTP_AUTHORIZATION'):
            tkn=request.META.get('HTTP_AUTHORIZATION').replace("Bearer ", "")
            token=models.AccessToken.objects.get(token=tkn)
            user=token.user

        #USER --> Cookie
        else:
            user=request.user

        #Permission Check: only superUser
        if not user.is_superuser:
            raise PermissionDenied() 

        #Query To DB
        with connection.cursor() as cursor:
            cursor.execute(
                
                "SELECT SUBSTRING(uid,14) AS CODICE_PERSONA, AP.name AS NAME, course_id, CG.created_date AS DATA_CERTIFICATO \
                from certificates_generatedcertificate CG \
                JOIN auth_user A ON A.id = CG.user_id \
                LEFT JOIN auth_userprofile AP ON A.id = AP.user_id \
                LEFT JOIN social_auth_usersocialauth SAU ON A.id = SAU.user_id \
                WHERE CG.status = 'downloadable' AND SUBSTRING(uid,14) IS NOT NULL \
                AND provider != 'ecoopenid-auth' \
                AND CONVERT(CG.created_date, datetime) >= CONVERT(%s, datetime) \
                AND CONVERT(CG.created_date, datetime) <= CONVERT(%s, datetime)", 
                (start_date, end_date))

            result = cursor.fetchall()

        return Response(result)

class LastCertsRESTView(APIView):
    

    def get(self, request):
        yesterday = (date.today() - timedelta(1)).strftime("%Y-%m-%d")
        today = date.today().strftime("%Y-%m-%d")

        historicalCertsRESTView=HistoricalCertsRESTView8()

        return historicalCertsRESTView.get(request, yesterday, today)    


class CourseListRESTView(APIView):

    def get(self, request):
        
        courseOverviewList=CourseOverview.objects.all()

        risultato=[];
        for corso in courseOverviewList:
            #logging.warning(corso)
            risultato.append([corso.clean_id(), corso.display_name, corso.url_name, corso.number, corso.display_number_with_default])


        logging.warning(risultato)

        return Response(risultato)



