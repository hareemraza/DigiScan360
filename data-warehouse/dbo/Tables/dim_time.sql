CREATE TABLE [dbo].[dim_time] (

	[date] date NOT NULL, 
	[day] int NULL, 
	[month] int NULL, 
	[year] int NULL, 
	[quarter] int NULL
);


GO
ALTER TABLE [dbo].[dim_time] ADD CONSTRAINT pk_dim_time_date primary key NONCLUSTERED ([date]);