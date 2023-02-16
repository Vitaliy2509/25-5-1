import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import email, password

@pytest.fixture
def chrom_options():
    chrom_options = webdriver.ChromeOptions()
    chrom_options.add_argument('--kiosk')
    chrom_options.add_argument("--window-size=800,600")
    return chrom_options

@pytest.fixture(scope = 'session', autouse = True)
def testing(): # подключаем драйвер Chrome и открываем веб-стрницу
    pytest.driver = webdriver.Chrome(r'C:\Chromedriver\chromedriver.exe')
    #Переходим на страницу авторизации
    pytest.driver.get('https://petfriends.skillfactory.ru/login')
    yield
    pytest.driver.quit()

@pytest.fixture(scope = 'session')
def authentication():
    pytest.driver.find_element(By.ID, 'email').send_keys(email)
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys(password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

@pytest.fixture(scope = 'session')
def my_pets_page():
    # переход на страницу с питомцами пользователя
    menu_pets = pytest.driver.find_element(By.CLASS_NAME, 'navbar-toggler-icon')
    menu_pets.click()
    my_pets_see = pytest.driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]')
    my_pets_see.click()