from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from api.models import Pass
from api.serializers import PassSerializer

# POST Hacker Pass
"""
@apiVersion 1.0.0
@api {post} /passes/ 1. Create Hacker Pass
@apiName CreateHackerPass
@apiGroup HackerPasses

@apiParam {Number} hacker ID of Hacker for whom hacker pass is to be generated

@apiSuccessExample {json} Success Response Code(HTTP/1.1 201 Created):
{"id":2,"qr_code":"https://wolfbeacon-static-assets.s3.amazonaws.com/qr_codes/qr_code1_1.jpg?AWSAccessKeyId=access_key&Expires=1670943221&Signature=signature_key","hacker":1}

"""

# List Hacker Passes
"""
@apiVersion 1.0.0
@api {get} /passes/ 2. List Hacker Passes
@apiName ListHackerPasses
@apiGroup HackerPasses
@apiDescription Additional search parameters can be <br><br> <i>hacker</i>, <i>id</i> <br><br>

@apiParamExample Sample Request 
https://api.wolfbeacon.com/passes?hacker=1

@apiSuccessExample {json} Success Response Code (HTTP/1.1 200 OK):
[{"id":2,"qr_code":"https://wolfbeacon-static-assets.s3.amazonaws.com/qr_codes/qr_code1_1.jpg?AWSAccessKeyId=access_key&Expires=1670943221&Signature=signature_key","hacker":1}]
"""

# DELETE Hacker Pass
"""
@apiVersion 1.0.0
@api {delete} /passes/:pass-id/ 3. Delete Hacker Pass
@apiName DeleteHackerPass
@apiGroup HackerPasses
@apiSuccessExample {json} Success Response Code:
HTTP/1.1 204 NO CONTENT
"""


class PassViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer

    filter_fields = (
        'id', 'hacker',
    )
