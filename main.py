import argparse
from playwright.sync_api import sync_playwright

def run(playwright, first_name, last_name, birth_month, birth_day, birth_year, gender):
    browser = playwright.chromium.launch(channel="chrome", headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Navegar a la página de creación de cuenta de Google
    page.goto("https://accounts.google.com/signup")

    # Esperar a que los campos estén disponibles y llenarlos en la primera pantalla
    page.wait_for_selector("input[name='firstName']")
    page.fill("input[name='firstName']", first_name)
    
    page.wait_for_selector("input[name='lastName']")
    page.fill("input[name='lastName']", last_name)
    
    # Clic en el botón de siguiente en la primera pantalla
    page.wait_for_selector("button[jsname='LgbsSe']")
    page.click("button[jsname='LgbsSe']")

    # Esperar a que la segunda pantalla cargue
    page.wait_for_selector("select[name='month']")

    # Seleccionar mes de nacimiento
    page.click("select[name='month']")
    page.select_option("select[name='month']", birth_month)
    
    # Llenar día y año de nacimiento
    page.wait_for_selector("input[name='day']")
    page.fill("input[name='day']", birth_day)
    
    page.wait_for_selector("input[name='year']")
    page.fill("input[name='year']", birth_year)

    # Seleccionar género
    page.click("select[name='gender']")
    page.select_option("select[name='gender']", gender)

    # Clic en el botón de siguiente en la segunda pantalla
    page.wait_for_selector("button[jsname='LgbsSe']")
    page.click("button[jsname='LgbsSe']")

    # Aquí podrías agregar más lógica para manejar el flujo completo del registro

    browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatizar la creación de una cuenta de Google.")
    parser.add_argument("--first_name", required=True, help="Nombre")
    parser.add_argument("--last_name", required=True, help="Apellido")
    parser.add_argument("--birth_month", required=True, help="Mes de nacimiento (Enero, Febrero, etc.)")
    parser.add_argument("--birth_day", required=True, help="Día de nacimiento")
    parser.add_argument("--birth_year", required=True, help="Año de nacimiento")
    parser.add_argument("--gender", required=True, help="Género (Masculino, Femenino)")

    args = parser.parse_args()

    with sync_playwright() as playwright:
        run(playwright, args.first_name, args.last_name, args.birth_month, args.birth_day, args.birth_year, args.gender)
