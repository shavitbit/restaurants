CREATE TABLE [dbo].[restaurantTable] (
    [id]              INT          IDENTITY (1, 1) NOT NULL,
    [restaurantName]  VARCHAR (50) NOT NULL,
    [restaurantStyle] VARCHAR (50) NULL,
    [vegetarian]      BIT          NULL,
    [deliveries]      BIT          NULL,
    [timeOpen]        TIME (7)     NULL,
    [timeClose]       TIME (7)     NULL,
    CONSTRAINT [PK_restaurantTable] PRIMARY KEY CLUSTERED ([id] ASC)
);


GO
