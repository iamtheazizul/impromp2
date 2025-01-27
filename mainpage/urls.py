from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("webcam/", views.webcam_page, name="webcam_page"),
    # path('process-video/', views.process_video, name='process_video'),
    path('upload/', views.upload_video, name='upload_video'),
    path('video/<int:video_id>/', views.view_video, name='view_video'),
    path('show_video/<int:video_id>/', views.show_video, name='show_video'),
    path('analyze-transcription/<int:video_id>/',
         views.analyze_transcription, name='analyze_transcription')
]
