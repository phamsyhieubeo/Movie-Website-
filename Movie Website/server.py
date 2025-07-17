from flask import Flask, render_template, send_from_directory
import os
import webbrowser as wb
import socket
#import logging
#logging.basicConfig(level= logging.DEBUG)

def gethost():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host_name = s.getsockname()[0]
    return host_name

app = Flask(__name__, template_folder= "template/")

wb.open(f"http://{gethost()}:5500")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Videos")
def vid():
    Videos_list = []
    for root, dir, files in os.walk("Video\\"):
        for file in files:
            if file.endswith((".mp4", ".mov", ".mkv")):
                Videos_list.append(file)
    print(Videos_list)
    return render_template("VideoPage/Videos.html", videos = Videos_list)

@app.route("/Movies")
def mov():
    Movies_list = []
    for root, dir, files in os.walk("Movie\\"):
        for file in files:
            if file.endswith((".mp4", ".mov", ".mkv")):
                Movies_list.append(file)
    print(Movies_list)
    return render_template("MoviePage/Movies.html", movies = Movies_list)

@app.route("/Series")
def ser():
    Folder_List = []
    Cover_List = []
    with os.scandir("Series\\") as entries:
        for entry in entries:
            if entry.is_dir():
                folder = entry.name
                Folder_List.append(folder)
                
                cover_path = os.path.join("Series", folder, "Cover.jpg")
                if os.path.isfile(cover_path):
                    Cover_List.append(f"/cover/{folder}/Cover.jpg")
                else:
                    Cover_List.append(None)
                    
    return render_template("SeriesPage/Series.html", folders = Folder_List, covers = Cover_List)
    #return f"{Folder_List}"
    
@app.route("/cover/<folder>/<filename>")
def serve_cover(folder, filename):
    return send_from_directory(os.path.join("Series", folder), filename)


@app.route("/Series/<folder>")
def series(folder):
    sub_folder = []
    with os.scandir(f"Series\\{folder}") as entries:
        for entry in entries:   
            if entry.is_dir():
                sub_folder.append(entry.name)
    return render_template("SeriesPage/Part.html", sub_folders = sub_folder , name = folder)
    

@app.route("/Series/<folder>/<sub_folder>")
def _episodes(folder, sub_folder):
    episodes = []
    for root, dirs, files in os.walk(f"Series\\{folder}\\{sub_folder}"):
        for file in files:
            if file.endswith((".mp4", ".mkv", ".mov")):
                episodes.append(file)
    print(folder)
    print(sub_folder)
    return render_template("SeriesPage/Episode.html", episodes = episodes, sub_folder = sub_folder)

@app.route("/Series/<folder>/<sub_folder>/<episode>")
def episode(folder, sub_folder, episode):
    return render_template("SeriesPage/Episode_Watch.html", folder = folder, sub_folder = sub_folder, episode = episode)

@app.route("/video/Series/<folder>/<sub_folder>/<episode>")
def serve_video(folder, sub_folder, episode):
    return send_from_directory(
        os.path.join("Series", folder, sub_folder),
        episode
    )


@app.route("/Movies/<title>")
def movie_track(title):
    return send_from_directory("Movie", title)



@app.route("/Video/<title>")
def video(title):
    return send_from_directory("Video", title)


app.run("0.0.0.0", 5500)
