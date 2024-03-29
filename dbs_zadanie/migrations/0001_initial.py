# Generated by Django 3.1 on 2021-04-03 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunSQL('''CREATE TABLE ov.companies
                                (
                                    cin bigint not null
                                        primary key,
                                    name varchar,
                                    br_section varchar,
                                    address_line varchar,
                                    last_update timestamp without time zone,
                                    created_at timestamp without time zone,
                                    updated_at timestamp without time zone
                                );
                                
                                
                                with temporary_table as (
                                    select cin,
                                    corporate_body_name,
                                    br_section,
                                    street || ' , ' || postal_code || ' ' || city as address,
                                    updated_at,
                                    row_number() over (partition by cin order by updated_at desc) as row_number
                                from ov.or_podanie_issues)
                                
                                INSERT INTO ov.companies (cin, name, br_section, address_line, last_update, created_at, updated_at)
                                SELECT cin,
                                    corporate_body_name,
                                    br_section,
                                    address,
                                    updated_at,
                                    now(),
                                    now()
                                FROM temporary_table
                                WHERE cin is not null AND row_number = 1
                                ON CONFLICT do nothing;
                                
                                
                                
                                with temporary_table as (
                                    select cin,
                                    corporate_body_name,
                                    br_section,
                                    street || ' , ' || postal_code || ' ' || city as address,
                                    updated_at,
                                    row_number() over (partition by cin order by updated_at desc) as row_number
                                from ov.likvidator_issues)
                                
                                INSERT INTO ov.companies (cin, name, br_section, address_line, last_update, created_at, updated_at)
                                SELECT cin,
                                    corporate_body_name,
                                    br_section,
                                    address,
                                    updated_at,
                                    now(),
                                    now()
                                FROM temporary_table
                                WHERE cin is not null AND row_number = 1
                                ON CONFLICT do nothing;
                                
                                
                                
                                with temporary_table as (
                                    select cin,
                                    corporate_body_name,
                                    null as br_section,
                                    street || ' , ' || postal_code || ' ' || city as address,
                                    updated_at,
                                    row_number() over (partition by cin order by updated_at desc) as row_number
                                from ov.konkurz_vyrovnanie_issues)
                                
                                INSERT INTO ov.companies (cin, name, br_section, address_line, last_update, created_at, updated_at)
                                SELECT cin,
                                    corporate_body_name,
                                    br_section,
                                    address,
                                    updated_at,
                                    now(),
                                    now()
                                FROM temporary_table
                                WHERE cin is not null AND row_number = 1
                                ON CONFLICT do nothing;
                                
                                
                                
                                with temporary_table as (
                                    select cin,
                                    corporate_body_name,
                                    br_section,
                                    street || ' , ' || postal_code || ' ' || city as address,
                                    updated_at,
                                    row_number() over (partition by cin order by updated_at desc) as row_number
                                from ov.znizenie_imania_issues)
                                
                                INSERT INTO ov.companies (cin, name, br_section, address_line, last_update, created_at, updated_at)
                                SELECT cin,
                                    corporate_body_name,
                                    br_section,
                                    address,
                                    updated_at,
                                    now(),
                                    now()
                                FROM temporary_table
                                WHERE cin is not null AND row_number = 1
                                ON CONFLICT do nothing;
                                
                                
                                
                                with temporary_table as (
                                    select cin,
                                    corporate_body_name,
                                    null as br_section,
                                    street || ' , ' || postal_code || ' ' || city as address,
                                    updated_at,
                                    row_number() over (partition by cin order by updated_at desc) as row_number
                                from ov.konkurz_restrukturalizacia_actors)
                                
                                INSERT INTO ov.companies (cin, name, br_section, address_line, last_update, created_at, updated_at)
                                SELECT cin,
                                    corporate_body_name,
                                    br_section,
                                    address,
                                    updated_at,
                                    now(),
                                    now()
                                FROM temporary_table
                                WHERE cin is not null AND row_number = 1
                                ON CONFLICT do nothing;
                                
                                
                                ALTER TABLE ov.or_podanie_issues
                                ADD column company_id bigint,
                                ADD foreign key (company_id)
                                REFERENCES ov.companies(cin);
                                
                                UPDATE ov.or_podanie_issues
                                SET company_id = cin
                                where cin is not null;
                                
                                ALTER TABLE ov.likvidator_issues
                                    ADD column company_id bigint,
                                    add foreign key (company_id)
                                REFERENCES ov.companies(cin);
                                
                                UPDATE ov.likvidator_issues
                                SET company_id = cin
                                where cin is not null;
                                
                                ALTER TABLE ov.konkurz_vyrovnanie_issues
                                    ADD column company_id bigint,
                                    add foreign key (company_id)
                                REFERENCES ov.companies(cin);
                                
                                UPDATE ov.konkurz_vyrovnanie_issues
                                SET company_id = cin
                                where cin is not null;
                                
                                ALTER TABLE ov.znizenie_imania_issues
                                    ADD column company_id bigint,
                                    add foreign key (company_id)
                                REFERENCES ov.companies(cin);
                                
                                UPDATE ov.znizenie_imania_issues
                                SET company_id = cin
                                where cin is not null;
                                
                                ALTER TABLE ov.konkurz_restrukturalizacia_actors
                                    ADD column company_id bigint,
                                    add foreign key (company_id)
                                REFERENCES ov.companies(cin);
                                
                                UPDATE ov.konkurz_restrukturalizacia_actors
                                SET company_id = cin
                                where cin is not null;''')
    ]
