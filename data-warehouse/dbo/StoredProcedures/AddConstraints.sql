CREATE PROCEDURE AddConstraints
AS
BEGIN
    -- Step 1: Add Primary Key to dim_products
    ALTER TABLE dim_products
    ADD CONSTRAINT pk_dim_products_ProductID PRIMARY KEY NONCLUSTERED (ProductID) NOT ENFORCED;

    -- Step 2: Add Composite Primary Key to fact_products
    ALTER TABLE fact_products
    ADD CONSTRAINT pk_fact_products PRIMARY KEY NONCLUSTERED (ProductID, date_accessed) NOT ENFORCED;

    -- Step 3: Add Primary Key to dim_time
    ALTER TABLE dim_time
    ADD CONSTRAINT pk_dim_time_date PRIMARY KEY NONCLUSTERED (date) NOT ENFORCED;

    -- Step 4: Add Foreign Key to fact_reviews to reference dim_products
    ALTER TABLE fact_reviews
    ADD CONSTRAINT pk_fact_reviews_id PRIMARY KEY NONCLUSTERED (id) NOT ENFORCED;

    -- Step 5: Add Foreign Key to fact_reviews to reference dim_products
    ALTER TABLE fact_reviews
    ADD CONSTRAINT fk_fact_reviews_ProductID FOREIGN KEY (ProductID)
    REFERENCES dim_products(ProductID) NOT ENFORCED;

    -- Step 6: Add Foreign Key to dim_products to reference seller
    ALTER TABLE dim_products
    ADD CONSTRAINT fk_seller FOREIGN KEY (SellerID)
    REFERENCES seller(SellerID) NOT ENFORCED;

    -- Step 7: Add Foreign Key to fact_products to reference dim_products
    ALTER TABLE fact_products
    ADD CONSTRAINT fk_fact_products_ProductID FOREIGN KEY (ProductID)
    REFERENCES dim_products(ProductID) NOT ENFORCED;

    -- Step 8: Add Foreign Key to fact_products to reference dim_time
    ALTER TABLE fact_products
    ADD CONSTRAINT fk_fact_products_date_accessed FOREIGN KEY (date_accessed)
    REFERENCES dim_time(date) NOT ENFORCED;

    -- Step 9: Add Foreign Key to fact_reviews to reference dim_time
    ALTER TABLE fact_reviews
    ADD CONSTRAINT fk_fact_reviews_date FOREIGN KEY (date)
    REFERENCES dim_time(date) NOT ENFORCED;
END;