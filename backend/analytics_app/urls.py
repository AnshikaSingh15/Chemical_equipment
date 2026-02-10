from django.urls import path
from .views import (
    UploadCSV,
    LatestSummary,
    UploadHistoryList,
)

urlpatterns = [
    # Upload CSV
    path("upload/", UploadCSV.as_view(), name="upload_csv"),

    # Latest uploaded dataset summary
    path("latest-summary/", LatestSummary.as_view(), name="latest_summary"),

    # Last 5 uploads history
    path("history/", UploadHistoryList.as_view(), name="upload_history"),
]
