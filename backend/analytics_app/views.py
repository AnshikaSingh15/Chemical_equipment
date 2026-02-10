from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .models import UploadHistory
import pandas as pd


class UploadCSV(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "No file uploaded"},
                status=status.HTTP_200_OK
            )

        try:
            df = pd.read_csv(file)
        except Exception as e:
            return Response(
                {"error": f"Invalid CSV file: {str(e)}"},
                status=status.HTTP_200_OK
            )

        # Normalize column names
        df.columns = df.columns.str.strip().str.lower()

        required_columns = {"flowrate", "pressure", "temperature", "type"}
        if not required_columns.issubset(df.columns):
            return Response(
                {
                    "error": "CSV must contain columns: Flowrate, Pressure, Temperature, Type"
                },
                status=status.HTTP_200_OK
            )

        # Calculations
        total_count = len(df)
        avg_flowrate = float(df["flowrate"].mean())
        avg_pressure = float(df["pressure"].mean())
        avg_temperature = float(df["temperature"].mean())
        type_distribution = df["type"].value_counts().to_dict()

        # Save upload
        UploadHistory.objects.create(
            dataset_name=file.name,
            total_count=total_count,
            avg_flowrate=avg_flowrate,
            avg_pressure=avg_pressure,
            avg_temperature=avg_temperature,
            type_distribution=type_distribution
        )

        # Keep only last 5 uploads
        excess = UploadHistory.objects.count() - 5
        if excess > 0:
            old_ids = (
                UploadHistory.objects
                .order_by("uploaded_at")
                .values_list("id", flat=True)[:excess]
            )
            UploadHistory.objects.filter(id__in=old_ids).delete()

        return Response(
            {
                "dataset_name": file.name,
                "total_count": total_count,
                "avg_flowrate": avg_flowrate,
                "avg_pressure": avg_pressure,
                "avg_temperature": avg_temperature,
                "type_distribution": type_distribution
            },
            status=status.HTTP_200_OK
        )


class LatestSummary(APIView):
    def get(self, request):
        latest = UploadHistory.objects.order_by("-uploaded_at").first()

        if not latest:
            return Response(
                {"message": "No data available"},
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "dataset_name": latest.dataset_name,
                "total_count": latest.total_count,
                "avg_flowrate": latest.avg_flowrate,
                "avg_pressure": latest.avg_pressure,
                "avg_temperature": latest.avg_temperature,
                "type_distribution": latest.type_distribution
            },
            status=status.HTTP_200_OK
        )


class UploadHistoryList(APIView):
    def get(self, request):
        history = UploadHistory.objects.order_by("-uploaded_at")[:5]

        data = []
        for h in history:
            data.append({
                "dataset_name": h.dataset_name,
                "uploaded_at": h.uploaded_at,
                "total_count": h.total_count,
                "avg_flowrate": h.avg_flowrate,
                "avg_pressure": h.avg_pressure,
                "avg_temperature": h.avg_temperature,
                "type_distribution": h.type_distribution,
            })

        return Response(data, status=status.HTTP_200_OK)
