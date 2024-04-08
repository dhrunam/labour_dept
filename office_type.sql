PGDMP      1                |            labour_dept_db    16.2    16.2     h           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            i           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            j           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            k           1262    17268    labour_dept_db    DATABASE     p   CREATE DATABASE labour_dept_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
    DROP DATABASE labour_dept_db;
                postgres    false            �            1259    17300    master_officetype    TABLE     �   CREATE TABLE public.master_officetype (
    id bigint NOT NULL,
    type character varying(128) NOT NULL,
    short_name character varying(5),
    is_deleted boolean NOT NULL
);
 %   DROP TABLE public.master_officetype;
       public         heap    postgres    false            �            1259    17299    master_officetype_id_seq    SEQUENCE     �   ALTER TABLE public.master_officetype ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.master_officetype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    222            e          0    17300    master_officetype 
   TABLE DATA           M   COPY public.master_officetype (id, type, short_name, is_deleted) FROM stdin;
    public          postgres    false    222          l           0    0    master_officetype_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.master_officetype_id_seq', 1, true);
          public          postgres    false    221            �           2606    17304 (   master_officetype master_officetype_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.master_officetype
    ADD CONSTRAINT master_officetype_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.master_officetype DROP CONSTRAINT master_officetype_pkey;
       public            postgres    false    222            �           2606    17308 2   master_officetype master_officetype_short_name_key 
   CONSTRAINT     s   ALTER TABLE ONLY public.master_officetype
    ADD CONSTRAINT master_officetype_short_name_key UNIQUE (short_name);
 \   ALTER TABLE ONLY public.master_officetype DROP CONSTRAINT master_officetype_short_name_key;
       public            postgres    false    222            �           2606    17306 ,   master_officetype master_officetype_type_key 
   CONSTRAINT     g   ALTER TABLE ONLY public.master_officetype
    ADD CONSTRAINT master_officetype_type_key UNIQUE (type);
 V   ALTER TABLE ONLY public.master_officetype DROP CONSTRAINT master_officetype_type_key;
       public            postgres    false    222            �           1259    17322 *   master_officetype_short_name_e0b289e7_like    INDEX     �   CREATE INDEX master_officetype_short_name_e0b289e7_like ON public.master_officetype USING btree (short_name varchar_pattern_ops);
 >   DROP INDEX public.master_officetype_short_name_e0b289e7_like;
       public            postgres    false    222            �           1259    17321 $   master_officetype_type_c3dd076a_like    INDEX     v   CREATE INDEX master_officetype_type_c3dd076a_like ON public.master_officetype USING btree (type varchar_pattern_ops);
 8   DROP INDEX public.master_officetype_type_c3dd076a_like;
       public            postgres    false    222            e   $   x�3�t�,.)�L.Q�OK�LN�t��L����� ~��     