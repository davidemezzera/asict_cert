# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta
from django.http import Http404, JsonResponse, HttpResponse
from django.utils.timezone import UTC
from certificates.models import *
from django.core import serializers



def heartbeat(request):  # pylint: disable=unused-argument
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    risposta = {
        "alive_at": now
    }

    return JsonResponse(risposta)


def certs_download(request, date_certs):  

    risposta = []
    
  
    generated_certificates = GeneratedCertificate.eligible_certificates.filter(
            created_date__gte='2017-10-29T13:16:18Z',
            status=CertificateStatuses.downloadable
        )

    risultato=[]
    #for cert in generated_certificates:
     #   risultato.append([cert.name, cert.created_date])

 

    #return JsonResponse(risultato, safe=False)
    data=serializers.serialize('json', generated_certificates)
    return HttpResponse(data, content_type="application/json")


