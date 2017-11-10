from api.models import Hacker
from api.serializers import HackerSerializer

from rest_framework import mixins, generics

# POST Hackers
"""
@apiVersion 1.0.0
@api {post} /hackathons/:hackathon-id/hackers/ 1. Create Hacker 
@apiName CreateHacker
@apiDescription Users are added to Hackathons as Hackers. Every Hackathon has it's own set of Hackers.
@apiGroup Hackers
@apiParam {String} user User ID of Hacker
@apiParam {String} hackathon Hackathon Id Hacker is to attend
@apiParam {String="organiser","volunteer","participant","mentor"} role Role of Hacker in Hackathon
@apiParamExample {json} Request Data Example:
{"user":1,"hackathon":1,"role":"organiser"}
@apiSuccessExample {json} Success Response Code (HTTP/1.1 200 OK):
{"id":1,"hackathon":1,"user":1,"created_at":"2017-11-06T09:46:31.459815Z","updated_at":"2017-11-06T09:46:31.459856Z","role":"organiser"}
"""

# GET All Hackers
"""
@apiVersion 1.0.0
@api {get} /hackathons/:hackathon-id/hackers/ 2. Get Hackers 
@apiName GetAllHackersForHackathon
@apiGroup Hackers
@apiSuccessExample {json} Sample Success Response
[{"id":1,"hackathon":1,"user":1,"created_at":"2017-11-06T09:46:31.459815Z","updated_at":"2017-11-06T09:46:31.459856Z","role":"volunteer"},{"id":2,"hackathon":1,"user":2,"created_at":"2017-11-06T12:42:00.335711Z","updated_at":"2017-11-06T12:42:00.335746Z","role":"organiser"}]
Success Response Code: HTTP/1.1 200 OK
"""


class HackerListAndCreate(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    """
    List All Users, Create a new Event
    """
    serializer_class = HackerSerializer

    # Custom queryset
    def get_queryset(self):
        # Get Hackathon id
        hackathon = self.kwargs['fk']

        # Filter for Hackathon's hackers
        queryset = Hacker.objects.filter(hackathon=hackathon)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Reinsert hackathon key for sanity
        request.data['hackathon'] = self.kwargs['fk']

        return self.create(request, *args, **kwargs)


# GET Hacker
"""
@apiVersion 1.0.0
@api {get} /hackathons/:hackathon-id/hackers/:hacker-id/ 3. Get Hacker
@apiName GetHacker
@apiGroup Hackers
@apiSuccessExample {json} Success Response Code:
HTTP/1.1 200 OK
"""

# PUT Hacker
"""
@apiVersion 1.0.0
@api {put} /hackathons/:hackathon-id/hackers/:hacker-id/ 4. Update Hacker
@apiName UpdateHacker
@apiDescription Supports Partial Update
@apiGroup Hackers
@apiSuccessExample {json} Success Response Code:
HTTP/1.1 200 OK
"""

# PUT Hacker
"""
@apiVersion 1.0.0
@api {patch} /hackathons/:hackathon-id/hackers/:hacker-id/ 5. Partially Update Hacker
@apiName PartiallyUpdateHacker
@apiDescription Supports Partial Update
@apiGroup Hackers
@apiSuccessExample {json} Success Response Code:
HTTP/1.1 200 OK
"""

# DELETE Hacker
"""
@apiVersion 1.0.0
@api {delete} /hackathons/:hackathon-id/hackers/:hacker-id/ 6. Delete Hacker
@apiName DeleteHacker
@apiGroup Hackers
@apiSuccessExample {json} Success Response Code:
HTTP/1.1 204 NO CONTENT
"""


class HackerRUD(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    """
    Get Visitor, Update Visitor, Delete Visitor
    """
    serializer_class = HackerSerializer
    queryset = Hacker.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Re-Insert keys for sanity
        request.data['hackathon'] = self.kwargs['fk']
        request.data['id'] = self.kwargs['pk']

        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Re-Insert keys for sanity
        request.data['hackathon'] = self.kwargs['fk']
        request.data['id'] = self.kwargs['pk']

        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
