# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from django.http import JsonResponse
from django.db import connection
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
import logging
from rest_framework import generics
from rest_framework import serializers
from openedx.core.lib.api.view_utils import DeveloperErrorViewMixin, view_auth_classes
from rest_framework.response import Response


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.models import Token
from provider.oauth2 import models



class HeartRESTView(APIView):

    def get(self, request, *args, **kw):

        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        risposta = {
            "alive_at": now
        }

        response = Response(risposta, status=status.HTTP_200_OK)
        return response

class CertsRESTView(APIView):

    def get(self, request, start_date, end_date):

        logging.warning(request.user.get_username()) 
        logging.warning(request.user.is_superuser)

        tkn=request.META.get('HTTP_AUTHORIZATION')
        tkn1=request.META.get('HTTP_USER_AGENT')
        tkn2=request.META.get('HTTP_ACCEPT')
        tkn3=request.META.get('HTTP_ACCEPT_ENCODING')
        #token=models.AccessToken.objects.get(token=tkn)
        logging.warning(tkn) 
        logging.warning(tkn1) 

        logging.warning(tkn2) 
        logging.warning(tkn3) 

        logging.warning(type(tkn))


        if not request.user.is_superuser:
            raise PermissionDenied() 

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






"""

def heartbeat(request):  # pylint: disable=unused-argument
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    risposta = {
        "alive_at": now
    }

    return JsonResponse(risposta)



def certs_download(request, start_date, end_date):  
    

    if not request.user.is_superuser:
        raise PermissionDenied() 

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

    return JsonResponse(result, safe=False)



def certs_download_yesterday(request):  

    yesterday = (date.today() - timedelta(1)).strftime("%Y-%m-%d")
    today = date.today().strftime("%Y-%m-%d")
    logging.warning(request.user.get_username()) 
    logging.warning(request.user.is_superuser)
    logging.warning(request.META.get('REMOTE_USER'))
  

    return certs_download(request, yesterday, today)    """


