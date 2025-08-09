# Подключение к VPS через SSH (Yandex Cloud)

## Шаги:
1. Сгенерирован SSH-ключ:
ssh-keygen -t ed25519 -C "ваш_email@example.com"

2. Ключ добавлен в метаданные VM:
- `user-data` с cloud-config
- поле `ssh-keys`

3. Подключение проверено:
ssh -i ~/.ssh/id_ed25519 ubuntu@<IP>

✅ Подключение прошло успешно.


