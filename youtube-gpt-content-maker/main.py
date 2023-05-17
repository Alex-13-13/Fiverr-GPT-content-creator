import os
import time
from slugify import slugify
from playwright.sync_api import Playwright, sync_playwright, expect
import config
from utils.textgenerator import generate_text_list
from utils.videogenerator import VideoGenerator
from upload import SignIn, run
from moviepy.config import change_settings
from dotenv import load_dotenv
import re
change_settings({"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})

if __name__ == "__main__":
    


    
    with sync_playwright() as playwright:
        load_dotenv() 
        mail=os.getenv('MAIL')
        password=os.getenv('PASSWORD')
        SignIn(playwright, mail, password)
    while True:
        #### Need folder to be Unique ID, and JSON to keep history of all created folders of videos
        found=True
        i=1
        while found:
            file_path = f'output/Folder'+str(i)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
                found=False
            else:
                i=i+1

        # Get a requested text from AI
        errors=0
        while True:
            prompt="Motivation"
            print("Creating video...")
            textlist = generate_text_list(prompt)
            division=textlist.split("[m]")
            text=division[0]
            text=text.replace("\"", '')
            title=division[1]
            title=title.replace("\"", '')
            desc=division[2]
            desc=desc.replace("\"", '')
            tags=division[3]
            tags=tags.replace("\"", '')
            file_name = 'video.mp4'
            textoclip=re.split(r'[^\w\s\'\"!]', text)
            wordsperpart=[]
            for texto in textoclip:
                numberwlist=texto.split()
                numberofwords=len(numberwlist)
                wordsperpart.append(numberofwords)
            durationperpart=[]
            for numberwords in wordsperpart:
                y=numberwords-1
                n=1+y*0.5
                durationperpart.append(n)
            d=0
            for durations in durationperpart:
                d=d+durations
            with open(file_path+'/title.txt', 'w') as f:
                f.write(title)
            with open(file_path+'/description.txt', 'w') as f:
                f.write(desc)
            with open(file_path+'/tags.txt', 'w') as f:
                f.write(tags)
            vg = VideoGenerator(
                video_folder=config.VIDEO,
                music_folder=config.MUSIC,
                duration=d,
                size=config.SIZE
            )
            try:
                video = vg.generate_video(textoclip,durationperpart)
                errors=0
            except OSError:
                errors=errors+1
                if errors==3:
                    print("Error, wait 60 seconds")
                    time.sleep(60)
                continue
            video.write_videofile(f'{file_path}/{file_name}', fps=config.FPS, preset="ultrafast", threads=4)

            #Amount of minutes the program waits to create and upload another video once the first one is uploaded
            minutes=0
            print("Uploading video...")
            with sync_playwright() as playwright:
                run(playwright, f'{file_path}/{file_name}', title, desc, tags,minutes)
            break
