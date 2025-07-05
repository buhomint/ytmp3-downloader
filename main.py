import tkinter, yt_dlp, ctypes, sys, tools, winsound, data, threading
import tkinter.font

def admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def mi_hook(d):
    global texto_estado
    if d['status'] == 'downloading':
        porcentaje = d.get('_percent_str', '').strip()
        texto_estado.set(f"Descargando: {porcentaje}")
    elif d['status'] == 'finished':
        texto_estado.set("¡Completado!")
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)

def clear_url():
    global url
    url.delete(0, tkinter.END)

def error_message(a):
    error = tkinter.Toplevel()
    error.title("Error")
        
    # Dimensiones deseadas
    ancho = 250
    alto = 100
        
    # Obtener posición y tamaño de la ventana principal
    ventana.update_idletasks()
        
    x_main = ventana.winfo_x()
    y_main = ventana.winfo_y()
    ancho_main = ventana.winfo_width()
    alto_main = ventana.winfo_height()
        
    # Calcular posición centrada
    x = x_main + (ancho_main - ancho) // 2
    y = y_main + (alto_main - alto) // 2
        
    error.geometry(f"{ancho}x{alto}+{x}+{y}")

    error.configure(bg="#1e1e1e")
        
    error.iconbitmap(iconempty)

    error.resizable(False, False)

    error.grid_columnconfigure(0, weight=1)
    error.grid_columnconfigure(1, weight=1)
    error.grid_columnconfigure(2, weight=1)
        
    error.grid_rowconfigure(0, weight=1)
    error.grid_rowconfigure(1, weight=1)
    error.grid_rowconfigure(2, weight=1)

    error_label = tkinter.Label(error, text=a, font=font, bg="#1e1e1e", fg="white", width=40, justify="center")
    error_label.grid(row=1, column=1, pady=(20, 20))

    error_button = tkinter.Button(error, text="Continuar", font=font, command= error.destroy, justify="center")
    error_button.grid(row=2, column=1, pady=(10, 10))

    winsound.MessageBeep(winsound.MB_ICONHAND)

def main_menu():
    global texto_estado, downloading

    if url.get() == "":
        return error_message("URL Inválida")
    
    downloading = tkinter.Toplevel()
    downloading.title("Descargando...")
        
    # Dimensiones deseadas
    ancho = 250
    alto = 100
        
    # Obtener posición y tamaño de la ventana principal
    ventana.update_idletasks()
        
    x_main = ventana.winfo_x()
    y_main = ventana.winfo_y()
    ancho_main = ventana.winfo_width()
    alto_main = ventana.winfo_height()
        
    # Calcular posición centrada
    x = x_main + (ancho_main - ancho) // 2
    y = y_main + (alto_main - alto) // 2
        
    downloading.geometry(f"{ancho}x{alto}+{x}+{y}")

    downloading.configure(bg="#1e1e1e")
        
    downloading.iconbitmap(iconempty)

    downloading.resizable(False, False)

    downloading.grid_columnconfigure(0, weight=1)
    downloading.grid_columnconfigure(1, weight=1)
    downloading.grid_columnconfigure(2, weight=1)
        
    downloading.grid_rowconfigure(0, weight=1)
    downloading.grid_rowconfigure(1, weight=1)
    downloading.grid_rowconfigure(2, weight=1)

    texto_estado = tkinter.StringVar()

    state_label = tkinter.Label(downloading, textvariable=texto_estado, font=font, bg="#1e1e1e", fg="white", width=40, justify="center")
    state_label.grid(row=1, column=1, pady=(20, 20))

    download_button.config(state='disabled')
    texto_estado.set("Iniciando descarga...")
    
    # Ruta local a ffmpeg
    ruta_ffmpeg = data.script_directory + "\\tools\\ffmpeg.exe"

    if download_option_var.get() == "Audio":
        opciones = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
                }],
            'outtmpl': data.script_directory + '\\%(title)s.%(ext)s',
            'progress_hooks': [mi_hook],
            'ffmpeg_location': ruta_ffmpeg
        }
    else:
        opciones = {
            'format': 'bv*[height=1080][ext=mp4]+ba[ext=m4a]/bestvideo[height=1080]+bestaudio',
            'merge_output_format': 'mp4',
            'outtmpl': data.script_directory + '\\%(title)s.%(ext)s',
            'noplaylist': True,  # por si la URL es de una playlist
            'quiet': False,      # mostrará mensajes de progreso
            'verbose': True,     # para ver más información
            'progress_hooks': [mi_hook],
            'ffmpeg_location': ruta_ffmpeg
        }
    
    def hilo_descarga():
            try:
                with yt_dlp.YoutubeDL(opciones) as ydl:
                    ydl.download([url.get()])
            except yt_dlp.DownloadError as e:
                downloading.destroy
                error_message("URL Inválida")
                texto_estado.set("Error durante la descarga")
                downloading.destroy
            except Exception as e:
                 downloading.destroy
                 error_message("Fallo inesperado")
                 texto_estado.set("Fallo inesperado")
            finally:
                download_button.config(state='normal')
    
    threading.Thread(target=hilo_descarga).start()


def main():
    global url, font, ventana, iconfile, iconempty, download_button, download_option_var

    if not data.is_compiled(): # Pide permisos de administrador en caso de que este ejecutandose como script .py
        if not admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()

    iconfile = data.script_directory + "\\tools\\icon.ico"
    iconempty = data.script_directory + "\\tools\\empty.ico"
    ventana = tkinter.Tk()
    ventana.title("Youtube Downloader")

    ventana.resizable(False, False)

    # Dimensiones deseadas de la ventana
    ancho = 400
    alto = 260
    
    # Obtener dimensiones de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    
    # Calcular posición centrada
    x = (ancho_pantalla - ancho) // 2
    y = (alto_pantalla - alto - 200) // 2

    # Aplicar geometry centrado
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    ventana.configure(bg="#1e1e1e")
    
    ventana.iconbitmap(iconfile)

    font = tkinter.font.Font(family="Segoe UI", size=12)
    
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_columnconfigure(1, weight=1)
    ventana.grid_columnconfigure(2, weight=1)
    ventana.grid_columnconfigure(3, weight=1)
    ventana.grid_columnconfigure(4, weight=1)

    ventana.grid_rowconfigure(0, weight=1)
    ventana.grid_rowconfigure(1, weight=1)
    ventana.grid_rowconfigure(2, weight=1)
    ventana.grid_rowconfigure(3, weight=1)
    ventana.grid_rowconfigure(4, weight=1)
    ventana.grid_rowconfigure(5, weight=1)

    label = tkinter.Label(ventana, text="Introduzca la URL de Youtube", font=font, bg="#1e1e1e", fg="white", width=30, justify="left")
    label.grid(row=1, column=2, sticky="swe", pady=1, padx=1)
    
    url = tkinter.Entry(ventana)
    url.grid(row=2, column=2, sticky="we", pady=10, padx=5)

    clear_button = tkinter.Button(text="Limpiar", font=font, command= clear_url, width=6, height=1)
    clear_button.grid(row=2, column=3, sticky="", pady=1, padx=1)

    download_option_var = tkinter.StringVar()
    download_option_var.set("Audio")

    download_audio = tkinter.Radiobutton(ventana, text="Audio", variable=download_option_var, value="Audio", bg="#1e1e1e", fg="white", selectcolor="#1e1e1e")
    download_audio.grid(row=3, column=2, sticky="nw", pady=1, padx=40)

    download_video = tkinter.Radiobutton(ventana, text="Video", variable=download_option_var, value="Video", bg="#1e1e1e", fg="white", selectcolor="#1e1e1e")
    download_video.grid(row=3, column=2, sticky="ne", pady=1, padx=40)


    download_button = tkinter.Button(text="Descargar", font=font, command=main_menu)
    download_button.grid(row=4, column=2, sticky="nwe", pady=1, padx=1)

    dev_label = tkinter.Label(ventana, text=f"Dev: bhmint", font=font, bg="#1e1e1e", fg="white", width=17)
    dev_label.grid(row=5, column=1, sticky="w", pady=1, padx=1)

    version = tools.version

    version_label = tkinter.Label(ventana, text=f"Version: {version}", font=font, bg="#1e1e1e", fg="white", width=17)
    version_label.grid(row=5, column=3, sticky="e", pady=1, padx=1)

    ventana.mainloop()

main()
