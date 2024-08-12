# messaging_app/views.py

from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from messaging.models import Message 

@csrf_exempt
def sync_messages(request):
    if request.method == 'POST':
        # Assume the request contains a JSON array of messages
        messages = json.loads(request.body)
        for message_data in messages:
            # Process each message
            Message.objects.create(**message_data)
        return JsonResponse({"status": "success"})
