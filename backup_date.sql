--
-- PostgreSQL database dump
--

\restrict xfaMlsBbdAnBALkr1gPEZJFDAzQT4ufY5atcfbJ7sAEMLxcj5WNKWWeXNOblHK4

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: Magazin_produse_par_ambalaj; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_customuser; Type: TABLE DATA; Schema: django; Owner: utilizator
--

INSERT INTO django."Magazin_produse_par_customuser" (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, telefon, tara, judet) VALUES (1, 'pbkdf2_sha256$1500000$Xi6ahDO36YQ2F3U3csFPfe$QVwOagauQLottk5r8C2EGXNq0SVxoT22UoaBuDeOGAU=', NULL, true, 'admin', '', '', 'lucautilizator675@gmail.com', true, true, '2026-11-24 11:23:33.550416+02', NULL, NULL, NULL);


--
-- Data for Name: Magazin_produse_par_angajat; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_brand; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_categorie; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_comanda; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_produs; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_comandaprodus; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_customuser_groups; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_customuser_user_permissions; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_departament; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_ingredient; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_listafavorite; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_listafavoriteprodus; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_produs_ingrediente; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_promotie; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_produs_promotii; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_profil; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_review; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_voucher; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_utilizatorvoucher; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Data for Name: Magazin_produse_par_variantaprodus; Type: TABLE DATA; Schema: django; Owner: utilizator
--



--
-- Name: Magazin_produse_par_ambalaj_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_ambalaj_id_seq"', 16, true);


--
-- Name: Magazin_produse_par_angajat_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_angajat_id_seq"', 1, false);


--
-- Name: Magazin_produse_par_brand_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_brand_id_seq"', 5, true);


--
-- Name: Magazin_produse_par_categorie_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_categorie_id_seq"', 6, true);


--
-- Name: Magazin_produse_par_comanda_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_comanda_id_seq"', 1, false);


--
-- Name: Magazin_produse_par_comandaprodus_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_comandaprodus_id_seq"', 1, false);


--
-- Name: Magazin_produse_par_customuser_groups_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_customuser_groups_id_seq"', 1, false);


--
-- Name: Magazin_produse_par_customuser_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_customuser_id_seq"', 1, true);


--
-- Name: Magazin_produse_par_customuser_user_permissions_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_customuser_user_permissions_id_seq"', 1, false);


--
-- Name: Magazin_produse_par_departament_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_departament_id_seq"', 1, false);


--
-- Name: Magazin_produse_par_ingredient_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_ingredient_id_seq"', 5, true);


--
-- Name: Magazin_produse_par_listafavorite_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_listafavorite_id_seq"', 1, false);


--
-- Name: Magazin_produse_par_listafavoriteprodus_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_listafavoriteprodus_id_seq"', 1, false);


--
-- Name: Magazin_produse_par_produs_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_produs_id_seq"', 10, true);


--
-- Name: Magazin_produse_par_produs_ingrediente_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_produs_ingrediente_id_seq"', 15, true);


--
-- Name: Magazin_produse_par_produs_promotii_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_produs_promotii_id_seq"', 8, true);


--
-- Name: Magazin_produse_par_profil_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_profil_id_seq"', 1, false);


--
-- Name: Magazin_produse_par_promotie_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_promotie_id_seq"', 5, true);


--
-- Name: Magazin_produse_par_review_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_review_id_seq"', 1, false);


--
-- Name: Magazin_produse_par_utilizatorvoucher_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_utilizatorvoucher_id_seq"', 1, false);


--
-- Name: Magazin_produse_par_variantaprodus_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_variantaprodus_id_seq"', 5, true);


--
-- Name: Magazin_produse_par_voucher_id_seq; Type: SEQUENCE SET; Schema: django; Owner: utilizator
--

SELECT pg_catalog.setval('django."Magazin_produse_par_voucher_id_seq"', 1, false);


--
-- PostgreSQL database dump complete
--

\unrestrict xfaMlsBbdAnBALkr1gPEZJFDAzQT4ufY5atcfbJ7sAEMLxcj5WNKWWeXNOblHK4

