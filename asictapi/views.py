# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta
from django.http import Http404, JsonResponse
from django.utils.timezone import UTC
from certificates.models import *
from django.db import connection



def heartbeat(request):  # pylint: disable=unused-argument
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    risposta = {
        "alive_at": now
    }

    return JsonResponse(risposta)


def certs_download(request, start_date, end_date):  
 
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT SUBSTRING(uid,14) as CODICE_PERSONA, AP.name as NAME, course_id,CG.created_date as DATA_CERTIFICATO from certificates_generatedcertificate CG JOIN auth_user A on A.id=CG.user_id LEFT JOIN auth_userprofile AP on A.id=AP.user_id LEFT JOIN social_auth_usersocialauth SAU on A.id=SAU.user_id where CG.status = 'downloadable' and SUBSTRING(uid,14) IS NOT NULL and provider != 'ecoopenid-auth' AND CONVERT(CG.created_date, datetime) >= CONVERT(%s, datetime) AND CONVERT(CG.created_date, datetime) <= CONVERT(%s, datetime)", 
            [start_date, end_date])
        result = cursor.fetchall()

    return JsonResponse(result, safe=False)

