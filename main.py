import argparse
from playwright.sync_api import sync_playwright

def run(playwright, username, first_name, last_name, password, birth_month, birth_day, birth_year, gender):
    browser = playwright.chromium.launch(channel="chrome", headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Navegar a la página de creación de cuenta de Google
    page.goto("https://accounts.google.com/signup")

    # Llenar los campos del formulario
    page.fill("input[name='Username']", username)
    page.fill("input[name='firstName']", first_name)
    page.fill("input[name='lastName']", last_name)
    page.fill("input[name='Passwd']", password)
    page.fill("input[name='ConfirmPasswd']", password)
    page.select_option("select[name='BirthMonth']", birth_month)
    page.fill("input[name='BirthDay']", birth_day)
    page.fill("input[name='BirthYear']", birth_year)
    page.select_option("select[name='Gender']", gender)

    # Clic en el botón de siguiente
    page.click("button[jsname='LgbsSe']")

    # Aquí podrías agregar más lógica para manejar el flujo completo del registro

    browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatizar la creación de una cuenta de Google.")
    parser.add_argument("--username", required=True, help="Nombre de usuario")
    parser.add_argument("--first_name", required=True, help="Nombre")
    parser.add_argument("--last_name", required=True, help="Apellido")
    parser.add_argument("--password", required=True, help="Contraseña")
    parser.add_argument("--birth_month", required=True, help="Mes de nacimiento")
    parser.add_argument("--birth_day", required=True, help="Día de nacimiento")
    parser.add_argument("--birth_year", required=True, help="Año de nacimiento")
    parser.add_argument("--gender", required=True, help="Género")

    args = parser.parse_args()

    with sync_playwright() as playwright:
        run(playwright, args.username, args.first_name, args.last_name, args.password, args.birth_month, args.birth_day, args.birth_year, args.gender)
