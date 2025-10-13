# -*- coding: utf-8 -*-

import urllib.parse
import requests
import time

class TgBot:
    def __init__(self, BOT_TOKEN, CHANNEL_ID):
         self.__BOT_TOKEN = BOT_TOKEN             
         self.__CHANNEL_ID = str(CHANNEL_ID)      
    

    def send_message(self, message_text):
        # otpravka
        encoded_text = urllib.parse.quote(message_text)

        # формируем url
        url = f"https://api.telegram.org/bot{self.__BOT_TOKEN}/sendMessage?chat_id={self.__CHANNEL_ID}&text={encoded_text}"
    
        try:
            # отправляем http запрос, получаем ответ
            response = requests.get(url, timeout=30)

            # выбираем json для удобства
            result = response.json()
            if result.get('ok'):
                print("Message sent successfully")
                message_id = result['result']['message_id']
                print(f"Message ID: {message_id}")
                return True
            else:
                error = result.get('description', 'Unknown error')
                print(f"Error: {error}")
                return False
            
        except Exception as e:
            print(f"Request failed: {e}")
            return False

    def test(self):
        self.send_message("Старт теста:\n")

        msg_count = 2
        for i in range(1, msg_count):
            self.send_message("Сообщение " + str(i) + " из " + str(msg_count - 1) + "\n")
            time.sleep(1)

        self.send_message("Завершение\nтеста\n✅\n")


    def get_cve_info(self, cve_id):
            # Функция для получения информации о CVE
            return "Выполнен запрос информации о CVE: " + str(cve_id) + "\nВыполнен запрос к БД и получен какой-то ответ о данной CVE"
            

    def start_long_polling(self):
        # Long polling для обработки команд
        self.send_message("Бот CVE угроз стартует")
        print("Starting long polling for CVE commands...")
        offset = 0
        
        # Бесконечная история
        while True:
            try:
                # Получаем обновления
                url = f"https://api.telegram.org/bot{self.__BOT_TOKEN}/getUpdates"
                params = {
                    'offset': offset,
                    'timeout': 10,
                    'limit': 1000
                }
                
                response = requests.get(url, params=params, timeout=35)
                data = response.json()
                
                if data.get('ok') and data.get('result'):
                    for update in data['result']:
                        offset = update['update_id'] + 1

                        if 'channel_post' in update and 'text' in update['channel_post']:
                            channel_post = update['channel_post']
                            text = channel_post['text'].strip()

                            # Обрабатываем команду /get_cve
                            if text.startswith('/get_cve'):
                                parts = text.split()
                                if len(parts) >= 2:
                                    cve_id = parts[1].upper()
                                    print(f"Obrabotka zaprosa CVE: {cve_id}")

                                    result_msg = self.get_cve_info(cve_id)
                                    self.send_message(result_msg)
                                else:
                                    # Если CVE ID не указан
                                    self.send_message("Использование: /get_cve <CVE_ID>\nПример: /get_cve CVE-2021-44228")

                            # Обрабатываем команду /start
                            elif text == '/start':
                                self.send_message("Бот для получения информации о CVE уязвимостях\n\nКоманды:\n/get_cve <CVE_ID> - получить информацию об уязвимости\n\nПример: /get_cve CVE-2021-44228")
                
                            # Обрабатываем команду /end на всякий случай
                            elif text == '/end':
                                self.send_message("Бот для получения информации о CVE уязвимостях прощается с вами\n")
                                return
                            else:
                                self.send_message("Команда " + text + " не верна\n")
                                
                time.sleep(1)
                
            except requests.exceptions.Timeout:
                # Таймаут для long polling
                continue
            except Exception as e:
                print(f"Beskonechny cikle - error: {e}")
                time.sleep(5)

def main():
    print(f"Программа запущена!")

    BOT_TOKEN = "BOT_TOKENBOT_TOKENBOT_TOKENBOT_TOKENBOT_TOKEN"
    CHANNEL_ID = "CHANNEL_IDCHANNEL_IDCHANNEL_IDCHANNEL_ID"
    
    bot = TgBot(BOT_TOKEN, CHANNEL_ID) 

    #  bot.test()

    # Запуск бесконечного запроса
    bot.start_long_polling()

    print(f"всё работает")

if __name__ == "__main__":
    main()
