import customtkinter as ctk
import pyperclip
import google.generativeai as genai

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

app = ctk.CTk()
app.geometry("400x450")
app.title("Gemini Chat")
app.resizable(False, False)

optionmodel_var = ctk.StringVar(value="gemini-1.5-flash")


selectmodel = ctk.CTkComboBox(
    master=app,
    values=['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro'],
    variable=optionmodel_var
)


text_box = ctk.CTkEntry(
    master=app,
    width=370,
    height=50,
    font=ctk.CTkFont("Arial", 16, "normal"),
    placeholder_text="Ingresa una instrucción aquí",
    placeholder_text_color="gray"
)
text_box.pack(pady=20)

gemtext = ctk.CTkLabel(
    master=app,
    text="Respuesta: ",
    font=ctk.CTkFont("Arial", 12)
)
gemtext.place(
    relx=0.05,
    rely=0.16
)

geminiresponse = ctk.CTkTextbox(
    master=app,
    height=200,
    width=370
)
geminiresponse.pack(pady=10)

selectmodel.pack()

def load_api_key():
    try:
        with open("key.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None 


def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

def process_request():
    api_key = load_api_key()
    if api_key:
        genai.configure(api_key=api_key)
    else:
        geminiresponse.delete('1.0', 'end')
        geminiresponse.insert("1.0", "No se encontro la llave para la api, configura el boton API Key e intenta de nuevo") 

    model = genai.GenerativeModel(
        model_name=optionmodel_var.get(),
        generation_config=generation_config,
    )
    chat_session = model.start_chat()
    global response
    clipboard_text = pyperclip.paste()
    instruction = text_box.get() 
    include_clipboard = switch.get()
    print(optionmodel_var.get())

    if include_clipboard:
        print(include_clipboard)
        prompt = f"Con el siguiente texto: \n\"{clipboard_text}\"\n aplica la siguiente instrucción: {instruction}"
    else:
        print(include_clipboard)
        prompt = f"{instruction}"

    try:
        response = chat_session.send_message(prompt)
        geminiresponse.delete("1.0", "end") 
        geminiresponse.insert("1.0", response.text)
    except Exception as e:
        pass

def open_api_key_window():

    def save_api_key():
        api_key = api_key_entry.get()
        if api_key:
            try:
                with open("key.txt", "w") as f:
                    f.write(api_key)
                status_label.configure(text="API key saved successfully!", text_color="green")
            except Exception as e:
                status_label.configure(text=f"Error saving API key: {e}", text_color="red")
        else:
            status_label.configure(text="Please enter an API key.", text_color="red")

    api_key_window = ctk.CTkToplevel(app)
    api_key_window.title("API Key")
    api_key_window.geometry("300x150") 

    api_key_label = ctk.CTkLabel(api_key_window, text="Obten tu API key en \n aistudio.google.com/apikey")
    api_key_label.pack(pady=10)
    api_key_entry = ctk.CTkEntry(api_key_window, width=250, show="*")  # Mask input for security
    api_key_entry.pack()

    save_button = ctk.CTkButton(api_key_window, text="Save", command=save_api_key)
    save_button.pack(pady=10)

    status_label = ctk.CTkLabel(api_key_window, text="")
    status_label.pack()

api_key_button = ctk.CTkButton(
    master=app,
    text="API Key",
    font=ctk.CTkFont("Arial", 12, weight="bold"),
    command=open_api_key_window,
    fg_color=_from_rgb((140, 0, 217)),
    hover_color=_from_rgb((100, 78, 240)),
    corner_radius=20,
    width=28
)
api_key_button.place(relx=0.8, rely=0.91)

switch = ctk.CTkSwitch(
    master=app,
    text="Incluir Portapapeles"
)
switch.pack()

button = ctk.CTkButton(
    master=app,
    text="Enviar instrucción",
    font=ctk.CTkFont("Arial", 12, weight="bold"),
    text_color="black",
    command=process_request,
    fg_color="#65c8f2",
    hover_color="#29b5ff",
    corner_radius=20,
)
button.pack(pady=10)

def responsetoclipboard():
    pyperclip.copy(geminiresponse.get("1.0", "end-1c"))
    print("Respuesta copiada al portapapeles")

copytoclip = ctk.CTkButton(
    master=app,
    text="Copiar",
    font=ctk.CTkFont("Arial", 12, weight="bold"),
    text_color="black",
    command=responsetoclipboard,
    fg_color=_from_rgb((173, 122, 217)),
    hover_color=_from_rgb((112, 78, 140)),
    corner_radius=20,
)
copytoclip.pack()

app.mainloop()