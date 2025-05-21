# Онлайн библиотека

## Установка
  ### Клонирование проекта
Зайти в терминал GitBash и прописать команду
```GitBash
git clone https://github.com/Tetsuozxcmid/test-Patres
```
Дальше активировать виртуальное окружение
```GitBash
python -m venv venv
```
Активировать его
```GitBash
venv/scripts/activate
```
Установить нужные зависимости
```GitBash
pip install  -r requirements.txt
```
Перейти в папку /app
```GitBash
cd app
```
Создать .env файл с содержимым снизу
```
DB_HOST=хост_бд

DB_PORT=порт_бд

DB_USER=юзернейм_бд

DB_PASS=пароль_от_бд

DB_NAME=название_бд

SECRET_KEY=Сгенерировать секретный ключ для дальнейшего использования с jwt(и занести сгенерированный ключ сюда)

ALGORITHM=HS256(симметричный алгоритм, который используется для подписи токенов, в частности JSON Web Tokens (JWT))


```
Запустить веб-приложение с помощью команды:

```
uvicorn run:app --port 8001
```


### Описание структуры проекта
app/
```├───alembic
│   ├───versions
│   │   └───#Версии миграций расширения .py
│   └───env.py #основной конфигурационный скрипт алембика
├───api
│   ├───v1
│   │   ├───admins
│   │   │   └───__init__.py
            │ auth.py #Логика создания acces токена для авторизации через jwt
            │ passlogic.py # Логика хэширования пароля и заноса в бд через CryptoContext
            │ router.py # Рутеры для библиотекарей(админов(Регистрация админа,авторизация))
│   │   ├───books
│   │   │   └───__init__.py
            │ book.py # Рутеры для взаимодействия с книгами
│   │   ├───borrowed
│   │   │   └───__init__.py
            │ borrow.py #Рутеры для записей о том какая и кому книга была выдана
│   │   ├───readers
│   │   │   └───__init__.py
            │ reader.py #Рутеры взаимодействия с пользователями(читателями)
│   │   └───__pycache__
│   └───__init__.py
├───core
│   ├───auth
│   │    │ __init__.py
│   │     └─── deps.py #Depends для сверки авторизован ли админ для взаимодействия с ручками
│   ├───database
│   │   └───__init__.py
│   │    │─base.py #Базовый класс для миграций в алембике
│   │    │─db.py #Создание async_engine,session_maker, get_db() func
│   └───__init__.py
├───crud
│   ├───books
│   │   └───__init__.py
│   │     │book.py # CRUD Операции для Книг 
│   │
│   ├───borrowed
│   │   └───__init__.py
│   │    │borrow.py # CRUD Операции для Записей занятия книги
│   │───__init__.py
│   ├───readers
│   │   └───__init__.py
│   │    │reader.py # CRUD Операции для Читателей(пользователей библиотеки)
│   └───__init__.py
├───models
│   ├───admin
│   │   └───__init__.py
│   │     │librarian.py # Модель админа(библиотекарей) для бд
│   ├───books
│   │   └───__init__.py
│   │     │book.py # Модель Книги для бд
│   ├───library
│   │   └───__init__.py
│   │     │borrowed.py # Модель записей занятия книг для бд
│   ├───users
│   │   └───__init__.py
│   │     │rader.py # Модель Читателей(пользователей) для бд
│   └───__init__.py
├───schemas
│   └───__init__.py
│    └───book.py #Схемы книг(Default,Update)
│    └───borrowed.py #Схемы записей(Base,Create,Update)
│    └───librarian.py #Схема библиотекарей(Auth,Register)
│    └───reader.py #Схема читателей(Default,Update)
└───__init__.py
```
### Описание принятых решений по структуре БД
  Мной были определены 4 Таблицы

  - librarians (библиотекари)

            -   id — уникальный идентификатор (первичный ключ)

            -   email — электронная почта 

            -   hashed_password — хешированный пароль 



-  books (книги)

            -   id — уникальный идентификатор

            -   title — название книги 

            -   author — автор (максимум 60 символов)

            -   publication_year — год публикации 

            -   isbn — международный идентификатор книги 

            -   quantity — количество экземпляров в наличии



  - readers (читатели)

            -   id — уникальный идентификатор

            -   name — имя читателя 

            -   email — электронная почта 



- borrowed_books (взятые книги)
    ```
    Эта таблица была сделана мной как связующая по двум причинам:

                    - Учёт выданных книг:

                    Фиксирует, кто (reader_id), какую книгу (book_id) и когда (borrow_date) взял

                    - Отслеживает возврат (return_date)

                    бизнес-назначение:

                    - История действий(Позволяет анализировать популярность книг, задержки возврата и активность читателей)

  ```

            -   id — уникальный идентификатор записи

            -   book_id — ссылка на книгу (внешний ключ к books.id)

            -   reader_id — ссылка на читателя (внешний ключ к readers.id)

            -   borrow_date — дата взятия книги

            -   return_date — дата возврата (может быть NULL, если книга ещё не сдана)

## Обьяснение ключевых эндпоинтов
### Auth
  -   Post/auth/register - Регистрация админа( библиотекаря ) email,password(хэшируется в бд)
  -   Post/auth/login - Аутенфикация библиотекаря и получение Access токена для дальнейшней работы в системе(нужно ввести пароль введенный при регистрации и email)
      После получения Access Токена нужно авторизоваться по токену ( реализовано через jwt, Bearer auth )  -> после этого получен доступ ко всем защищенным эндпоинтам
      
### Books interaction
  -   Get/books/all_books - Получение всех доступных книг
  -   Post/books/load_book - Защищено jwt, Создание книги и занос ее в бд
  -   Patch/books/update_book - Защищено jwt,Обновление книги, изменение ранее созданных данных
  -   Delete/books/delete_book - Защищено jwt,Удаление книги
     
### Readers interaction - Защищено jwt
  -   Get/raeaders/get_all_readers - Получение всех созданных читателей
  -   Post/readers/create_reader - Создание читателя, пользователя
  -   Patch/readers/update_reader - Изменение данных читателя
  -   Delete/readers/delete_reader - Удаление читателя
    
### Borrowed interaction - Защищено jwt ( Записи о том кто взял и какую книгу ) 
  -   Get/borrowed/get_all_notes - Получение всех записей определленого юзера ( не вижу смысла выдавать сразу все записи, библиотекарю удобнее по определенному читателю смотреть ) 
  -   Post/borrowed/load_note - Создание Записи какой читатель взял какую книгу, и дата взятия
  -   Patch/borrowed/update_borrowed_note - Изменение записи( по сути возврат книги так же в какую дату была возвращена )
  -   Delete/borrowed/delete_borrowed_note - Удаление читателя( удаление записи )


## бизнес-логика обьяснение
### Получение информации ( Защита токеном эндпоинтов)
  - Защитил все ключевые эндпоинты кроме Получения всех книг( по моему мнению, пользователи юзающие приложение должны иметь доступ к просмотре доступных для заказа книг ), а все остальное лежит на администраторе( Библиотекаре ) тоесть выдача, обновление, возрват, добавление новых книг, удаление и тд. И соответсвенно защищено токеном
### Остальная логика 
  - 4.1 
```
 Книгу можно выдать, только если есть доступные экземпляры (количество экземпляров > 0). При выдаче количество экземпляров уменьшается на 1
```
  Решил эту задачу путем добавления в модель книги поля quantity,отвечающее за количество книг, при выдаче книги и создания записи происходит запись в таблицу borrowed_books,и выполняется условие в CRUD'е crud/borrow.py отвечающее за уменьшее количества книг ( по дефолту 1)
```Python 
        async def create_borrow(self, book_id: int, reader_id: int) -> BorrowedBook:
        book = await self.db.get(Book, book_id)
        active_borrows_count = await self.db.execute(
            select(count(BorrowedBook.id))
            .where(BorrowedBook.book_id == book_id)
            .where(BorrowedBook.return_date == None)
        )
        active_borrows_count = active_borrows_count.scalar()

        if book.quantity <= 0:
            raise ValueError("Книги закончились")

        active_borrows = await self.get_borrowed_books(reader_id)
        if len(active_borrows) >= 3:
            raise ValueError(
                "Пользователь уже взял 3 книги, верните хотя бы 1, что бы взять еще")

        book.quantity -= 1
        borrowed = BorrowedBook(
            book_id=book_id,
            reader_id=reader_id,
            borrow_date=datetime.now()
        )
        self.db.add(borrowed)
        await self.db.commit()
        await self.db.refresh(borrowed)
        return borrowed
```
  - 4.2
```
Один читатель не может взять более 3-х книг одновременно.
```

```
1 читатель не может взять больше 3-х книг, значит нужно написать условие, при котором считается количество уже взятых читателем книг, количество которых не должно привышать 3
```
-  Так же снизу часть круда создания записи выдачи книги, в котором происходит выборка по айдишнику читателя, и если количество книг превышает 3 -> выбрасывается ошибка что нужно вернуть хотя бы 1 книгу(Реализовал возврат через Patch запрос где автоматически с помощью datetime сохраняется время возврата книги по айдишнику записи(borrowed_book) )
```Python 
active_borrows_count = await self.db.execute(
            select(count(BorrowedBook.id))
            .where(BorrowedBook.book_id == book_id)
            .where(BorrowedBook.return_date == None)
        )
        active_borrows_count = active_borrows_count.scalar()

        if book.quantity <= 0:
            raise ValueError("Книги закончились")

        active_borrows = await self.get_borrowed_books(reader_id)
        if len(active_borrows) >= 3:
            raise ValueError(
                "Пользователь уже взял 3 книги, верните хотя бы 1, что бы взять еще")
```
- 4.3
```
Нельзя вернуть книгу, которая не была выдана этому читателю или уже возвращена
```
Нужно написать условие при котором будет селектиться запись взятой книги учитывай (reader_id) , (book_id) и сравниваться есть ли такая книга по айдишнику в теле записи? 

```Python
async def update_borrow_note(
    self, 
    reader_id: int, 
    book_id: int,
    borrow_data: BorrowUpdate
    ) -> BorrowedBook:
    
        result = await self.db.execute( # -> Ключевой момент данного круда для реализации всей логике проверки есть ли такая книга в записи
        select(BorrowedBook)
        .where(BorrowedBook.reader_id == reader_id)
        .where(BorrowedBook.book_id == book_id) 
        .where(BorrowedBook.return_date == None)
        )
        borrowed = result.scalars().first()

        if not borrowed:
            raise HTTPException(
                status_code=404,
                detail="Активная запись о взятии этой книги не найдена для данного читателя"
            )

    
        if borrowed.return_date is not None:
            raise HTTPException(
                status_code=400,
                detail="Эта книга уже была возвращена"
            )

    
        update_data = borrow_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(borrowed, key, value)

    
        book = await self.db.get(Book, book_id)
        book.quantity += 1

        await self.db.commit()
        await self.db.refresh(borrowed)

        return borrowed
```
