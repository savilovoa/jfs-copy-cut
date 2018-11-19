DECLARE @DBName nvarchar(100)
SET @DBName = '$(newDB)'
--проверка на существование БД
if db_id(@DBName) is null return

--БД 1С
exec('use '+@DBName);
DECLARE @date_trim datetime=N'$(dat)'; --дата, до которой удалять документы
set @date_trim = DATEADD(YEAR, 2000, @date_trim); -- в 1С используется смещение дат на 2000

exec('truncate table ['+@DBName+'].[dbo].[_InfoRg43447]'); --очистка РегистрСведений.ВерсииОбъектов
exec('truncate table ['+@DBName+'].[dbo].[_InfoRgChngR43467]'); --очистка РегистрСведений.ВерсииОбъектов.Изменения
DECLARE @sql VARCHAR(MAX) ,
	@tablename VARCHAR(MAX)
DECLARE @Deleted_Rows INT;
--удаление документов из РегистрСведений.РеестрДокументов
if object_id(@DBName+'[dbo].[_InfoRg67845]') is not null
begin
	set @sql='delete from ['+@DBName+'].dbo._InfoRg67845 where _Fld67864 < ''' + convert(varchar(25), @date_trim, 120)+'''';
	exec(@sql);
end;
--очистка РегистрСведений.РеестрДокументов.Изменения
if object_id(@DBName+'[dbo].[_InfoRgChngR67877]') is not null
	exec('truncate table ['+@DBName+'].[dbo].[_InfoRgChngR67877]');
DECLARE doc CURSOR FOR 
--отбор таблиц для обработки
SELECT distinct tab.name
FROM sys.tables tab
inner join sys.columns col
	on col.object_id = tab.object_id
WHERE type='U'
	and ((col.name='_Period' AND ((tab.name LIKE '%AccumRg%' and tab.name not LIKE '%AccumRgAggDict%') or (tab.name LIKE '%InfoRg%' and tab.name not LIKE '%InfoRgOpt%')
			or tab.name LIKE '%AccRg%'))
	or (col.name='_date_time' AND tab.name LIKE '%Document%') or tab.name like '%Document%_VT%')
OPEN doc
FETCH NEXT FROM doc 
INTO @tablename
WHILE @@FETCH_STATUS = 0 
	BEGIN
		if @tablename not like '%Document%_VT%'
			if @tablename not like '%Document%'
				SET @sql = 'delete TOP (10000) from ['+@DBName+'].dbo.[' + @tablename + '] where [_Period] < ''' + convert(varchar(25), @date_trim, 120)+''''
				--SET @sql = 'select * from [' + @tablename + '] where [_Period] < ''' + convert(varchar(25), @date_trim, 120)+''''
			else
				SET @sql = 'delete TOP (10000) from ['+@DBName+'].dbo.[' + @tablename + '] where [_date_time] < ''' + convert(varchar(25), @date_trim, 120)+''''
				--SET @sql = 'select * from [' + @tablename + '] where [_date_time] < ''' + convert(varchar(25), @date_trim, 120)+''''
		else
			SET @sql = 'delete TOP (10000) from SubData from ['+@DBName+'].dbo.[' + @tablename + '] SubData left join ['+@DBName+'].dbo.['+ substring(@tablename,1,charindex('_VT',@tablename)-1) + '] MainData on SubData.' + substring(@tablename,1,charindex('_VT',@tablename)-1) + '_IDRRef = MainData._IDRRef WHERE MainData._IDRRef IS NULL'
			--SET @sql = 'select * from [' + @tablename + '] SubData left join ['+ substring(@tablename,1,charindex('_VT',@tablename)-1) + '] MainData on SubData.' + substring(@tablename,1,charindex('_VT',@tablename)-1) + '_IDRRef = MainData._IDRRef WHERE MainData._IDRRef IS NULL'
		--PRINT @sql
		SET @Deleted_Rows = 1;
		WHILE (@Deleted_Rows > 0)
		BEGIN
			BEGIN TRANSACTION
			-- Delete some small number of rows at a time
			EXEC (@sql)
			SET @Deleted_Rows = @@ROWCOUNT;
			COMMIT TRANSACTION
			CHECKPOINT -- for simple recovery model
		END
		FETCH NEXT
	FROM doc
	INTO @tablename
	END
CLOSE doc
DEALLOCATE doc
--Сжимаем базу данных
exec ('ALTER DATABASE ['+@DBName+'] SET RECOVERY SIMPLE');
declare @t varchar(500)
set @t = ''
select @t = name FROM sys.database_files WHERE physical_name LIKE '%LDF%'

DBCC SHRINKFILE (@t, 5)

exec ('ALTER DATABASE ['+@DBName+'] SET RECOVERY SIMPLE');

DBCC SHRINKDATABASE(@DBName)