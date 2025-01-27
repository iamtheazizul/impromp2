import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from typing import List
from punctuators.models import PunctCapSegModelONNX
from moviepy.video.io import VideoFileClip
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import VideoForm
from .models import Video, VideoAnalysis
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from openai import OpenAI
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from langchain_dartmouth.llms import ChatDartmouth

def homepage(request):
    return render(request, "mainpage/landing.html")


def webcam_page(request):
    # This view simply renders the template with the webcam recording functionality.
    return render(request, 'mainpage/webcam_page.html')


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            # Redirect to the view_video URL with the video's ID
            return redirect(reverse('show_video', kwargs={'video_id': video.id}))
    else:
        form = VideoForm()
    return render(request, 'mainpage/main_page.html', {'form': form})

# Change the function below to work with the video that we upload above.

# Assume VideoForm is imported correctly
# Assume you have functions convert_video_to_audio(video) and transcribe_audio(audio)


def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()


def audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

def openAI_puntuator(text):
    print("Finding punctuations")
    client = ChatDartmouth(model_name="llama-3-8b-instruct")
    
    # Compose the user prompt
    user_prompt = f"You are an amazing text editor. Add punctuation and capitalization to the following text: {text}"
    print("You are amazing")
    # Call the model to generate a response
    response = client.invoke(user_prompt)
    print("You surely are amazing!")

    
    # Extract the punctuated text from the response
    punctuated_text = response.content
    return punctuated_text


def show_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'mainpage/show_video.html', {'video': video})


def view_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video_path = video.video.path
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    extract_audio(video_path, audio_path)
    text = audio_to_text(audio_path)
    # Punctuate and capitalize the transcribed text
    punctuated_text = openAI_puntuator(text)

    return JsonResponse({'transcription': punctuated_text})

def analyze_transcription(request, video_id):
    print("Analyzing transcription")
    # Ensure the request is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        video = get_object_or_404(Video, id=video_id)
        # Use the submitted transcription text
        text = request.POST.get('transcription_text', '')
        print("I'm here!")
        
        # Initialize the ChatDartmouth client
        client = ChatDartmouth(model_name="llama-3-8b-instruct")  # Specify your model here
        print("I'm here too!")

        # Compose the user prompt for analysis
        user_prompt = (
            "You are an analytical assistant designed to provide brief, actionable feedback on public speeches. "
            "Analyze the transcript for clarity, filler word usage, and effectiveness. "
            "Provide feedback in less than 10 bullet points, highlighting specific sentences for clarity issues, "
            "counting filler words, and calculating the filler word ratio. Directly reference the transcript for examples. "
            "Keep it less than 10 sentences: " + text
        )
        
        # Call the model to generate an analysis
        analysis_response = client.invoke(user_prompt)
        print("I'm here three!")
        
        # Get the analysis result from the response
        analysis_result = analysis_response.content
        
        print("I'm here four!")
        # Return the analysis result as JSON
        return JsonResponse({
            'video_id': video_id,
            'analysis_result': analysis_result
        })
    
    # If not an AJAX request, return an error
    return HttpResponseBadRequest("Invalid request")

# To show the data of analysis for the video.


def view_analysis_results(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    # Get all analyses for this video, newest first
    analyses = video.analyses.all().order_by('-created_at')

    return render(request, 'mainpage/view_analysis_results.html', {
        'video': video,
        'analyses': analyses
    })