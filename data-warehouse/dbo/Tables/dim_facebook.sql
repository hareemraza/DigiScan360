CREATE TABLE [dbo].[dim_facebook] (

	[page_id] varchar(255) NOT NULL, 
	[name] varchar(255) NULL, 
	[username] varchar(255) NULL, 
	[contact_address] varchar(255) NULL, 
	[current_location] varchar(255) NULL
);


GO
ALTER TABLE [dbo].[dim_facebook] ADD CONSTRAINT pk_dim_facebook_page_id primary key NONCLUSTERED ([page_id]);