# users_scrapper_telegram_bot
это телеграм бот для скраппинга участников телеграм групп и приглашенияих в канал, где вы являетесь админом с возможностью приглашения пользователей.
____
## как запустить бота на heroku?
1. создайте свое приложение на https://my.telegram.org/apps, вам будут нужны api_hash и api_id вашего приложения    
2. клонируйте репозиторий с гитхаба и перейдите в папку с проектом    
```
$ git clone https://github.com/evlachs/users_scrapper_telegram_bot.git && cd users_scrapper_telegram_bot
```
3. создайте виртуальное окружение и установите все необходимые библиотеки    
```
$ python -m venv venv
$ venv/Scripts/activate.bat
$ pip install -r requirements.txt
```

4. откройте make_session.py и заполните api_id и api_hash данными из вашего приложения телеграм, введите телефон, на который зарегестрирован ваш аккаунт телеграм    
```Python
from telethon.sync import TelegramClient

phone: str = '+phone'  # enter your number here starting with +
api_id: int = 'api_id'  # enter your api_id from the telegram application configuration
api_hash: str = 'api_hash'  # enter your api_hash from the telegram application configuration

client = TelegramClient(phone, api_id, api_hash)

client.start()
```
5. запустите make_session.py
```
$ python make_session.py
```
```
Please enter your phone (or bot token): your phone but without +
Please enter the code you received: code
```
если все указано верно, вы получите сообщение `'Signed in successfully as username'` и файл .session в директории users_scrapper_telegram_bot    
6. установите heroku cli отсюда https://devcenter.heroku.com/articles/heroku-cli    
7. авторизируйтесь в своем аккаунте heroku    
```
$ heroku login
```
```
heroku: Press any key to open up the browser to login or q to exit:
Opening browser to https://cli-auth.heroku.com/auth/cli/browser/...
heroku: Waiting for login...
Logging in... done
Logged in as user@user.com
```
8. создайте приложение heroku    
```
$ heroku create your-app-name
```
9. сохраните изменения в репозитории, сделайте коммит и запушьте проект на heroku    
```
$ git add .
$ git commit -m "commit"
$ git push heroku branch_name
```
10. после этого перейдите на https://id.heroku.com/login и авторизируйтесь, затем выберете свое приложение    
11. на вкладке 'Settings' добавьте все необходимые ключи и вставьте соответсвующие значения    
![скрин3](https://user-images.githubusercontent.com/101788734/201453580-b6fd9ffa-6165-405c-8dfe-04d8c2656dd8.png)
![скрин2](https://user-images.githubusercontent.com/101788734/201453583-94b9ddd2-ed7e-40db-b684-a143a59996a2.png)
12. после добавления всех значений нажмите 'More' и выберете 'restart all dynos'    
![скрин1](https://user-images.githubusercontent.com/101788734/201453591-3c553ae5-7455-4646-ae4a-ab559742120a.png)
13. бот работает!    
____
## Тесты и рекомендуемые параметры
Я проводил тесты на следующих параметрах: 

### Неудачный тест
* лимит на приглашения в день - 100
* задержка – 60
* время – любое/управлять вручную
* результат – добавлено 30 подписчиков, парсинг до конца не доработал, я получил ограничение на приглашение на непонятное количество часов (думаю - сутки). возможно, на лимите 100 я получил ограничение, тк до этого активно тестил бота и уже отработал некоторое количество допустимых запросов.

### Удачный тест
* лимит на приглашения в день - 50
* задержка – 30
* время – любое/управлять вручную
* результат – добавлено 18 подписчиков, парсинг успешно завершился, ограничений не получено.

### РЕКОМЕНДУЕМЫЕ МНОЙ ПАРАМЕТРЫ
* лимит на приглашения в день – 50-100
* задержка – 40-60 и больше
* время – любое/управлять вручную
* ожидаемый результат ~40-50% от лимита приглашений.
____
## Как работает добавление пользователей?
### С помощью библиотеки telethon вы авторизируетесь в телеграме, скрипт использует ваш аккаунт, чтобы приглашать пользователей из групп, в которых вы состоите, как если бы это делали вы сами
1. интерфейс бота
    - 1.1. сначала бот спросит у вас название канала, которое нужно ему отправить в формате @channel (вы обязательно должны быть админом этого канала и иметь возможность приглашать новых пользователей)
    - 1.2. затем бот предложит вам выбрать группу, из которой следует собирать участников для приглашений; бот узнает ваши группы с помощью метода UsersScrapper.get_groups()
    - 1.3. потом бот попросит задать лимит на приглашения в день, а также задержку между приглашениями и время ежедневного автозапуска
2. scrapping_settings.csv и users.csv
    - 2.1. параметр 'scrapping_sctatus' в scrapping_settings.csv проверяется каждую минуту. 
        - 2.1.1. если его значение True, то скраппер ждет наступления время запуска 'launch_time' 
    - 2.2. при наступлении 'launch_time' начинается скраппинг участников группы 'active_group' методом UsersScrapper.get_chat_participants()
        - 2.2.1 при обновлении 'active_group' users.csv очищается методом UsersScrapper.clear_users_data()
        - 2.2.2 полученный список участников добавляется в users.csv с помощью UsersScrapper.save_new_users_to_csv(), а всем юзернеймам присваивается значение параметра 'invited', равное 0
    - 2.3. после того как участники группы собраны (дефолтное значение = 200 участников из группы за 1 раз), бот может взять их из users.csv методом UsersScrapper.get_users_to_invite()
    - 2.4. начинается приглашение участников группы в канал 'active_channel' через метод UsersScrapper.invite_users()
        - 2.4.1. задержка между приглашениями составляет время, соответствующее параметру 'delay'; лимит на приглашения в день задается параметром 'limit'
        - 2.4.2. после каждого приглашенного пользователя его статус 'invited' в таблице users.csv обновляется на 1 методом UsersScrapper.update_users_status() и бот больше не будет их приглашать
3. после приглашения всех доступных пользователей (но не больше установленного лимита) скраппинг завершается и бот снова ждет времени еждневного автозапуска или пока вы запустите его вручную
