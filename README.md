# AI image upscaler


**Command:**

Commands for upscale through cmd.

1. ./realesrgan-ncnn-vulkan.exe -i input.jpg -o output.png
2. ./realesrgan-ncnn-vulkan.exe -i input.jpg -o output.png -n realesr-animevideov3
3. ./realesrgan-ncnn-vulkan.exe -i input_folder -o outputfolder -n realesr-animevideov3 -s 2 -f jpg
4. ./realesrgan-ncnn-vulkan.exe -i input_folder -o outputfolder -n realesr-animevideov3 -s 4 -f jpg


**Commands for enhancing anime videos:**

1. Use ffmpeg to extract frames from a video (Remember to create the folder `tmp_frames` ahead)

    ffmpeg -i onepiece_demo.mp4 -qscale:v 1 -qmin 1 -qmax 1 -vsync 0 tmp_frames/frame%08d.jpg

2. Inference with Real-ESRGAN executable file (Remember to create the folder `out_frames` ahead)

    ./realesrgan-ncnn-vulkan.exe -i tmp_frames -o out_frames -n realesr-animevideov3 -s 2 -f jpg

3. Merge the enhanced frames back into a video

    ffmpeg -i out_frames/frame%08d.jpg -i onepiece_demo.mp4 -map 0:v:0 -map 1:a:0 -c:a copy -c:v libx264 -r 23.98 -pix_fmt yuv420p output_w_audio.mp4

**Paste following directly into cmd to see enhanced video.**

"
mkdir tmp_frames, out_frames
ffmpeg -i onepiece_demo.mp4 -qscale:v 1 -qmin 1 -qmax 1 -vsync 0 tmp_frames/frame%08d.jpg
./realesrgan-ncnn-vulkan.exe -i tmp_frames -o out_frames -n realesr-animevideov3 -s 2 -f jpg
ffmpeg -i out_frames/frame%08d.jpg -i onepiece_demo.mp4 -map 0:v:0 -map 1:a:0 -c:a copy -c:v libx264 -r 23.98 -pix_fmt yuv420p output_w_audio.mp4
"

**Once you obtained output, you can delete frames using following command. (It is irreversible)**

"
Remove-Item -Path tmp_frames, out_frames -Recurse -Force
"

This executable file is **portable** and includes all the binaries and models required. No CUDA or PyTorch environment is needed.
