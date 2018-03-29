# Altering a field with a unique constraint drops and rebuilds FKs to other fields in the table

https://code.djangoproject.com/ticket/29193

Repro Requirements

- python 3.6
- Postgresql 9.6.2

```bash
# start with django 1.8.17 and psycopg2
pipenv install
createuser -s bug_29193
createdb --owner=bug_29193 bug_29193

# do initial migrations including a custom user model inheriting from
# AbstractUser
python manage.py migrate

pipenv install django==1.11.11
python manage.py makemigrations dogs -n abstract_user_alter_username_max_length
python manage.py sqlmigrate dogs 0002_abstract_user_alter_username_max_length
```

on django 1.10.8

```sql
BEGIN;
--
-- Alter field username on user
--
ALTER TABLE "dogs_user" ALTER COLUMN "username" TYPE varchar(150) USING "username"::varchar(150);
COMMIT;
```

on django 1.11.11

```sql
BEGIN;
--
-- Alter field username on user
--
SET CONSTRAINTS "dogs_dog_user_id_4b101eabdd3a8c85_fk_dogs_user_id" IMMEDIATE; ALTER TABLE "dogs_dog" DROP CONSTRAINT "dogs_dog_user_id_4b101eabdd3a8c85_fk_dogs_user_id";
ALTER TABLE "dogs_user" ALTER COLUMN "username" TYPE varchar(150) USING "username"::varchar(150);
ALTER TABLE "dogs_dog" ADD CONSTRAINT "dogs_dog_user_id_54f88662_fk" FOREIGN KEY ("user_id") REFERENCES "dogs_user" ("id") DEFERRABLE INITIALLY DEFERRED;
COMMIT;
```