from rest_framework.serializers import ModelSerializer
from api.models import *

class OngModelSerializer(ModelSerializer):
	class Meta:
		model = Ong
		fields = '__all__'

	def create(self, validated_data):
		instance = self.Meta.model(**validated_data)
		instance.save()

		return instance


class TagModelSerializer(ModelSerializer):
	class Meta:
		model = Tag
		fields = '__all__'

	def create(self, validated_data):
		instance = self.Meta.model(**validated_data)
		instance.save()

		return instance


class NeedProductModelSerializer(ModelSerializer):
	class Meta:
		model = NeedProduct
		fields = '__all__'

	def create(self, validated_data):
		instance = self.Meta.model(**validated_data)

		instance.save()

		return instance


class NeedBillModelSerializer(ModelSerializer):
	class Meta:
		model = NeedBill
		fields = '__all__'

	def create(self, validated_data):
		instance = self.Meta.model(**validated_data)
		instance.save()

		return instance


class NeedVoluntaryModelSerializer(ModelSerializer):
	class Meta:
		model = NeedVoluntary
		fields = '__all__'

	def create(self, validated_data):
		instance = self.Meta.model(**validated_data)
		instance.save()

		return instance

class GrantorModelSerializer(ModelSerializer):
	class Meta:
		model = Grantor
		fields = '__all__'

	def create(self, validated_data):
		instance = self.Meta.model(**validated_data)
		instance.save()

		return instance