CREATE USER utilizator WITH ENCRYPTED PASSWORD 'utilizator';
GRANT ALL ON DATABASE django_magazin_par TO utilizator;
ALTER ROLE utilizator SET search_path = django, public;
GRANT ALL ON SCHEMA django TO utilizator;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA django TO utilizator;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA django TO utilizator;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA django TO utilizator;