@ECHO OFF
IF EXIST backup_date.sql DEL backup_date.sql
SET PGPASSWORD=admin

pg_dump --column-inserts --data-only --inserts -h localhost -U utilizator -p 5432 -d django_magazin_par -n django --exclude-table="django.django_*" --exclude-table="django.auth_*" > backup_date.sql

SET PGPASSWORD=
ECHO Backup curat finalizat!
PAUSE