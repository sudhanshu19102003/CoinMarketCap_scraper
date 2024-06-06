from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import start_scraping
from celery.result import AsyncResult

class StartScrapingView(APIView):
    def post(self, request):
        coin_list = request.data
        # Validate the payload is a list
        if not isinstance(coin_list, list):
            return Response({"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Start the scraping task
        job = start_scraping.apply_async(args=[coin_list])
        # Return the job ID
        return Response({"job_id": job.id}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        job = AsyncResult(job_id)
        if job.state == 'PENDING':
            return Response({"status": "Pending", "job_id": job_id}, status=status.HTTP_200_OK)
        elif job.state != 'FAILURE':
            result = job.result or {}
            return Response({"status": job.state, "data": result, "job_id": job_id}, status=status.HTTP_200_OK)
        else:
            # Something went wrong in the background job
            return Response({"status": "Failed", "job_id": job_id}, status=status.HTTP_400_BAD_REQUEST)
