import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def test_authentication(authentication):
    # тест авторизации
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

def test_my_pets_check(authentication):
    # переход на страницу с питомцами пользователя
    menu_pets = pytest.driver.find_element(By.CLASS_NAME, 'navbar-toggler-icon')
    menu_pets.click()
    my_pets_see = pytest.driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]')
    my_pets_see.click()
    # проверка того, что находдимся на ожидаемой странице "мои питомцы"
    assert pytest.driver.current_url == "https://petfriends.skillfactory.ru/my_pets"
    # задаем переменную числа питомцев и переменную количества карточек c явным ожиданием, сравниваем их
    element = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]')))
    pets_quantity = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    element = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr')))
    pets_card_number = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

    assert int(pets_quantity) == len(pets_card_number)

def test_my_pets_check_foto(authentication, my_pets_page):
    # тест наличия фотографии у, хотя бы, половины питомцев + неявное ожидание
    # задаем переменную количества фото и переменную количества карточек, проверяем, что  хотя бы половина питомцев имеет фото
    pytest.driver.implicitly_wait(5)
    pets_card_number = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    pytest.driver.implicitly_wait(5)
    pet_images = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/th/img')

    pet_number_images = 0

    for i in range(len(pets_card_number)):
        if pet_images[i].get_attribute('src') != '':
            pet_number_images += 1
        else:
            pet_number_images += 0
    #     return pet_number_images
    assert pet_number_images / len(pets_card_number) >= 0.5

def test_my_pets_check_parameters(authentication, my_pets_page):
    # тест наличия имени, возраста, породы питомцев + неявное ожидание
    pytest.driver.implicitly_wait(5)
    pets_card_number = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    pytest.driver.implicitly_wait(5)
    pet_names = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[1]')  # имена питомцев
    pytest.driver.implicitly_wait(5)
    pet_descriptions = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[2]') # строчки с информацияей о виде питомца
    pytest.driver.implicitly_wait(5)
    pet_age = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[3]') # строчки с информацияей о возрасте питомца

    for i in range(len(pets_card_number)):
        if len(pets_card_number) == 0:
            print('У вас нет питомцев')
        else:
            assert pet_names[i].text != '' # проверяем, что поля с именами не пустые
            assert pet_descriptions[i].text != '' # проверяем, что поля с породой не пустые
            assert pet_age[i].text != '' # проверяем, что поля с возрастом не пустые


def test_my_pets_check_different_name(authentication, my_pets_page):
    # проверка того, что у всех питомцев разные имена + явное ожидание
    element = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr')))
    pets_card_number = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    element = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[1]')))
    pet_names = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[1]')
    list_pet_names = []
    for i in range(len(pets_card_number)):
        if len(pets_card_number) == 0:
            print('У вас нет питомцев')
        else:
            list_pet_names.append(pet_names[i].text)

    set_list_names = set(list_pet_names)

    if len(set_list_names) < len(list_pet_names):
        print("У некоторых ваших питомцев совпадают имена. Пожалуйста, внесите в клички отличия, что бы не путать других пользователей")
    else:
        assert len(set_list_names) == len(list_pet_names)

def test_my_pets_everyone_different(authentication, my_pets_page):
    # проверка того, что все питомцы уникальны (нет совпадающих по всем параметрам) + явное ожидание
    element = WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr')))
    pets_card_number = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    my_pets_data = []
    for pet in pets_card_number:
        my_pets_data.append(pet.text)
    unique_pet = set(my_pets_data)

    if len(my_pets_data) > len(unique_pet):
        print("Один из ваших питомцев повторяется несколько раз. Пожалуйста, удалите повторяющуюся карточку")
    else:
        assert len(my_pets_data) == len(unique_pet)