from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import requests
import json

from api.models import *
from api.utils import *
from lib.need import *
from backend.settings import *
import local

class HelloWord(APIView):
	def get(self, request):
		return Response(True, status=status.HTTP_200_OK)


class OngAPI(APIView):
	def post(self, request):
		cnpj        = request.POST.get('cnpj')
		cep         = request.POST.get('cep')
		cause       = request.POST.get('cause')

		if not all([cnpj, cep]):
			return Response({'success': False, 'detail':'Parâmetros insuficientes'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			int(cep)
			int(cnpj)
		except:
			return Response({'success': False, 'detail':'Parâmetros incorretos'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			ong = Ong.objects.get(cnpj=cnpj)
		except: 
			ong = None

		if ong != None:
			return Response({'success': False, 'detail':'Ong já cadastrada'}, status=status.HTTP_400_BAD_REQUEST)
			
		try:
			tags = insertTag(cause)
		except:
			tags = False
		
		serializer = OngModelSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()

			response = {'success': True, 'ong': serializer.data}

			return Response(response, status=status.HTTP_201_CREATED)
		
		return Response({'success': False, 'detail':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request, id=None):
		if id == None:
			return Response({'success': False, 'detail':'Parâmetros insuficientes'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			ong = Ong.objects.get(id=id)
		except:
			return Response({'success': False, 'detail':'Id ong não encontrada'}, status=status.HTTP_404_NOT_FOUND)

		serializer = OngModelSerializer(ong)

		products = NeedProduct.objects.filter(ong=ong)
		bills = NeedBill.objects.filter(ong=ong)
		
		response = {'success': True, 'ong': serializer.data}
		response['ong'].update({'need_products': products, 'need_bills': bills})

		return Response(response)


class OngAPIList(APIView):
	def get(self, request):
		search = request.GET.get('search')

		if search:
			try:
				ong = Ong.objects.filter(
					Q(name__icontains=search) | Q(Q(state__icontains=search) | Q(city__icontains=search) | Q(address__icontains=search)) | Q(cause__icontains=search)
				)
			except Exception as e:
				return Response({'success': False, 'detail':'Ongs não encontradas', 'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

		else:
			try:
				ong = Ong.objects.all()
			except:
				return Response({'success': False, 'detail':'Ongs não encontradas'}, status=status.HTTP_404_NOT_FOUND)

		serializer = OngModelSerializer(ong, many=True)
		ongs = []
		ongs.extend(serializer.data)

		for ong in ongs:
			tags = []

			products = NeedProduct.objects.filter(ong=ong.get('id'))
			bills = NeedBill.objects.filter(ong=ong.get('id'))
			
			if products:
				tags += products__tags__name
			if bills:
				tags += bills__tags__name
		
			ong['need_products']    = products
			ong['need_bills']       = bills
			ong['tags']             = tags

		response = {'success': True, 'ongs': ongs}

		return Response(response)


class NeedProductAPI(APIView):
	def post(self, request):
		product = request.POST.get('product', None)
		
		if product == None:
			return Response({'success': False, 'detail':'Parâmetros insuficientes'}, status=status.HTTP_400_BAD_REQUEST)

		product = json.loads(product)

		id_product = insertProducts(product.get('name'), product.get('value'), product.get('image'), product.get('url'))

		if not id_product:
			return Response({'success': False, 'detail':'Parâmetros incorretos'}, status=status.HTTP_400_BAD_REQUEST)

		request.data['product'].update(id_product)

		serializer = NeedProductModelSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()

			response = {'success': True, 'need': serializer.data}

			return Response(response, status=status.HTTP_201_CREATED)
		
		return Response({'success': False, 'detail':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


	def get(self, request, id=None):
		if id == None:
			return Response({'success': False, 'detail':'Parâmetros insuficientes'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			need = NeedProduct.objects.get(id=id)
		except:
			return Response({'success': False, 'detail':'Id necessidade não encontrado'}, status=status.HTTP_404_NOT_FOUND)

		serializer = NeedProductModelSerializer(need)

		response = {'success': True, 'need': serializer.data}

		return Response(response)


class NeedBillAPI(APIView):
	def post(self, request):
		pass

	def get(self, request, id=None):
		if id == None:
			return Response({'success': False, 'detail':'Parâmetros insuficientes'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			need = NeedBill.objects.get(id=id)
		except:
			return Response({'success': False, 'detail':'Id necessidade não encontrado'}, status=status.HTTP_404_NOT_FOUND)

		serializer = NeedBillModelSerializer(need)

		response = {'success': True, 'need': serializer.data}

		return Response(response)


class TagAPI(APIView):
	def post(self, request):
		name = request.POST.get('name')

		if not name:
			return Response({'success': False, 'detail':'Parâmetros insuficientes'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			tag = Tag.objects.get(name=name)
		except: 
			tag = None

		if tag != None:
			return Response({'success': False, 'detail':'Tag já cadastrada'}, status=status.HTTP_400_BAD_REQUEST)
		
		serializer = TagModelSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()

			response = {'success': True, 'tag': serializer.data}

			return Response(response, status=status.HTTP_201_CREATED)
		
		return Response({'success': False, 'detail':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request):
		try:
			tags = Tag.objects.all()
		except:
			return Response({'success': False, 'detail':'Erro ao buscar tags'}, status=status.HTTP_404_NOT_FOUND)

		serializer = TagModelSerializer(tags, many=True)

		response = {'success': True, 'tags': serializer.data}

		return Response(response)


class TagNeedProductAPI(APIView):
	def post(self, request):
		name = request.POST.get('name')

		if not name:
			return Response({'success': False, 'detail':'Parâmetros insuficientes'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			tag = Tag.objects.get(name=name)
		except: 
			tag = None

		if tag != None:
			return Response({'success': False, 'detail':'Tag já cadastrada'}, status=status.HTTP_400_BAD_REQUEST)
		
		serializer = TagModelSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()

			response = {'success': True, 'tag': serializer.data}

			return Response(response, status=status.HTTP_201_CREATED)
		
		return Response({'success': False, 'detail':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request):
		try:
			tags = Tag.objects.all()
		except:
			return Response({'success': False, 'detail':'Erro ao buscar tags'}, status=status.HTTP_404_NOT_FOUND)

		serializer = TagModelSerializer(tags, many=True)

		response = {'success': True, 'tags': serializer.data}

		return Response(response)


class GrantorAPI(APIView):
	def post(self, request):
		email = request.POST.get('email')

		try:
			email = Grantor.objects.get(email=email)
		except:
			email = None

		if email != None:
			return Response({'success': False, 'detail':'Doador já cadastrado'}, status=status.HTTP_400_BAD_REQUEST)
		
		serializer = GrantorModelSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()

			response = {'success': True, 'grantor': serializer.data}

			return Response(response, status=status.HTTP_201_CREATED)
		
		return Response({'success': False, 'detail':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request):
		email = request.GET.get('email', None)

		if email == None:
			return Response({'success': False, 'detail':'Parâmetros insuficientes'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			grantor = Grantor.objects.get(email=email)
		except:
			return Response({'success': False, 'detail':'Doador não encontrado'}, status=status.HTTP_404_NOT_FOUND)

		serializer = GrantorModelSerializer(grantor)

		response = {'success': True, 'grantor': serializer.data}

		return Response(response)
