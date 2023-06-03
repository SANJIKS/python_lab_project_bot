import telebot #pytelegrambotapi
from telebot import types

class TodoBot:
    def __init__(self):
        self.bot = telebot.TeleBot('Your Token')
        self.tasks = {}
        self.register_handlers()


    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start_handler(message):
            self.bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=self.show_menu())


        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            chat_id = call.message.chat.id
            if call.data == 'read':
                self.read_todos(chat_id)
            elif call.data == 'retrieve':
                self.retrieve_todo(chat_id)
            elif call.data == 'create':
                self.create_todo(chat_id)
            elif call.data == 'update':
                self.update_todo(chat_id)
            elif call.data == 'delete':
                self.delete_todo(chat_id)
            elif call.data == 'completed':
                self.completed_todo(chat_id)


    def show_menu(self):
        markup = types.InlineKeyboardMarkup(row_width=2)
        read_button = types.InlineKeyboardButton(text='Read', callback_data='read')
        retrieve_button = types.InlineKeyboardButton(text='Retrieve', callback_data='retrieve')
        create_button = types.InlineKeyboardButton(text='Create', callback_data='create')
        update_button = types.InlineKeyboardButton(text='Update', callback_data='update')
        delete_button = types.InlineKeyboardButton(text='Delete', callback_data='delete')
        completed_button = types.InlineKeyboardButton(text='Completed?', callback_data='completed')
        markup.add(read_button, retrieve_button, create_button, update_button, delete_button, completed_button)
        return markup


    def read_todos(self, chat_id):
        if chat_id in self.tasks and self.tasks[chat_id]:
            task_list = '\n'.join(f"ID: {task['id']}, Текст: {task['text']}, Выполнено: {task['completed']}" for task in self.tasks[chat_id])
            self.bot.send_message(chat_id, f'TODOS:\n{task_list}', reply_markup=self.show_menu())
        else:
            self.bot.send_message(chat_id, 'Ваш список TODO пуст!', reply_markup=self.show_menu())



    def retrieve_todo(self, chat_id):
        self.bot.send_message(chat_id, 'Введите ID:')
        self.bot.register_next_step_handler_by_chat_id(chat_id, self.retrieve_todo_step)


    def retrieve_todo_step(self, message):
        chat_id = message.chat.id
        task_id = message.text.strip()
        if chat_id in self.tasks:
            task = next((task for task in self.tasks[chat_id] if task['id'] == task_id), None)
            if task:
                task_text = f"ID: {task['id']}, Текст: {task['text']}, Выполнено: {task['completed']}"
                self.bot.send_message(chat_id, f'Task:\n{task_text}', reply_markup=self.show_menu())
            else:
                self.bot.send_message(chat_id, 'TODO не найдено', reply_markup=self.show_menu())
        else:
            self.bot.send_message(chat_id, 'TODO не найдено', reply_markup=self.show_menu())


    def create_todo(self, chat_id):
        self.bot.send_message(chat_id, 'Введите текст:')
        self.bot.register_next_step_handler_by_chat_id(chat_id, self.create_todo_step)


    def create_todo_step(self, message):
        chat_id = message.chat.id
        task_text = message.text.strip()
        if chat_id not in self.tasks:
            self.tasks[chat_id] = []

        task_id = str(len(self.tasks[chat_id]) + 1)
        task = {'id': task_id, 'text': task_text, 'completed': False}
        self.tasks[chat_id].append(task)
        self.bot.send_message(chat_id, 'TODO успешно создан!\nВыберите следующее действие:', reply_markup=self.show_menu())


    def update_todo(self, chat_id):
        self.bot.send_message(chat_id, 'Введите ID:')
        self.bot.register_next_step_handler_by_chat_id(chat_id, self.update_todo_step)


    def update_todo_step(self, message):
        chat_id = message.chat.id
        task_id = message.text.strip()
        if chat_id in self.tasks:
            task = next((task for task in self.tasks[chat_id] if task['id'] == task_id), None)
            if task:
                self.bot.send_message(chat_id, 'Введите новое название:')
                self.bot.register_next_step_handler_by_chat_id(chat_id, self.update_todo_text_step, task)
            else:
                self.bot.send_message(chat_id, 'TODO не найдено', reply_markup=self.show_menu())
        else:
            self.bot.send_message(chat_id, 'TODO не найдено', reply_markup=self.show_menu())


    def update_todo_text_step(self, message, task):
        chat_id = message.chat.id
        task_text = message.text.strip()
        task['text'] = task_text
        self.bot.send_message(chat_id, 'Успешно обновлено!\nВыберите следующее действие:', reply_markup=self.show_menu())


    def delete_todo(self, chat_id):
        self.bot.send_message(chat_id, 'Введите ID:')
        self.bot.register_next_step_handler_by_chat_id(chat_id, self.delete_todo_step)


    def delete_todo_step(self, message):
        chat_id = message.chat.id
        task_id = message.text.strip()
        if chat_id in self.tasks:
            task = next((task for task in self.tasks[chat_id] if task['id'] == task_id), None)
            if task:
                self.tasks[chat_id].remove(task)
                self.bot.send_message(chat_id, 'Успешно удалено!\nВыберите следующее действие:', reply_markup=self.show_menu())
            else:
                self.bot.send_message(chat_id, 'TODO не найдено', reply_markup=self.show_menu())
        else:
            self.bot.send_message(chat_id, 'TODO не найдено', reply_markup=self.show_menu())

    
    def completed_todo(self, chat_id):
        self.bot.send_message(chat_id, 'Введите ID:')
        self.bot.register_next_step_handler_by_chat_id(chat_id, self.completed_todo_step)


    def completed_todo_step(self, message):
        chat_id = message.chat.id
        task_id = message.text.strip()
        if chat_id in self.tasks:
            task = next((task for task in self.tasks[chat_id] if task['id'] == task_id), None)
            if task:
                task['completed'] = True
                self.bot.send_message(chat_id, 'Задача выполнена!', reply_markup=self.show_menu())
            else:
                self.bot.send_message(chat_id, 'TODO не найдено', reply_markup=self.show_menu())
        else:
            self.bot.send_message(chat_id, 'TODO не найдено', reply_markup=self.show_menu())



    def run(self):
        self.bot.polling()


if __name__ == '__main__':
    todos = TodoBot()
    todos.run()

