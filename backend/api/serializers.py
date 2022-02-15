from django.contrib.auth.models import  User
from rest_framework import  serializers

class  UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin']

    # you can create serializer method fields that return back custom attributes

    def get_id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        # passing into built in django field first_name
        name = obj.first_name
        if name == '':
            name = obj.email
        return name