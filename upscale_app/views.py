import os
import uuid
from django.conf import settings
from django.shortcuts import render
from .forms import UploadImageForm
import subprocess

def upscale_image(input_path, output_path):
    try:
        # Get the absolute path to the executable
        executable_path = os.path.join(settings.BASE_DIR, 'realesrgan-ncnn-vulkan.exe')
        
        # Verify the executable exists
        if not os.path.exists(executable_path):
            raise FileNotFoundError(f"Real-ESRGAN executable not found at {executable_path}")
            
        # Verify input file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input image not found at {input_path}")
            
        result = subprocess.run([
            executable_path,
            '-i', input_path,
            '-o', output_path,
            '-n', 'realesrgan-x4plus'
        ], check=True, capture_output=True, text=True)
        
        print("Upscaling output:", result.stdout)
        if result.stderr:
            print("Upscaling errors:", result.stderr)
            
        return os.path.exists(output_path)  # Return True if output file was created
        
    except subprocess.CalledProcessError as e:
        print(f"Upscaling failed with error: {e}")
        print("Command output:", e.stdout)
        print("Command error:", e.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error during upscaling: {e}")
        return False

def index(request):
    upscaled_url = original_url = None
    error = None

    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['image']
            
            # Ensure media directory exists
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            
            # Generate unique filenames
            ext = os.path.splitext(uploaded_file.name)[1]
            filename = f"{uuid.uuid4()}{ext}"
            input_path = os.path.join(settings.MEDIA_ROOT, filename)
            output_filename = f"upscaled_{filename}"
            output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

            # Save the uploaded image
            with open(input_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Verify the file was saved
            if not os.path.exists(input_path):
                error = "Failed to save uploaded image."
            else:
                # Upscale the image
                if upscale_image(input_path, output_path):
                    original_url = settings.MEDIA_URL + filename
                    upscaled_url = settings.MEDIA_URL + output_filename
                else:
                    error = "Failed to upscale the image. Please check the console for errors."
                    
                    # Clean up files if upscaling failed
                    if os.path.exists(input_path):
                        os.remove(input_path)
                    if os.path.exists(output_path):
                        os.remove(output_path)
    else:
        form = UploadImageForm()

    return render(request, 'upscale_app/index.html', {
        'form': form,
        'original': original_url,
        'upscaled': upscaled_url,
        'error': error
    })