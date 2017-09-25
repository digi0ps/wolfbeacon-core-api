from rest_framework import serializers
from api.models.hackathon_member_model import Hackathon


class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = ('hackathon_id', 'cms_id', 'data', 'is_published')
