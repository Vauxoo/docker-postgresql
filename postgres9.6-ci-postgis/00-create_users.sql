 DO
    $body$
    BEGIN
        CREATE ROLE odoo LOGIN PASSWORD 'odoo' SUPERUSER;
        EXCEPTION WHEN others THEN
            RAISE NOTICE 'odoo role exists, not re-creating';
    END
    $body$