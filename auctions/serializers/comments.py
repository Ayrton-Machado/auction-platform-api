from rest_framework import serializers
from ..models import Comments

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class AddCommentSerializer(serializers.Serializer):
    comment = serializers.CharField(
        max_length=500,
        allow_blank=False,
        required=True,
        trim_whitespace=True
    )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['listing'] = self.context['listing']

        return Comments.objects.create(**validated_data)