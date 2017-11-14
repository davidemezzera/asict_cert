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
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from .api import permission_check


class HeartRESTView(APIView):

    def get(self, request, *args, **kw):

        permission_check(request)
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        risposta = {
            "alive_at": now
        }

        response = Response(risposta, status=status.HTTP_200_OK)
        return response


class HistoricalCertsRESTView(APIView):

    def get(self, request, start_date, end_date):

        permission_check(request)

        #Query To DB
        with connection.cursor() as cursor:
            
            try:
                cursor.execute(
                "SELECT SUBSTRING(uid,14) AS CODICE_PERSONA, AP.name AS NAME, course_id, CG.created_date AS DATA_CERTIFICATO, CG.id \
                from certificates_generatedcertificate CG \
                JOIN auth_user A ON A.id = CG.user_id \
                LEFT JOIN auth_userprofile AP ON A.id = AP.user_id \
                LEFT JOIN social_auth_usersocialauth SAU ON A.id = SAU.user_id \
                WHERE CG.status = 'downloadable' AND SUBSTRING(uid,14) IS NOT NULL \
                AND provider != 'ecoopenid-auth' \
                AND CONVERT(CG.created_date, datetime) >= CONVERT(%s, datetime) \
                AND CONVERT(CG.created_date, datetime) <= CONVERT(%s, datetime)", 
                (start_date, end_date))
            
            except MySQLdb.Error, e:
                return Response("MySQL Error: %s" % str(e))

            query_result = cursor.fetchall()
            result=[]

            [result.append({"id":row[4], "codice_persona":row[0], "nome_cognome":row[1], "identificativo_univoco_corso":row[2], "data_certificato":row[3]}) for row in query_result]

        return Response(result)


class LastCertsRESTView(APIView):
    
    def get(self, request):
        yesterday = (date.today() - timedelta(1)).strftime("%Y-%m-%d")
        today = date.today().strftime("%Y-%m-%d")

        historicalCertsRESTView=HistoricalCertsRESTView()

        return historicalCertsRESTView.get(request, yesterday, today)    


class CourseListRESTView(APIView):

    def get(self, request):
        
        permission_check(request)

        courseOverviewList=CourseOverview.objects.all()

        result=[];
        for corso in courseOverviewList:
            values=unicode(corso.id).split("+")
            if len(values)>1: #delete old courses: e.g. edX/Open_DemoX/edx_demo_course
                result.append({"identificativo_univoco_corso":unicode(corso.id), "codice_corso": values[-2], "codice_edizione":values[-1], "titolo_corso":corso.display_name, "descrizione_corso":corso.short_description, "inizio":corso.start, "fine":corso.end})

        return Response(result)



