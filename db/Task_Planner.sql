drop
database if exists Task_Planner;
create
database Task_Planner;
use Task_Planner;

create table Task
(
    Task_ID      int primary Key auto_increment,
    erledigt     bool,
    Titel        varchar(50),
    Beschreibung varchar(50),
    DatumUhrzeit datetime
);

insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit)
values (1, false, 'Tony mahony', 'Enhanced neutral definition', '2024-05-08 01:28:54');

insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit)
values (2, false, 'Task1', 'Monitored tertiary hierarchy', '2023-11-28 03:58:47');

insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit)
values (3, true, 'Task2', 'Configurable coherent knowledge base', '2023-10-27 09:19:10';

insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit)
values (4, true, 'Task3', 'Customer-focused real-time focus group', '2023-10-27 15:30:33');

insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit)
values (5, false, 'sleep again', 'Future-proofed mobile function', '2023-08-31 17:16:13');

insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit)
values (6, true, 'Task6', 'Object-based even-keeled success', '2023-08-12 18:50:29');

insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit)
values (7, false, 'Movie', 'Function-based zero tolerance local area network', '2024-04-04 14:56:46');

insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit)
values (8, false, 'Homework', 'Profit-focused web-enabled paradigm', '2024-03-15 10:15:43');

insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit)
values (9, true, 'Homework2', 'Pre-emptive coherent utilisation', '2023-11-15 19:15:36');

insert into Task (Task_ID, erledigt, Titel, Beschreibung, DatumUhrzeit)
values (10, false, 'Task7', 'Virtual empowering data-warehouse', '2023-06-18 15:16:17');

