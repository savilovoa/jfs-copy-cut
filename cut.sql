use $(newDB); --БД 1С
DECLARE @date_trim datetime=N'$(dat)'; --дата, до которой удалять документы
set @date_trim = DATEADD(YEAR, 2000, @date_trim); -- в 1С используется смещение дат на 2000

truncate table [dbo].[_InfoRg43447]; --очистка РегистрСведений.ВерсииОбъектов
truncate table [dbo].[_InfoRgChngR43467]; --очистка РегистрСведений.ВерсииОбъектов.Изменения
DECLARE @sql VARCHAR(MAX) ,
    @tablename VARCHAR(MAX)
--удаление документов из РегистрСведений.РеестрДокументов
set @sql='delete from _InfoRg67845 where _Fld67864 < ''' + convert(varchar(25), @date_trim, 120)+'''';
exec(@sql);
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
				SET @sql = 'delete from [' + @tablename + '] where [_Period] < ''' + convert(varchar(25), @date_trim, 120)+''''
				--SET @sql = 'select * from [' + @tablename + '] where [_Period] < ''' + convert(varchar(25), @date_trim, 120)+''''
			else
				SET @sql = 'delete from [' + @tablename + '] where [_date_time] < ''' + convert(varchar(25), @date_trim, 120)+''''
				--SET @sql = 'select * from [' + @tablename + '] where [_date_time] < ''' + convert(varchar(25), @date_trim, 120)+''''
		else
			SET @sql = 'delete from SubData from [' + @tablename + '] SubData left join ['+ substring(@tablename,1,charindex('_VT',@tablename)-1) + '] MainData on SubData.' + substring(@tablename,1,charindex('_VT',@tablename)-1) + '_IDRRef = MainData._IDRRef WHERE MainData._IDRRef IS NULL'
			--SET @sql = 'select * from [' + @tablename + '] SubData left join ['+ substring(@tablename,1,charindex('_VT',@tablename)-1) + '] MainData on SubData.' + substring(@tablename,1,charindex('_VT',@tablename)-1) + '_IDRRef = MainData._IDRRef WHERE MainData._IDRRef IS NULL'
        --PRINT @sql
        EXEC (@sql)
        FETCH NEXT
   FROM doc
   INTO @tablename
    END
CLOSE doc
DEALLOCATE doc
--Сжимаем базу данных
ALTER DATABASE $(newDB) SET RECOVERY SIMPLE
GO
declare @t varchar(500)
set @t = ''
select @t = name FROM sys.database_files WHERE physical_name LIKE '%LDF%'
DBCC SHRINKFILE (@t, 5)
GO
ALTER DATABASE $(newDB) SET RECOVERY FULL
GO
DBCC SHRINKDATABASE($(newDB))
go