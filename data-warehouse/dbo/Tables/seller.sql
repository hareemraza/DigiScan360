CREATE TABLE [dbo].[seller] (

	[SellerID] varchar(8000) NOT NULL
);


GO
ALTER TABLE [dbo].[seller] ADD CONSTRAINT pk_seller_sellerid primary key NONCLUSTERED ([SellerID]);