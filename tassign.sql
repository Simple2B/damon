USE [BurtonTrucking]
GO

/****** Object:  Table [dbo].[tassign]    Script Date: 10/21/2020 6:17:12 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

DROP TABLE [dbo].[tassign]
GO

CREATE TABLE [dbo].[tassign](
	[assignID] [int] NOT NULL,
	[TicketID] [int] NOT NULL,
	[Loads] [varchar](20) NULL,
	[Status] [char](9) NULL,
 CONSTRAINT [PK_tassign] PRIMARY KEY CLUSTERED
(
	[assignID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[tassign]  WITH CHECK ADD  CONSTRAINT [FK_tassign_tTickets] FOREIGN KEY([TicketID])
REFERENCES [dbo].[tTickets] ([TicketID])
GO

ALTER TABLE [dbo].[tassign] CHECK CONSTRAINT [FK_tassign_tTickets]
GO


