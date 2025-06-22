import os, uuid
from django.conf import settings
from django.shortcuts import render
from .forms import UploadImageForm
import subprocess

def upscale_image(input_path, output_path):
    subprocess.run([
        'realesrgan-ncnn-vulkan.exe',
        '-i', input_path,
        '-o', output_path,
        '-n', 'realesrgan-x4plus'
    ], check=True)

def index(request):
    original_url = upscaled_url = None

    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data['image']
            filename = f"{uuid.uuid4()}.png"
            input_path = os.path.join(settings.MEDIA_ROOT, filename)
            output_filename = f"upscaled_{filename}"
            output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

            with open(input_path, 'wb+') as f:
                for chunk in img.chunks():
                    f.write(chunk)

            upscale_image(input_path, output_path)

            original_url = settings.MEDIA_URL + filename
            upscaled_url = settings.MEDIA_URL + output_filename
    else:
        form = UploadImageForm()

    return render(request, 'upscale_app/index.html', {
        'form': form,
        'original': original_url,
        'upscaled': upscaled_url
    })
