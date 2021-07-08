/* Init for for demo environment
*/

DROP TABLE IF EXISTS consent_europe;

-- Table: consent_europe
CREATE TABLE IF NOT EXISTS consent_europe(
    email TEXT NOT NULL, 
    consent char NOT NULL 
    );

DROP TABLE IF EXISTS customer;

-- Table: customer
CREATE TABLE customer (
    id int GENERATED ALWAYS AS IDENTITY,
    customer_name varchar(255)  NOT NULL,
    policy_version_id int  NOT NULL,
    customer_address varchar(255)  NOT NULL,
    customer_email varchar(255) NOT NULL,
    ts_inserted timestamp NOT NULL
);


INSERT INTO customer (customer_name, policy_version_id, customer_address, customer_email, ts_inserted) VALUES ('Jewelry Store', 4, 'Long Street 120', 'abc@gmail.com', '2020/1/9 14:1:20');
INSERT INTO customer (customer_name, policy_version_id, customer_address, customer_email, ts_inserted) VALUES ('Bakery', 1, 'Kurfürstendamm 25', 'news@bbc.com', '2020/1/9 17:52:15');
INSERT INTO customer (customer_name, policy_version_id, customer_address, customer_email, ts_inserted) VALUES ('Café', 1, 'Tauentzienstraße 44', 'qwe@yahoo.com', '2020/1/10 8:2:49');
INSERT INTO customer (customer_name, policy_version_id, customer_address, customer_email, ts_inserted) VALUES ('Restaurant', 3, 'Ulica lipa 15', 'ajshd@gmail.com', '2020/1/10 9:20:21');
