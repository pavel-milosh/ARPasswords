��          �      |      �     �     �  	   �  
             "  
   4     ?     R     e     |     �     �  
   �  	   �     �     �     �  	   �     �     �  U     (   b  ,   �  �   �  G   A  7   �  `   �  "   "  3   E  �   y  0   >  !   o  �   �  2   .     a  ,   w  �   �  4  P  �   �  _     (   k  �  �            
                                                              	                       add backup backup_db backup_log backup_uploading backup_very_large delete_all delete_all_deleted delete_all_message delete_all_not_deleted generate_passwords generate_passwords_message key key_button key_enter key_installed key_message key_not_installed key_wrong show start_message Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Language: ru
 Добавить новую запись Создать резервную копию Файл базы данных. <b>Все данные в нем зашифрованы Вашим ключом шифрования</b> Файл журнала. Используется для отладки Резервная копия загружается... Файл базы данных слишком большой для отправки в Telegram Удалить все записи <b>Все данные были удалены!</b> Вы действительно хотите <b>безвозвратно удалить все записи?</b> Для подтверждения введите: <code>delete_all {user_id}</code> Данные <b>не</b> были удалены Генерация паролей Ваши сгенерированные пароли:
{passwords}

<i>Сообщение автоматически удалится через 1 час</i> Настройка ключа шифрования Ввести ключ Введите ключ шифрования Ключ <code>{key}</code> установлен. Сообщение удалится через 10 секунд. <b>Не забудьте сохранить ключ!</b> <b>Ключ шифрования:</b>
				Текущий: <tg-spoiler>{key}</tg-spoiler>
				Время сброса пароля: <code>{time}</code>

Ключ шифрования - уникальная символьная комбинация, служащая для защиты Ваших записей. Единственным требованием является минимальная длина в 8 символов. В целях безопасности ключ необходимо вводить заново каждые 24 часа
<b>ВНИМАНИЕ! Обязательно используйте один и тот же ключ, чтобы не потерять доступ к данным!</b>

<i>Сообщение автоматически удалится через 2 минуты</i> Ключ шифрования не установлен. Для установки воспользуйтесь командой /key Ключ шифрования не совпадает с установленным ранее! Отобразить все записи Здравствуйте, {name}! Я - менеджер паролей <b>ARPasswords</b>
Прежде чем начать создайте надежный ключ шифрования (master пароль) и добавьте его с помощью команды /key. После этого Вы сможете добавить запись, используя команду /add_record 