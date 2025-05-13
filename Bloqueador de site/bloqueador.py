import os
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import font 
import ctypes


def is_admin():
    try:
        return os.geteuid() == 0  
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0  


if not is_admin():
    messagebox.showerror("Erro", "Este script precisa ser executado como administrador!")
    sys.exit()


hosts_path = "C:\\Windows\\System32\\drivers\\etc\\hosts"  


redirect_ip = "127.0.0.1"


def bloquear_site():
    site = entry_site.get()
    if site:
        try:
            with open(hosts_path, 'r+') as file:
                linhas = file.readlines()
                
                if any(site in linha for linha in linhas):
                    messagebox.showinfo("Aviso", "Este site já está bloqueado!")
                else:
                    
                    file.write(f"{redirect_ip} {site}\n")
                    messagebox.showinfo("Sucesso", f"Site {site} bloqueado com sucesso!")
        except PermissionError:
            messagebox.showerror("Erro", "Permissões insuficientes para modificar o arquivo de hosts.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao bloquear o site: {e}")
    else:
        messagebox.showwarning("Aviso", "Por favor, insira um site.")


def desbloquear_site():
    site = entry_site.get()
    if site:
        try:
            with open(hosts_path, 'r+') as file:
                linhas = file.readlines()
                file.seek(0)
                file.truncate(0)
                
                for linha in linhas:
                    if site not in linha:
                        file.write(linha)
                messagebox.showinfo("Sucesso", f"Site {site} desbloqueado com sucesso!")
        except PermissionError:
            messagebox.showerror("Erro", "Permissões insuficientes para modificar o arquivo de hosts.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao desbloquear o site: {e}")
    else:
        messagebox.showwarning("Aviso", "Por favor, insira um site.")


def listar_sites_bloqueados():
    try:
        with open(hosts_path, 'r') as file:
            linhas = file.readlines()
            sites_bloqueados = [linha.split()[1] for linha in linhas if linha.startswith(redirect_ip)]
            if sites_bloqueados:
                messagebox.showinfo("Sites Bloqueados", "\n".join(sites_bloqueados))
            else:
                messagebox.showinfo("Sem Sites Bloqueados", "Não há sites bloqueados.")
    except PermissionError:
        messagebox.showerror("Erro", "Permissões insuficientes para acessar o arquivo de hosts.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar os sites bloqueados: {e}")


def desbloquear_todos_os_sites():
    try:
        with open(hosts_path, 'r+') as file:
            linhas = file.readlines()
            file.seek(0)
            file.truncate(0)

            for linha in linhas:
                if not linha.startswith(redirect_ip):
                    file.write(linha)
            messagebox.showinfo("Sucesso", "Todos os sites foram desbloqueados!")
    except PermissionError:
        messagebox.showerror("Erro", "Permissões insuficientes para modificar o arquivo de hosts.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao desbloquear todos os sites: {e}")


def criar_interface():
    global entry_site
    root = tk.Tk()
    root.title("Bloqueador de Sites")


    root.geometry("500x500")
    root.resizable(False, False)
    root.configure(bg="#2C3E50")


    header_font = font.Font(family="Helvetica", size=16, weight="bold")
    entry_font = font.Font(family="Helvetica", size=12)
    button_font = font.Font(family="Helvetica", size=12, weight="bold")

    title_label = tk.Label(root, text="Bloqueador de Sites", font=header_font, fg="white", bg="#2C3E50")
    title_label.pack(pady=20)


    label_site = tk.Label(root, text="Insira o site:", font=entry_font, fg="white", bg="#2C3E50")
    label_site.pack(pady=10)

    entry_site = tk.Entry(root, width=40, font=entry_font)
    entry_site.pack(pady=5)


    botao_bloquear = tk.Button(root, text="Bloquear", font=button_font, bg="#3498DB", fg="white", width=20, command=bloquear_site)
    botao_bloquear.pack(pady=10)

    botao_desbloquear = tk.Button(root, text="Desbloquear", font=button_font, bg="#E74C3C", fg="white", width=20, command=desbloquear_site)
    botao_desbloquear.pack(pady=10)

    botao_listar_bloqueados = tk.Button(root, text="Listar Sites Bloqueados", font=button_font, bg="#2ECC71", fg="white", width=20, command=listar_sites_bloqueados)
    botao_listar_bloqueados.pack(pady=10)

    botao_desbloquear_todos = tk.Button(root, text="Desbloquear Todos", font=button_font, bg="#F39C12", fg="white", width=20, command=desbloquear_todos_os_sites)
    botao_desbloquear_todos.pack(pady=10)


    botao_sair = tk.Button(root, text="Sair", font=button_font, bg="#95A5A6", fg="white", width=20, command=root.quit)
    botao_sair.pack(pady=20)

    root.mainloop()


criar_interface()
