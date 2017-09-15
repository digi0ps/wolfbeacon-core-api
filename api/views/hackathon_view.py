from api.models.hackathon_member_model import Hackathon
from api.models.hackathon_member_model import Member
from api.serializers.hackathon_serializer import HackathonSerializer
from api.serializers.member_serializer import MemberSerializer
from api.services import hackathon_service
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404


# POST Hackathon

class HackathonListAndCreate(generics.ListCreateAPIView):
    """
    List All Hackathon, Create a new Hackathon

    Optional Parameters: featured=true
    """

    def get_queryset(self):
        queryset = Hackathon.objects.all()

        # Featured Hackathons
        featured = self.request.query_params.get('featured', None)
        if featured == 'true':
            queryset = hackathon_service.filter_featured_hackathons()

        return queryset

    serializer_class = HackathonSerializer


class HackathonRUD(generics.RetrieveUpdateDestroyAPIView):
    """
    List a Hackathon, Update a Hackathon, Delete a Hackathon
    """
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer


class MemberListAndCreate(APIView):
    """
    List all Hackathon Members, Add a new Member to a Hackathon
    """

    def get(self, request, *args, **kwargs):
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Get hackathon key from request
        hackathon_id = self.kwargs['pk']

        # Append Hackathon Id to data
        data = request.data
        data['hackathon'] = hackathon_id

        # Create Membership
        serialized_member = MemberSerializer(data=data)
        if serialized_member.is_valid():
            serialized_member.save()

            return Response(serialized_member.data, status=status.HTTP_201_CREATED)

        return Response(serialized_member.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberRUD(APIView):
    """
    List details for a Hackathon Member, Update a Hackathon Member, Delete a Hackathon Member
    """

    def get_object(self, hackathon_id, user_id):
        try:
            return Member.objects.get(hackathon=hackathon_id, member=user_id)

        except Member.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        # Get Member
        hackathon_id = self.kwargs['pk']
        user_id = self.kwargs['fk']
        member = self.get_object(hackathon_id, user_id)

        serializer = MemberSerializer(member)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        # Get Member
        hackathon_id = self.kwargs['pk']
        user_id = self.kwargs['fk']
        member = self.get_object(hackathon_id, user_id)

        # Add hackathon and member details to data
        data = request.data
        data['hackathon'] = hackathon_id
        data['member'] = user_id

        serializer = MemberSerializer(member, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Get Member
        hackathon_id = self.kwargs['pk']
        user_id = self.kwargs['fk']
        member = self.get_object(hackathon_id, user_id)

        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
