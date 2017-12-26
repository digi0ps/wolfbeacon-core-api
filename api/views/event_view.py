from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.models import Event, Hacker
from api.serializers import EventSerializer
from api.utils import validators

# POST Events
"""
@apiVersion 1.0.0
@api {post} /hackathons/:hackathon-id/events/ 1. Create Event 
@apiName CreateEvent
@apiDescription Events are a part of Hackathons
@apiGroup Events

@apiParam {Integer} hackathon ID of Hackathon this Event is a part of
@apiParam {String="mini-mlh-event","general-workshop","company-workshop","speaker-session", "fireside-chats", "open-source-event", "activity"} type Type of Event
@apiParam {String{50 chars}} name Name of Event
@apiParam {String{150 chars}} tagline Tagline for Event
@apiParam {String{350 chars}} description Description of Event
@apiParam {json} speaker_details Speaker Details
@apiParam {String{150 chars}} location Location of Event
@apiParam {String} giveaway Event Giveaways

@apiParamExample {json} Request Data Example:
{"hackathon":1,"name":"Test Name","type":"general-workshop","tagline":"Test Workshop","description":"Test Description","speaker_details":{},"location":"Building A","giveaway":"Tshirt"}
@apiSuccessExample {json} Success Response Code (HTTP/1.1 200 OK):
{"id":3,"created_at":"2017-11-06T19:41:30.644678Z","updated_at":"2017-11-06T19:41:30.644721Z","hackathon":1,"type":"general-workshop","name":"Test Name","tagline":"Test Workshop","description":"Test Description","speaker_details":{},"location":"Building A","giveaway":"Tshirt","no_of_attendees":0,"rating":0}
"""

# List Events
"""
@apiVersion 1.0.0
@api {get} /hackathons/? 2. List Events 
@apiName ListEvents
@apiGroup Events
@apiParam {Number} hackathon Hackathon ID Event if a part of

@apiDescription Allowed additional filter parameters are <br><br> <i>hackathon, type, name</i> <br><br>

@apiParamExample Sample Request 
https://api.wolfbeacon.com/v1/events?hackathon=1

@apiSuccessExample {json} Sample Success Response
[{"id":3,"created_at":"2017-11-06T19:41:30.644678Z","updated_at":"2017-11-06T19:41:30.644721Z","hackathon":1,"type":"general-workshop","name":"Test Name","tagline":"Test Workshop","description":"Test Description","speaker_details":{},"location":"Building A","giveaway":"Tshirt","no_of_attendees":0,"rating":0},{"id":2,"created_at":"2017-11-06T19:41:30.439853Z","updated_at":"2017-11-06T19:41:30.439882Z","hackathon":1,"type":"general-workshop","name":"Test Name","tagline":"Test Workshop","description":"Test Description","speaker_details":{},"location":"Building A","giveaway":"Tshirt","no_of_attendees":0,"rating":0}]Success Response Code: HTTP/1.1 200 OK
"""

# GET Event
"""
@apiVersion 1.0.0
@api {get} /events/:event-id/ 3. Get Event
@apiName GetEvent
@apiGroup Events
@apiSuccessExample {json} Success Response Code:
HTTP/1.1 200 OK
"""

# PUT Event
"""
@apiVersion 1.0.0
@api {put} /events/:event-id/ 4. Replace Event
@apiName ReplaceEvent
@apiGroup Events
@apiSuccessExample {json} Success Response Code:
HTTP/1.1 200 OK
"""

# PATCH Event
"""
@apiVersion 1.0.0
@api {patch} /events/:event-id/ 5. Update Event
@apiName UpdateEvent
@apiDescription Supports Partial Update
@apiGroup Events
@apiSuccessExample {json} Success Response Code:
HTTP/1.1 200 OK
"""

# DELETE Event
"""
@apiVersion 1.0.0
@api {delete} /events/:event-id/ 6. Delete Event
@apiName DeleteEvent
@apiGroup Events
@apiSuccessExample {json} Success Response Code:
HTTP/1.1 204 NO CONTENT
"""


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    filter_fields = (
        'hackathon', 'type', 'name',
    )

    def get_queryset(self):
        queryset = Event.objects.all()

        # Filter for Hackathons
        hackathon = self.request.query_params.get('hackathon', None)
        if hackathon:
            queryset = queryset.filter(hackathon=hackathon)

        return queryset

    def create(self, request, *args, **kwargs):
        # request.data['hackathon'] = self.kwargs['fk']

        return super(EventViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super(EventViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(EventViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # validators.validate_body_url_id([request.data['id']], [self.kwargs['pk']])

        return super(EventViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # validators.validate_body_url_id([request.data['id']], [self.kwargs['pk']])

        return super(EventViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(EventViewSet, self).destroy(request, *args, **kwargs)


# ADD Hacker to Event
"""
@apiVersion 1.0.0
@api {post} /hackathons/:hackathon-id/events/:event-id/hackers/:hacker-id/ 7. Add Hacker to Event
@apiDescription This endpoint simply adds a Hacker attending a Hackathon to an Event of that Hackathon. Since no new Entity is being created, the request body is empty but with an HTTP 201 CREATED status code
@apiName AddHackerToEvent
@apiGroup Events
@apiSuccessExample {json} Success Response Code:
HTTP/1.1 201 CREATED
"""

# DELETE Hacker from Event
"""
@apiVersion 1.0.0
@api {delete} /hackathons/:hackathon-id/events/:event-id/hackers/:hacker-id/ 8. Remove Hacker from Event 
@apiName RemoveHackerFromEvent
@apiGroup Events
@apiSuccessExample {json} Success Response Code:
HTTP/1.1 204 NO CONTENT
"""


class EventHackerAddRemove(APIView):
    """
    List all Event Hackers, Add Hacker to Event
    """

    def post(self, request, *args, **kwargs):

        hackathon_id = self.kwargs['fk2']
        event_id = self.kwargs['fk']
        hacker_id = self.kwargs['pk']

        try:
            event = Event.objects.get(hackathon=hackathon_id, id=event_id)
            hacker = Hacker.objects.get(id=hacker_id)

            event.hackers.add(hacker)

            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):

        hackathon_id = self.kwargs['fk2']
        event_id = self.kwargs['fk']
        hacker_id = self.kwargs['pk']

        try:
            event = Event.objects.get(hackathon=hackathon_id, id=event_id)
            hacker = Hacker.objects.get(id=hacker_id)

            event.hackers.remove(hacker)

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
