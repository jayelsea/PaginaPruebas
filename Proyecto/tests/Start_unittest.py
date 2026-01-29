from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Edge() 

driver.get("http://www.clouditeducation.com/pruebas")

elemento = driver.find_element(By.ID, "noImportante")

if elemento is not None:
    print ("El elemento by ID fue encontrado")

elemento2 = driver.find_element(By.NAME, "ultimo")

if elemento2 is not None:
    print ("El elemento by NAME fue encontrado")
    
driver.quit()
