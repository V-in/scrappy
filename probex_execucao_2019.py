from scrappy.tasks.task import Task
from scrappy.persistor.in_memory import InMemoryPersistor
from scrappy.scheduler.round_robin import RoundRobin
from scrappy.persistor.document import Document
import json
import code
import re


class LocaisRealizacao(Task):
    def __init__(self, persistor):
        Task.__init__(self, persistor)

    def bootstrap(self, driver):
        driver.get('https://sigaa.ufpb.br/sigaa/logon.jsf')

        box = driver.find_element_by_css_selector('#form\:login')
        box.clear()
        box.click()
        box.send_keys("lincolneloi")

        box = driver.find_element_by_css_selector('#form\:senha')
        box.click()
        box.send_keys("lin987")

        driver.find_element_by_css_selector('#form\:entrar').click()

        try:
            driver.find_element_by_css_selector(
                '#btnNaoResponderContinuar').click()
            driver.find_element_by_css_selector(
                '#btnSimLembrarQuestionario').click()
        except:
            pass

        driver.find_element_by_css_selector(
            '.list-group-item-action').click()

        try:
            driver.find_element_by_css_selector(
                '#btnNaoResponderContinuar').click()
            driver.find_element_by_css_selector(
                '#btnSimLembrarQuestionario').click()
            time.sleep(6)
        except:
            pass

        driver.find_element_by_css_selector(
            '#form\:moduloExtensao').click()
        driver.find_element_by_xpath(
            '//a[contains(text(), "Buscar Ações")]').click()

        box = driver.find_element_by_css_selector(
            '#formBuscaAtividade\:buscaAno')
        box.clear()
        box.send_keys('2019')

        driver.find_element_by_xpath(
            "//select[@name = 'formBuscaAtividade:buscaEdital']//option[contains(text(), 'EDITAL Nº 01/2019 - PROBEX 2019')]").click()
        driver.find_element_by_css_selector(
            '#formBuscaAtividade\:btBuscar').click()
        driver.find_element_by_xpath("//select[@name = 'formBuscaAtividade:buscaSituacao']//option[contains(text(),'EM EXECUÇÃO')]").click()

    def run(self, driver, persistor):
        table_header = driver.find_element_by_xpath("/html[1]/body[1]/div[2]/div[2]/form[2]/table[1]/caption[1]")
        n_items = int(re.match(r'.*\(([0-9]*)\).*', table_header.text).groups()[0])

        for i in range(2):
            driver.find_elements_by_css_selector('td:nth-child(6) img')[i].click()
            button_text = driver.find_elements_by_xpath("//a[contains(text(),'Clique aqui para visualizar os participantes desta')]")[0].get_attribute("onclick")
            doc_id = re.match(r".*'id':'(\d*)'", button_text).groups()[0]
            persistor.save_one(Document(doc_id, driver.page_source))
            driver.back()
            print('Scrapped {} of {}. ID={}'.format(i + 1, n_items, doc_id) + str(i))


p = InMemoryPersistor()
task = LocaisRealizacao(p)
with RoundRobin(1, headless=False) as scheduler:
    scheduler.schedule_task(task)

print(json.dumps(p.data), file=open("./results/locais_realizacao.json", "w"))
