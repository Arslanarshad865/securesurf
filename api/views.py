from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import URLSerializer, ResultSerializer
from .utils import analyze_url

class URLAnalyzerView(APIView):
    def post(self, request):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            result = analyze_url(url)
            result_serializer = ResultSerializer(data=result)
            if result_serializer.is_valid():
                return Response(result_serializer.data)
        return Response(serializer.errors, status=400)