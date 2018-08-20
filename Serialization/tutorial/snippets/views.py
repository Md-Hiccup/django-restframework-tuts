from django.shortcuts import render

""" Tut: 1 Serialization """
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser

""" Tut: 2 Request and Responses """
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
# from django.utils.six import BytesIO

# Create your views here.
# @csrf_exempt  # POST from clients that won't have a CSRF token	:	Tut 1
@api_view(['GET','POST'])	#	Tut: 2
def snippet_list(request, format=None):
	"""
  	List all code snippets, or create a new snippet. 
  	"""
	if request.method == 'GET':
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many=True)
		# return JsonResponse(serializer.data, safe=False)		#	Tut: 1
		return Response(serializer.data)
	
	elif request.method == 'POST':
		# data = JSONParser().parse(request)					#	Tut: 1
		data = request.data		# Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
		serializer = SnippetSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			# return JsonResponse(serializer.data, status=201)	#	Tut: 1
		# return JsonResponse(serializer.errors, status=400)	#	Tut: 1


# @csrf_exempt	# POST from clients that won't have a CSRF token	#	Tut: 1
@api_view
def snippet_detail(request, pk, format=None):
	"""
	Retrieve, update or delete a code snippet.
	"""
	try:
		snippet = Snippet.objects.get(pk=pk)
	except Snippet.DoesNotExist:
		# return HttpResponse(status=404)		#	Tut: 1
		return HttpResponse(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = SnippetSerializer(snippet)
		# return JsonResponse(serializer.data)	#	Tut: 1
		return Response(serializer.data)
	
	elif request.method == 'PUT':
		# data = JSONParser().parse(request)	#	Tut: 1
		data = request.data		# Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
		serializer = SnippetSerializer(snippet, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			# return JsonResponse(serializer.data)
		# return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
		# return HttpResponse(status=204)
