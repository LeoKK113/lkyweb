from pathlib import Path
import subprocess,imageio_ffmpeg
root=Path(__file__).resolve().parent
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loop','1','-i',str(root/'public/assets/architecture-hero.png'),'-vf',"scale=2400:-1,zoompan=z='1.04+0.025*sin(on/240*3.14159265)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=240:s=1600x900:fps=24",'-frames:v','240','-c:v','libx264','-preset','fast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(root/'public/assets/hero-architecture.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
print('Created 10-second seamless spatial video')
