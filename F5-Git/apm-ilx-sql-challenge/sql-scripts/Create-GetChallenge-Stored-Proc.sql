SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[GetChallenge]
AS

DECLARE @SelectedId INT;
SELECT TOP 1 @SelectedId = Id FROM Challenges ORDER BY NEWID();

UPDATE Challenges
  SET LastUsed = GETDATE() 
OUTPUT INSERTED.* 
  WHERE Id = @SelectedId;

  
GO
