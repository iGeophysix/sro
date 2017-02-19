import requests
from bs4 import BeautifulSoup
import re


class ParseSRO():
    def __init__(self, link, suffix):
        self._link = link
        self._suffix = suffix
        self._page_number = self.get_number_of_pages(self._link)
        self._sro = []

    @staticmethod
    def read_sro(line):
        sro_details = re.split(r'<td>', str(line))
        sro_number = sro_details[1][:-6]
        sro_name = sro_details[2][:-6]
        sro_address = sro_details[3][:-6]
        sro_subject = sro_details[4][:-6]
        sro_fed_okrug = re.split(r"</td>", sro_details[5])[0]
        if len(re.findall(r"Действует", sro_details[5][:-2])) > 0:
            sro_status = True
        else:
            sro_status = False

        return (sro_name, sro_number, sro_address, sro_subject, sro_fed_okrug, sro_status)

    @staticmethod
    def get_page(link):
        page = requests.get(link)
        soup = BeautifulSoup(page.content.decode('utf-8'), 'html.parser')
        return soup.find_all('tr', 'sro-link')

    @staticmethod
    def get_number_of_pages(link):
        page = requests.get(link)
        soup = BeautifulSoup(page.content.decode('utf-8'), 'html.parser')
        max_page = re.findall(r'page=\d+">\d+', str(soup.find_all('ul', 'pagination')))[-1].split(">")[-1]
        return int(max_page) + 1

    def parse_sro(self):
        sum = 0
        for i in range(1, self._page_number):
            this_page_records = self.get_page("{}{}{}".format(self._link, self._suffix, i))
            for this_record in this_page_records:
                self._sro.append(self.read_sro(this_record))
            records_count = len(this_page_records)
            sum += records_count
            # print("Страница {} : {} записей".format(i, records_count))
        print("Всего записей: {}".format(sum))

    def __str__(self):
        out_str = ""
        for this_record in self._sro:
            out_str += ("{}\n{}\n{}\n\n".format(this_record[0], this_record[1], this_record[2]))
        return out_str


sro = ParseSRO("http://reestr.nostroy.ru/", "?page=")
sro.parse_sro()
print(sro)
