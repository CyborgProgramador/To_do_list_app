# Modulos requeridos
import tkinter as tk   
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql


# Función para añadir tareas
def add_task():  
    task_string = task_field.get()   
    if len(task_string) == 0:   
        messagebox.showinfo('Error', 'Field is Empty.')  
    else:  
        tasks.append(task_string)  
        the_cursor.execute('insert into tasks values (?)', (task_string ,))   
        list_update()  
        task_field.delete(0, 'end')  
  
# Función para actualizar lista de tareas
def list_update():  
    clear_list()  
    for task in tasks:   
        task_listbox.insert('end', task)  
  
# Función para eliminar tareas de la lista  
def delete_task():  
    try:  

        the_value = task_listbox.get(task_listbox.curselection())  
        if the_value in tasks:  
            tasks.remove(the_value)   
            list_update()  
            the_cursor.execute('delete from tasks where title = ?', (the_value,))  
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')        
  
# Función para eliminar todas las tareas de la lista
def delete_all_tasks():  
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')  
    if message_box == True:   
        while(len(tasks) != 0):  
            tasks.pop()  
        the_cursor.execute('delete from tasks')  
        list_update()  

# Función para hacer limpiar la lista
def clear_list():  
    task_listbox.delete(0, 'end')  
  
# Función para cerrar la aplicación
def close():  
    print(tasks)   
    guiWindow.destroy()  
  
# Función para recibir datos de la DB
def retrieve_database():   
    while(len(tasks) != 0):    
        tasks.pop()   
    for row in the_cursor.execute('select title from tasks'):   
        tasks.append(row[0])  
  
# Configuración de la interfaz 
if __name__ == "__main__":  
    guiWindow = tk.Tk()  
    guiWindow.title("To-Do List Application")  
    guiWindow.geometry("500x450+750+250")  
    guiWindow.resizable(0, 0)  
    guiWindow.configure(bg = "#8869A5")  
  
    # Conección con la DB 
    the_connection = sql.connect('listOfTasks.db')  
    the_cursor = the_connection.cursor()  
    the_cursor.execute('create table if not exists tasks (title text)')  
  
    # Lista para almacenar las tareas
    tasks = []  
      
    # Definiendo frames de los elementos con tk.Frame()
    header_frame = tk.Frame(guiWindow, bg = "#8869A5")  
    functions_frame = tk.Frame(guiWindow, bg = "#8869A5")  
    listbox_frame = tk.Frame(guiWindow, bg = "#8869A5")  
  
    #Ubicando los elementos frame.pack()
    header_frame.pack(fill = "both")  
    functions_frame.pack(side = "left", expand = True, fill = "both")  
    listbox_frame.pack(side = "right", expand = True, fill = "both")  
      
    # Definiendo plantillas con el widget ttk.Label()
    header_label = ttk.Label(  
        header_frame,  
        text = "Your To-Do list...",  
        font = ("Brush Script MT", "50"),  
        background = "#8869A5",  
        foreground = "#B1BEEA"  
    )  

    header_label.pack(padx = 20, pady = 20)  
  

    task_label = ttk.Label(  
        functions_frame,  
        text = "Enter the Task:",  
        font = ("Consolas", "11", "bold"),  
        background = "#8869A5",  
        foreground = "#ffffff"  
    )  

    task_label.place(x = 30, y = 40)  
      
    # Definendo el recuadro de entrada con el widget ttk.Entry()  
    task_field = ttk.Entry(  
        functions_frame,  
        font = ("Consolas", "12"),  
        width = 18,  
        background = "#B1BEEA",  
        foreground = "#8fce00"
    )  
    # Ubicando el recuadro de entrada con place()
    task_field.place(x = 30, y = 80)  
  
    # Añadiendo los botones usando el widget ttk.Button()
    add_button = ttk.Button(  
        functions_frame,  
        text = "Add Task",  
        width = 24,  
        command = add_task,
        
    )  
    del_button = ttk.Button(  
        functions_frame,  
        text = "Delete Task",  
        width = 24,  
        command = delete_task  
    )  
    del_all_button = ttk.Button(  
        functions_frame,  
        text = "Delete All Tasks",  
        width = 24,  
        command = delete_all_tasks

    )  
    exit_button = ttk.Button(  
        functions_frame,  
        text = "Exit",  
        width = 24,  
        command = close
    )  
    # Ubicando los botones dentro de la aplicación con el método place() 
    add_button.place(x = 30, y = 120)  
    del_button.place(x = 30, y = 160)  
    del_all_button.place(x = 30, y = 200)  
    exit_button.place(x = 30, y = 240)  
  
    # Definiendo la List Box
    task_listbox = tk.Listbox(  
        listbox_frame,  
        width = 26,  
        height = 13,  
        selectmode = 'SINGLE',  
        background = "#ffffff",  
        foreground = "#000000",  
        selectbackground = "#8095CE",  
        selectforeground = "#FFFFFF"  
    )  
    # Ubicando la list box con el método place()
    task_listbox.place(x = 10, y = 20)  
  
    # Llamando función adicional
    retrieve_database()

    list_update()  
    # Ejecución de la aplicación con el método mainloop()
    guiWindow.mainloop()  

    # Estableciendo conexión con la base de datos
    the_connection.commit()  
    the_cursor.close()  

