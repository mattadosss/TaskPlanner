drop
database if exists Task_Planner;
create
database Task_Planner;
use
Task_Planner;

create table Task
(
    Task_ID      int primary Key auto_increment,
    erledigt     bool,
    Titel        varchar(50),
    Beschreibung varchar(50),
    DatumUhrzeit datetime,
    Datei        varchar(50),
    Ort_ID       int,
    Prioritaet   int,
    Partner_ID   int,
    Abhaengikeit int,
    foreign key (Abhaengikeit) references Task (Task_ID)
);

create table Partner
(
    Partner_ID int primary key auto_increment,
    Name       varchar(50)
);

create table Tag
(
    Tag_ID   int primary key auto_increment,
    Tag_Name varchar(50)
);

create Table TagTask
(
    Tag_ID  int,
    Task_ID int,
    primary key (Tag_ID, Task_ID)
);

create table Material
(
    Material_ID int primary key auto_increment,
    Name        varchar(50)
);

create table MaterialTask
(
    Material_ID int,
    Task_ID     int,
    primary key (Material_ID, Task_ID)
);

create table Ort
(
    Ort_ID  int primary key auto_increment,
    PLZ     int,
    Strasse varchar(50),
    Latitude double,
    Longitude double
);

create table PLZOrt
(
    PLZ       int primary key,
    Orts_Name varchar(50)
);

alter table TagTask
    add foreign key (Tag_ID) references Tag (Tag_ID)
    on delete cascade;
alter table TagTask
    add foreign key (Task_ID) references Task (Task_ID)
    on delete cascade;
alter table MaterialTask
    add foreign key (Material_ID) references Material (Material_ID)
    on delete cascade;
alter table MaterialTask
    add foreign key (Task_ID) references Task (Task_ID)
    on delete cascade;

use
Task_Planner;
create view v_Task as
select Task.Task_ID,
       Task.erledigt,
       Task.Titel,
       Task.Beschreibung,
       Task.DatumUhrzeit,
       Task.Datei,
       Task.Ort_ID,
       Task.Prioritaet,
       Task.Partner_ID,
       Task.Abhaengikeit
from Task;
select *
from v_Task;

create view v_Tag as
select Tag.Tag_ID, Tag.Tag_Name, TagTask.Task_ID
from Tag
         inner join TagTask ON TagTask.Tag_ID = Tag.Tag_ID;
select *
from v_Tag;

create view v_Partner as
select Partner.Partner_ID, Partner.Name
from Partner;
select *
from v_Partner;

create view v_Ort as
select Ort.Ort_ID, Ort.Plz, PLZOrt.Orts_Name, Ort.Strasse, Ort.Latitude, Ort.Longitude
from Ort
         inner join PLZOrt on (Ort.PLZ = PLZOrt.PLZ);
select *
from v_Ort;

create view v_Material as
select Material.Material_ID, Material.Name
from Material;
select *
from v_Material;

DELIMITER //
drop PROCEDURE if exists spi_Task //
create PROCEDURE spi_Task(
    in erledigt bool,
    in Titel varchar (50),
    in Beschreibung varchar (50),
    in DatumUhrzeit datetime,
    in Datei varchar (50),
    in Ort_ID int,
    in Prioritaet int,
    in Partner_ID int,
    in Abhaengikeit int)
begin
insert into Task (erledigt, Titel, Beschreibung, DatumUhrzeit, Datei, Ort_ID, Prioritaet, Partner_ID,
                  Abhaengikeit)
values (erledigt, Titel, Beschreibung, DatumUhrzeit, Datei, Ort_ID, Prioritaet, Partner_ID, Abhaengikeit);
end
//
DELIMITER ;

DELIMITER //
drop procedure if exists spu_Task //
create procedure spu_Task(
    in Task_ID int,
    in erledigt bool,
    in Titel varchar (50),
    in Beschreibung varchar (50),
    in DatumUhrzeit datetime,
    in Datei varchar (50),
    in Ort_ID int,
    in Prioritaet int,
    in Partner_ID int,
    in Abhaengikeit int)

begin
update Task
set Task.erledigt      = erledigt,
    Task.Titel         = Titel,
    Task.Beschreibung  = Beschreibung,
    Task.DatumUhrzeit  = DatumUhrzeit,
    Task.Datei         = Datei,
    Task.Ort_ID        = Ort_ID,
    Task.Prioritaet    = Prioritaet,
    Task.Partner_ID    = Partner_ID,
    Task.Abhaengikeit = Abhaengikeit
where Task.Task_ID = Task_ID;
end
//

create procedure spd_Task(in Task_ID int)
begin
UPDATE Task SET Task.Abhaengikeit = NULL WHERE Task.Abhaengikeit = Task_ID;
delete
from Task
where Task.Task_ID = Task_ID;
end
//



drop procedure if exists spi_Partner //
create procedure spi_Partner(
    in Name varchar (50))
begin
start transaction;
insert into Partner (Name)
values (Name);
commit;
end
//


drop procedure if exists spu_Partner //
create procedure spu_Partner(
    in Partner_ID int,
    in Name varchar (50))

begin
update Partner
set Partner.Name = Name
where Partner.Partner_ID = Partner_ID;
end
//

create procedure spd_Partner(in Partner_ID int)
begin
delete
from Partner
where Partner.Partner_ID = Partner_ID;
end
//

create procedure rem_tag(in Tag_ID Int, in Task_ID int)
begin
delete
from TagTask
where TagTask.Tag_ID = Tag_ID
  and TagTask.Task_ID = Task_ID;
end
//


drop procedure if exists spi_Tag //
create procedure spi_Tag(
    in Tag_Name varchar (50))
begin
insert into Tag (Tag_Name)
values (Tag_Name);
end
//


drop procedure if exists spu_Tag //
create procedure spu_Tag(
    in Tag_ID int,
    in Tag_Name varchar (50))

begin
update Tag
set Tag.Tag_Name = Tag_Name
where Tag.Tag_ID = Tag_ID;
end
//

drop procedure if exists spd_Tag//
create procedure spd_Tag(in Tag_ID int)
begin
delete
from Tag
where Tag.Tag_ID = Tag_ID;
end
//


drop procedure if exists spi_Ort //
create procedure spi_Ort(
    PLZ int,
    Strasse varchar (50),
    Latitude double,
    Longitude double)
begin
start transaction;
insert into Ort (PLZ, Strasse, Latitude, Longitude)
values (PLZ, Strasse, Latitude, Longitude);
commit;
end
//


drop procedure if exists spu_Ort //
create procedure spu_Ort(
    Ort_ID int,
    PLZ int,
    Strasse varchar (50),
    Latitude double,
    Longitude double)

begin
update Ort
set Ort.Ort_ID    = Ort_ID,
    Ort.PLZ       = PLZ,
    Ort.Strasse   = Strasse,
    Ort.Latitude  = Latitude,
    Ort.Longitude = Longitude
where Ort.Ort_ID = Ort_ID;
end
//

create procedure spd_Ort(in Ort_ID int)
begin
delete
from Ort
where Ort.Ort_ID = Ort_ID;
end
//


create procedure rem_Material(in Material_ID Int, in Task_ID int)
begin
delete
from MaterialTask
where MaterialTask.Material_ID = Material_ID
  and MaterialTask.Task_ID = Task_ID;
end
//


drop procedure if exists spi_Material //
create procedure spi_Material(
    in Name varchar (50))
begin
insert into Material (Name)
values (Name);
end
//


drop procedure if exists spu_Material //
create procedure spu_Material(
    in Material_ID int,
    in Name varchar (50))

begin
update Material
set Material.Name = Name
where Material.Material_ID = Material_ID;
end
//

drop procedure if exists spd_Material//
create procedure spd_Material(in Material_ID int)
begin
delete
from Material
where Material.Material_ID = Material_ID;
end
//

DELIMITER ;



use
Task_Planner;
create view v2_Task as
(
select Task.Task_ID,
       Task.erledigt,
       Task.Titel,
       Task.Beschreibung,
       Task.DatumUhrzeit,
       Task.Datei,
       Ort.Ort_ID,
       Ort.PLZ,
       Ort.Strasse,
       Ort.Latitude,
       Ort.Longitude,
       Task.Prioritaet,
       Task.Partner_ID,
       Partner.Name  as "Partner Name",
       material.Name as "Material Name",
       Task.Abhaengikeit
from Task
         left join TagTask on (Task.Task_ID = TagTask.Task_ID)
         left join Tag on (Tag.Tag_ID = TagTask.Tag_ID)
         left join MaterialTask on (Task.Task_ID = MaterialTask.Task_ID)
         left join Material on (Material.Material_ID = MaterialTask.Material_ID)
         left join Ort on (Task.Ort_ID = Ort.Ort_ID)
         left join PLZOrt on (plzort.PLZ = Ort.PLZ)
         left join Partner on (Task.Partner_ID = Partner.Partner_ID)
    );

insert into Partner (Partner_ID, Name)
values (1, 'Lucky');
insert into Partner (Partner_ID, Name)
values (2, 'Gilberte');
insert into Partner (Partner_ID, Name)
values (3, 'Melesa');
insert into Partner (Partner_ID, Name)
values (4, 'Poppy');
insert into Partner (Partner_ID, Name)
values (5, 'Naomi');
insert into Partner (Partner_ID, Name)
values (6, 'Dorice');
insert into Partner (Partner_ID, Name)
values (7, 'Theo');
insert into Partner (Partner_ID, Name)
values (8, 'Hanna');
insert into Partner (Partner_ID, Name)
values (9, 'Pierrette');
insert into Partner (Partner_ID, Name)
values (10, 'Monika');

insert into PLZOrt (PLZ, Orts_Name)
values (5358, 'Sharga');
insert into PLZOrt (PLZ, Orts_Name)
values (2266, 'Jimenez');
insert into PLZOrt (PLZ, Orts_Name)
values (6262, 'Saint Cloud');
insert into PLZOrt (PLZ, Orts_Name)
values (2799, 'Mont-Dore');
insert into PLZOrt (PLZ, Orts_Name)
values (9222, 'Awilega');
insert into PLZOrt (PLZ, Orts_Name)
values (1899, 'Agía Foteiní');
insert into PLZOrt (PLZ, Orts_Name)
values (6072, 'Boevange-sur-Attert');
insert into PLZOrt (PLZ, Orts_Name)
values (6989, 'Sąspów');
insert into PLZOrt (PLZ, Orts_Name)
values (3146, 'Tramandaí');
insert into PLZOrt (PLZ, Orts_Name)
values (8037, 'Atlanta');

insert into Ort (Ort_ID, PLZ, Strasse, Latitude, Longitude)
values (1, 5358, 'Larry', -6.9, 113.1565);
insert into Ort (Ort_ID, PLZ, Strasse, Latitude, Longitude)
values (2, 2266, 'Knutson', 53.5050031, -6.4671298);
insert into Ort (Ort_ID, PLZ, Strasse, Latitude, Longitude)
values (3, 6262, 'Fairfield', 53.7835379, 91.3543318);
insert into Ort (Ort_ID, PLZ, Strasse, Latitude, Longitude)
values (4, 2799, 'South', 39.07472, 117.30056);
insert into Ort (Ort_ID, PLZ, Strasse, Latitude, Longitude)
values (5, 9222, 'Waywood', -14.91256, -69.874893);
insert into Ort (Ort_ID, PLZ, Strasse, Latitude, Longitude)
values (6, 1899, 'Bluejay', -5.266667, -74.283333);
insert into Ort (Ort_ID, PLZ, Strasse, Latitude, Longitude)
values (7, 6072, 'Farwell', 8.3104933, 122.9938347);
insert into Ort (Ort_ID, PLZ, Strasse, Latitude, Longitude)
values (8, 6989, 'Utah', 38.5434693, -9.0610972);
insert into Ort (Ort_ID, PLZ, Strasse, Latitude, Longitude)
values (9, 3146, 'Goodland', 34.540852, 109.44096);
insert into Ort (Ort_ID, PLZ, Strasse, Latitude, Longitude)
values (10, 8037, 'Vera', 31.394935, 92.835795);

insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit, Datei, Ort_ID, Prioritaet, Partner_ID,
                  Abhaengikeit)
values (1, false, 'Tony mahony', 'Enhanced neutral definition', '2024-05-08 01:28:54', 'Ventosanzap', 1, 3, 1, null);
insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit, Datei, Ort_ID, Prioritaet, Partner_ID,
                  Abhaengikeit)
values (2, false, 'Task1', 'Monitored tertiary hierarchy', '2023-11-28 03:58:47', 'Zaam-Dox', 2, 3, 4,
        null);
insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit, Datei, Ort_ID, Prioritaet, Partner_ID,
                  Abhaengikeit)
values (3, true, 'Task2', 'Configurable coherent knowledge base', '2023-10-27 09:19:10', 'Daltfresh', 3, 5,
        5, null);
insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit, Datei, Ort_ID, Prioritaet, Partner_ID,
                  Abhaengikeit)
values (4, true, 'Task3', 'Customer-focused real-time focus group', '2023-10-27 15:30:33', 'Fixflex', 4, 4, 2, null);
insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit, Datei, Ort_ID, Prioritaet, Partner_ID,
                  Abhaengikeit)
values (5, false, 'sleep again', 'Future-proofed mobile function', '2023-08-31 17:16:13', 'It', 5, 2, 5, null);
insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit, Datei, Ort_ID, Prioritaet, Partner_ID,
                  Abhaengikeit)
values (6, true, 'Task6', 'Object-based even-keeled success', '2023-08-12 18:50:29', 'Home Ing', 6, 1, 5, null);
insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit, Datei, Ort_ID, Prioritaet, Partner_ID,
                  Abhaengikeit)
values (7, false, 'Movie', 'Function-based zero tolerance local area network', '2024-04-04 14:56:46', 'Fix San', 7, 4,
        1, null);
insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit, Datei, Ort_ID, Prioritaet, Partner_ID,
                  Abhaengikeit)
values (8, false, 'Homework', 'Profit-focused web-enabled paradigm', '2024-03-15 10:15:43', 'Lotlux', 8, 4, 1, null);
insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit, Datei, Ort_ID, Prioritaet, Partner_ID,
                  Abhaengikeit)
values (9, true, 'Homework2', 'Pre-emptive coherent utilisation', '2023-11-15 19:15:36', 'Zoolab', 9, 4, 2, null);
insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit, Datei, Ort_ID, Prioritaet, Partner_ID,
                  Abhaengikeit)
values (10, false, 'Task7', 'Virtual empowering data-warehouse', '2023-06-18 15:16:17', 'Ventosanzap', 10, 1, 5,
        null);

insert into Tag (Tag_ID, Tag_Name)
values (1, 'Dabvine');
insert into Tag (Tag_ID, Tag_Name)
values (2, 'Yodel');
insert into Tag (Tag_ID, Tag_Name)
values (3, 'Dynabox');
insert into Tag (Tag_ID, Tag_Name)
values (4, 'Skidoo');
insert into Tag (Tag_ID, Tag_Name)
values (5, 'Blogspan');
insert into Tag (Tag_ID, Tag_Name)
values (6, 'Tanoodle');
insert into Tag (Tag_ID, Tag_Name)
values (7, 'Skipstorm');
insert into Tag (Tag_ID, Tag_Name)
values (8, 'Zoonoodle');
insert into Tag (Tag_ID, Tag_Name)
values (9, 'Yambee');
insert into Tag (Tag_ID, Tag_Name)
values (10, 'Oozz');

insert into TagTask (Tag_ID, Task_ID)
values (1, 1);
insert into TagTask (Tag_ID, Task_ID)
values (2, 2);
insert into TagTask (Tag_ID, Task_ID)
values (3, 3);
insert into TagTask (Tag_ID, Task_ID)
values (4, 4);
insert into TagTask (Tag_ID, Task_ID)
values (5, 5);
insert into TagTask (Tag_ID, Task_ID)
values (6, 6);
insert into TagTask (Tag_ID, Task_ID)
values (7, 7);
insert into TagTask (Tag_ID, Task_ID)
values (8, 8);
insert into TagTask (Tag_ID, Task_ID)
values (9, 9);
insert into TagTask (Tag_ID, Task_ID)
values (10, 10);

insert into Material (Material_ID, Name)
values (1, 'Aluminum');
insert into Material (Material_ID, Name)
values (2, 'Granite');
insert into Material (Material_ID, Name)
values (3, 'Aluminum');
insert into Material (Material_ID, Name)
values (4, 'Steel');
insert into Material (Material_ID, Name)
values (5, 'Brass');
insert into Material (Material_ID, Name)
values (6, 'Plastic');
insert into Material (Material_ID, Name)
values (7, 'Rubber');
insert into Material (Material_ID, Name)
values (8, 'Stone');
insert into Material (Material_ID, Name)
values (9, 'Plexiglass');
insert into Material (Material_ID, Name)
values (10, 'Plastic');

insert into MaterialTask (Material_ID, Task_ID)
values (1, 1);
insert into MaterialTask (Material_ID, Task_ID)
values (2, 2);
insert into MaterialTask (Material_ID, Task_ID)
values (3, 3);
insert into MaterialTask (Material_ID, Task_ID)
values (4, 4);
insert into MaterialTask (Material_ID, Task_ID)
values (5, 5);
insert into MaterialTask (Material_ID, Task_ID)
values (6, 6);
insert into MaterialTask (Material_ID, Task_ID)
values (7, 7);
insert into MaterialTask (Material_ID, Task_ID)
values (8, 8);
insert into MaterialTask (Material_ID, Task_ID)
values (9, 9);
insert into MaterialTask (Material_ID, Task_ID)
values (10, 10);
CALL spi_Task(False,"1","1","1111-11-11T11:11","file",1,1,1,1);
CALL spu_Task(1,False,"1","1","1111-11-11T11:11","file",1,1,1,1);